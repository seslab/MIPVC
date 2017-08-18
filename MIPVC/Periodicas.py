#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:KepcoGestionControl.py
#Descripción		:Interfaz de usuario y control de fuentes marca Kepco del SESLab.
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

from graphics import *
from button import *
import SerialKepco as SK
#from HarmGen import *
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import base64
import Tkinter as tk
from urllib2 import urlopen
import glob ##### para buscar los puertos USB disponibles
import subprocess
import tkMessageBox

#from controlTektronix import *

global SK
def main():
	xgrid=80;
	ygrid=28;
	refx=10;
	refy=ygrid-4;
	width_b=10;
	heigh_b=2;
	width_b2=5;
	heigh_b2=2.5;
	Tm=0.0005;
	global Source;
		
	win = GraphWin("Funciones periodicas",width=800, height=280)
	win.setCoords(0,0,xgrid,ygrid) #x1 y1 x2 y2
	background = Image(Point(xgrid/2,ygrid/2), 'backg.gif')
	background.draw(win)	
	
	line = Line(Point(xgrid/2, 3), Point(xgrid/2, ygrid))
	line.setFill("white")
	line.setWidth(2)
	line.draw(win)
	
	line2 = Line(Point(0, 8), Point(xgrid, 8))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)
	
	line3 = Line(Point(0, 3), Point(xgrid, 3))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)
	
	
	##Fuente 1
	Sin1 = Button(win, Point(refx+23,refy-6), width_b2, heigh_b2, "☑")
	stop1 = Button(win, Point(refx+23,refy-10), width_b2, heigh_b2, "■")
	
	##Fuente 2
	Sin2 = Button(win, Point(refx+63,refy-6), width_b2, heigh_b2, "☑")
	stop2 = Button(win, Point(refx+63,refy-10), width_b2, heigh_b2, "■")
	

	
	connects1 = Button(win, Point(refx+23,refy), width_b, heigh_b, "Conectar")
	connects1.activate()
	connects2 = Button(win, Point(refx+63,refy), width_b, heigh_b, "Conectar")
	
	puertos=glob.glob('/dev/tty[U]*')
	try:
		puerto1 = puertos[0]
	except IndexError:
		Sin1.deactivate()
		stop1.deactivate()
		connects1.deactivate()
		puerto1 = 'no hay dispositivo'
		
	try:
		puerto2 = puertos[1]
	except IndexError:
		Sin2.deactivate()
		stop2.deactivate()
		connects2.deactivate()
		puerto2 = 'no hay dispositivo'
	
	
	
	cal = Button(win, Point(xgrid/4+10,refy-22.5), width_b, heigh_b, "Calibrar")
	cal.activate()
	
	quitButton = Button(win, Point(3*xgrid/4-10,refy-22.5), width_b, heigh_b, "Salir")
	quitButton.rect.setFill("#C01A19")
	quitButton.activate()
	
	###############################---Datos Fuente 1---###############################
	
			################## Puerto Serial 1 ##################

	
	port1_name=Text(Point(refx-3,refy),"Puerto Serial 1: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(10)
	port1_name.setTextColor("black")
	port1_name.draw(win)
	
	port1_val=Entry(Point(refx+10,refy),19)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)
	
		################## Frecuencia 1 ##################
	
	freq=Text(Point(refx,refy-3),"Frecuencia(Hz): ")
	freq.setFace('arial')
	freq.setStyle('bold')
	freq.setSize(10)
	#freq.setTextColor("#8EB84A")
	freq.setTextColor("black")
	freq.draw(win)
	
	freq_val=Entry(Point(refx+12,refy-3),10)
	freq_val.setFace('arial')
	freq_val.setSize(10)
	freq_val.setTextColor("white")
	freq_val.setFill('#6B6B6B')
	freq_val.setText('0')
	freq_val.draw(win)
			
		################## Tensión 1 ##################
		
	volt=Text(Point(refx,refy-5.5),"Tensión Limite(V): ")
	volt.setFace('arial')
	volt.setStyle('bold')
	volt.setSize(10)
	volt.setTextColor("black")
	volt.draw(win)
	
	volt_val=Entry(Point(refx+12,refy-5.5),10)
	volt_val.setFace('arial')
	volt_val.setSize(10)
	volt_val.setTextColor("white")
	volt_val.setFill('#6B6B6B')
	volt_val.setText('0')
	volt_val.draw(win)

		################## Corriente 1 ##################
		
	curr=Text(Point(refx,refy-8),"Corriente(A): ")
	curr.setFace('arial')
	curr.setStyle('bold')
	curr.setSize(10)
	curr.setTextColor("black")
	curr.draw(win)
	
	curr_val=Entry(Point(refx+12,refy-8),10)
	curr_val.setFace('arial')
	curr_val.setSize(10)
	curr_val.setTextColor("white")
	curr_val.setFill('#6B6B6B')
	curr_val.setText('0')
	curr_val.draw(win)
	
		################## Periodos 1 ##################

	period=Text(Point(refx,refy-10.5),"Periodos: ")
	period.setFace('arial')
	period.setStyle('bold')
	period.setSize(10)
	period.setTextColor("black")
	period.draw(win)
	
	period_val=Entry(Point(refx+12,refy-10.5),10)
	period_val.setFace('arial')
	period_val.setSize(10)
	period_val.setTextColor("white")
	period_val.setFill('#6B6B6B')
	period_val.setText('0')
	period_val.draw(win)

		################## Armonicas 1 ##################

	harm=Text(Point(refx,refy-13),"Ármonicas: ")
	harm.setFace('arial')
	harm.setStyle('bold')
	harm.setSize(10)
	harm.setTextColor("black")
	harm.draw(win)
	
	harm_val=Entry(Point(refx+12,refy-13),10)
	harm_val.setFace('arial')
	harm_val.setSize(10)
	harm_val.setTextColor("white")
	harm_val.setFill('#6B6B6B')
	harm_val.setText('1')
	harm_val.draw(win)

	
	#############################################################################################3
	
	###############################---Datos Fuente 2---###############################
	
			################## Puerto Serial 2 ##################
	
	port2_name=Text(Point(refx+37,refy),"Puerto Serial 2: ")
	port2_name.setFace('arial')
	port2_name.setStyle('bold')
	port2_name.setSize(10)
	port2_name.setTextColor("black")
	port2_name.draw(win)
	
	port2_val=Entry(Point(refx+50,refy),18)
	port2_val.setFace('arial')
	port2_val.setSize(10)
	port2_val.setTextColor("white")
	port2_val.setFill('#6B6B6B')
	port2_val.setText(puerto2)
	port2_val.draw(win)

		################## Frecuencia 2 ##################
	
	freq2=Text(Point(refx+40,refy-3),"Frecuencia(Hz): ")
	freq2.setFace('arial')
	freq2.setStyle('bold')
	freq2.setSize(10)
	freq2.setTextColor("black")
	freq2.draw(win)
	
	freq2_val=Entry(Point(refx+52,refy-3),10)
	freq2_val.setFace('arial')
	freq2_val.setSize(10)
	freq2_val.setTextColor("white")
	freq2_val.setFill('#6B6B6B')
	freq2_val.setText('0')
	freq2_val.draw(win)
	
		################## Tensión 2 ##################

	volt2=Text(Point(refx+40,refy-5.5),"Tensión Limite(V): ")
	volt2.setFace('arial')
	volt2.setStyle('bold')
	volt2.setSize(10)
	volt2.setTextColor("black")
	volt2.setTextColor("black")
	volt2.draw(win)
	
	volt2_val=Entry(Point(refx+52,refy-5.5),10)
	volt2_val.setFace('arial')
	volt2_val.setSize(10)
	volt2_val.setTextColor("white")
	volt2_val.setFill('#6B6B6B')
	volt2_val.setText('0')
	volt2_val.draw(win)

		################## Corriente 2 ##################

	curr2=Text(Point(refx+40,refy-8),"Corriente(A): ")
	curr2.setFace('arial')
	curr2.setStyle('bold')
	curr2.setSize(10)
	curr2.setTextColor("black")
	curr2.draw(win)
	
	curr2_val=Entry(Point(refx+52,refy-8),10)
	curr2_val.setFace('arial')
	curr2_val.setSize(10)
	curr2_val.setTextColor("white")
	curr2_val.setFill('#6B6B6B')
	curr2_val.setText('0')
	curr2_val.draw(win)

		################## Periodos 2 ##################
		
	period2=Text(Point(refx+40,refy-10.5),"Periodos: ")
	period2.setFace('arial')
	period2.setStyle('bold')
	period2.setSize(10)
	period2.setTextColor("black")
	period2.draw(win)
	
	period2_val=Entry(Point(refx+52,refy-10.5),10)
	period2_val.setFace('arial')
	period2_val.setSize(10)
	period2_val.setTextColor("white")
	period2_val.setFill('#6B6B6B')
	period2_val.setText('0')
	period2_val.draw(win)

		################## Armonicas 2 ##################

	harm2=Text(Point(refx+40,refy-13),"Ármonicas: ")
	harm2.setFace('arial')
	harm2.setStyle('bold')
	harm2.setSize(10)
	harm2.setTextColor("black")
	harm2.draw(win)
	
	harm2_val=Entry(Point(refx+52,refy-13),10)
	harm2_val.setFace('arial')
	harm2_val.setSize(10)
	harm2_val.setTextColor("white")
	harm2_val.setFill('#6B6B6B')
	harm2_val.setText('1')
	harm2_val.draw(win)


	
		################## Mensaje de lectura ##################
	mensaje1=Text(Point(xgrid/4,refy-18),"Fuente 1")
	mensaje1.setFace('arial')
	mensaje1.setStyle('bold')
	mensaje1.setSize(10)
	mensaje1.setTextColor("black")
	mensaje1.draw(win)
	
	mensaje2=Text(Point(3*xgrid/4,refy-18),"Fuente 2")
	mensaje2.setFace('arial')
	mensaje2.setStyle('bold')
	mensaje2.setSize(10)
	mensaje2.setTextColor("black")
	mensaje2.draw(win)

	pt = win.getMouse()
	
	while not quitButton.clicked(pt):
		n=float(period_val.getText())
		f=float(freq_val.getText())
		V=float(volt_val.getText())
		C=float(curr_val.getText())
		n2=float(period2_val.getText())
		f2=float(freq2_val.getText())
		V2=float(volt2_val.getText())
		C2=float(curr2_val.getText())
	
		if (C > 4) or (C < -4) or (C2 > 4) or (C2 < -4):
			curr_val.setText('0')
			tkMessageBox.showerror("Error", "Valor C no puede ser mayor a 4A o menor a -4A")
		
		if (V > 50) or (V < -50):
			volt_val.setText('0')
			tkMessageBox.showerror("Error", "Valor V no puede ser mayor a 50V o menor a -50V")
		
		if (V2 > 50) or (V2 < -50) :
			volt2_val.setText('0')
			tkMessageBox.showerror("Error", "Valor V no puede ser mayor a 50V o menor a -50V")
		
		if (n < 0):
			period_val.setText('0')
			tkMessageBox.showerror("Error", "Valor n no puede ser menor a 0 periodos")
		
		if (n2 < 0):
			period2_val.setText('0')
			tkMessageBox.showerror("Error", "Valor n no puede ser menor a 0 periodos")

		puertos=glob.glob('/dev/tty[U]*')
		try:
			puerto1 = puertos[0]
			connects1.activate()
		except IndexError:
			Sin1.deactivate()
			stop1.deactivate()
			connects1.deactivate()
			puerto1 = 'no hay dispositivo'
		try:
			puerto2 = puertos[1]
			connects2.activate()
		except IndexError:
			Sin2.deactivate()
			stop2.deactivate()
			connects2.deactivate()
			puerto2 = 'no hay dispositivo'
		port1_val.setText(puerto1)
		port2_val.setText(puerto2)
		try:
			mensaje1.setText(puerto1)
			mensaje2.setText(puerto2)
		except Exception, e:
			mensaje1.setText('no hay dispositivo')
			mensaje2.setText('no hay dispositivo')
		
			
		if connects1.clicked(pt):
			port1=port1_val.getText()
			kepco1=SK.Source("Fuente1",port1)
			m1=kepco1.connectport()
			m2=kepco1.identify()
			mensaje1.setText(m1 + "\n" + m2)
			Sin1.activate()
			Sin1.rect.setFill("#33CC00")
			stop1.activate()
			stop1.rect.setFill("#C01A19")
				
		if connects2.clicked(pt):
			port2=port2_val.getText()
			kepco2=SK.Source("Fuente2",port2)
			m1=kepco2.connectport()
			m2=kepco2.identify()
			mensaje2.setText(m1 + "\n" + m2)
			Sin2.activate()
			Sin2.rect.setFill("#33CC00")
			stop2.activate()
			stop2.rect.setFill("#C01A19")
		
		if Sin1.clicked(pt):
			n=float(period_val.getText())
			f=float(freq_val.getText())
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			y1=harm_val.getText();
			y1=y1.split(',');
			y=[int(i) for i in y1]
			if y > 1:
				kepco1.WriteHarm(V,f,n,C,y)
			else:
				kepco1.WriteVoltSine(V,f,n,C)
					
		if Sin2.clicked(pt):
			n2=float(period2_val.getText())
			f2=float(freq2_val.getText())
			V2=float(volt2_val.getText())
			C2=float(curr2_val.getText())
			y3=harm_val.getText();
			y3=y3.split(',');
			y2=[int(i) for i in y3]
			if y2 > 1:
				kepco2.WriteHarm(V2,f2,n2,C2,y2)
			else:
				kepco2.WriteVoltSine(V2,f2,n2,C2)
		
		if stop1.clicked(pt):
			kepco1.stop()
			
		if stop2.clicked(pt):
			kepco2.stop()
		
		if cal.clicked(pt):
			p = subprocess.Popen(['python', 'calv.py'])

		pt = win.getMouse()
	win.close()
main()