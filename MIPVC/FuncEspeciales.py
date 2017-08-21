#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:FuncEspeciales.py
#Descripción		:Permite caracterizar y medir calidad de energia de micro inversores.
#Autor          	:Javier Campos Rojas
#Fecha            	:Agosto-2017
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
	xgrid=80;
	ygrid=48;
	refx=xgrid/2;
	refy=3*ygrid/4-5;
	width_b=16;
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
	
		
	win = GraphWin("Fuentes Kepco SESLab",width=800, height=480)
	win.master.overrideredirect(True)
	win.setCoords(0,0,xgrid,ygrid) #x1 y1 x2 y2
	#win.setBackground('#BCC6CC')
	background = Image(Point(xgrid/2,ygrid/2), 'backg2.gif')
	background.draw(win)
	logoTEC = Image(Point(xgrid/2-20,ygrid-5), 'TEC.gif')
	logoTEC.draw(win)
	LogoSESLab = Image(Point(xgrid/2+20,ygrid-5), 'SESLab.gif')
	LogoSESLab.draw(win)
	
	##Columna 1
	CMI = Button(win, Point(refx-20,refy), width_b, heigh_b, "Caracterización MI")
	CMI.activate()
	
	##Columna 2
	CalidadE = Button(win, Point(refx,refy), width_b, heigh_b, "Calidad de Energia")
	CalidadE.activate()
	
	##Columna 3
	Salir = Button(win, Point(refx+20,refy), width_b, heigh_b, "Salir")
	Salir.rect.setFill("#C01A19")
	Salir.activate()
	
	Ayuda = Button(win, Point(refx+20,refy-5), width_b, heigh_b, "Ayuda")
	Ayuda.rect.setFill("#3F51B5")
	Ayuda.activate()
	
	
		################## Mensaje de lectura ##################
	mensaje=Text(Point(xgrid/2,3.5),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	A1="✔Caracterización MI: Permite caracterizar micro inversores para sistemas fotovoltaicos"+"\n"
	A2="✔Calidad de Energia: Permite realizar mediciones de tensión, corriente y analisis de armonicos de un micro inversor"+"\n"
	AyudaMensaje=A1+A2
	
	pt = win.getMouse()
	while not Salir.clicked(pt):	
			
		if CMI.clicked(pt):
			mensaje.setText("Ejecutando rutina de caracterización...")
			execfile('caracterizar.py')
			mensaje.setText("¡Listo!")
		if CalidadE.clicked(pt):
			execfile('Analizador.py')
			
		if Ayuda.clicked(pt):
			win.master.option_add('*font', 'Helvetica -12')
			tkMessageBox.showinfo('Ayuda',AyudaMensaje)
			
		pt = win.getMouse()
	win.close()
main()
