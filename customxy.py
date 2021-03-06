import os
import cv2
# import matplotlib.pyplot as plt
from skimage import io, color, transform
import numpy as np


def prepare_x_and_y(image_path, img_dim=(256,256)):
    """Takes in image_path (path to the RGB image),
    adjust the image dimensions converts the image to LAB format
    and returns dict with three keys: X (LAB L), Y (LAB ab), and resized RGB.
    """
    try:
        rgb = cv2.imread(image_path)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, img_dim)
        
    except:
        print("[WARNING] Unable to process {} as image.".format(image_path))
        return {}
    
    lab = color.rgb2lab(rgb).astype(np.float32)
    L = lab[:,:,0] = 2 * lab[:,:,0]/100 - 1 # X
    ab = lab[:,:,1:] = lab[:, :, 1:] / 127 # Y
    
    return {"X": L, "Y" : ab, "RGB" : rgb}
    
def resize_image(image_path, img_dim=(256,256)):
    """Resizes image and returns it in a dictionary"""
    try:
        rgb = cv2.imread(image_path)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, img_dim)
        
    except:
        print("[WARNING] Unable to process {} as image.".format(image_path))
        return {}
        
    return {"RGB" : rgb}
    
    
### PUT CUSTOM PROCESSING FUNCTIONS HERE

# Look at the above examples for guidance.
# Input params must be path to image, and image_dims
# Output of the function must be in a python dictionary format.

###