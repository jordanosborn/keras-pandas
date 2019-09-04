from collections import OrderedDict

from setuptools import setup, find_packages

__version__ = '3.1.0'

# Add README as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# Parse requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tf2-keras-pandas',
    description='Easy and rapid deep learning - updated for tensorflow 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    url='https://github.com/bjherger/keras-pandas',
    author='Brendan Herger',
    author_email='13herger@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=required,
    project_urls=OrderedDict((
        ('Code', 'https://github.com/jordanosborn/keras-pandas'),
        ('Documentation', 'http://keras-pandas.readthedocs.io/en/latest/intro.html'),
        ('PyPi', 'https://pypi.org/project/tf2-keras-pandas/'),
        ('Issue tracker', 'https://github.com/jordanosborn/keras-pandas/issues'),
    )),
)
