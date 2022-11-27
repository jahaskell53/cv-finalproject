import keras_ocr
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
from random import randint
from math import sqrt

pipleline = keras_ocr.pipeline.Pipeline()
images = [keras_ocr.tools.read('test.png'), keras_ocr.tools.read('stop.jpeg')]

prediction_groups = pipleline.recognize(images)
fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, 
                                    predictions=predictions, 
                                    ax=ax)



print(prediction_groups[1])

pillow_image = Image.open("stop.jpeg")

for text, box in prediction_groups[1]:
    print("hello")
    corners = np.array(box)
    tleft = corners[0]
    print(tleft)
    tright = corners[1]
    bright = corners[2]
    bleft = corners[3]
    width = int(sqrt((tright[0] - tleft[0])**2 + (tright[1] - tleft[1])**2))
    height = int(sqrt((tright[0] - bright[0])**2 + (tright[1] - bright[1])**2))
    overlay_img = Image.new('RGB', (width, height), color='blue')
    imgDraw = ImageDraw.Draw(overlay_img)
    imgDraw.text((10, 10), text, fill=(255, 255, 0))

    test_int = randint(1, 100)

    pillow_image.paste(overlay_img, (int(tleft[0]), int(tleft[1])))
    #overlay_img.save('result' + str(test_int) + '.png')
    #print(box)
    #print(text)
    #print(text)
    #print(box)

#width = 512
#height = 128
#smessage = "Hello, world!"


#plt.show()
pillow_image.show()








