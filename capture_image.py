import cv2
import time

capture = cv2.VideoCapture(0)

_, frame = capture.read()
cv2.imwrite(
  '/tmp/bonbon-%s.png' % time.strftime("%Y%m%d%H%M%S", time.localtime()),
  frame
)

capture.release()
cv2.destroyAllWindows()
