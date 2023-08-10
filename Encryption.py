# coding=utf-8
from distutils.core import setup
from Cython.Build import cythonize
import os

transfer_files = os.listdir('./')
transfer_files = [file for file in transfer_files if (not file.startswith('.')) and file.endswith('.py')]
this_name = os.path.basename(__file__)
transfer_files.remove(this_name)

setup(ext_modules = cythonize(transfer_files))