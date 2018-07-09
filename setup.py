#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-contexts',
    version='0.1.2',
    author='Harry Percival',
    author_email='obeythetestinggoat@gmail.com',
    maintainer='Harry Percival',
    maintainer_email='obeythetestinggoat@gmail.com',
    license='GNU GPL v3.0',
    url='https://github.com/madedotcom/pytest-contexts',
    description='A plugin to run tests written with the Contexts framework using pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_contexts'],
    python_requires='>=3.6',
    install_requires=['pytest', 'contexts'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'contexts = pytest_contexts',
        ],
    },
)
