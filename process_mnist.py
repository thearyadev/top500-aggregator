import cv2
import os

unprocessed = "assets/top_500_unprocessed_images"
mnist = "assets/top_500_mnist_images"

for carpeta in os.listdir(os.path.join(unprocessed, "train")):
    origin = os.path.join(unprocessed, "train", carpeta)
    destiny = os.path.join(mnist, "train", carpeta)

    if not os.path.exists(destiny):
        os.makedirs(destiny)

    for file_name in os.listdir(origin):

        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            
            image = cv2.imread(os.path.join(origin, file_name))
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            image_8bits = cv2.convertScaleAbs(image_gray)
            cv2.imwrite(os.path.join(destiny, file_name), image_8bits)


for carpeta in os.listdir(os.path.join(unprocessed, "test")):
    origin = os.path.join(unprocessed, "test", carpeta)

    destiny = os.path.join(mnist, "test", carpeta)
    if not os.path.exists(destiny):
        os.makedirs(destiny)

    for file_name in os.listdir(origin):
        
        if file_name.endswith(".jpg") or file_name.endswith(".png"):

            image = cv2.imread(os.path.join(origin, file_name))
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_8bits = cv2.convertScaleAbs(image_gray)
            cv2.imwrite(os.path.join(destiny, file_name), image_8bits)
