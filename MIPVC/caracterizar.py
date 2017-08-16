#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:caracterizar.py
#Descripción		:Programa de caracterización.
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
#import controlTektronix as CT
import RPi.GPIO as GPIO
import SensorVC as VC
global GPIO
global SK
global CT
global VC

def main():
	##Relay##
	relay=14;
	GPIO.setwarnings(False);
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(relay, GPIO.OUT,initial=GPIO.LOW)

	xgrid=30;
	ygrid=10;
	refy=19;
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

		
	win = GraphWin("Caracterizador",width=400, height=350)
	win.setCoords(0,0,ygrid,xgrid)
	#win.setBackground('#BCC6CC')
	myImage = Image(Point(5,15), 'backg2.gif')
	myImage.draw(win)
	LogoSESLab = Image(Point(5,27), 'SESLab.gif')
	LogoSESLab.draw(win)


	line = Line(Point(0, refy+2), Point(ygrid,refy+2))
	line.setFill("white")
	line.setWidth(2)
	line.draw(win)

	line2 = Line(Point(0, refy-11.5), Point(ygrid,refy-11.5))
	line2.setFill("white")
	line2.setWidth(2)
	line2.draw(win)

	line3 = Line(Point(0, refy-14.5), Point(ygrid,refy-14.5))
	line3.setFill("white")
	line3.setWidth(2)
	line3.draw(win)


	connects1 = Button(win, Point(refx-0.5,refy-13), width_b, heigh_b, "Conectar")
	connects1.activate()

	caracterizar = Button(win, Point(refx+3,refy-13), width_b, heigh_b, "Caracterizar")
	#caracterizar.activate()

	Salir = Button(win, Point(refx+6.5,refy-13), width_b, heigh_b, "Salir")
	Salir.activate()


	###############################---Datos Fuente 1---###############################
		################## Frecuencia 1 ##################

	freq=Text(Point(refx,refy),"Frecuencia(Hz): ")
	freq.setFace('arial')
	freq.setStyle('bold')
	freq.setSize(12)
	#freq.setTextColor("#8EB84A")
	freq.setTextColor("white")
	freq.draw(win)

	freq_val=Entry(Point(refx+5,refy),20)
	freq_val.setFace('arial')
	freq_val.setSize(10)
	freq_val.setTextColor("white")
	freq_val.setFill('#6B6B6B')
	freq_val.draw(win)

		################## Tensión 1 ##################
		
	volt=Text(Point(refx,refy-3),"Tensión(V): ")
	volt.setFace('arial')
	volt.setStyle('bold')
	volt.setSize(12)
	volt.setTextColor("white")
	volt.draw(win)

	volt_val=Entry(Point(refx+5,refy-3),20)
	volt_val.setFace('arial')
	volt_val.setSize(10)
	volt_val.setTextColor("white")
	volt_val.setFill('#6B6B6B')
	volt_val.draw(win)

		################## Corriente 1 ##################
		
	curr=Text(Point(refx,refy-6),"Corriente(A): ")
	curr.setFace('arial')
	curr.setStyle('bold')
	curr.setSize(12)
	curr.setTextColor("white")
	curr.draw(win)

	curr_val=Entry(Point(refx+5,refy-6),20)
	curr_val.setFace('arial')
	curr_val.setSize(10)
	curr_val.setTextColor("white")
	curr_val.setFill('#6B6B6B')
	curr_val.draw(win)

		################## Periodos 1 ##################

	period=Text(Point(refx,refy-9),"Δt de barrido(s): ")
	period.setFace('arial')
	period.setStyle('bold')
	period.setSize(12)
	period.setTextColor("white")
	period.draw(win)

	period_val=Entry(Point(refx+5,refy-9),20)
	period_val.setFace('arial')
	period_val.setSize(10)
	period_val.setTextColor("white")
	period_val.setFill('#6B6B6B')
	period_val.draw(win)


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
	mensaje=Text(Point(5,2),"")
	mensaje.setFace('arial')
	mensaje.setStyle('bold')
	mensaje.setSize(11)
	mensaje.setTextColor("black")
	mensaje.draw(win)


		
	def rutinaDeltaf(V,f,C,n,fuente):
		for i in range(int(f)-5,int(f)+5):
			fuente.WriteVoltSine(V,i,i*n,C)
			time.sleep(1);
	def rutinaDeltaV(V,f,C,n,fuente):
		for i in range(int(V),int(V)+15):
			fuente.WriteVoltSine(i,f,f*n,C)
			time.sleep(1);
		for i in range(int(V)+15,int(V)-15,-1):
			fuente.WriteVoltSine(i,f,f*n,C)
			time.sleep(1);

	pt = win.getMouse()
	a=1;
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
			caracterizar.activate()
		if caracterizar.clicked(pt):
			GPIO.output(relay, GPIO.LOW);
			time.sleep(0.2)
			n=float(period_val.getText())
			f=float(freq_val.getText())
			V=float(volt_val.getText())
			C=float(curr_val.getText())
			#ts=float(tsm.getText())
			Salir.deactivate()
			mensaje.setText("Caracterizando...")
			#osc1=CT.getWave();
			#meas=VC.Sensor();
			meas=VC.Sensor(55*(1+n));
			#alerta1=osc1.connectOsc()
			#mensaje.setText("Caracterizando..."+'\n'+alerta1)
			#alerta2=osc1.OscWave()
			#mensaje.setText("Caracterizando..."+'\n'+alerta2)
			meas.start();
			#meas.CurrMeas(55*(1+n));
			##Rutina Barrido de Frecuencias##
			osc1=CT.getWave();
			rutinaDeltaf(V,f,C,n,kepco1);
			osc1=CT.getWave();
			rutinaDeltaV(V,f,C,n,kepco1)
			osc1=CT.getWave();
			##Rutina Barrido de Desconexion##
			GPIO.output(relay, GPIO.HIGH);
			time.sleep(1);
			GPIO.output(relay, GPIO.LOW);
			Salir.activate()
			mensaje.setText("¡Caracterización lista!")
		pt = win.getMouse()
	win.close()
main()
