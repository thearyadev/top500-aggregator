import cv2
import numpy as np

from neural_network import Model

# Label index to label name relation
top_500_mnist_labels = {
    0: 'Ana',
    1: 'Ashe',
    2: 'Baptiste',
    3: 'Bastion',
    4: 'Blank',
    5: 'Blank',
    6: 'Brigitte',
    7: 'Cassidy',
    8: 'D.Va',
    9: 'Doomfist',
    10: 'Echo',
    11: 'Genji',
    12: 'Hanzo',
    13: 'Junker Queen',
    14: 'Junkrat',
    15: 'Kiriko',
    16: 'Lucio',
    17: 'Mei',
    18: 'Mercy',
    19: 'Moira',
    20: 'Orisa',
    21: 'Pharah',
    22: 'Ramattra',
    23: 'Reaper',
    24: 'Reinhardt',
    25: 'Roadhog',
    26: 'Sigma',
    27: 'Sojourn',
    28: 'Soldier 76',
    29: 'Sombra',
    30: 'Symmetra',
    31: 'Torbjorn',
    32: 'Tracer',
    33: 'Widowmaker',
    34: 'Winston',
    35: 'Wrecking Ball',
    36: 'Zarya',
    37: 'Zenyatta',
}

# Read an image
image_data = cv2.imread('assets\hero_images\Winston.png', cv2.IMREAD_GRAYSCALE)

# Resize to the same size as Fashion MNIST images
image_data = cv2.resize(image_data, (49, 50))

# Reshape and scale pixel data
image_data = (image_data.reshape(1, -1).astype(np.float32) - 127.5) / 127.5

# Load the model
model = Model().load("neural_network/top_500_mnist.model")

# Predict on the image
confidences = model.predict(image_data)

print(confidences[0])

# Get prediction instead of confidence levels
predictions = model.output_layer_activation.predictions(confidences)

print(predictions)

# Get label name from label index
prediction = top_500_mnist_labels[predictions[0]]

print(prediction)
