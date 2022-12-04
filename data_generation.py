import zipfile
import datetime
import string
import math
import os

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

assert tf.test.is_gpu_available(), 'No GPU is available.'

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
        random_character = rand.randint(0,len(alphabet))
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

    # draw.text((x_location, y_location),"Sample Text",(red_value,green_value,blue_value),font=font)
        font_size = rand.randint(20,100)
        rand_font = ImageFont.truetype(random_font, font_size)
        I1.text((x_location, y_location), random_character, fill=(red_value, green_value, blue_value), font = rand_font)
    img.show()
    


    save_directory = ""
    os.mkdir(save_directory)  
    image = img.save(f"{save_directory}/image.png")





