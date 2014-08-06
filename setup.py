#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='Patchmate',
      version='0.1',
      author='Tomasz Kolek, '
             'Maor Lipchuk',
      author_email='tomasz-kolek@o2.pl, '
                   'mlipchuk@redhat.com',
      scripts=["patchmate/script/add_reviewers.py"],
      requires=["mock",
                "requests"],
      packages=find_packages()
      )
