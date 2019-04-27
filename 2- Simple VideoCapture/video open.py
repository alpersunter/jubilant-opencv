import cv2
import numpy
vc = cv2.VideoCapture()

vc.open("mmbb.mp4")
fps = vc.get(cv2.CAP_PROP_FPS)
print(fps)
fcount = vc.get(cv2.CAP_PROP_FRAME_COUNT)
print(fcount/fps)

return_value, frame = vc.read()
lut = int(1000.0/(fps))
while(return_value):

    cv2.imshow("Me Me Big Boy", frame)
    return_value, frame = vc.read()
    cv2.waitKey(lut)
cv2.waitKey()
vc.release()

