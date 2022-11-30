

import argparse
import keras_ocr
import matplotlib.pyplot as plt
from googletrans import Translator
from googletrans import constants


def parse_args():
    """ Perform command-line argument parsing. """

    parser = argparse.ArgumentParser(
        description="Lets have some!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument( '--img_path',
        required=False,
        default = "french_image.jpeg",
        help='''the source image you would to detect test and translate''')
    parser.add_argument( '--src_lang',
        required=False,
        choices= constants.LANGUAGES.values(),
        default = "english",
        help='''the source language you are trying to translate''')
    parser.add_argument(
        '--dest_lang',
        required = False,
        default='french',
        choices= constants.LANGUAGES.values(),
        help='the language you are trying to translate the original piece to')
    parser.add_argument(
        '--vis',
        required = False,
        default = "False",
        choices = ["True, False"],
        help='whether or not you would like to visualize the text recognition'
    )

    return parser.parse_args()
    

def recognize_text():
    pipeline = keras_ocr.pipeline.Pipeline()


    images = [
    keras_ocr.tools.read(img) for img in [ARGS.img_path]
    ]

    # plot the text predictions
    prediction_groups = pipeline.recognize(images)
    fig, axs = plt.subplots(nrows=len(images), figsize=(10, 8))

    keras_ocr.tools.drawAnnotations(image=images[0], 
                                        predictions=prediction_groups[0], 
                                        ax=axs)
    if(ARGS.vis == "True"):
        plt.show()
    return prediction_groups

def translate_text(prediction_groups, src_lang, dest_lang):
    predicted_image = prediction_groups[0]
    translate_client = Translator()
    all_text = [text[0] for text in predicted_image]

    
    print("Original text in {}: {}".format(constants.LANGUAGES[src_lang], all_text))
    translation_list = translate_client.translate(all_text, src = src_lang, dest = dest_lang)
    translated_text = [text.text for text in translation_list]

    print("Translated text in {}: {}".format(constants.LANGUAGES[dest_lang], translated_text))

    return translated_text

def main():

    prediction_groups = recognize_text()

    values_list = list(constants.LANGUAGES.values())
    key_list = list(constants.LANGUAGES.keys())

    src_lang = values_list.index(ARGS.src_lang)
    dest_lang = values_list.index(ARGS.dest_lang)

    src_lang_code = key_list[src_lang]
    dest_lang_code = key_list[dest_lang]

    translated_text = translate_text(prediction_groups, src_lang_code, dest_lang_code)


ARGS = parse_args()
main()

