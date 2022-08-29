from espeakng import Speaker
from vosk import Model, KaldiRecognizer
import json
import requests
from array import array
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
THRESHOLD = 2000
WORDS_PER_MINUTE = 140
PITCH = 120
TTS_VOICE = 'es'


def tts(texto):
    esng = Speaker()

    esng.wpm = WORDS_PER_MINUTE
    esng.pitch = PITCH
    esng.voice = TTS_VOICE
    esng.say(texto)

def sr(audio):
    model = Model(model_path='../model')
    rec = KaldiRecognizer(model, RATE)

    wf = open(audio, "rb")
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
    return res['text']

def record(write_file):
    audio = pyaudio.PyAudio()
    audio_data = []
    can_record = False
    finish_record = False
    silent_chunks = 0
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    

    while not finish_record:
        chunk = stream.read(CHUNK)
        data_array = array('h', chunk)
        print(max(data_array))
        if not can_record:
            can_record = max(data_array) >= THRESHOLD
        else:
            audio_data.append(chunk)
            if (max(data_array) <= THRESHOLD):
                silent_chunks += 1
                print("Silencio {0}".format(silent_chunks))
            else:
                silent_chunks = 0
            if silent_chunks >= 10:
                finish_record = True
        


    print ("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(write_file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(audio_data))
    waveFile.close()

def chatbot_connect(message):
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": 'test', "message": message})
    bot_message = ''

    if r is not None:
        print(r.json())
        for request in r.json():
            try:
                bot_message += request['text']
            except KeyError:
                print(request)
        print(bot_message)

    return bot_message


if __name__ == '__main__':
    while True:
        record(WAVE_OUTPUT_FILENAME)
        transcripcion = sr(WAVE_OUTPUT_FILENAME)
        respuesta = chatbot_connect(transcripcion)
        print(respuesta)
        tts(respuesta)
