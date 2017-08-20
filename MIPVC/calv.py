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
import matplotlib.pyplot as plt
import numpy as np
import math
import glob ##### para buscar los puertos USB disponibles

global SK
def main():
	xgrid=80;
	ygrid=48;
	refx=40;
	refy=ygrid-14;
	width_b=10;
	heigh_b=2;
	width_b2=5;
	heigh_b2=2.5;
	Tm=0.0005;
	puertos=glob.glob('/dev/tty[U]*')
	global Source;
	win = GraphWin("Fuente de Tensión",width=800, height=480)
	win.setCoords(0,0,xgrid,ygrid) #x1 y1 x2 y2
	background = Image(Point(xgrid/2,ygrid/2), 'backg.gif')
	background.draw(win)
	
	logoTEC = Image(Point(xgrid/2-20,ygrid-5), 'TEC.gif')
	logoTEC.draw(win)
	LogoSESLab = Image(Point(xgrid/2+20,ygrid-5), 'SESLab.gif')
	LogoSESLab.draw(win)
	

	line = Line(Point(xgrid/2, refy-14), Point(xgrid/2, refy+2))
	line.setFill("white")
	line.setWidth(2)
	line.draw(win)
	
	line2 = Line(Point(0, refy+5), Point(xgrid, refy+5))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)
			
	line3 = Line(Point(0, refy+2), Point(xgrid, refy+2))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)
	
	line4 = Line(Point(0, refy-14), Point(xgrid, refy-14))
	line4.setFill("white")
	line4.setWidth(2)
	line4.draw(win)
	
	line5 = Line(Point(refx-12, refy-14), Point(refx-12, refy+2))
	line5.setFill("white")
	line5.setWidth(2)
	line5.draw(win)
	
	line6 = Line(Point(refx+12, refy-14), Point(refx+12, refy+2))
	line6.setFill("white")
	line6.setWidth(2)
	line6.draw(win)
	
	line7 = Line(Point(0, refy-18), Point(xgrid, refy-18))
	line7.setFill("white")
	line7.setWidth(2)
	line7.draw(win)
	
	zero = Button(win, Point(refx-6,refy), width_b, heigh_b, "Zero Volt")
	zero.label.setSize(10)
	
	fullsP = Button(win, Point(refx-6,refy-3), width_b, heigh_b, "Max Scale V")
	fullsP.label.setSize(10)
	fullsM = Button(win, Point(refx-6,refy-6), width_b, heigh_b, "Min Scale V")
	fullsM.label.setSize(10)
	
	vprcprP = Button(win, Point(refx-6,refy-9), width_b, heigh_b, "Vmax Proct")
	vprcprP.label.setSize(10)
	vprcprM = Button(win, Point(refx-6,refy-12), width_b, heigh_b, "Vmin Proct")
	vprcprM.label.setSize(10)


	zeroc = Button(win, Point(refx+6,refy), width_b, heigh_b, "Zero Curr")
	zeroc.label.setSize(10)
	
	fullsPc = Button(win, Point(refx+6,refy-3), width_b, heigh_b, "Max Scale C")
	fullsPc.label.setSize(10)
	fullsMc = Button(win, Point(refx+6,refy-6), width_b, heigh_b, "Min Scale C")
	fullsMc.label.setSize(10)
	
	vprcprPc = Button(win, Point(refx+6,refy-9), width_b, heigh_b, "Cmax Proct")
	vprcprPc.label.setSize(10)
	vprcprMc = Button(win, Point(refx+6,refy-12), width_b, heigh_b, "Cmin Proct")
	vprcprMc.label.setSize(10)
	
	plusF = Button(win, Point(refx+16,refy-3), width_b-5, heigh_b, "+")
	plusF.label.setSize(10)
	minusF = Button(win, Point(refx+22,refy-3), width_b-5, heigh_b, "-")
	minusF.label.setSize(10)
	plusC = Button(win, Point(refx+16,refy-6), width_b-5, heigh_b, "++")
	plusC.label.setSize(10)
	minusC = Button(win, Point(refx+22,refy-6), width_b-5, heigh_b, "--")
	minusC.label.setSize(10)
	
	info = Button(win, Point(refx+19,refy-9), width_b, heigh_b, "información")
	info.rect.setFill("#3F51B5")
	info.label.setSize(10)
	info.activate()
	stop = Button(win, Point(refx+19,refy-12), width_b, heigh_b, "■")
	stop.rect.setFill("#C01A19");
	stop.label.setSize(10)

	calstart = Button(win, Point(refx-18,refy-6), width_b, heigh_b, "Empezar")
	calstart.label.setSize(10)
	calstart.activate()
	save = Button(win, Point(refx-18,refy-9), width_b, heigh_b, "Guardar")
	save.label.setSize(10)
	
	quitButton = Button(win, Point(refx-18,refy-12), width_b, heigh_b, "Salir")
	quitButton.label.setSize(10)
	
		
	try:
		puerto1 = puertos[0]
	except IndexError:
		puerto1 = 'no hay dispositivo'


	###############################---Datos Fuente 1---###############################

		################## Calibracion Fina ##################
	
	calval=Text(Point(refx+19,refy),"Calibración:")
	calval.setFace('arial')
	calval.setStyle('bold')
	calval.setSize(10)
	#freq.setTextColor("#8EB84A")
	calval.setTextColor("black")
	calval.draw(win)

	
		################## Puerto Serial ##################
	
	port1_name=Text(Point(refx-5,refy+3.5),"Puerto serial: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(10)
	port1_name.setTextColor("black")
	port1_name.draw(win)
	
	port1_val=Entry(Point(refx+10,refy+3.5),25)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)
	
		################## Constraseña ##################
	
	passw=Text(Point(refx-18,refy-1),"Password:")
	passw.setFace('arial')
	passw.setStyle('bold')
	passw.setSize(10)
	#passw.setTextColor("#8EB84A")
	passw.setTextColor("black")
	passw.draw(win)
	
	passw_val=Entry(Point(refx-18,refy-3),13)
	passw_val.setFace('arial')
	passw_val.setSize(10)
	passw_val.setTextColor("white")
	passw_val.setFill('#6B6B6B')
	passw_val.setText('DEFAULT')
	passw_val.draw(win)

		################## Mensaje de lectura ##################
	mensaje=Text(Point(refx,refy-16),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
		
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
			save.activate();
			save.rect.setFill("#33CC00");
		
		if save.clicked(pt):
			kepco1.calSave();
			quitButton.activate();
			quitButton.rect.setFill("#C01A19");
		
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
			val1='2'
			kepco1.calPlusFine(val1);
		
		if minusF.clicked(pt):
			val2='2'
			kepco1.calMinusFine(val2);
			
		if plusC.clicked(pt):
			val3='1'
			kepco1.calPlusCoarse(val3);
		
		if minusC.clicked(pt):
			val4='1'
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
