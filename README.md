# HDF5 Image Dataset Builder (BETA)

![Price: free](https://img.shields.io/badge/price-FREE-0098f7.svg)
![Version: 1.0.2](https://img.shields.io/badge/version-1.0.0_-green.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

**Use this script if you want to store images from a folder into a single hdf5 file. You also modify images before storing them in the dataset file.
Great way also to quickly create X,Y datasets for deep learning.**

### Desciption
This script reads images from folder and processes them through the custom processing function and stores them in a HDF5 file.

HD5F is a file format that is optimized for fast access of the data from disk (much faster than is we read files from the regular disk folder).
It also provides a neat way of transporting data as a single file. Great tutorial regarding HDF5 file format can be found at https://www.uetke.com/blog/python/how-to-use-hdf5-files-in-python/.

*The main advantage of this script is that it enables custom processing functions to be integrated in the code
without modification of the rest of the code. The output of the processing function must be a python dict but it can have  with arbitrary number keys. Look at 'customxy.py' for sample functions.*

### Instructions ###

**General**
1. clone the repo
2. install dependancies
3. run *"python main.py"* to generate sample hdf5 dataset file
4. run *"python inspect_file.py"* to get summary from the hdf5 dataset file

**In the terminal:**
```
$ git clone https://github.com/noblerabbit/hdf5-dataset-builder.git
$ cd hdf5-dataset-builder/
$ pip install -r requirements.txt
$ python main.py
$ python inspect_file.py
```

### Arguments ###
**main.py (python main.py args)**
* **-x** (Path to image folder; default:"test_images")
* **-d** (tupple of width and height of the resized image; default: (256, 256)
* **-f** (name of the processing function defined in customxy.py; default: "prepare_x_and_y")
* **-i** (which image type to include. ie. ".jpg"; default: "" - all images)
* **-s** (path where to store hdf5 datafile; default: "test_hdf5_data/test_data.hdf5")

```
   example: $ python main.py -x "test_images/"
```


**inspect_file.py (python inspect_file.py)**
* -f (provide path to hdft file for analysis: default: "test_hdf5_data/test_data.hdf5")
```
   example: $ python inspect_file.py -f "test_hdf5_data/test_data.hdf5"
```
### Processing Functions
Functions that dictate the output dictionary which contains processed image data to be stored to the hdf5 file. They are defined in "customxy.py".

#### Current custom functions: ####


**1. prepare_x_and_y**

Takes in RGB image, resizes the image, converts it to LAB format and returns dict as LAB L channel ("X"), LAB ab channel ("X")
and RGB resized image ("X").
This function is useful to prepare data to train CNN to colorize grayscale images.

**In the terminal:**
``` 
$ python main.py -f prepare_x_and_y
```


**2. resize_image**

Takes in RGB image, resizes the image and returns it as "RGB" key in the dictionary.

**In the terminal:**
```
 $ python main.py -r resize_image
```

### TODO ###
- [ ] Add option to parse subfolders
- [ ] Custom function example to parse category from filename
- [ ] Create custom function for categorical data (where Yi is name of category for each Xi)

### License
[MIT](https://choosealicense.com/licenses/mit/)