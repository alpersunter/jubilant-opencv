import cv2
import numpy as np

import wave
import struct
import math


# BURADA KULLANICIYA HANGİ BÖLGEYİ İSTEDİĞİNİ SORUYORUZ
boySerbest = None

print("Seçim alanının boyu serbest mi olacak?")

while(boySerbest is None):
    d = input("e/h?")
    if(d == "e" or d == "E"):
        boySerbest = True
    elif(d == "h" or d == "H"):
        boySerbest = False

# Eğer boy serbest ise program olduğu gibi çalışmalı
# değilse, o halde roi_yükseklik ve roi_genişlik hakkında
# kullanıcıya sorulmalı (satır 47'ye gidin)


video = cv2.VideoCapture()
video.open("cips.mp4")

fps = video.get(cv2.CAP_PROP_FPS)
frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(frame_count)

ret, frame = video.read()

# roi = [sol_ust_x, sol_ust_y, genislik, yukseklik]
roi = cv2.selectROI("Bolge secin, sonra Enter veya Bosluk",
                    frame, False, False)
# print(str(roi[0]) + " - " + str(roi[1]) + " - " + str(roi[2]) + " - " + str(roi[3]))

roi_tl_x = roi[0]
roi_tl_y = roi[1]
roi_genislik = roi[2]
roi_yukseklik = roi[3]

if(not boySerbest):
    # yükseklik girin
    istenen_yükseklik = int(input("Yükseklik şu kadar olsun: "))
    # genişlik girin
    istenen_genişlik = int(input("Genişlik şu kadar olsun: "))
    roi_genislik = istenen_genişlik
    roi_yukseklik = istenen_yükseklik

bolge_matrisi = frame[roi_tl_y:roi_tl_y +
                      roi_yukseklik, roi_tl_x:roi_tl_x+roi_genislik]
# Filtre sonradan değiştirilebilir !!!!!!
filtre = np.ones((roi_yukseklik, roi_genislik, 3))
filtreden_sonra = np.mean(np.multiply(filtre, bolge_matrisi))

# print(filtreden_sonra)

# BURADA TÜM ZAMANLARDA İLGİLİ PİKSELİN PARLAKLIĞINI KAYDEDİYORUZ

ready = input("Hazır??")
sesVektörü = np.empty(1, dtype=int)
ctr = 0
while(ret):
    bolge_matrisi = frame[roi_tl_y:roi_tl_y +
                          roi_yukseklik, roi_tl_x:roi_tl_x+roi_genislik]
    filtreden_sonra = np.mean(np.multiply(filtre, bolge_matrisi))
    sesVektörü = np.append(sesVektörü, filtreden_sonra)
    ret, frame = video.read()
    ctr += 1
    if(ctr % 1000 == 0):
        print(str(ctr) + " kare okundu.\tYüzde: " + str((ctr/frame_count)*100))

sesVektörü[0] = 0
# OKUNDU! DOSYAYA YAZILIYOR
print("Okuma tamamlandı, dosyaya yazılıyor...")
video.release()
# dosya adı: 2x2 (x, y).txt
dosya_adı = str(roi_genislik) + "x" + str(roi_yukseklik) + \
    " (" + str(roi_tl_x) + ", " + str(roi_tl_y) + ").txt"
np.savetxt(dosya_adı, sesVektörü, fmt="%d")
print(dosya_adı + " kaydedildi.")


# SESE DÖNÜŞTÜRÜLÜYOR
print("Wav olarak kaydediliyor...")
sampleRate = 21649.0  # hertz
frameCount = frame_count  # samples
ses_adı = str(roi_genislik) + "x" + str(roi_yukseklik) + \
    " (" + str(roi_tl_x) + ", " + str(roi_tl_y) + ").wav"

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
