
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

def generateTecla(freq,amp,time): #TODO: deixar a funcao mais versatil com valores padroes & colocar samples como variavel (fs)
	resp = np.add(sinal.generateSin(freq[0],amp,time,48000), sinal.generateSin(freq[1],amp,time,48000))
	return resp


def generateAm(freq,rec,fs=48000,t=2): #TODO: deixar a funcao mais versatil com valores padroes & colocar samples como variavel (fs)
	resp = np.multiply(sinal.generateSin(freq,1,t,fs)[1], rec)
	return resp

def getTopFreq(freq,maxdiff):
	resp = [freq[0]] #TODO: melhorar funcao para nao assumir o primeiro valor e sim o maior valor entre eles, TIP: colocar uma lista temporaria
	for i in freq:
		if maxdiff < np.abs(resp[-1] - i):
			resp.append(i)
	return resp



def FIRFilter(yAudioNormalizado, samplerate = 48000, dbb = 60.0, cutoff_hz = 4000.0):
	nyq_rate = samplerate/2
	width = 5.0/nyq_rate
	ripple_db = dbb #dB
	N , beta = signal.kaiserord(ripple_db, width)
	taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	yFiltrado = signal.lfilter(taps, 1.0, yAudioNormalizado)
	return yFiltrado


tecla = input("Tecla: ")
if tecla[0] == "s":
	myrecording = sd.rec(int(tecla[1] * 48000), samplerate=48000, channels=1) #TODO: fazer uma funcao para esta linha
	sd.wait()
	myrecording = np.ndarray.flatten(myrecording)

	myrecording /= np.max(myrecording)


	AM=generateAm(10000,myrecording)

	sd.play(AM,48000)
	sd.wait()

elif tecla=="fs":
	data, fs = sf.read("senda.ogg", dtype='float32')
	fs=48000
	data /= np.max(data) #normalizando o vetor do audio do arquivo
	time = len(data)/fs
	AM=generateAm(12000,data,fs,time)
	AMClean=generateAm(12000,AM,fs,time)
	final = FIRFilter(AMClean,fs,60,12000)
	print(final)


	sd.play(final,fs)
	sd.wait()

elif tecla == "r":
	fs=48000
	myrecording = sd.rec(int(tecla[1] * fs), samplerate=fs, channels=1) #TODO: fazer uma funcao para esta linha
	sd.wait()
	myrecording = np.ndarray.flatten(myrecording)

	AMClean=generateAm(12000,myrecording,fs,tecla[1])
	final = FIRFilter(AMClean,fs,60,12000)
	print(final)


	sd.play(final,48000)
	sd.wait()

		#freqsort = [x for _, x in sorted(zip(calcu,freq))] # ultimo item é o maior


		#print("CALCU: ", calcu)
		#print(getTopFreq(freqsort,2)[-5:-1])


else:
	sd.play(generateTecla(dictTecla[tecla],1,1)[1],48000)
	sd.wait()
	print(generateTecla(dictTecla[tecla],1,1)[1],48000)
	#sinal.plotFFT(generateTecla(dictTecla[tecla],1,1),48000)
	plt.plot(generateTecla(dictTecla[tecla],1,1)[0][:500],generateTecla(dictTecla[tecla],1,1)[1][:500])
	plt.draw()
	plt.pause(pltDelay)
	plt.close()
