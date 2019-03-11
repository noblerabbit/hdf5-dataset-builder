# HDF5 Image Dataset Builder

Short scipts that procrsses images from supplied folder and stores them as a hdf5 data file.

Processing functions are located in the customxy.py file.

USAGE:
0. clone the repo
1. create virtual_env
2. pip install requirments
3.  run python main.py with arugments.
4.  






HDF5 Image Database Builder for Deep Learning

Use this program if you want to organize and modify your images for deep learning...


- check system specs
- anayse input foldr (nubmer of images etc)
- estimate workload (ie seconds remaning)
- 

args: 
path to images
path to image description (json format, so it can be converted to python dictionary):
                          if = None just store X
                          if = json/convert
                        
new_image_name = 'same' or 'name'
create_group = True (aka folder X, Y)

#part of hdf5 is also original mapping, filenames back to image 


Make an application that takes folder to input images, and labels

processes them and saves them in the hdf5 file in compressed state.

if no input is given then just compress x,
or allow to provide the compressing function

input arg: size of the image

// im MB size
du -sh * - show image folders
du --summary --human-readable *
ls -l --block-size=M

28MB - size - 5.127326965332031 seconds -with skimage
28 MB - size - 1.0338988304138184 seconds - with cv2. cv2 is much faster


import time
import curses

def pbar(window):
    for i in range(10):
        window.addstr(10, 10, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.refresh()
        time.sleep(0.5)

curses.wrapper(pbar)