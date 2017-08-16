#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:calv.py
#Descripción		:Interfaz de usuario para la calibración de las fuentes Kepco.
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
import glob ##### para buscar los puertos USB disponibles

global SK
def main():
	refy=35;
	refy2=20;
	refx=15;
	width_b=8;
	heigh_b=2;
	Tm=0.0005;
	puertos=glob.glob('/dev/tty[U]*')
	try:
		puerto1 = puertos[0]
	except IndexError:
		puerto1 = 'no hay dispositivo'
	
	win = GraphWin("Control de Fuentes Kepco",width=450, height=400)
	win.setCoords(0,0,40,40)
	#win.setBackground('#BCC6CC')
	myImage = Image(Point(10,12.5), 'backg.gif')
	myImage.draw(win)
	
	line1 = Line(Point(10, refy-refy2), Point(10, refy+2))
	line1.setFill("white")
	line1.setWidth(2)
	line1.draw(win)
	
	line2 = Line(Point(30, refy-refy2), Point(30, refy+2))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)
	
	line3 = Line(Point(0, refy+2), Point(40, refy+2))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)
	
	line4 = Line(Point(0, refy-refy2), Point(40, refy-refy2))
	line4.setFill("white")
	line4.setWidth(2)
	line4.draw(win)
	
	zero = Button(win, Point(refx,refy), width_b, heigh_b, "Zero Volt")
	zero.label.setSize(10)
	
	fullsP = Button(win, Point(refx,refy-3), width_b, heigh_b, "Max Scale V")
	fullsP.label.setSize(10)
	fullsM = Button(win, Point(refx,refy-6), width_b, heigh_b, "Min Scale V")
	fullsM.label.setSize(10)
	
	vprcprP = Button(win, Point(refx,refy-9), width_b, heigh_b, "Vmax Proct")
	vprcprP.label.setSize(10)
	vprcprM = Button(win, Point(refx,refy-12), width_b, heigh_b, "Vmin Proct")
	vprcprM.label.setSize(10)


	zeroc = Button(win, Point(refx+10,refy), width_b, heigh_b, "Zero Curr")
	zeroc.label.setSize(10)
	
	fullsPc = Button(win, Point(refx+10,refy-3), width_b, heigh_b, "Max Scale C")
	fullsPc.label.setSize(10)
	fullsMc = Button(win, Point(refx+10,refy-6), width_b, heigh_b, "Min Scale C")
	fullsMc.label.setSize(10)
	
	vprcprPc = Button(win, Point(refx+10,refy-9), width_b, heigh_b, "Cmax Proct")
	vprcprPc.label.setSize(10)
	vprcprMc = Button(win, Point(refx+10,refy-12), width_b, heigh_b, "Cmin Proct")
	vprcprMc.label.setSize(10)
	
	info = Button(win, Point(refx+20,refy-15), width_b, heigh_b, "info")
	info.label.setSize(10)
	info.activate()
	stop = Button(win, Point(refx+20,refy-18), width_b, heigh_b, "Stop")
	stop.label.setSize(10)
	
	plusF = Button(win, Point(refx+18,refy-9), width_b-5, heigh_b, "+")
	plusF.label.setSize(10)
	minusF = Button(win, Point(refx+22,refy-9), width_b-5, heigh_b, "-")
	minusF.label.setSize(10)
	plusC = Button(win, Point(refx+18,refy-12), width_b-5, heigh_b, "++")
	plusC.label.setSize(10)
	minusC = Button(win, Point(refx+22,refy-12), width_b-5, heigh_b, "--")
	minusC.label.setSize(10)
	
	calstart = Button(win, Point(refx-10,refy-6), width_b, heigh_b, "Empezar")
	calstart.label.setSize(10)
	calstart.activate()
	save = Button(win, Point(refx-10,refy-9), width_b, heigh_b, "Guardar")
	save.label.setSize(10)
	
	quitButton = Button(win, Point(30,2), width_b-2, heigh_b, "Salir")
	quitButton.label.setSize(10)
	
	
	###############################---Datos Fuente 1---###############################

		################## Calibracion Fina ##################
	
	calval=Text(Point(refx+20,refy-3),"Calibración:")
	calval.setFace('arial')
	calval.setStyle('bold')
	calval.setSize(10)
	#freq.setTextColor("#8EB84A")
	calval.setTextColor("black")
	calval.draw(win)
	
	calval_val=Entry(Point(refx+20,refy-6),2)
	calval_val.setFace('arial')
	calval_val.setSize(10)
	calval_val.setTextColor("white")
	calval_val.setFill('#6B6B6B')
	calval_val.setText(0)
	calval_val.draw(win)
	
		################## Puerto Serial ##################
	
	port1_name=Text(Point(refx-10,refy+3.5),"Puerto serial: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(10)
	port1_name.setTextColor("black")
	port1_name.draw(win)
	
	port1_val=Entry(Point(refx+5,refy+3.5),25)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)
	
		################## Constraseña ##################
	
	passw=Text(Point(refx-10,refy-1),"Password:")
	passw.setFace('arial')
	passw.setStyle('bold')
	passw.setSize(10)
	#passw.setTextColor("#8EB84A")
	passw.setTextColor("black")
	passw.draw(win)
	
	passw_val=Entry(Point(refx-10,refy-3),13)
	passw_val.setFace('arial')
	passw_val.setSize(10)
	passw_val.setTextColor("white")
	passw_val.setFill('#6B6B6B')
	passw_val.setText('DEFAULT')
	passw_val.draw(win)

		################## Mensaje de lectura ##################
	mensaje=Text(Point(20,refy-27),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	mensaje2=Text(Point(15,refy-30),"")
	mensaje2.setFace('arial')
	mensaje2.setStyle('bold')
	mensaje2.setSize(11)
	mensaje2.setTextColor("black")
	mensaje2.draw(win)
	
	pt = win.getMouse()
	
	while not quitButton.clicked(pt):

		puertos=glob.glob('/dev/tty[U]*')
		try:
			puerto1 = puertos[0]
		except IndexError:
			puerto1 = 'no hay dispositivo'
		port1_val.setText(puerto1)
		
		if calstart.clicked(pt):
			port1=port1_val.getText()
			kepco1=SK.Source("Fuente1",port1)
			m1=kepco1.connectport()
			m2=kepco1.identify()
			mensaje.setText(m1 + "\n" + m2)
			password1=passw_val.getText()
			kepco1.calStart(password1);
			minusF.activate();
			plusF.activate()
			minusC.activate();
			plusC.activate()
			vprcprP.activate();
			vprcprPc.activate();
			vprcprM.activate();
			vprcprMc.activate();
			zero.activate();
			zeroc.activate();
			fullsP.activate();
			fullsPc.activate();
			fullsM.activate();
			fullsMc.activate();
			stop.activate();
			save.activate()
		
		if save.clicked(pt):
			kepco1.calSave();
			quitButton.activate();	
		
		### Tension #####
		if zero.clicked(pt):
			kepco1.calZero();
	
		if fullsP.clicked(pt):
			kepco1.calMax();
		
		if fullsM.clicked(pt):
			kepco1.calMin();
		
		if vprcprP.clicked(pt):
			kepco1.calVPRmax();
		
		if vprcprM.clicked(pt):
			kepco1.calVPRmin();
			
		### Corriente #####
		if zeroc.clicked(pt):
			kepco1.calZeroC();
	
		if fullsPc.clicked(pt):
			kepco1.calMaxC();
		
		if fullsMc.clicked(pt):
			kepco1.calMinC();
		
		if vprcprPc.clicked(pt):
			kepco1.calCmax();
		
		if vprcprMc.clicked(pt):
			kepco1.calCmin();
		
		######
		
		if plusF.clicked(pt):
			val1=calval.getText()
			kepco1.calPlusFine(val1);
		
		if minusF.clicked(pt):
			val2=calval.getText()
			kepco1.calMinusFine(val2);
			
		if plusC.clicked(pt):
			val3=calval.getText()
			kepco1.calPlusCoarse(val3);
		
		if minusC.clicked(pt):
			val4=calval.getText()
			kepco1.calMinusCoarse(val4);
		
		if info.clicked(pt):
			source1=kepco1.identify()
			print(source1)
			mensaje.setText(source1)

		if stop.clicked(pt):
			kepco1.stop()

		pt = win.getMouse()
	win.close()
main()
