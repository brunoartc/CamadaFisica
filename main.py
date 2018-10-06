
from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
#import wave
import time
import pickle
#import peakutils

sinal = signalMeu()

def generateTecla(freq,amp,time):
	resp = np.add(sinal.generateSin(freq[0],amp,time,48000), sinal.generateSin(freq[1],amp,time,48000))
	return resp[1]

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

tecla = input("Tecla: ")
if tecla == "s":
	sequencia = input("sequencia?(634554322465433456422)")
	for i in "18540525,18540525,28540525,28540525,48540525,48540525,18540525,18540525":
		if i == "," or i == " ":
			time.sleep(0.25)
		else:
			myrecording = sd.play(generateTecla(dictTecla[i],1,0.25),48000)
			sd.wait()
			print(myrecording)
			
elif tecla == "r":
	while True:
		myrecording = sd.rec(int(1 * 48000), samplerate=48000, channels=2)
		sd.wait()
		print(sinal.calcFFT(myrecording[0],48000),np.shape(myrecording))
		sinal.plotFFT(myrecording[0],48000)

else:
	sd.play(generateTecla(dictTecla[tecla],1,0.25),48000)
	sd.wait()

