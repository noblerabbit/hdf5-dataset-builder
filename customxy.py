import os
import cv2
import matplotlib.pyplot as plt
from skimage import io, color, transform
import numpy as np


def prepare_x_and_y(image_path, img_dim=(256,256)):
    """Takes in image_path (path to the RGB image) and returns the image in LAB format,
    with height and width, corresponding to the img_dim tupple
    """
    # rgb = io.imread(image_path)
    # rgb = transform.resize(rgb, img_dim)
    
    rgb = cv2.imread(image_path)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, img_dim)
    
    lab = color.rgb2lab(rgb).astype(np.float32)
    L = lab[:,:,0] = 2 * lab[:,:,0]/100 - 1
    ab = lab[:,:,1:] = lab[:, :, 1:] / 127
    
    return L, ab, rgb