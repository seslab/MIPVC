#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:Sinusoidales.py
#Descripción		:Interfaz de control de fuentes para generar barrido de corriente.
#Autor          	:Javier Campos Rojas
#Fecha            	:Agosto-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================


from graphics import *
from button import *
import SerialKepco as SK
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
import numpy as np
import math
import io
import base64
import Tkinter as tk
from urllib2 import urlopen
import glob ##### para buscar los puertos USB disponibles
import tkMessageBox

global SK

def main():
	xgrid=80;
	ygrid=48;
	refx=25;
	refy=ygrid-18;
	width_b=10;
	heigh_b=2;
	width_b2=5;
	heigh_b2=2.5;
	Tm=0.0005;
	global Source;
	puertos=glob.glob('/dev/tty[U]*')

	win = GraphWin("Fuente de Tensión",width=800, height=480)
	win.setCoords(0,0,xgrid,ygrid) #x1 y1 x2 y2
	background = Image(Point(xgrid/2,ygrid/2), 'backg2.gif')
	background.draw(win)
	logoTEC = Image(Point(xgrid/2-20,ygrid-5), 'TEC.gif')
	logoTEC.draw(win)
	LogoSESLab = Image(Point(xgrid/2+20,ygrid-5), 'SESLab.gif')
	LogoSESLab.draw(win)
			
	line0 = Line(Point(0, refy+6), Point(xgrid,refy+6))
	line0.setFill("white")
	line0.setWidth(2)
	line0.draw(win)
	
	line1 = Line(Point(0, refy+2), Point(xgrid,refy+2))
	line1.setFill("white")
	line1.setWidth(2)
	line1.draw(win)

	line2 = Line(Point(0, refy-14.5), Point(xgrid,refy-14.5))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)

	line3 = Line(Point(0, refy-17.5), Point(xgrid,refy-17.5))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)


	connects1 = Button(win, Point(refx,refy-16), width_b, heigh_b, "Conectar")
	connects1.activate()

	sweep = Button(win, Point(refx+15,refy-16), width_b, heigh_b, "Barrido")
	#sweep.activate()

	Salir = Button(win, Point(refx+30,refy-16), width_b, heigh_b, "Salir")
	Salir.activate()
	
	try:
		puerto1 = puertos[0]
	except IndexError:
		puerto1 = 'no hay dispositivo'
	try:
		puerto2 = puertos[1]
	except IndexError:
		puerto2 = 'no hay dispositivo'


	###############################---Datos Fuente 1---###############################
		################## Frecuencia 1 ##################

	v1=Text(Point(refx+7.5,refy),"Corriente(A) I₁: ")
	v1.setFace('arial')
	v1.setStyle('bold')
	v1.setSize(12)
	#v1.setTextColor("#8EB84A")
	v1.setTextColor("white")
	v1.draw(win)

	v1_val=Entry(Point(refx+22.5,refy),20)
	v1_val.setFace('arial')
	v1_val.setSize(10)
	v1_val.setTextColor("white")
	v1_val.setFill('#6B6B6B')
	v1_val.setText('0')
	v1_val.draw(win)

		################## Tensión 1 ##################
		
	v2=Text(Point(refx+7.5,refy-3),"Corriente(A) I₂: ")
	v2.setFace('arial')
	v2.setStyle('bold')
	v2.setSize(12)
	v2.setTextColor("white")
	v2.draw(win)

	v2_val=Entry(Point(refx+22.5,refy-3),20)
	v2_val.setFace('arial')
	v2_val.setSize(10)
	v2_val.setTextColor("white")
	v2_val.setFill('#6B6B6B')
	v2_val.setText('0')
	v2_val.draw(win)
	
			################## Delta V ##################
		
	deltaV=Text(Point(refx+7.5,refy-6),"ΔI: ")
	deltaV.setFace('arial')
	deltaV.setStyle('bold')
	deltaV.setSize(12)
	deltaV.setTextColor("white")
	deltaV.draw(win)

	deltaV_val=Entry(Point(refx+22.5,refy-6),20)
	deltaV_val.setFace('arial')
	deltaV_val.setSize(10)
	deltaV_val.setTextColor("white")
	deltaV_val.setFill('#6B6B6B')
	deltaV_val.setText('0')
	deltaV_val.draw(win)

		################## Corriente 1 ##################
		
	curr=Text(Point(refx+7.5,refy-9),"Tensión Limite: ")
	curr.setFace('arial')
	curr.setStyle('bold')
	curr.setSize(12)
	curr.setTextColor("white")
	curr.draw(win)

	curr_val=Entry(Point(refx+22.5,refy-9),20)
	curr_val.setFace('arial')
	curr_val.setSize(10)
	curr_val.setTextColor("white")
	curr_val.setFill('#6B6B6B')
	curr_val.setText('0')
	curr_val.draw(win)

		################## deltaTos 1 ##################

	deltaT=Text(Point(refx+7.5,refy-12),"Δt: ")
	deltaT.setFace('arial')
	deltaT.setStyle('bold')
	deltaT.setSize(12)
	deltaT.setTextColor("white")
	deltaT.draw(win)

	deltaT_val=Entry(Point(refx+22.5,refy-12),20)
	deltaT_val.setFace('arial')
	deltaT_val.setSize(10)
	deltaT_val.setTextColor("white")
	deltaT_val.setFill('#6B6B6B')
	deltaT_val.setText('1')
	deltaT_val.draw(win)


		################## Puerto Serial 1 ##################


	port1_name=Text(Point(refx+7.5,refy+4),"Puerto Serial 1: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(12)
	port1_name.setTextColor("white")
	port1_name.draw(win)

	port1_val=Entry(Point(refx+22.5,refy+4),20)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)

		################## Mensaje de lectura ##################
	mensaje=Text(Point(refx+15,5),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	
	def rutinaDeltaV(vi,vf,C,dT,dV,fuente):
		corriente=[]
		tension=[]
		if vi > vf:
			dV=-dV
		else:
			dV=dV
		sweep=np.arange(vi,vf,dV)
		print sweep
		print vi
		print vf
		#for i in range(int(vi),int(vf+dV),int(dV)):
		for i in sweep:
			kepco1.WriteCurr(i,C)
			time.sleep(dT)
			c1=kepco1.measC()
			v2=kepco1.measV()
			t=time.strftime("%Y,%m,%d,%H,%M,%S")
			print "I= " + str(c1) + " V= " +str(v2) + " t= " +str(t)
			#print corriente
			corriente.append(float(c1))
			tension.append(float(v2))
		corriente=np.array(corriente)	
		tension=np.array(tension)
		np.savetxt("/home/SESLab/medicion.csv",np.array([corriente,tension]).T,delimiter=',')
		#plt.style.use('ggplot')
		#plt.plot(sweep,corriente)
		#plt.xlabel('Tension (V)')
		#plt.ylabel('Corriente (A)')
		#plt.show(block=False)
		
					
	pt = win.getMouse()
	while not Salir.clicked(pt):
		dT=float(deltaT_val.getText())
		dV=float(deltaV_val.getText())
		v1_in=float(v1_val.getText())
		v2_in=float(v2_val.getText())
		C=float(curr_val.getText())
		if (dT < 0.0005):
			deltaT_val.setText('0.0005')
			tkMessageBox.showerror("Error", "Valor Δt debe ser mayor a 0.0005s")
		
		if (dV > max(v1_in,v2_in)):
			deltaV_val.setText('0')
			tkMessageBox.showerror("Error", "Valor ΔV no puede ser mayor a V₁ o V₂")
		
		if (C > 4) or (C < -4) :
			curr_val.setText('0')
			tkMessageBox.showerror("Error", "Valor C no puede ser mayor a 4A o menor a -4A")
		
		if (v1_in > 50) or (v1_in < -50) :
			v1_val.setText('0')
			tkMessageBox.showerror("Error", "Valor V no puede ser mayor a 50V o menor a -50V")	
		
		if (v2_in > 50) or (v2_in < -50) :
			v2_val.setText('0')
			tkMessageBox.showerror("Error", "Valor V no puede ser mayor a 50V o menor a -50V")
		
		puertos=glob.glob('/dev/tty[U]*')
		
		try:
			puerto1 = puertos[0]
		except IndexError:
			puerto1 = 'no hay dispositivo'
		port1_val.setText(puerto1)
		if connects1.clicked(pt):
			port1=port1_val.getText()
			kepco1=SK.Source("Fuente1",port1)
			m1=kepco1.connectport()
			m2=kepco1.identify()
			mensaje.setText(m1 + m2)
			sweep.activate()
		if sweep.clicked(pt):
			dT=float(deltaT_val.getText())
			dV=float(deltaV_val.getText())
			v1_in=float(v1_val.getText())
			v2_in=float(v2_val.getText())
			C=float(curr_val.getText())
			mensaje.setText("Barrido en progreso...")
			
			##Rutina Barrido de Frecuencias##
			rutinaDeltaV(v1_in,v2_in,C,dT,dV,kepco1)
			Salir.activate()
			mensaje.setText("Barrido finalizado")
			
		pt = win.getMouse()
	if sweep.active==True:
		kepco1.stop()
	win.close()
main()
