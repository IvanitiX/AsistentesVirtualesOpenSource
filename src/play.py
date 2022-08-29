import wave
import pyaudio

pyaudio_play = pyaudio.PyAudio()
archivo = wave.open('file.wav','rb')

stream = pyaudio_play.open(
    format = pyaudio_play.get_format_from_width(archivo.getsampwidth()),
    channels = archivo.getnchannels(),
    rate = archivo.getframerate(),
    output = True
)

datos = archivo.readframes(1024)

while len(datos) > 0:
        # writing to the stream is what *actually* plays the sound.
    stream.write(datos)
    datos = archivo.readframes(1024)

pyaudio_play.close(stream)
print("Ha acabado la reproducción")