import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
# import tesseract
import pytesseract

# Create a black image
img = np.zeros((512,512,3), np.uint8)
# load billboard img
img2 = cv.imread('billboard.jpg',1)
# Draw a diagonal blue line with thickness of 5 px
cv.line(img2,(0,0),(511,511),(255,0,0),5)
# find the text in the image
text = pytesseract.image_to_string(img2)
print(text)
# draw bounding box around text

# show image
cv.imshow('image',img2)
cv.waitKey(0)