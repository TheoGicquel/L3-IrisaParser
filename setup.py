from setuptools import setup, find_packages

import irisaparser

setup(
    name=irisaparser.__name__,
    version=irisaparser.__version__,
    author='Author name',
    author_email='author@gmail.com',
    description='Scientific paper parser',
    packages=find_packages(),
    install_requires=[],  # e.g. ['numpy >= 1.11.1', 'matplotlib >= 1.5.1']
)