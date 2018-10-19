
from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
#import wave
import time
import pickle
#import peakutils
import operator

sinal = signalMeu()

def generateTecla(freq,amp,time): #TODO: deixar a funcao mais versatil com valores padroes & colocar samples como variavel (fs)
	resp = np.add(sinal.generateSin(freq[0],amp,time,48000), sinal.generateSin(freq[1],amp,time,48000))
	return resp


def generateAm(freq,rec): #TODO: deixar a funcao mais versatil com valores padroes & colocar samples como variavel (fs)
	resp = np.multiply(sinal.generateSin(freq,1,2,48000)[1], rec)
	return resp

def getTopFreq(freq,maxdiff):
	resp = [freq[0]] #TODO: melhorar funcao para nao assumir o primeiro valor e sim o maior valor entre eles, TIP: colocar uma lista temporaria
	for i in freq:
		if maxdiff < np.abs(resp[-1] - i):
			resp.append(i)
	return resp



def FIRFilter(samplerate = 48000, dbb = 60.0, cutoff_hz = 4000.0):
	nyq_rate = samplerate/2
	width = 5.0/nyq_rate
	ripple_db = dbb #dB
	N , beta = signal.kaiserord(ripple_db, width)
	taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	yFiltrado = signal.lfilter(taps, 1.0, yAudioNormalizado)


tecla = input("Tecla: ")
if tecla == "s":
	myrecording = sd.rec(int(2 * 48000), samplerate=48000, channels=1) #TODO: fazer uma funcao para esta linha
	sd.wait()
	myrecording = np.ndarray.flatten(myrecording)

	myrecording /= np.max(myrecording)


	AM=generateAm(10000,myrecording)

	sd.play(AM,48000)
	sd.wait()


elif tecla == "r":
	myrecording = sd.rec(int(2 * 48000), samplerate=48000, channels=1) #TODO: fazer uma funcao para esta linha
	sd.wait()
	myrecording = np.ndarray.flatten(myrecording)


	AM=generateAm(10000,myrecording)

	sd.play(AM,48000)
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
