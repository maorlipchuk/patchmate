#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='Add Potential Reviewers',
      version='0.1',
      author='Tomasz Kolek',
      author_email='tomasz-kolek@o2.pl',
      scripts=["script/add_reviewers.py"],
      packages=find_packages()
      )
