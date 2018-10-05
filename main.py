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
}

#tecla = input("Tecla: ")

for i in "32123332223333212333322321":
	sd.play(generateTecla(dictTecla[i],1,0.25),48000)
	sd.stop()

