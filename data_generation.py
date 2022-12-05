import zipfile
import datetime
import string
import math
import os
import shutil

import tqdm
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn.model_selection
import cv2
import keras_ocr
import random as rand
import glob 

from PIL import Image
from PIL import ImageFont, ImageDraw

data_dir = '.'
alphabet = string.digits + string.ascii_letters + '!?. '
print(alphabet)
recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
fonts = keras_ocr.data_generation.get_fonts(
    alphabet=alphabet,
    cache_dir=data_dir
)


backgrounds = keras_ocr.data_generation.get_backgrounds(cache_dir=data_dir)

text_generator = keras_ocr.data_generation.get_text_generator(alphabet=alphabet)
print('The first generated text is:', next(text_generator))
font_list = glob.glob('**/**/*.ttf', recursive=True)

# TODO: insert LOCAL ABSOLUTE PATH below
save_directory = "/Users/os/Documents/CS-Classes/cs1430/cv-finalproject/data_generated"
# TODO: COMMENT THIS LINE BELOW IF THIS IS YOUR FIRST RUN (no directory created yet)
shutil.rmtree(save_directory) # NOTICE: if your directory is empty and you want to delete it, use os.remove(save_directory)
os.mkdir(save_directory)  

counter = 0
for image_path in backgrounds: 

    image = cv2.imread(image_path)
    # plt.imshow(image)

    # offset = font_size
    # top_right_bound = (x_location + offset, y_location)
    # bottom_left_bound = (x_location, y_location+offset)
    # bottom_right_bound = (x_location + offset, y_location+offset)
    # # draw = ImageDraw.Draw(image)
    img = Image.open(image_path)

    I1 = ImageDraw.Draw(img)

    random_int = rand.randint(5,10)
    for i in range(0, random_int):
        random_character = rand.randint(0,len(alphabet) - 1)
        random_character = alphabet[random_character]

        red_value = rand.randrange(0,255)
        green_value = rand.randrange(0,255)
        blue_value = rand.randrange(0,255)

        y_location = rand.randrange(len(image))
        x_location = rand.randrange(len(image[0]))

        top_left_bound = (x_location, y_location)


        i = rand.randrange(len(font_list))

        random_font = font_list[i]
        print(random_font)

        font_size = rand.randint(20,100)
        rand_font = ImageFont.truetype(random_font, font_size)
        try:
            I1.text((x_location, y_location), random_character, fill=(red_value, green_value, blue_value), font = rand_font)
        except:
            continue
        # the below code excerpt is taken from here: https://github.com/python-pillow/Pillow/issues/3921 
        right, bottom = rand_font.getsize(random_character)
        width, height = rand_font.getmask(random_character).size
        right += x_location
        bottom += y_location
        top = bottom - height
        left = right - width
        I1.rectangle((left, top, right, bottom), None, "#f00")
    # img.show()
    # I1.rectangle(img.getbbox())
    
    filename = image_path.split("/")[-1]
    image = img.save(f"{save_directory}/" + filename + ".png")
    break