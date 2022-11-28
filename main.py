import keras_ocr
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageTransform, ImageFont
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

    # Determine adequate font size
    font_size = 1
    font = ImageFont.truetype("Arial.ttf", font_size)
    max_fraction = 0.90

    breakpoint = max_fraction * height
    jumpsize = 75
    while True:
        #print("hello")
        if font_size < breakpoint:
            font_size += jumpsize
            print(font_size)
        else:
            jumpsize = jumpsize // 2
            font_size -= jumpsize
        font = ImageFont.truetype("arial.ttf", font_size)
        if jumpsize <= 1:
            break
    
    imgDraw = ImageDraw.Draw(overlay_img)
    imgDraw.text((0, 0), text, fill=(255, 255, 0), font=font)

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








