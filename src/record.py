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
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(audio_data))
waveFile.close()