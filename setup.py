#!/usr/bin/env python
from setuptools import setup

setup(name="asyncrandom",
      description="Async random int generator.",
      version="0.0.1",
      author="Yavor Paunov",
      author_email='contact@yavorpaunov.com',
      entry_points={
          "console_scripts": ["asyncrandom=asyncrandom:main"]
      },
      install_requires=["tornado>=4.4", "enum34"],
      tests_require=["mock"],
      py_modules=["asyncrandom"],
      test_suite="tests")
