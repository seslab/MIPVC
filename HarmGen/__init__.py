#Titulo				:__init__.py
#Descripción		:Biblioteca para fuentes Kepco SerialKepco.py.
#Autor          	:Javier Campos Rojas
#Fecha            	:Febero-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

__all__ = ["HarmGen"]

from .version import __version__
from .HarmGen import HarmGen
