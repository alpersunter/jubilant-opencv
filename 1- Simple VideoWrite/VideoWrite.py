import cv2
import numpy
vw = cv2.VideoWriter()
print(type(vw))

elon = cv2.imread("elon-musk-grimace.jpg")
h, w, d = elon.shape
# shape returns (row, column, ...)
# Therefore, for shape = (100, 50), the image has height 100 and width 50



# for fun
reis = cv2.imread("reis.jpg")
rh, rw, _ = reis.shape
# zoom to make it as tall as elon, then crop right and left sides
height_ratio = h / rh
new_reis_w, new_reis_h = int(rw*height_ratio), h
reis = cv2.resize(reis,(new_reis_w, new_reis_h))
print(reis.shape)

center_reis = new_reis_w / 2
left_bound = int(center_reis - w/2)
right_bound = int(center_reis + w/2)

new_reis = reis[:, left_bound:right_bound]

print(new_reis.shape)



fourcc = cv2.VideoWriter.fourcc(*'MJPG')
# HOWEVER, frameSize of VideoWriter requires (w,h)
# contrary to (h,w) standart of numpy and opencv::Mat
vw.open("./wowowo.avi", fourcc, 5.0, (w, h))
if not vw.isOpened():
    print("File couldn't be opened.")
    exit()

print(elon.shape)

if not (elon.shape == new_reis.shape):
    print("Elon and reis have different sizes.")
    exit()

# two seconds of elon, two seconds of erdogan
for k in range(10):
    vw.write(elon)
for k in range(10):
    vw.write(new_reis)

vw.release()
