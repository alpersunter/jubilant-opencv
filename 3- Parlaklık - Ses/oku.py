import cv2
import numpy as np

import wave, struct, math


### BURADA KULLANICIYA HANGİ PİKSELİ İSTEDİĞİNİ SORUYORUZ
# x ve y'ye normalde programın kabul etmeyeceği değerler veriyorum ki değerler uygun değil diyip kullanıcıya sorsun (satır 25 ve 27)
x, y = -1, -1

video = cv2.VideoCapture()
video.open("cips.mp4")

fps = video.get(cv2.CAP_PROP_FPS)
frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(frame_count)

ret, frame = video.read()

cv2.imshow("Piksel begenin, herhangi bir tusa basip konsola gidin", frame)
retval = cv2.waitKey()

while(not (0<x and x < width)):
    x = int(input("Uygun bir X girin:"))
while(not (0<y and y < height)):
    y = int(input("Uygun bir Y girin:"))


### BURADA TÜM ZAMANLARDA İLGİLİ PİKSELİN PARLAKLIĞINI KAYDEDİYORUZ

ready = input("Hazır??")
vector = np.empty(1,dtype=int)
ctr = 0
while(ret):
    b, g, r = frame[y, x,:]
    vector = np.append(vector, [int(b)+int(g)+int(r)])
    ret, frame = video.read()
    ctr += 1
    if(ctr % 1000 == 0):
        print(str(ctr) + " kare okundu.\tYüzde: " + str((ctr/frame_count)*100))

vector[0]=0
### OKUNDU! DOSYAYA YAZILIYOR
print("Okuma tamamlandı, dosyaya yazılıyor...")
video.release()
dosya_adı = ses_adı = "x-"+str(x)+"--y-"+str(y)+".txt"
np.savetxt(dosya_adı, vector, fmt="%d")
print(dosya_adı  + " kaydedildi.") 


### SESE DÖNÜŞTÜRÜLÜYOR
print("Wav olarak kaydediliyor...")
sampleRate = 21649.0 # hertz
frameCount = frame_count  # samples
ses_adı = "x-"+str(x)+"--y-"+str(y)+".wav"

wavef = wave.open(ses_adı,'w')
wavef.setnchannels(1) # mono
wavef.setsampwidth(2) 
wavef.setframerate(sampleRate)

vector = vector - np.mean(vector)
vector = vector / np.absolute(vector).max()

for i in range(vector.size):
    value = int(vector[i]*32767.0)
    data = struct.pack('<h', value)
    wavef.writeframesraw( data )

wavef.close()
print(ses_adı  + " kaydedildi.") 
