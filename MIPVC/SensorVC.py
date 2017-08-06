#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:SensorVC.py
#Descripción		:Programa de captura de sensorVC.
#Autor          	:Javier Campos Rojas
#Fecha            	:Junio-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================
import time
import Adafruit_ADS1x15 as ADC
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import RPi.GPIO as GPIO
import threading

class Sensor(threading.Thread):
	def __init__(self, period):
		threading.Thread.__init__(self)
		self.time=period;
		filename='C000000';
		self.adc1 = ADC.ADS1115()
		self.numeracion=open('numeracion.txt','r');
		a=self.numeracion.readline(1); 
		self.numeracion=open('numeracion.txt','w');
		self.numeracion.write(str(int(a)+1));
		self.file1=filename[0:len(filename)-len(a)-2]+'CH1'+a;
		self.file2=filename[0:len(filename)-len(a)-2]+'CH1'+a;
		self.numeracion.close();
		self.GAIN = 16
		self.adc1.start_adc(2, gain=self.GAIN, data_rate=860)
	def run(self):
		print('Inicio')
		vout=[]
		start=time.time();
		while (time.time() - start) <= float(self.time):
			volt1 = self.adc1.get_last_result()
			vout.append(volt1)
		t=np.linspace(0,self.time,len(vout))
		vout=np.array(vout)
		Cal=460.5659
		volt1Meas=Cal*vout/32767.0
		a=max(volt1Meas)-((max(volt1Meas)-min(volt1Meas))/2.0)
		volt1Meas=volt1Meas-a
		w=savgol_filter(volt1Meas,5,1,mode='nearest')
		w=savgol_filter(w,11,1)
		a=np.zeros(len(w))
		atm=a;
		tm=t[1]-t[0]
		atm[0]=len(w);
		atm[1]=tm;		
		self.file1=self.file1+'.CSV'
		np.savetxt(self.file1,np.array([a,atm,a,t,w]).T,delimiter=',')
		#plt.style.use('ggplot')
		#plt.plot(t,w)
		#plt.show()
		self.adc1.stop_adc()
		print('Final')
