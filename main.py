import cv2
import numpy as np
from PIL import Image
import os


def mse(img1, img2):

    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    mse = err / (float(h * w))
    return mse, diff


comparisons = []

comparor = cv2.cvtColor(np.array(Image.open("comp.png").resize((45, 45))), cv2.COLOR_BGR2GRAY)

for f in os.listdir("images"):
    i = Image.open(f"images/{f}")
    i = i.resize((45, 45))
    i = np.array(i)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    sim, _ = mse(comparor, i)
    comparisons.append(
        (sim, f, i)
    )

sComparisons = sorted(comparisons, key=lambda x: x[0])
for l in sComparisons:
    print(l[0])
    cv2.imshow("hmx", l[2])
    cv2.waitKey(0)


