

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
        choices= constants.LANGUAGES,
        default = "fr",
        help='''the source language you are trying to translate''')
    parser.add_argument(
        '--dest_lang',
        required = False,
        default='kr',
        choices= constants.LANGUAGES,
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

    translation_list = translate_client.translate(all_text, src = src_lang, dest = dest_lang)
    translated_text = [text.text for text in translation_list]

    return translated_text

def main():

    prediction_groups = recognize_text()
    translated_text = translate_text(prediction_groups, ARGS.src_lang, ARGS.dest_lang)
    print(translated_text)


ARGS = parse_args()
main()

