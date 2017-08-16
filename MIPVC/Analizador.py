#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:Analizador.py
#Descripción		:Programa analizador de datos y calculo de FFT.
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

import matplotlib.pyplot as plt
import numpy as np
import math
import EnergyQ as PQ
import tkFileDialog
from graphics import *
from button import *


def main():
	xgrid=100;
	ygrid=60;
	refy=15;
	refx=90;
	refx2=12;
	width_b=12;
	heigh_b=2.5;
	win = GraphWin("Análisis de Calidad de Energía",width=750, height=400)
	win.setCoords(0,0,xgrid,ygrid)
	BG = Image(Point(12,15), 'backg.gif')
	BG.draw(win)
	line = Line(Point(xgrid-20, 0), Point(xgrid-20, ygrid))
	line.setFill("black")
	line.setWidth(2)
	line.draw(win)
	global PQ;
	osc1=PQ.fft_osc();
	
	LastFile = Button(win, Point(refx,refy-2), width_b, heigh_b, "Última Lectura")
	LastFile.label.setSize(10)
	LastFile.activate()
	SearchFile = Button(win, Point(refx,refy-6), width_b, heigh_b, "Buscar Archivo")
	SearchFile.label.setSize(10)
	SearchFile.activate()
	Salir = Button(win, Point(refx,refy-10), width_b, heigh_b, "Salir")
	Salir.label.setSize(10)
	Salir.activate()
	texto=["Amplitud: ","Frecuencia: ","TDH(%):  ","F.P: "];
	meas=[0 for i in range(16)]
	for i in range(0,4):
		mensaje=Text(Point(refx-5,refy+44-(i*10)),"Medición"+str(i+1))
		mensaje.setFace('arial')
		mensaje.setStyle('bold')
		mensaje.setSize(10)
		mensaje.setTextColor("white")
		mensaje.draw(win)
		for u in range(0,4):
			mensaje=Text(Point(refx-5,refy+42-(u*2)-(i*10)),texto[u])
			mensaje.setFace('arial')
			mensaje.setStyle('bold')
			mensaje.setSize(10)
			mensaje.setTextColor("black")
			mensaje.draw(win)
			
	
	for i in range(0,4):
		for u in range(i*4,i*4+4):
			meas[u]=Text(Point(refx+5,refy+42-((u-4*i)*2)-(i*10)),"")
			meas[u].setFace('arial')
			meas[u].setStyle('bold')
			meas[u].setSize(10)
			meas[u].setTextColor("black")
			meas[u].draw(win)
	
	pt = win.getMouse()
	while not Salir.clicked(pt):

		if LastFile.clicked(pt):
			filename='C000000';
			numeracion=open('numeracion.txt','r');
			a=numeracion.readline(1); 
			numeracion.close();
			FolderName=filename[0:len(filename)-len(a)]+a;
			file1=filename[0:len(filename)-len(a)-2]+a+'CH1';
			file2=filename[0:len(filename)-len(a)-2]+a+'CH2';
			file1='/media/javier/JAVIER/'+FolderName+'/'+file1+'.CSV'
			file2='/media/javier/JAVIER/'+FolderName+'/'+file2+'.CSV'
			file_name=[]
			file_name.append(file1);
			file_name.append(file2);
			data=osc1.file(file_name,1,4);
			for i in range(0,16):
					meas[i].setText("")
			for i in range(0,len(file_name)):
				for u in range(i*4,i*4+4):
					meas[u].setText(str(round(data[i][(u-4*i)],4)))
			Medicion = Image(Point(xgrid/2-10,ygrid/2), 'f1.png')
			Medicion.draw(win)
			print(data)
			
		if SearchFile.clicked(pt):
			file_name=[]
			file_name=tkFileDialog.askopenfilenames(initialdir='/',filetypes=[('CSV files', '*.CSV'), ('all files', '*')])
			data=osc1.file(file_name,1,4);
			for i in range(0,16):
					meas[i].setText("")
			for i in range(0,len(file_name)):
				for u in range(i*4,i*4+4):
					meas[u].setText(round(data[i][(u-4*i)],4))
			Medicion = Image(Point(xgrid/2-10,ygrid/2), 'f1.png')
			Medicion.draw(win)
			print(data)
		"""
		if NewMeas.clicked(pt):
			##
		"""
		pt = win.getMouse()
	win.close()
main()






