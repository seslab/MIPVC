#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:controlTektronix.py
#Descripción		:Biblioteca para control de Osciloscopio Tektronix
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

import numpy as np
import io
import base64
import usbtmc
import glob ##### para buscar los puertos USB disponibles
import datetime

class getWave:
	def connectOsc(self):
		try:
			osc=usbtmc.Instrument(1689, 870)
			self.osc=osc
			tek=osc.ask('*IDN?')
			fecha=datetime.datetime.now()
			self.fecha=fecha;
			self.filename='C000000';
			return tek
		except Exception:
			return "No existe instrumento de medición conectado"
		#return tek

	def OscWave(self):
		try:
			self.numeracion=open('numeracion.txt','r');
			a=self.numeracion.readline(1); 
			self.numeracion=open('numeracion.txt','w');
			self.numeracion.write(str(int(a)+1));
			FolderName=self.filename[0:len(self.filename)-len(a)]+a;
			file1=self.filename[0:len(self.filename)-len(a)-2]+'CH1'+a;
			file2=self.filename[0:len(self.filename)-len(a)-2]+'CH1'+a;
			self.numeracion.close();
			Folder='FILESystem:MKDir "A:'+'\\'+FolderName+'"'
			WFile1='SAV:WAVE CH1, "A:'+'\\'+FolderName+'\\'+file1+'.CSV"'
			WFile2='SAV:WAVE CH2, "A:'+'\\'+FolderName+'\\'+file2+'.CSV"'
			print(Folder)
			print(WFile1)
			print(WFile2)
			self.osc.write(Folder);
			self.osc.write(WFile1);
			self.osc.write(WFile2);
		except:
			return "No existe instrumento de medición conectado"
