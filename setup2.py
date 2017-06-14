#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

from __future__ import with_statement

# http://docs.python.org/distutils/
# http://packages.python.org/distribute/
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

import os.path

version_py = os.path.join(os.path.dirname(__file__), 'HarmGen', 'version.py')
with open(version_py, 'r') as f:
    d = dict()
    exec(f.read(), d)
    version = d['__version__']

setup(
    name = 'python-HarmGen',
    description = 'Python HarmGen generador de vectores armonicos para fuentes Kepco controlada por comandos SCPI',
    version = version,
    long_description = '''Esta biblioteca genera de vectores armonicos las fuentes Kepco con puerto serial controlables con comandos SCPI.''',
    author = 'Javier Campos Rojas',
    author_email = 'nautilus28c@gmail.com	',
    url = 'http://www.ie.tec.ac.cr/seslab/',
    download_url = 'https://github.com/seslab/MIPVC/tree/master/HarmGen',
    keywords = 'USB SCPI Kepco Serial SESLab Source Fuentes',
    license = 'Licencia ITCR',
    classifiers=[
        'Development Status :: 3.5',
        'Environment :: Graphics',
        'License :: OSI Approved :: Licencia ITCR',
        'Natural Language :: Español',
        'Operating System :: Linux',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
        ],
    packages = find_packages(exclude=['SerialKepco', 'controlTektronix'])
)
