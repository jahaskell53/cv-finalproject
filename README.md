# CV Finalproject
Computer Vision (CS1430) Final Project by Jakobi Haskell, Anh Duong, Ayman Benjelloun Touimi & Adam Mroueh.
Full Colab notebook here: https://colab.research.google.com/drive/1tCy18ThUYPCqvCGPS7Sx6-C2hfNiaveT?authuser=1#scrollTo=yYxtkRxM_Hdn 

# Description
The project is a mini version of Google Translate by images. 

We wrote our own scripts to generate and prepare data (generating masks) to comply to COCO format. The data is a list of thousands of images with randomly sized, colored and fonted alphabetical lowercase characters. 
Example:
![Unknown](https://github.com/jahaskell53/cv-finalproject/assets/84537455/7b1b317e-7362-4a0f-be79-263eab5ce990)
![Unknown-4](https://github.com/jahaskell53/cv-finalproject/assets/84537455/dedc1436-ff79-4b7e-9139-a0e063dcc331)

We then trained Mask-RCNN on character detection & classification:

![Unknown-2](https://github.com/jahaskell53/cv-finalproject/assets/84537455/16ea200a-6a96-4c49-9bb5-df508d8d5354)
![Unknown-3](https://github.com/jahaskell53/cv-finalproject/assets/84537455/55fd02de-c5cd-4c9b-a692-8ea43ba3a499)

Finally, we wrote our own parsing algorithm that parses the character into words, and words into string. These strings are then translated using Google Translate API, and finally overlaid on top of the original image, also using another algorithm we wrote.

<img width="688" alt="Screenshot 2023-07-07 at 11 24 02 PM" src="https://github.com/jahaskell53/cv-finalproject/assets/84537455/925e2092-f0de-492a-b5c5-79d4d62dbd0e">

# Poster
[Text Recognition, Translation, and Transformation with Mask-RCNN.pdf](https://github.com/jahaskell53/cv-finalproject/files/11988739/Text.Recognition.Translation.and.Transformation.with.Mask-RCNN.pdf)
