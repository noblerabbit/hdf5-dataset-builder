import numpy as np
import time
import h5py
import cv2
import os
from skimage import io, color, transform
import json
import customxy
import argparse
import inspect_file

 # constrct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-x", "--x_path", required = False, default="test_images/", help="Path to IMAGE folder.")
# ap.add_argument("-y", "--y_path", required = False, default="y_test.json", help="Path to JSON file with image info.")
# ap.add_argument("-p", "--prefix", required = False, default="", help="Give new name for files, or leave blank to keep the orginal names.")
ap.add_argument("-d", "--dimensions", required = False, default=(256, 256), help = "Set image dimensions. If empty images will be in (256, 256) size")
ap.add_argument("-compress", "--compress", required=False, default=True, help = "Set to False in order to avoid (gzip) compression inside hdf5")
ap.add_argument("-sf", "--save_to_file", required=False, default="test_hdf5_data/test_data.hdf5", help=  "Name of the output HDF5 file with images")
ap.add_argument("-img", "--image_type", required=False, default="", help = "Include only files specific filetype (ie. jpg). default is: '' - all files")
ap.add_argument("-func", "--proc_func", required=False, default="prepare_x_and_y", help= "Function to the  process images.")

args = vars(ap.parse_args())


# Link constants to input vars
DATAFILENAME = args['save_to_file']
IMAGE_DIR_PATH = args['x_path']
IMG_DIMS = args['dimensions']
# Y_FILE_PATH = args['y_path']
# X_FILE_PREFIX = "X"
# Y_FILE_PREFIX = "Y"
FILE_TYPE = args['image_type']
COMPRESS = args['compress']
PROC_FUNC = args['proc_func']

#get array of filenames
def get_filenames(folder_path, file_type=""):
    """Returns list of filenames in the folder_path.
    Ommits hidden files in the folder. """
    
    return [file for file in os.listdir(folder_path) if not file.startswith(".") and file.endswith(file_type)]

# TODO explore dataset after creation function and print out the summary

def main(processing_function):
    """App entry point."""
    # print("HDF5 Database Builder for Deep Learning")
    
    filenames = get_filenames(IMAGE_DIR_PATH)
    print("[INFO] Scanning folder {}".format(IMAGE_DIR_PATH))
    # print("[INFO] Image Processing function: {}".format(processing_function))
    print("[INFO] Detected {} files".format(len(filenames)))
    print(line)
    
    # with open(Y_FILE_PATH) as jf:
    #     img_desciprtion = json.load(jf)

    filenames_mapping = {}
    file_counter = 0
    
    with h5py.File(DATAFILENAME, 'w') as f:

        for filename in filenames:
            if (file_counter % 10 == 0):
                print("[INFO] Processing {}-th image.".format(file_counter))
                
            processed_image_data = processing_function(IMAGE_DIR_PATH+filename, IMG_DIMS)
            
            if processed_image_data == {}:
                continue
                
            # save data dict to dataset
            for key in processed_image_data.keys():
                f.create_dataset(key+"_"+str(file_counter), data=processed_image_data[key], compression='gzip')
        
            filenames_mapping[str(file_counter)] = filename
            
            file_counter += 1

        f.create_dataset('original_filenames_mapping', data=json.dumps(filenames_mapping))
        
        # creating a dataset with builder information
        f.create_dataset('hdf5-image-dataset-builder-signature', data=json.dumps({"signature":"version1"}))
    
    print(line)
    print("[SUMMARY] Stored {} images in {} file.".format(file_counter,DATAFILENAME))


if __name__ == '__main__':

    line = "========================================================"
    print(line)
    print("HDF5 Dataset Image Builder\n")
    print("Image processing function: {}".format(PROC_FUNC))
    print("Image type: {}".format(FILE_TYPE if FILE_TYPE!="" else "All supported image formats."))
    print ("[NOTE] All Image procesing functions must be defined in customxy.py\n")
    print(line)
    
    tic = time.time()
    main(getattr(customxy, PROC_FUNC))
    print("[SUMMARY] It took {} seconds to create the dataset.".format(round(time.time()-tic)))
    print(line)
    inspect_file.inspect(DATAFILENAME)
