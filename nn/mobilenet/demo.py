import cv2
import numpy as np

cap = cv2.VideoCapture("C:\\Users\SXU1\Videos\demo.mp4")
# cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("cap", frame)
    if cv2.waitKey(100) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()