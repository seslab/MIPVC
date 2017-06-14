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

version_py = os.path.join(os.path.dirname(__file__), 'controlTektronix', 'version.py')
with open(version_py, 'r') as f:
    d = dict()
    exec(f.read(), d)
    version = d['__version__']

setup(
    name = 'python-controlTektronix',
    description = 'Python controlTektronix controlador de osciloscopios tektronix por comandos SCPI',
    version = version,
    long_description = '''Esta bibliteca permite realizar captura de datos remota por medio de un osciloscipio marca Tektronix.''',
    author = 'Javier Campos Rojas',
    author_email = 'nautilus28c@gmail.com	',
    url = 'http://www.ie.tec.ac.cr/seslab/',
    download_url = 'https://github.com/seslab/MIPVC/tree/master/ControlTektronix',
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
    packages = find_packages(exclude=['SerialKepco', 'HarmGen']))
)
