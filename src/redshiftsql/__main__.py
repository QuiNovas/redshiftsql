from __future__ import print_function

import argparse
import atexit
import boto3
import os
import socket
import sys
import logging.config

from botocore.client import Config
from illumicare.config_parsers import S3ConfigParser
from paramiko import RSAKey, Transport, SFTPServer
from paramiko.ssh_exception import SSHException
from uploader_server import UploaderServer
from uploader_sftpserver import UploaderSFTPServer


if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m redshift-sql"


@atexit.register
def app_exit():
    logging.getLogger().info("Terminating")


def _parse_command_line_arguments():
    argv_parser = argparse.ArgumentParser()
    argv_parser.add_argument('--log-config',
                             metavar='log_config.ini',
                             required=True,
                             help='The logging ini file')
    argv_parser.add_argument('--aws-environment',
                             help='The IllumiCare environment we are running in. Used in path to terraform.ini')
    argv_parser.add_argument('--config-bucket',
                             help='The IllumiCare config bucket to read the ini\'s from')
    argv_parser.add_argument('--rsa-keyfile',
                             required=True,
                             help='The rsa private key to use for this sftp server')
    return argv_parser.parse_args()


def main():
    try:
        args = _parse_command_line_arguments()

        # configures logging for the application
        logging.config.fileConfig(args.log_config)

        # set AWS logging level
        logging.getLogger('botocore').setLevel(logging.ERROR)
        logging.getLogger('boto3').setLevel(logging.ERROR)

        if not args.config_bucket:
            args.config_bucket = os.environ['CONFIG_BUCKET']

        if not args.aws_environment:
            args.aws_environment = os.environ['AWS_ENVIRONMENT']

        config = S3ConfigParser()
        config.read_s3(args.config_bucket, 'ini/{}/terraform.ini'.format(args.aws_environment))
        config.read_s3(args.config_bucket, 'ini/{}/uploader_app_config.ini'.format(args.aws_environment))

        logger = logging.getLogger()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 22))
        server_socket.listen(10)

        logger.info('Listening on {}:{}'.format('0.0.0.0', 22))

        s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

        while True:
            (connection, address) = server_socket.accept()
            logger.debug('Incoming connection from {}'.format(address))
            transport = Transport(connection)
            transport.add_server_key(RSAKey.from_private_key_file(args.rsa_keyfile))
            transport.set_subsystem_handler('sftp', SFTPServer, UploaderSFTPServer)
            try:
                transport.start_server(server=UploaderServer(s3, config))
                logger.info('Established SSH connection with address {}'.format(address))
            except SSHException:
                logger.exception('SSH connection from address {} failed'.format(address))

    except KeyboardInterrupt:
        print("Service interrupted", file=sys.stderr)

    except Exception as e:
        print("Initialization FAILED: ", e.message, file=sys.stderr)
        print('')
        raise e


if __name__ == '__main__':
    main()

