
from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
#import wave
import time
import pickle
#import peakutils
import operator
import soundfile as sf
import scipy.signal as signal

sinal = signalMeu()

def generateAm(freq,rec,fs=48000,t=2): #TODO: deixar a funcao mais versatil com valores padroes & colocar samples como variavel (fs)
	resp = np.multiply(sinal.generateSin(freq,1,t,fs)[1], rec)
	return resp

def FIRFilter(yAudioNormalizado, samplerate = 48000, dbb = 60.0, cutoff_hz = 4000.0):
	nyq_rate = samplerate/2
	width = 5.0/nyq_rate
	ripple_db = dbb #dB
	N , beta = signal.kaiserord(ripple_db, width)
	taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	yFiltrado = signal.lfilter(taps, 1.0, yAudioNormalizado)
	return yFiltrado

def plotGraphs(s1, s2):
	plt.subplot(2, 1, 1)
	plt.plot(np.arange(0,1,1/48000)[:500],s1[:500])
	plt.ylabel('Original')

	plt.subplot(2, 1, 2)
	plt.plot(np.arange(0,1,1/48000)[:500],s2[:500])
	plt.ylabel('Normalizado')

	plt.show()

tecla = input("Tecla: ")

if tecla[0] == "s":
	myrecording = sd.rec(int(int(tecla[1]) * 48000), samplerate=48000, channels=1) #TODO: fazer uma funcao para esta linha
	sd.wait()

	myrecording = np.ndarray.flatten(myrecording)
	sinalNormalizado = myrecording/np.max(myrecording)
	sinalFiltrado = FIRFilter(sinalNormalizado,48000,60.0,4000.0)
	AM=generateAm(12000,sinalFiltrado,48000,int(tecla[1]))

	plotGraphs(myrecording,sinalNormalizado)
	plotGraphs(sinalFiltrado,AM)

	sd.play(AM,48000)
	sd.wait()

elif tecla=="fs":
	myrecording, fs = sf.read("senda.ogg", dtype='float32')
	fs=48000

	sinalNormalizado = myrecording/np.max(myrecording) #normalizando o vetor do audio do arquivo
	time = len(sinalNormalizado)/fs
	sinalFiltrado = FIRFilter(sinalNormalizado,fs,60.0,4000.0)
	AM=generateAm(12000,sinalFiltrado,fs,time)

	plotGraphs(myrecording,sinalNormalizado)
	plotGraphs(sinalFiltrado,AM)

	print(AM)

	sd.play(AM,fs)
	sd.wait()

elif tecla[0] == "r":

	fs=48000
	myrecording = sd.rec(int(10*fs), samplerate=fs, channels=1) #TODO: fazer uma funcao para esta linha 
	sd.wait()
	myrecording = np.ndarray.flatten(myrecording)
	time = len(myrecording)/fs

	AM = generateAm(12000,myrecording,48000,time)
	final = FIRFilter(AM,fs,60.0,4000.0)

	sd.play(final,fs)
	sd.wait()

	plotGraphs(myrecording,final)
