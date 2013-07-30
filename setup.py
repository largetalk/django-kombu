from distutils.core import setup
import re
import os
import sys


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(name='django-kombu',
        version='0.1',
        description='django-kombu',
        author='Arthur',
        author_email='largetalk@gmail.com',
        url='',
        packages=get_packages('django_kombu'),
        install_requires=[],
        )
