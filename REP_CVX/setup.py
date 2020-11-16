# -*- coding: utf-8 -*-

import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'REP_CVX',
    version = '1.1',
    author = 'M. A. Tahavori, N. Golinucci, N. Namazifard',
    author_email = 'm.amintahavori@gmail.com',
    description = 'A module for Supply and Use Input-Output Analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='??',
    packages=["REP_CVX"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')