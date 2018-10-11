
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

def getTopFreq(freq,maxdiff):
	resp = [freq[0]] #TODO: melhorar funcao para nao assumir o primeiro valor e sim o maior valor entre eles, TIP: colocar uma lista temporaria
	for i in freq:
		if maxdiff < np.abs(resp[-1] - i):
			resp.append(i)
	return resp

dictTecla = {
	"1":[1209,697],
	"2":[1336,697],
	"3":[1477,697],
	"4":[1209,770],
	"5":[1336,770],
	"6":[1477,770],
	"7":[1209,852],
	"8":[1336,852],
	"9":[1477,852],
	"0":[1336,941],
}

DTMF = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
pltDelay = 5


tecla = input("Tecla: ")
if tecla == "s":
	sequencia = input("sequencia?(634554322465433456422)")
	for i in sequencia:
		if i == "," or i == " ":
			time.sleep(0.25)
		else:
			myrecording = sd.play(generateTecla(dictTecla[i],1,0.25),48000)
			sd.wait()
			print(myrecording)
			
elif tecla == "r":
	#plt.axis([0,25000,0,70])
	#plt.ion()
	#plt.show()
	while True:
		myrecording = sd.rec(int(1 * 48000), samplerate=48000, channels=1) #TODO: fazer uma funcao para esta linha 
		sd.wait()
		myrecording = np.ndarray.flatten(myrecording)
		freq,calcu = sinal.calcFFT(np.ndarray.flatten(myrecording),48000)
		calcu = np.abs(calcu)

		dictFreq = dict(zip(freq, calcu))
		freqsOrdenadas = sorted(dictFreq.items(), key=operator.itemgetter(1))  # tuple: ultimo item é o de maior frequencia

		freqOrd = []

		for k in reversed(freqsOrdenadas):
			freqOrd.append(k)

		freqOrd = freqOrd[0:10]

		listaTeclas = []
		
		for i in freqOrd:
			if int(round(i[0])) in DTMF:
				listaTeclas.append(int(round(i[0])))
		print(sorted(listaTeclas, reverse=True))

		for digito, freq in dictTecla.items():
			if freq == sorted(listaTeclas, reverse=True):
				print("Foi pressionada a tecla ", digito)
				print(" picos=",freqOrd)

				sinal.plotFFT(np.ndarray.flatten(myrecording),48000)
				#print(np.max(myrecording))
				plt.draw()
				plt.figure('Sinal')
				plt.plot(np.arange(0,1,1/48000)[:500],myrecording[:500])
				plt.title("Sine")
				plt.draw()
				plt.pause(pltDelay) #TODO: achar outro metodo para plotar os graficos
				#plt.show()
				plt.close()
				plt.close()

		#freqsort = [x for _, x in sorted(zip(calcu,freq))] # ultimo item é o maior


		#print("CALCU: ", calcu)
		#print(getTopFreq(freqsort,2)[-5:-1])

		

		#    !!!!!!!!!!!! OLD METHOD, DEPRECIATED !!!!!!!!!!!!!!
		#sor = np.sort(calcu) !!!!!!!!!!!!old method, depreciated
		#top100 = freq[np.where(calcu == sor[-1])] #frequencia da onda é o 0 frequencia de acontecimentos 1
		#print(top100[0],top100[-1],sor[-1],">",sor[-99])
		#print(getTopFreq(top100,2))
		#   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KEEP FOR LOG !!!!!!!

else:
	sd.play(generateTecla(dictTecla[tecla],1,1)[1],48000)
	sd.wait()
	print(generateTecla(dictTecla[tecla],1,1)[1],48000)
	#sinal.plotFFT(generateTecla(dictTecla[tecla],1,1),48000)
	plt.plot(generateTecla(dictTecla[tecla],1,1)[0][:500],generateTecla(dictTecla[tecla],1,1)[1][:500])
	plt.draw()
	plt.pause(pltDelay)
	plt.close()
