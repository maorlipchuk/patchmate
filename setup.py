#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='Patchmage',
      version='0.1',
      author='Tomasz Kolek, Maor Lipchuk',
      author_email='tomasz-kolek@o2.pl, mlipchuk@redhat.com',
      scripts=["script/add_reviewers.py"],
      packages=find_packages()
      )
