
import keras_ocr
import matplotlib.pyplot as plt
from googletrans import Translator
# from google.cloud import translate_v2 as translate


pipeline = keras_ocr.pipeline.Pipeline()


images = [
    keras_ocr.tools.read(img) for img in ["/Users/ajmroueh/Desktop/fall_2022/computer_vision/cv-finalproject/billboard2.jpeg","/Users/ajmroueh/Desktop/fall_2022/computer_vision/cv-finalproject/billboard.jpg", "/Users/ajmroueh/Desktop/fall_2022/computer_vision/cv-finalproject/french_image.jpeg"]
]

# plot the text predictions
prediction_groups = pipeline.recognize(images)
fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))

for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, 
                                    predictions=predictions, 
                                    ax=ax)

# plt.show()

predicted_image = prediction_groups[2]
translate_client = Translator()
all_text = [text[0] for text in predicted_image]
print(all_text)

translation_list = translate_client.translate(all_text, src = "fr", dest = "en")

translated_text = [text.text for text in translation_list]
print(translated_text)

# for text, box in predicted_image:
#     print(translate_client.translate(text, src = "fr", dest = "en").text)
    
# translate_client = translate.Client()

# translated = translate.translate('Je suis allergique')

