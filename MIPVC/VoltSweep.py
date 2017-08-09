#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:v2Sweep.py
#Descripción		:Programa de barrido de tension.
#Autor          	:Javier Campos Rojas
#Fecha            	:Agosto-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

from graphics import *
from button import *
import SerialKepco as SK
from HarmGen import *
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
global SK

def main():
	xgrid=35;
	ygrid=10;
	refy=23;
	refx=2;
	refx2=11;
	width_b=2.5;
	heigh_b=1.8;
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

		
	win = GraphWin("Volt Sweep",width=400, height=400)
	win.setCoords(0,0,ygrid,xgrid)
	#win.setBackground('#BCC6CC')
	myImage = Image(Point(5,15), 'backg2.gif')
	myImage.draw(win)
	LogoSESLab = Image(Point(5,refy+8), 'SESLab.gif')
	LogoSESLab.draw(win)


	line = Line(Point(0, refy+2), Point(ygrid,refy+2))
	line.setFill("white")
	line.setWidth(2)
	line.draw(win)

	line2 = Line(Point(0, refy-14.5), Point(ygrid,refy-14.5))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)

	line3 = Line(Point(0, refy-17.5), Point(ygrid,refy-17.5))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)


	connects1 = Button(win, Point(refx-0.5,refy-16), width_b, heigh_b, "Conectar")
	connects1.activate()

	sweep = Button(win, Point(refx+3,refy-16), width_b, heigh_b, "Barrido")
	#sweep.activate()

	Salir = Button(win, Point(refx+6.5,refy-16), width_b, heigh_b, "Salir")
	Salir.activate()


	###############################---Datos Fuente 1---###############################
		################## Frecuencia 1 ##################

	v1=Text(Point(refx,refy),"Tensión(V) V₁: ")
	v1.setFace('arial')
	v1.setStyle('bold')
	v1.setSize(12)
	#v1.setTextColor("#8EB84A")
	v1.setTextColor("white")
	v1.draw(win)

	v1_val=Entry(Point(refx+5,refy),20)
	v1_val.setFace('arial')
	v1_val.setSize(10)
	v1_val.setTextColor("white")
	v1_val.setFill('#6B6B6B')
	v1_val.draw(win)

		################## Tensión 1 ##################
		
	v2=Text(Point(refx,refy-3),"Tensión(V) V₂: ")
	v2.setFace('arial')
	v2.setStyle('bold')
	v2.setSize(12)
	v2.setTextColor("white")
	v2.draw(win)

	v2_val=Entry(Point(refx+5,refy-3),20)
	v2_val.setFace('arial')
	v2_val.setSize(10)
	v2_val.setTextColor("white")
	v2_val.setFill('#6B6B6B')
	v2_val.draw(win)
	
			################## Delta V ##################
		
	deltaV=Text(Point(refx,refy-6),"Δt de barrido(V): ")
	deltaV.setFace('arial')
	deltaV.setStyle('bold')
	deltaV.setSize(12)
	deltaV.setTextColor("white")
	deltaV.draw(win)

	deltaV_val=Entry(Point(refx+5,refy-6),20)
	deltaV_val.setFace('arial')
	deltaV_val.setSize(10)
	deltaV_val.setTextColor("white")
	deltaV_val.setFill('#6B6B6B')
	deltaV_val.draw(win)

		################## Corriente 1 ##################
		
	curr=Text(Point(refx,refy-9),"Corriente Limite: ")
	curr.setFace('arial')
	curr.setStyle('bold')
	curr.setSize(12)
	curr.setTextColor("white")
	curr.draw(win)

	curr_val=Entry(Point(refx+5,refy-9),20)
	curr_val.setFace('arial')
	curr_val.setSize(10)
	curr_val.setTextColor("white")
	curr_val.setFill('#6B6B6B')
	curr_val.draw(win)

		################## deltaTos 1 ##################

	deltaT=Text(Point(refx,refy-12),"Δt de barrido(s): ")
	deltaT.setFace('arial')
	deltaT.setStyle('bold')
	deltaT.setSize(12)
	deltaT.setTextColor("white")
	deltaT.draw(win)

	deltaT_val=Entry(Point(refx+5,refy-12),20)
	deltaT_val.setFace('arial')
	deltaT_val.setSize(10)
	deltaT_val.setTextColor("white")
	deltaT_val.setFill('#6B6B6B')
	deltaT_val.draw(win)


		################## Puerto Serial 1 ##################


	port1_name=Text(Point(refx,refy+4),"Puerto Serial 1: ")
	port1_name.setFace('arial')
	port1_name.setStyle('bold')
	port1_name.setSize(12)
	port1_name.setTextColor("white")
	port1_name.draw(win)

	port1_val=Entry(Point(refx+5,refy+4),20)
	port1_val.setFace('arial')
	port1_val.setSize(10)
	port1_val.setTextColor("white")
	port1_val.setFill('#6B6B6B')
	port1_val.setText(puerto1)
	port1_val.draw(win)

		################## Mensaje de lectura ##################
	mensaje=Text(Point(5,refy-20),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)
	
	
	def rutinaDeltaV(vi,vf,C,dT,dV,fuente):
		corriente=[]
		tension=[]
		if vf > vi:
			dV=-dV
		sweep=np.arange(vi,vf,dV)
		#for i in range(int(vi),int(vf+dV),int(dV)):
		for i in sweep:
			kepco1.WriteVolt(i,C)
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
		plt.style.use('ggplot')
		plt.plot(sweep,corriente)
		plt.xlabel('Tension (V)')
		plt.ylabel('Corriente (A)')
		plt.show(block=False)
		
					
	pt = win.getMouse()
	while not Salir.clicked(pt):
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
	win.close()
main()
