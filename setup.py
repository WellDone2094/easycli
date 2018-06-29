#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python Egg Setup file."""
from setuptools import setup, find_packages

setup(
    name="climb",
    version='0.1',
    author="Andrea Benfatti",
    author_email="welldone2094@gmail.com",
    description="Climb is a library that allow you to build CLI tools.",
    url="https://github.com/WellDone2094/climb",
    license='GPLv3',
    install_requires=[],
    packages=find_packages()
)  # yapf: disable
