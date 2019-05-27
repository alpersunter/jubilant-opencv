import numpy as np
import wave
import struct
import math


f = open("demofile.txt", "r")
sesVektörü = f.read().split()
sesVektörü = [ float(x) for x in sesVektörü]
sesVektörü = np.array(sesVektörü)

# SESE DÖNÜŞTÜRÜLÜYOR
print("Wav olarak kaydediliyor...")
sampleRate = 21649.0  # hertz
ses_adı = f.name + "-.wav"

wavef = wave.open(ses_adı, 'w')
wavef.setnchannels(1)  # mono
wavef.setsampwidth(2)
wavef.setframerate(sampleRate)


sesVektörü = sesVektörü - np.mean(sesVektörü)
sesVektörü = sesVektörü / np.absolute(sesVektörü).max()



for i in range(sesVektörü.size):
    value = int(sesVektörü
                [i]*32767.0)
    data = struct.pack('<h', value)
    wavef.writeframesraw(data)

wavef.close()
print(ses_adı + " kaydedildi.")
