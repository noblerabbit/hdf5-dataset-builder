import numpy as np
import time
import h5py
import cv2
import os
from skimage import io, color, transform
import json


DATAFILENAME = "data.hdf5"
IMAGE_DIR_PATH = "test/"
IMAGE_DESCRIPTION_PATH = "None" #json file, if none just save image without descriptions
file_prefix = 'None' #if none save the same as file name, else rename to prefix and count1
file_type = "None" #try to load all images, else load only specific file type
IMG_DIMS = (256, 256)
path_to_json_file = "data_dict.json"


#get array of filenames
def get_filenames(folder_path, file_type=""):
    """Returns list of filenames in the folder_path.
    Ommits hidden files in the folder.

    params:
        @file_type: what type of files to include
                    if "" - all files
                    if "jpg" anly jpg files
    returns: list of filenames
    """
    return [file for file in os.listdir(folder_path) if not file.startswith(".") and file.endswith(file_type)]

def prepare_image(image_path, img_dims):
    """Method takes in path to the image and desired image dimensions
    and reutrns resized image in a numpy array"""
    # img = io.imread(image_path)
    # img = transform.resize(img, img_dims)
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, img_dims)
    return img

def get_image_info(filename, decriptions_dict=None):
    """Lookup in jason file for image dict and return description
    for specific file name
    """
    if decriptions_dict == None:
        return ""
    # return decriptions_dict[filename]
    # return "Basic image descipriton"
    return 10000



def main(path_to_dir, img_dims = (256, 256), file_prefix="", database_name = DATAFILENAME):
    """This function saves hdf5 file of processed images to base directory
    If the file already exists it is overwritten.
    
    params:
        @path_to_dir: path to image directory
        @img_dims: tupple of final image width and heght
        @file_prefix: the basename for new image
                      if empty string '' it saves under original filename
        @databse_name: the name of the output hdf5 file
    
    returns:
        saves the hdf5 file in base directory. the file is named database_name.
    """
    filenames = get_filenames(path_to_dir)
    with open(path_to_json_file) as jf:
        img_desciprtion = json.load(jf)

    original_filenames = {}
    file_counter = 0
    
    with h5py.File(database_name, 'w') as f:
        for filename in filenames:
            data = prepare_image(path_to_dir+filename, img_dims)
            description = get_image_info(filename, img_desciprtion)
            
            if file_prefix != "":
                new_filename = file_prefix+str(file_counter)
                original_filenames[new_filename] = filename
                filename = new_filename
            
            # save image (X)
            ff = f.create_dataset(filename, data=data, compression='gzip', dtype='i1')
            ff.attrs["Y"] = 1
            file_counter +=1
            # save image description (Y)
            description = np.string_("Hello asshole")
            f.create_dataset(filename+"_desc", data=description)
            
        if len(original_filenames): 
            f.create_dataset('original_filenames', data=json.dumps(original_filenames))
        
    with h5py.File(database_name, 'r') as f:
        for key in f.keys():
            print(key)
        dset = f['flowers-macro-sunflowers-46216.jpg']
        # data1 = data[:]
        print(dset[()])
        print(dset.attrs['Y'])
            
            

if __name__ == '__main__':
    tic = time.time()
    main(IMAGE_DIR_PATH)
    print("It took {} seconds to create a database".format(time.time()-tic))
