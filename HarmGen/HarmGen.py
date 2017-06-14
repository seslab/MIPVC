#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:HarmGen.py
#Descripción		:Biblioteca para la generación de vectores de señales con armonicas.
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

import matplotlib.pyplot as plt
import numpy as np

class HarmGen:
	def __init__(self, amplitud,freq,nHarm):  ##Función para iniciar la
		self.tau=1.0/(2*freq);
		self.t0=self.tau/2.0;
		self.a=float(amplitud);
		self.f=float(freq);
		self.y=nHarm;
		Tp=1.0/self.f;
		self.Tp=Tp;
		#Tm=0.0002;
		Tm=0.0005;
		self.Tm=Tm;
		self.w0=2*np.pi*self.f;
	
	def fourier_ak(self,k):
		self.k=k;
		self.Tp=1/self.f;
		Y=(2/self.Tp)*np.sinc(self.k*self.w0*self.tau/2)*np.cos(self.w0*k*(self.t0+(self.tau/2)));
		return Y
	
	def fourier_bk(self,k):
		self.k=k;
		self.Tp=1/self.f;
		Y=(2/self.Tp)*np.sinc(self.k*self.w0*self.tau/2)*np.sin(self.w0*k*(self.t0+(self.tau/2)));
		return Y
	
	def Harm(self):
		a0=2/self.Tp;
		t=np.arange(0,2*self.Tp,self.Tm);
		Y=a0/2;
		if len(self.y)>1:
			for k in self.y:
				a=self.fourier_ak(k);
				b=self.fourier_bk(k);
				Y=Y+a*np.cos(self.w0*k*t)+b*np.sin(self.w0*k*t);
		elif len(self.y)==1:
			for k in range(1,self.y[0]+1	):
				a=self.fourier_ak(k);
				b=self.fourier_bk(k);
				Y=Y+a*np.cos(self.w0*k*t)+b*np.sin(self.w0*k*t);
		m1=max(Y);
		m2=min(Y);
		m=m2+(m1-m2)/2;
		A=(m1-m2)/2;
		Y=(Y-m)*(self.a/A);	
		#plt.plot(t,Y);
		#plt.show(block=False)
		#print(str(len(Y)));
		#print(Y);
		return Y
