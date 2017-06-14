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
import base64
import Tkinter as tk
from urllib2 import urlopen
import glob ##### para buscar los puertos USB disponibles
#from controlTektronix import *
import tkFileDialog
from EnergyQ import *

def main():
	xgrid=30;
	ygrid=30;
	refy=15;
	refx=15;
	refx2=12;
	width_b=9;
	heigh_b=3;
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
	
		
	win = GraphWin("MicroInverter Characterization",width=500, height=200)
	win.setCoords(0,0,ygrid,xgrid)
	#win.setBackground('#BCC6CC')
	background = Image(Point(15,15), 'back2.gif')
	background.draw(win)
	logoTEC = Image(Point(22,25), 'TEC.gif')
	logoTEC.draw(win)
	LogoSESLab = Image(Point(7,25), 'SESLab.gif')
	LogoSESLab.draw(win)
	
	Fuentes = Button(win, Point(refx-7,refy), width_b, heigh_b, "Fuentes Kepco")
	Fuentes.activate()
	caracterizar = Button(win, Point(refx+7,refy), width_b, heigh_b, "Caracterización")
	caracterizar.activate()
	CalidadE = Button(win, Point(refx-7,refy-8), width_b, heigh_b, "Calidad de Energía")
	CalidadE.activate()
	Salir = Button(win, Point(refx+7,refy-8), width_b, heigh_b, "Salir")
	Salir.activate()
	
		################## Mensaje de lectura ##################
	mensaje=Text(Point(refx,refy-12),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	
	pt = win.getMouse()
	
	while not Salir.clicked(pt):

		if Fuentes.clicked(pt):
			execfile('KepcoGestionControl.py')
			
		if caracterizar.clicked(pt):
			mensaje.setText("Ejecutando rutina de caracterización...")
			execfile('caracterizar.py')
			mensaje.setText("¡Listo!")
		if CalidadE.clicked(pt):
			execfile('Analizador.py')

		pt = win.getMouse()
	win.close()
main()
