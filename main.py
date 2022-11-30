import keras_ocr
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
from random import randint
from math import sqrt
import math

pipleline = keras_ocr.pipeline.Pipeline()
images = [keras_ocr.tools.read('test.png'), keras_ocr.tools.read('billboard.jpg')]

prediction_groups = pipleline.recognize(images)
fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, 
                                    predictions=predictions, 
                                    ax=ax)

pillow_image = Image.open("billboard.jpg")
pillow_image = pillow_image.convert("RGBA")

textboxDict = {}
for text, box in prediction_groups[1]:
    text_tleft = (box[0][0], box[0][1])
    text_tright = (box[1][0], box[1][1])
    text_bright = (box[2][0], box[2][1])
    text_bleft = (box[3][0], box[3][1]) # to calc height
    key_tuple = (text, text_tleft, text_tright, text_bright, text_bleft)
    textboxDict[key_tuple] = 1
print("textboxDict", textboxDict)
# loop_condition = True
word_size = len(textboxDict.keys())
current_word_index = 0
while current_word_index < word_size:
    textboxes = list(textboxDict.keys())
    current_textbox = textboxes[current_word_index]
    minDistance = math.inf
    closestTextbox = textboxes[0]
    closestTextboxIndex = 0
    for index, textbox in enumerate(textboxes):
        # if it's current word index, then skip
        if (index == current_word_index):
            continue
        # if it's not the current word, we process
        current_tright = current_textbox[2]
        index_tleft = textbox[1]
        # we find the closest text box TO THE RIGHT
        distance = sqrt((current_tright[0] - index_tleft[0])**2 + (current_tright[1] - index_tleft[1])**2)
        if (distance < minDistance):
            minDistance = distance
            closestTextbox = textbox
            closestTextboxIndex = index
    
    # after we have gotten the min distance:
    current_bright = current_textbox[3]
    current_tright = current_textbox[2]
    height = sqrt((current_bright[0] - current_tright[0])**2 + (current_bright[1] - current_tright[1])**2)
    em = height * 1.5
    closest_bleft = closestTextbox[4]
    closest_tleft = closestTextbox[1]
    closest_height = sqrt((closest_bleft[0] - closest_tleft[0])**2 + (closest_bleft[1] - closest_tleft[1])**2)
    if (minDistance < 0.75 * em and closest_height > height * 0.5 and closest_height < height * 1.5):
        # we connect this textbox with the closest textbox (to the right)
        closest_textbox_tright = closestTextbox[2]
        closest_textbox_bright = closestTextbox[3]
        current_bleft = current_textbox[4]
        current_tleft = current_textbox[1]
        connected_text = current_textbox[0] + " " + closestTextbox[0]
        connected_textbox = (connected_text, current_tleft, closest_textbox_tright, closest_textbox_bright, current_bleft)

        # we pop out current textbox:
        textboxDict.pop(current_textbox)
        # decrease current_index & word_size:
        current_word_index -= 1
        word_size -= 1

        # we pop out closest textbox:
        textboxDict.pop(closestTextbox)
        # decrease current_index & word_size, ACCORDINGLY:
        if (current_word_index > closestTextboxIndex):
            current_word_index -= 1
        word_size -= 1

        # we add newest connected textbox:
        textboxDict[connected_textbox] = 1
        word_size += 1

    current_word_index += 1
print("new textboxDict", textboxDict)

concatenated_words = list(textboxDict.keys())
for text, text_tleft, text_tright, text_bright, text_bleft in concatenated_words:
    # corners = np.array(box)
    tleft = text_tleft
    tright = text_tright
    bright = text_bright
    bleft = text_bleft
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