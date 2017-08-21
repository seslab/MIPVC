#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:serialKepco_tmsv3.py
#Descripción		:Biblioteca para el control de las funciones de las fuentes marca Kepco del SESLab.
#Autor          	:Javier Campos Rojas
#Fecha            	:marzo-2017
#Versión         	:3
#Notas          	:
#==============================================================================

import serial
import numpy as np
import time
from HarmGen import *
import time

class Source:
	def __init__(self, name, port):
		k=serial.Serial()						
		k.baudrate=9600;						
		k.bytesize=serial.EIGHTBITS;			
		k.parity=serial.PARITY_NONE;			
		k.stopbits=serial.STOPBITS_ONE;			
		k.timeout=0.5;							
		k.xonxoff=True;							
		k.rtscts=False;							
		k.write_timeout=0.5;				
		k.dsrdtr=False;							
		k.inter_byte_timeout=None;				
		k.port=port;							
		self.port=port;							
		self.k=k;			
		self.name=name;							
		#k.open();
		
	def connectport(self):						
		try: 									
			self.k.open()						
			return "Conectado en puerto: " + "\n" + self.k.port	
		except IOError, e:					
			return ("Error: " + "\n" +  str(e)[0:len(str(e))/2] + "\n" + str(e)[len(str(e))/2:len(str(e))]) 
			#exit()
		
		if self.k.isOpen():						
			try:									
				self.k.write('*idn?\n');
				return self.k.readline();			 
			except IOError, e1:				
				return ("error de comunicacion: " + "\n" +  str(e)[0:len(str(e1))/2] + "\n" + str(e1)[len(str(e1))/2:len(str(e1))])
		else:
			try:									
				ser.inWaiting()						
				return "Conectado en puerto: " + "\n" + self.k.port				 
			except IOError, e1:
				return ("No se pudo abrir puerto serial")
				
				
	def WriteSquare(self,Volt,f,n,C,ofs):
		if f > 2000:
			f=2000;
		self.V=Volt;
		self.C=C;
		self.f=f;
		self.n=n;
		self.ofs=ofs;
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:VOLT ');	
		funct=[str(self.V),str(-self.V)];
		self.voltList=funct;
		self.k.write('LIST:VOLT ');
		self.k.write(self.voltList[0]);
		self.k.write(',');
		self.k.write(self.voltList[0]);
		self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(1.0/(2*self.f)));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');		

	def WriteSaw(self,Volt,f,n,C,ofs):
		self.V=Volt;
		self.C=C;
		self.f=f
		self.n=n
		self.ofs=ofs;
		#self.k.write('*RST\n');			
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:VOLT ');	
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts);
		m=round(m/2)*2;	
		funct=self.V*np.arange(0,1,1/(m/2))+self.ofs;
		funct=np.round(funct)
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		self.voltList=funct;
		step=10;				
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]			
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):					
			self.k.write('LIST:VOLT ');			#Se escribe listas de tensiones y se separan en sublistas
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);	#
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');
		print([ts,1.0/(ts*len(funct))]);

	def WriteTrian(self,Volt,f,n,C,ofs):
		self.V=Volt;
		self.C=C;
		self.f=f
		self.n=n
		self.ofs=ofs;
		#self.k.write('*RST\n');			
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:VOLT ');	
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts);
		m=round(m/2)*2;	
		funct1=self.V*np.arange(0,1,1/(m/2))+self.ofs;
		funct2=self.V*np.arange(1,0,-1/(m/2))
		funct=np.concatenate([funct1,funct2])
		funct=np.round(funct)
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		self.voltList=funct;
		step=10;				
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]			
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):					
			self.k.write('LIST:VOLT ');			#Se escribe listas de tensiones y se separan en sublistas
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);	#
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');
		print([ts,1.0/(ts*len(funct))]);
################################ MODO CORRIENTE ###################################
	def WriteSquareC(self,Volt,f,n,C,ofs):
		if f > 2000:
			f=2000;
		self.V=Volt;
		self.C=C;
		self.f=f;
		self.n=n;
		self.ofs=ofs;
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:CURR ');	
		funct=[str(self.V),str(-self.V)];
		self.voltList=funct;
		self.k.write('LIST:CURR ');
		self.k.write(self.voltList[0]);
		self.k.write(',');
		self.k.write(self.voltList[0]);
		self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(1.0/(2*self.f)));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('CURR:MODE LIST\n');		

	def WriteSawC(self,Volt,f,n,C,ofs):
		self.V=Volt;
		self.C=C;
		self.f=f
		self.n=n
		self.ofs=ofs;
		#self.k.write('*RST\n');			
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:CURR ');	
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts);
		m=round(m/2)*2;	
		funct=self.V*np.arange(0,1,1/(m/2))+self.ofs;
		funct=np.round(funct)
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		self.voltList=funct;
		step=10;				
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]			
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):					
			self.k.write('LIST:CURR ');			#Se escribe listas de tensiones y se separan en sublistas
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);	#
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:CURR?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('CURR:MODE LIST\n');
		print([ts,1.0/(ts*len(funct))]);

	def WriteTrianC(self,Volt,f,n,C,ofs):
		self.V=Volt;
		self.C=C;
		self.f=f
		self.n=n
		self.ofs=ofs;
		#self.k.write('*RST\n');			
		self.k.write('LIST:CLE\n');				
		self.k.write('LIST:CURR ');	
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts);
		m=round(m/2)*2;	
		funct1=self.V*np.arange(0,1,1/(m/2))+self.ofs;
		funct2=self.V*np.arange(1,0,-1/(m/2))
		funct=np.concatenate([funct1,funct2])
		funct=np.round(funct)
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		self.voltList=funct;
		step=10;				
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]			
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):					
			self.k.write('LIST:CURR ');			#Se escribe listas de tensiones y se separan en sublistas
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);	#
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:CURR?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('CURR:MODE LIST\n');
		print([ts,1.0/(ts*len(funct))]);
	######################################################3

	def WriteVoltSine2(self, Volt,f,n,C):
		self.V=Volt;
		self.f=f;
		self.n=n;
		self.C=C;
		self.k.flushInput();
		self.k.write('LIST:CLEAR\n');
		self.k.write('OUTP OFF\n');
		self.k.write('*RST\n');
		self.k.write('LIST:VOLT:APPLY SINE,');
		self.k.write(str(float(self.f)));
		self.k.write(',')
		self.k.write(str(float(self.n)));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(int(self.n)));
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('OUTP ON\n');
		self.k.write('VOLT:MODE LIST\n');

################## MODO CORRIENTE
	def WriteVoltSineC(self, Volt,f,n,C,ofs):
		self.k.flushInput();
		self.k.write('*OUTP OFF\n');
		self.k.write('*RST\n');
		self.V=Volt;
		self.ofs=ofs;
		self.f=f
		self.n=n
		self.C=C
		#self.tsm=tm
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		self.tsm=tsm;
		T=1.0/self.f
		#ts=self.tsm;
		m=float(int(T/self.tsm));
		ts=round(T/m,9);
		#t=np.arange(0,T,ts);
		t=np.arange(0,m*ts,ts);
		funct=self.V*np.sin(2*np.pi*self.f*t)+self.ofs
		"""		
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		"""
		voltList=np.round(funct,3)
		self.voltList=voltList;
		#step=20;
		step=10;
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]
		voltList2=self.voltList[m:len(self.voltList)]
		self.k.write('FUNC:MODE CURR\n');
		self.k.write('LIST:CLEAR\n');
		#self.stop();
		for j in range(0,step):
			self.k.write('LIST:CURR ');
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR:POIN \n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.flushInput();
		self.k.write('LIST:DWEL?\n');
		print(self.k.readline());
		self.k.write('LIST:COUN ');
		self.k.write(str(int(self.n)));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('VOLT');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('CURR:MODE LIST\n');
		self.k.flushInput()
		#plt.plot(t,funct)
		#plt.show(block=False);
		print([ts,1.0/(ts*len(funct)),Volt]);

	def WriteHarmC(self, Volt,f,n,C,y,ofs):
		self.V=Volt;
		self.f=f
		self.n=n
		self.C=C
		self.ofs=ofs
		self.y=y #puede ser lista o un numero entero
		self.k.write('*RST\n');
		self.k.write('*CLS\n');
		self.k.write('LIST:CLE\n');
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts)
		Harm1=HarmGen(self.V,self.f,self.y);
		funct=Harm1.Harm()+self.ofs
		voltList=np.round(funct,3)
		self.voltList=voltList;
		step=10;
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):
			self.k.write('LIST:CURR ');
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:CURR:POIN \n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('VOLT');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('CURR:MODE LIST\n');
		self.k.write('*OPC\n');
		print([ts,1.0/(ts*len(funct))],self.y);
##########################33


	def WriteVoltSine(self, Volt,f,n,C,ofs):
		self.k.flushInput();
		self.k.write('*OUTP OFF\n');
		self.k.write('*RST\n');
		self.V=Volt;
		self.ofs=ofs;
		self.f=f
		self.n=n
		self.C=C
		#self.tsm=tm
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		self.tsm=tsm;
		T=1.0/self.f
		#ts=self.tsm;
		m=float(int(T/self.tsm));
		ts=round(T/m,9);
		#t=np.arange(0,T,ts);
		t=np.arange(0,m*ts,ts);
		funct=self.V*np.sin(2*np.pi*self.f*t)+self.ofs
		"""		
		if len(t) < len(funct):
			m=len(t);
			funct=funct[0:m]
			t=t[0:m]
		elif len(funct) < len(t):
			m=len(funct);
			funct=funct[0:m]
			t=t[0:m]
		"""
		voltList=np.round(funct,3)
		self.voltList=voltList;
		#step=20;
		step=10;
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]
		voltList2=self.voltList[m:len(self.voltList)]
		self.k.write('FUNC:MODE VOLT\n');
		self.k.write('LIST:CLEAR\n');
		#self.stop();
		for j in range(0,step):
			self.k.write('LIST:VOLT ');
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT:POIN \n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.flushInput();
		self.k.write('LIST:DWEL?\n');
		print(self.k.readline());
		self.k.write('LIST:COUN ');
		self.k.write(str(int(self.n)));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');
		self.k.flushInput()
		#plt.plot(t,funct)
		#plt.show(block=False);
		print([ts,1.0/(ts*len(funct)),Volt]);

	def WriteHarm(self, Volt,f,n,C,y,ofs):
		self.V=Volt;
		self.f=f
		self.n=n
		self.C=C
		self.ofs=ofs
		self.y=y #puede ser lista o un numero entero
		self.k.write('*RST\n');
		self.k.write('*CLS\n');
		self.k.write('LIST:CLE\n');
		#tsm=0.0002;		#Tiempo de muestreo minimo
		tsm=0.0005
		T=1.0/self.f
		m=float(int(T/tsm));
		ts=round(T/m,6);
		t=np.arange(0,T,ts)
		Harm1=HarmGen(self.V,self.f,self.y);
		funct=Harm1.Harm()+self.ofs
		voltList=np.round(funct,3)
		self.voltList=voltList;
		step=10;
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):
			self.k.write('LIST:VOLT ');
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT:POIN \n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(ts));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		#self.k.write('LIST:VOLT?\n');
		#self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');
		self.k.write('*OPC\n');
		print([ts,1.0/(ts*len(funct))],self.y);

	def WriteVolt(self,voltValue,C):
		self.voltValue=voltValue;
		self.C=C
		self.k.write('*RST\n');
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.voltValue));
		self.k.write('\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		#self.k.write('MEAS:VOLT?');
		#self.k.write('\n');
		
	def WriteCurr(self,voltValue,C):
		self.voltValue=voltValue;
		self.C=C
		self.k.write('*RST\n');
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.voltValue));
		self.k.write('\n');
		self.k.write('CURR');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('FUNC:MODE CURR\n');
		self.k.write('FUNC:MODE?\n');
		state = self.k.readline()
		return state;

	def identify(self):
		self.k.flushInput()
		self.k.write('*idn?\n');
		name = self.k.readline()
		return name;
	
	def stop(self):
		self.k.write('LIST:CLE\n');
		self.k.write('*RST\n');
		self.k.write('*OUTP OFF\n');
		self.k.flushInput()

	def measV(self):
		self.k.flushInput()
		self.k.write('MEAS:VOLT?\n')
		volt = self.k.readline()
		return volt;
		
	def readM(self):
		volt = self.k.readline()
		return volt;
		
	def measC(self):
		self.k.flushInput()
		self.k.write('MEAS:CURR?\n')
		curr = self.k.readline()
		return curr;
		
	def calPlusFine(self,val):
		self.k.write('CAL:DATA ');
		self.k.write(str(val));
		self.k.write('\n');
		
	def calMinusFine(self,val):
		self.k.write('CAL:DATA ');
		self.k.write('-');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calPlusCoarse(self,val):
		self.k.write('CAL:DPOT ');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calMinusCoarse(self,val):
		self.k.write('CAL:DPOT ');
		self.k.write('-');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calStart(self,password):
		self.k.write('*RST\n');
		self.k.write('SYST:PASS:CEN ');
		self.k.write(str(password));	
		self.k.write('\n');
		self.k.write('CAL:STAT 1\n');
		
	def calZero(self):
		self.k.write('CAL:VOLT ZERO\n');
		
	def calMax(self):
		self.k.write('CAL:VOLT MAX\n');
		
	def calMin(self):
		self.k.write('CAL:VOLT MIN\n');
		
	def calVPRmax(self):
		self.k.write('CAL:VPR MAX\n');
		
	def calVPRmin(self):
		self.k.write('CAL:VPR MIN\n');
	
	def calZeroC(self):
		self.k.write('CAL:CURR ZERO\n');
		
	def calMaxC(self):
		self.k.write('CAL:CURR MAX\n');
		
	def calMinC(self):
		self.k.write('CAL:CURR MIN\n');
		
	def calCmax(self):
		self.k.write('CAL:LCURR MAX\n');
		
	def calCmin(self):
		self.k.write('CAL:LCURR MIN\n');
		
	def calSave(self):
		self.k.write('CAL:DATA SAVE\n');
		self.k.write('CAL:STAT 0\n');
		self.k.write('CAL:STAT?\n');
		status = self.k.readline()
		return status;

