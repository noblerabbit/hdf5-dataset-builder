import numpy as np
import time
import h5py
import cv2
import os
from skimage import io, color, transform
import json
import customxy
import argparse

# constrct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-x", "--x_path", required = False, default="test/", help="Path to IMAGE folder.")
ap.add_argument("-y", "--y_path", required = False, default="y_test.json", help="Path to JSON file with image info.")
ap.add_argument("-p", "--prefix", required = False, default="", help="Give new name for files, or leave blank to keep the orginal names.")
ap.add_argument("-d", "--dimensions", required = False, default=(256, 256), help = "Set image dimensions. If empty images will be in (256, 256) size")
ap.add_argument("-compress", "--compress", required=False, default=True, help = "Set to False in order to avoid (gzip) compression inside hdf5")
ap.add_argument("-sf", "--save_to_file", required=False, default="data.hdf5", help=  "Name of the output HDF5 file with images")
ap.add_argument("-img", "--image_type", required=False, default="", help = "Include only files specific filetype (ie. jpg). default is: '' - all files")
args = vars(ap.parse_args())


# Link constants to input vars
DATAFILENAME = args['save_to_file']
IMAGE_DIR_PATH = args['x_path']
IMG_DIMS = args['dimensions']
Y_FILE_PATH = args['y_path']
X_FILE_PREFIX = "X"
Y_FILE_PREFIX = "Y"
FILE_TYPE = args['image_type']
COMPRESS = args['compress']


#get array of filenames
def get_filenames(folder_path, file_type=""):
    """Returns list of filenames in the folder_path.
    Ommits hidden files in the folder. """
    
    return [file for file in os.listdir(folder_path) if not file.startswith(".") and file.endswith(file_type)]

def prepare_image(image_path, img_dims):
    """Method takes in path to the image and desired image dimensions
    and reutrns resized image in a numpy array"""
    
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, img_dims)
    return img

def get_image_info(filename, image_info_dict=None):
    """Lookup in jason file for image dict and return description
    for specific file name"""
    
    if image_info_dict == None:
        return ""
    return image_info_dict[filename]
    

def main(processing_function):
    """App entry point."""
    print("HDF5 Database Builder for Deep Learning")
    
    filenames = get_filenames(IMAGE_DIR_PATH)
    print("[INFO] Scanning folder {}".format(IMAGE_DIR_PATH))
    print("[INFO] Image Processing function: {}".format(processing_function))
    print("[INFO] Detected {} files".format(len(filenames)))
    
    with open(Y_FILE_PATH) as jf:
        img_desciprtion = json.load(jf)

    original_filenames = {}
    file_counter = 0
    image_information = {}
    
    with h5py.File(DATAFILENAME, 'w') as f:

        for filename in filenames:
            if (file_counter % 10 == 0):
                print("[INFO] Processing {}-th image.".format(file_counter))
                
            # x, y, rgb = customxy.prepare_x_and_y(IMAGE_DIR_PATH+filename, IMG_DIMS)
            x, y, rgb = processing_function(IMAGE_DIR_PATH+filename, IMG_DIMS)
            # description = get_image_info(filename, img_desciprtion)

            new_filename = X_FILE_PREFIX+str(file_counter)
            original_filenames[new_filename] = filename
            original_filename = filename
            filename = new_filename
            
            # save image (X)
            ff = f.create_dataset(filename+"_RGB", data=rgb, compression='gzip')
            f.create_dataset(filename, data=x, compression='gzip')
            f.create_dataset(Y_FILE_PREFIX+str(file_counter), data=y, compression='gzip')
            
            # save original name attribute
            ff.attrs["original_filename"] = original_filename
            
            file_counter +=1
            
            # image_information[filename] = {"category":description['category'], "class":description['class']}
            
        f.create_dataset('original_filenames', data=json.dumps(original_filenames))


if __name__ == '__main__':
    
    tic = time.time()
    main(customxy.prepare_x_and_y)
    print("\nIt took {} seconds to create a database".format(time.time()-tic))
