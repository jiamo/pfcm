#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

MINIMUM_PYTHON_VERSION = 3, 6

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('changelog.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.0',
    'google-api-python-client>=1.6.4',
    'oauth2client>=4.1.2',
    'requests',
    'PyYAML',
    'aiohttp',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='pfcm',
    version='0.1.3',
    description="another fcm wrapper in python",
    long_description=readme + '\n\n' + history,
    author="jiamo",
    author_email='life.130815@gmail.com',
    url='https://github.com/jiamo/pfcm',
    packages=find_packages(include=['pfcm']),
    entry_points={
        'console_scripts': [
            'pfcm=pfcm.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pfcm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
