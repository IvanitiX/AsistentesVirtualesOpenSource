#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import json

model = Model(model_path='../model')

# Large vocabulary free form recognition
rec = KaldiRecognizer(model, 16000)

wf = open(sys.argv[1], "rb")
wf.read(44) # skip header

while True:
    data = wf.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        print('Partial')
        print (res['text'])

res = json.loads(rec.FinalResult())
print('Total')
print (res['text'])