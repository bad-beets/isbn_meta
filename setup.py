#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='isbn_meta',
      version='0.69',
      # Modules to import from other scripts:
      packages=find_packages(),
      # Executables
      scripts=["choose.py",
               "field_trans.py",
               "get.py",
               "isbn_gen.py",
               "load_config.py",
               "log_setup.py",
               "main.py",
               "metric.py",
               "setup.py"],
      )
