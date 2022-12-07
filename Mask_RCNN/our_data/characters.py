import os
import sys
import math
import random
import numpy as np
import cv2

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import utils

import pandas as pd
from PIL import Image

chars_to_id = {}

class CharactersConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "characters"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 52  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    #IMAGE_MIN_DIM = 64
    #IMAGE_MAX_DIM = 1024

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 32

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 100

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 5

class CharactersDataset(utils.Dataset):

    def load_characters(self, dataset_dir, subset):

        # We need to loop through every single capital and lowercase character.
        for i in range(65, 91):
            char_id = i - 65
            chars_to_id[chr(i)] = char_id
            self.add_class("characters", char_id, chr(i))
        for i in range(97, 123):
            char_id = i - 97 + 26
            chars_to_id[chr(i)] = char_id
            self.add_class("characters", char_id, chr(i))

        # Subset has to be either "test" or "train"
        dataset_dir = os.path.join(dataset_dir, subset)

        df = pd.read_csv("text_box_data.csv")
        filenames = df.filename.unique().tolist()

        for fn in filenames:
            mask = df["filename"] == fn
            rows = df[mask]
            
            chars = []
            for row in rows:
                coords = (row["topleftx"], row["toplefty"], row["bottomrightx"], row["bottomrighty"])
                chars.append((row["character"], coords))

            path = os.path.join("our_data", "chars_dataset", "train", fn)

            # While Anh adds width and height
            img = Image.open(path)
            width = img.width
            height = img.height
            
            self.add_image(source="characters", image_id=fn, path=path, width=width, height=height, chars=chars)
            
    def load_mask(self, image_id):
        df = pd.read_csv("text_box_data.csv")
        filenames = df.filename.unique().tolist()

        fp = os.path.join("our_data", "chars_dataset", "train", image_id)
        mask = df["filename"] == image_id
        rows = df[mask]

        all_masks = []
        class_ids = np.zeros(len(rows))

        for row in rows:
            char = row["character"]
            mask_array = np.zeros((row["width"], row["height"]))
            
            tly = row["toplefty"]
            bry = row["bottomrighty"]
            tlx = row["topleftx"]
            brx = row["bottomrightx"] 

            mask_array[tly:bry, tlx:brx] = 1
            all_masks.append(mask_array)

            char_id = chars_to_id[char]
            class_ids[char_id] = 1

        return np.array(all_masks).astype(np.bool), class_ids

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        if info["source"] == "characters":
            return info["path"]