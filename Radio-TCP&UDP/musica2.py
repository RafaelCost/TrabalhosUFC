import pyaudio
import wave
import time


while True:
    chunk = 2048
    wf = wave.open('radio2.wav', 'rb')
    p = pyaudio.PyAudio()

    stream = p.open( 
        format = 8,
        channels = 2,
        rate = 44100,
        output = True)
    data = wf.readframes(chunk)
    print(p.get_format_from_width(wf.getsampwidth()))
    print(wf.getnchannels())
    print(wf.getframerate())

    while data != b'':
        ini = time.time()
        stream.write(data)
        fim = time.time()
        var = fim - ini
        
        print(var)
        data = wf.readframes(chunk)



    stream.close()
    p.terminate()