#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:MicroInverterPVCharacterization(MIPVC).py
#Descripción		:Interfaz de usuario Principal para control de calidad de energia de Micro Inversores.
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

from graphics import *
from button import *
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import os
import base64
import Tkinter as tk
from urllib2 import urlopen
import glob ##### para buscar los puertos USB disponibles
#from controlTektronix import *
import tkFileDialog
from EnergyQ import *
import subprocess
import tkMessageBox

def main():
	xgrid=50;
	ygrid=20;
	refx=xgrid/4;
	refy=3*ygrid/4-5;
	width_b=14.5;
	heigh_b=2.5;
	Tm=0.0005;
	puertos=glob.glob('/dev/tty[U]*')
	try:
		puerto1 = puertos[0]
	except IndexError:
		puerto1 = 'no hay dispositivo'
	try:
		puerto2 = puertos[1]
	except IndexError:
		puerto2 = 'no hay dispositivo'
	
		
	win = GraphWin("Fuentes Kepco SESLab",width=500, height=200)
	win.master.overrideredirect(True)
	win.setCoords(0,0,xgrid,ygrid) #x1 y1 x2 y2
	#win.setBackground('#BCC6CC')
	background = Image(Point(xgrid/2,ygrid/2), 'backg2.gif')
	background.draw(win)
	logoTEC = Image(Point(xgrid/2-12,ygrid-5), 'TEC.gif')
	logoTEC.draw(win)
	LogoSESLab = Image(Point(xgrid/2+12,ygrid-5), 'SESLab.gif')
	LogoSESLab.draw(win)
	
	##Columna 1
	CMI = Button(win, Point(refx,refy), width_b, heigh_b, "Caracterización MI")
	CMI.activate()
	CalidadE = Button(win, Point(refx,refy-4), width_b, heigh_b, "Calidad de Energia")
	CalidadE.activate()
	
	##Columna 2
	Salir = Button(win, Point(refx+2*xgrid/4,refy-ygrid/6), width_b, heigh_b, "Salir")
	Salir.rect.setFill("#C01A19")
	Salir.activate()
	
		################## Mensaje de lectura ##################
	mensaje=Text(Point(xgrid/2,3.5),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	while not Salir.clicked(pt):	
			
		if CMI.clicked(pt):
			mensaje.setText("Ejecutando rutina de caracterización...")
			execfile('caracterizar.py')
			mensaje.setText("¡Listo!")
		if CalidadE.clicked(pt):
			execfile('Analizador.py')

		pt = win.getMouse()
	win.close()
main()
