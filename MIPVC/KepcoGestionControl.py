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
from HarmGen import *
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import base64
import Tkinter as tk
from urllib2 import urlopen
import glob ##### para buscar los puertos USB disponibles
#from controlTektronix import *

global SK
def main():
	xgrid=27;
	ygrid=23;
	refy=22;
	refx=2;
	refx2=12;
	width_b=3;
	heigh_b=1.5;
	Tm=0.0005;
	global Source;
		
	win = GraphWin("Control de Fuentes Kepco",width=800, height=300)
	win.setCoords(0,0,ygrid,xgrid)
	#win.setBackground('#BCC6CC')
	myImage = Image(Point(10,12.5), 'backg.gif')
	myImage.draw(win)
	
	
	line = Line(Point(10, 0), Point(10, xgrid))
	line.setFill("white")
	line.setWidth(2)
	line.draw(win)
	
	line2 = Line(Point(20, 0), Point(20, xgrid))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)
	
	sin = Button(win, Point(refx,refy), width_b, heigh_b, "sin(ωt)")
	sin.label.setSize(10)
	#sin.activate()
	Harm = Button(win, Point(refx,refy-3), width_b, heigh_b, "Ármonicas")
	Harm.label.setSize(10)
	#Harm.activate()
	currM = Button(win, Point(refx,refy-6), width_b, heigh_b, "Modo-Corriente")
	currM.label.setSize(10)
	#currM.activate()
	dcout = Button(win, Point(refx,refy-9), width_b, heigh_b, "Salida DC")
	dcout.label.setSize(10)
	#dcout.activate()
	info = Button(win, Point(refx,refy-12), width_b, heigh_b, "Información")
	info.label.setSize(10)
	#info.activate()
	stop = Button(win, Point(refx,refy-15), width_b, heigh_b, "Detener")
	stop.label.setSize(10)
	#stop.activate()

	sin2 = Button(win, Point(refx2,refy), width_b, heigh_b, "sin(ωt)")
	sin2.label.setSize(10)
	#sin2.activate()
	Harm2 = Button(win, Point(refx2,refy-3), width_b, heigh_b, "Ármonicas")
	Harm2.label.setSize(10)
	#Harm2.activate()
	currM2 = Button(win, Point(refx2,refy-6), width_b, heigh_b, "Modo Corriente")
	currM2.label.setSize(10)
	#currM2.activate()
	dcout2 = Button(win, Point(refx2,refy-9), width_b, heigh_b, "Salida DC")
	dcout2.label.setSize(10)
	#dcout2.activate()
	info2 = Button(win, Point(refx2,refy-12), width_b, heigh_b, "Información")
	info2.label.setSize(10)
	#info2.activate()
	stop2 = Button(win, Point(refx2,refy-15), width_b, heigh_b, "Detener")
	stop2.label.setSize(10)
	#stop2.activate()
	
	puertos=glob.glob('/dev/tty[U]*')
	try:
		puerto1 = puertos[0]
	except IndexError:
		sin.deactivate()
		Harm.deactivate()
		currM.deactivate()
		dcout.deactivate()
		info.deactivate()
		stop.deactivate()
		puerto1 = 'no hay dispositivo'
		
	try:
		puerto2 = puertos[1]
	except IndexError:
		sin2.deactivate()
		Harm2.deactivate()
		currM2.deactivate()
		dcout2.deactivate()
		info2.deactivate()
		stop2.deactivate()
		puerto2 = 'no hay dispositivo'
	
	
	connects1 = Button(win, Point(refx+6.5,refy+3), width_b-1, heigh_b, "Conectar")
	connects1.label.setSize(10)
	connects1.activate()
	connects2 = Button(win, Point(refx2+6.5,refy+3), width_b-1, heigh_b, "Conectar")
	connects2.label.setSize(10)
	connects2.activate()
	
	caracterizar = Button(win, Point(21.5,10), 2, 2, "Caracterizar")
	caracterizar.label.setSize(10)
	caracterizar.activate()
	
	cal = Button(win, Point(21.5,6), 2, 2, "Calibrar")
	cal.label.setSize(10)
	cal.activate()
	
	quitButton = Button(win, Point(21.5,2), 2, 2, "Salir")
	quitButton.label.setSize(10)
	quitButton.activate()
	
	
	###############################---Datos Fuente 1---###############################
		################## Frecuencia 1 ##################
	
	freq=Text(Point(refx+4,refy),"Frecuencia(Hz): ")
	freq.setFace('arial')
	freq.setStyle('bold')
	freq.setSize(10)
	#freq.setTextColor("#8EB84A")
	freq.setTextColor("black")
	freq.draw(win)
	
	freq_val=Entry(Point(refx+6.5,refy),10)
	freq_val.setFace('arial')
	freq_val.setSize(10)
	freq_val.setTextColor("white")
	freq_val.setFill('#6B6B6B')
	freq_val.draw(win)
	
		################## Tensión 1 ##################
		
	volt=Text(Point(refx+4,refy-3),"Tensión(V): ")
	volt.setFace('arial')
	volt.setStyle('bold')
	volt.setSize(10)
	volt.setTextColor("black")
	volt.draw(win)
	
	volt_val=Entry(Point(refx+6.5,refy-3),10)
	volt_val.setFace('arial')
	volt_val.setSize(10)
	volt_val.setTextColor("white")
	volt_val.setFill('#6B6B6B')
	volt_val.draw(win)

		################## Corriente 1 ##################
		
	curr=Text(Point(refx+4,refy-6),"Corriente(A): ")
	curr.setFace('arial')
	curr.setStyle('bold')
	curr.setSize(10)
	curr.setTextColor("black")
	curr.draw(win)
	
	curr_val=Entry(Point(refx+6.5,refy-6),10)
	curr_val.setFace('arial')
	curr_val.setSize(10)
	curr_val.setTextColor("white")
	curr_val.setFill('#6B6B6B')
	curr_val.draw(win)
	
		################## Periodos 1 ##################

	period=Text(Point(refx+4,refy-9),"Periodos: ")
	period.setFace('arial')
	period.setStyle('bold')
	period.setSize(10)
	period.setTextColor("black")
	period.draw(win)
	
	period_val=Entry(Point(refx+6.5,refy-9),10)
	period_val.setFace('arial')
	period_val.setSize(10)
	period_val.setTextColor("white")
	period_val.setFill('#6B6B6B')
	period_val.draw(win)

		################## Armonicas 1 ##################

	harm=Text(Point(refx+4,refy-12),"Ármonicas: ")
	harm.setFace('arial')
	harm.setStyle('bold')
	harm.setSize(10)
	harm.setTextColor("black")
	harm.draw(win)
	
	harm_val=Entry(Point(refx+6.5,refy-12),10)
	harm_val.setFace('arial')
	harm_val.setSize(10)
	harm_val.setTextColor("white")
	harm_val.setFill('#6B6B6B')
	harm_val.draw(win)

		################## Puerto Serial 1 ##################

	
	port1_name=Text(Point(refx,refy+3),"Puerto Serial 1: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(10)
	port1_name.setTextColor("black")
	port1_name.draw(win)
	
	port1_val=Entry(Point(refx+3.5,refy+3),18)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)
	
	#############################################################################################3
	
	###############################---Datos Fuente 2---###############################
		################## Frecuencia 2 ##################
	
	freq2=Text(Point(refx2+4,refy),"Frecuencia(Hz): ")
	freq2.setFace('arial')
	freq2.setStyle('bold')
	freq2.setSize(10)
	freq2.setTextColor("black")
	freq2.draw(win)
	
	freq2_val=Entry(Point(refx2+6.5,refy),10)
	freq2_val.setFace('arial')
	freq2_val.setSize(10)
	freq2_val.setTextColor("white")
	freq2_val.setFill('#6B6B6B')
	#freq2_val.setText(66)
	freq2_val.draw(win)
	

		################## Tensión 2 ##################

	volt2=Text(Point(refx2+4,refy-3),"Tensión(V): ")
	volt2.setFace('arial')
	volt2.setStyle('bold')
	volt2.setSize(10)
	volt2.setTextColor("black")
	volt2.draw(win)
	
	volt2_val=Entry(Point(refx2+6.5,refy-3),10)
	volt2_val.setFace('arial')
	volt2_val.setSize(10)
	volt2_val.setTextColor("white")
	volt2_val.setFill('#6B6B6B')
	volt2_val.draw(win)

		################## Corriente 2 ##################

	curr2=Text(Point(refx2+4,refy-6),"Corriente(A): ")
	curr2.setFace('arial')
	curr2.setStyle('bold')
	curr2.setSize(10)
	curr2.setTextColor("black")
	curr2.draw(win)
	
	curr2_val=Entry(Point(refx2+6.5,refy-6),10)
	curr2_val.setFace('arial')
	curr2_val.setSize(10)
	curr2_val.setTextColor("white")
	curr2_val.setFill('#6B6B6B')
	curr2_val.draw(win)

		################## Periodos 2 ##################
		
	period2=Text(Point(refx2+4,refy-9),"Periodos: ")
	period2.setFace('arial')
	period2.setStyle('bold')
	period2.setSize(10)
	period2.setTextColor("black")
	period2.draw(win)
	
	period2_val=Entry(Point(refx2+6.5,refy-9),10)
	period2_val.setFace('arial')
	period2_val.setSize(10)
	period2_val.setTextColor("white")
	period2_val.setFill('#6B6B6B')
	period2_val.draw(win)

		################## Armonicas 2 ##################

	harm2=Text(Point(refx2+4,refy-12),"Ármonicas: ")
	harm2.setFace('arial')
	harm2.setStyle('bold')
	harm2.setSize(10)
	harm2.setTextColor("black")
	harm2.draw(win)
	
	harm2_val=Entry(Point(refx2+6.5,refy-12),10)
	harm2_val.setFace('arial')
	harm2_val.setSize(10)
	harm2_val.setTextColor("white")
	harm2_val.setFill('#6B6B6B')
	harm2_val.draw(win)

		################## Puerto Serial 2 ##################
	
	port2_name=Text(Point(refx+10,refy+3),"Puerto Serial 2: ")
	port2_name.setFace('arial')
	port2_name.setStyle('bold')
	port2_name.setSize(10)
	port2_name.setTextColor("black")
	port2_name.draw(win)
	
	port2_val=Entry(Point(refx+13.5,refy+3),18)
	port2_val.setFace('arial')
	port2_val.setSize(10)
	port2_val.setTextColor("white")
	port2_val.setFill('#6B6B6B')
	port2_val.setText(puerto2)
	port2_val.draw(win)
	
	
		################## Mensaje de lectura ##################
	mensaje=Text(Point(5,2),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(10)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	mensaje2=Text(Point(15,2),"")
	mensaje2.setFace('arial')
	mensaje2.setStyle('bold')
	mensaje2.setSize(10)
	mensaje2.setTextColor("black")
	mensaje2.draw(win)

	pt = win.getMouse()
	
	while not quitButton.clicked(pt):
		puertos=glob.glob('/dev/tty[U]*')
		try:
			puerto1 = puertos[0]
		except IndexError:
			sin.deactivate()
			Harm.deactivate()
			currM.deactivate()
			dcout.deactivate()
			info.deactivate()
			stop.deactivate()
			puerto1 = 'no hay dispositivo'
			
		try:
			puerto2 = puertos[1]
		except IndexError:
			sin2.deactivate()
			Harm2.deactivate()
			currM2.deactivate()
			dcout2.deactivate()
			info2.deactivate()
			stop2.deactivate()
			puerto2 = 'no hay dispositivo'
		port1_val.setText(puerto1)
		port2_val.setText(puerto2)
		try:
			mensaje.setText(puerto1)
			mensaje2.setText(puerto2)
		except Exception, e:
			mensaje.setText('no hay dispositivo')
			mensaje2.setText('no hay dispositivo')
		
			
		if connects1.clicked(pt):
			port1=port1_val.getText()
			kepco1=SK.Source("Fuente1",port1)
			m1=kepco1.connectport()
			m2=kepco1.identify()
			mensaje.setText(m1 + "\n" + m2)
			sin.activate()
			Harm.activate()
			currM.activate()
			dcout.activate()
			info.activate()
			stop.activate()
				
		if connects2.clicked(pt):
			port2=port2_val.getText()
			kepco2=SK.Source("Fuente2",port2)
			m1=kepco2.connectport()
			m2=kepco2.identify()
			mensaje2.setText(m1 + "\n" + m2)
			sin2.activate()
			Harm2.activate()
			currM2.activate()
			dcout2.activate()
			info2.activate()
			stop2.activate()
		
		if dcout.clicked(pt):
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			kepco1.WriteVolt(V,C)
		
		if dcout2.clicked(pt):
			V2=float(volt2_val.getText())
			C2=float(curr2_val.getText())
			kepco2.WriteVolt(V2,C2)
		
		if currM.clicked(pt):
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			estado=kepco1.WriteCurr(V,C)
			mensaje.setText(estado)
		
		if currM2.clicked(pt):
			V2=float(volt2_val.getText())
			C2=float(curr2_val.getText())
			estado2=kepco2.WriteCurr(V2,C2)
			mensaje2.setText(estado2)
						
		if Harm.clicked(pt):
			y1=harm_val.getText();
			y1=y1.split(',');
			y=[int(i) for i in y1]
			n=float(period_val.getText())
			f=float(freq_val.getText())
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			kepco1.WriteHarm(V,f,n,C,y)

		if Harm2.clicked(pt):
			y3=harm2_val.getText()
			y2=[];
			for i in range(0,len(y3),2):
				y2.append(int(y3[i]))
			n2=float(period2_val.getText())
			f2=float(freq2_val.getText())
			V2=float(volt2_val.getText())
			C2=float(curr2_val.getText())
			kepco2.WriteHarm(funct2,f2,n2,C2)
		
		if sin.clicked(pt):
			n=float(period_val.getText())
			f=float(freq_val.getText())
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			#ts=float(tsm.getText())
			kepco1.WriteVoltSine(V,f,n,C)

		if sin2.clicked(pt):
			n2=float(period2_val.getText())
			f2=float(freq2_val.getText())
			V2=float(volt2_val.getText())
			C2=float(curr2_val.getText())
			kepco2.WriteVoltSine(V2,f2,n2,C2)

		if info.clicked(pt):
			source1=kepco1.identify()
			print(source1)
			mensaje.setText(source1)
		
		if info2.clicked(pt):
			source2=kepco2.identify()
			print(source2)
			mensaje2.setText(source2)
		
		if cal.clicked(pt):
			execfile('calv.py')	
		
		if stop.clicked(pt):
			kepco1.stop()
			
		if stop2.clicked(pt):
			kepco2.stop()
		
		if caracterizar.clicked(pt):
			execfile('caracterizar.py')
		
		pt = win.getMouse()
	win.close()
main()
