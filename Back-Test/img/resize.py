import cv2 
import os

for i in range(1, 5):
    ls_name = f"test_{i}/"
    for img in os.listdir(ls_name):
        m = cv2.imread(f"{ls_name}{img}")
        m = cv2.resize(m, (720, 480))
        cv2.imwrite(f"{img}", m)