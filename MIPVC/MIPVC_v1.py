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
	xgrid=80;
	ygrid=48;
	refx=xgrid/4;
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
	FuenteV = Button(win, Point(refx,refy), width_b, heigh_b, "Fuentes Tensión")
	FuenteV.activate()
	FuenteC = Button(win, Point(refx,refy-ygrid/6), width_b, heigh_b, "Fuentes Corriente")
	FuenteC.activate()
	FuencE = Button(win, Point(refx,refy-2*ygrid/6), width_b, heigh_b, "Funciones Especiales")
	FuencE.activate()
	
	##Columna 2
	Seno = Button(win, Point(refx+xgrid/4,refy), width_b, heigh_b, "Sinusoidal")
	Seno.activate()
	Periodicas = Button(win, Point(refx+xgrid/4,refy-ygrid/6), width_b, heigh_b, "Periodicas Especiales")
	Periodicas.activate()
	Salir = Button(win, Point(refx+xgrid/4,refy-2*ygrid/6), width_b, heigh_b, "Salir")
	Salir.rect.setFill("#C01A19")
	Salir.activate()
	
	##Columna 3
	BarridoV = Button(win, Point(refx+2*xgrid/4,refy), width_b, heigh_b, "Barrido Tensión")
	BarridoV.activate()
	BarridoC = Button(win, Point(refx+2*xgrid/4,refy-ygrid/6),width_b, heigh_b, "Barrido Corriente")
	BarridoC.activate()
	Ayuda = Button(win, Point(refx+2*xgrid/4,refy-2*ygrid/6), width_b, heigh_b, "Ayuda")
	Ayuda.rect.setFill("#3F51B5")
	Ayuda.activate()
	
	
		################## Mensaje de lectura ##################
	mensaje=Text(Point(xgrid/2,5),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	A1="✔Fuente de Tensión: Permite salida de tensión fija con corriente limite"+"\n"
	A2="✔Fuente de Corriente: Permite salida de corriente fija con tensión limite"+"\n"
	A3="✔Sinusoidal: Permite salida de sinusoidal e inyección de armonicas"+"\n"
	A4="✔Periodicas especiales: Permite salida triangular, diente de sierra y señal cuadrada"+"\n"
	A5="✔Barrido de Tensión: Permite barridos de tensión (Para caracterización de modulos PV)"+"\n"
	A6="✔Barrido de Corriente: Permite barridos de corriente (Para caracterización de modulos PV)"+"\n"
	A7="✔Funciones especiales: Funciones para caracterización de micro inversores"
	AyudaMensaje=A1+A2+A3+A4+A5+A6+A7
	pt = win.getMouse()
	a=0;
	b=0;
	
	#while not Salir.clicked(pt):
	while not ((xgrid-10<= pt.getX() <=xgrid) and (ygrid-10<= pt.getY() <=ygrid) and a==1 and b==1):
		
		if LogoSESLab.clicked(pt):
			a=1;
			b=0
		if logoTEC.clicked(pt):
			b=1;
		if FuenteV.clicked(pt):
			#execfile('FuenteV.py')
			subprocess.Popen(["python", "FuenteV.py"])
			#subprocess.Popen(["python", "FuenteV.py"] + sys.argv[1:])
		if FuenteC.clicked(pt):
			execfile('FuenteC.py')
			#subprocess.Popen(["python", "FuenteC.py"] + sys.argv[1:])
		if BarridoV.clicked(pt):
			#execfile('BarridoV.py')
			subprocess.Popen(["python", "BarridoV.py"] + sys.argv[1:])
			
		if BarridoC.clicked(pt):
			#execfile('BarridoC.py')
			subprocess.Popen(["python", "BarridoC.py"] + sys.argv[1:])
			
		if Seno.clicked(pt):
			#execfile('Sinusoidales.py')
			subprocess.Popen(["python", "Sinusoidales.py"] + sys.argv[1:])
			
		if Periodicas.clicked(pt):
			#execfile('Periodicas.py')
			subprocess.Popen(["python", "Periodicas.py"] + sys.argv[1:])
			
		if FuencE.clicked(pt):
			#execfile('FuncEspeciales.py')
			subprocess.Popen(["python", "FuncEspeciales.py"] + sys.argv[1:])
			
		if Ayuda.clicked(pt):
			#winshowInfo('Ayuda',AyudaMensaje)
			win.master.option_add('*font', 'Helvetica -12')
			tkMessageBox.showinfo('Ayuda',AyudaMensaje)
			#msgbox(AyudaMensaje,'Ayuda')
		
		if Salir.clicked(pt):
			os.system("shutdown now")

		pt = win.getMouse()
	win.close()
main()
