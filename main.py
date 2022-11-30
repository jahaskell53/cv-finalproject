import keras_ocr
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
from random import randint
from math import sqrt

pipleline = keras_ocr.pipeline.Pipeline()
images = [keras_ocr.tools.read('test.png'), keras_ocr.tools.read('billboard.jpg')]

prediction_groups = pipleline.recognize(images)
fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, 
                                    predictions=predictions, 
                                    ax=ax)



print(prediction_groups[1])

pillow_image = Image.open("billboard.jpg")
pillow_image = pillow_image.convert("RGBA")

for text, box in prediction_groups[1]:
    corners = np.array(box)
    tleft = corners[0]
    tright = corners[1]
    bright = corners[2]
    bleft = corners[3]
    width = int(sqrt((tright[0] - tleft[0])**2 + (tright[1] - tleft[1])**2))
    height = int(sqrt((tright[0] - bright[0])**2 + (tright[1] - bright[1])**2))
    overlay_img = Image.new('RGBA', (width, height), color='blue')
    imgDraw = ImageDraw.Draw(overlay_img)
    imgDraw.text((10, 10), text, fill=(255, 255, 0))

    test_int = randint(1, 100)

    # FOR SOME EDGE CASES, THIS APPROACH MIGHT NOT WORK
    current_vector = np.array([1,0])
    original_vector = np.array([tright[0] - tleft[0], tright[1] - tleft[1]])
    # normalizing original_vector
    original_vector = original_vector / np.linalg.norm(original_vector)
    # calculating the rotation angle # this angle is equal to the vertical angle
    theta = np.arccos(np.dot(current_vector, original_vector))
    # getting the height
    additional_height = np.sin(theta) * width
    # converting theta from radian to degree
    theta = np.degrees(theta)
    if (tleft[1] < tright[1]):
        theta = -theta
    rotated_overlay_img = overlay_img.rotate(theta, expand=True, resample=Image.BICUBIC, fillcolor=(0,0,0,0))
    pillow_image.paste(rotated_overlay_img, (int(tleft[0]), int(tleft[1] - additional_height)), mask=rotated_overlay_img)

pillow_image.show()








