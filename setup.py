from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()

# TODO: Change the following variables to match your app
app_name = 'uploader'

# Versions should comply with PEP440.  For a discussion on single-sourcing
# the version across setup.py and the project code, see
# https://packaging.python.org/en/latest/single_source_version.html
app_version = '1.1.0'

app_description = 'SFTP to S3 server'

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable
app_dev_status = '5 - Production/Stable'

# What does your project relate to?
app_keywords = 'illumicare'

# List run-time dependencies here.  These will be installed by pip when
# your project is installed. For an analysis of "install_requires" vs pip's
# requirements files see:
# https://packaging.python.org/en/latest/requirements.html
app_install_requires = ['argparse', 'paramiko', 'argon2_cffi', 'boto3', 'illumicare-config-parsers']


setup(
    name='illumicare-'+app_name,

    version=app_version,

    description=app_description,
    long_description=long_description,

    url='http://www.illumicare.com',

    author='IllumiCare Inc.',
    author_email='support@illumicare.com',

    # Choose your license
    license='Proprietary - IllumiCare Inc. - all rights reserved',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: '+app_dev_status,

        # Indicate who your project is intended for
        'Intended Audience :: Healthcare Industry',
        'Topic :: System :: Software Distribution',

        # Pick your license as you wish (should match "license" above)
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    keywords=app_keywords,

    install_requires=app_install_requires,

    package_dir={'': 'src'},
    packages=find_packages('src'),
)
