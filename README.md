# HDF5 Image Dataset Builder (V.1.0)



This scripts reads images from folder and procresses them through the custom processing function and stores them in a HDF5 file.

HD5F is a file format that is optimized for quickly reading data from the file into memory (faster than is we read filed from the folder on the disk).
It also provides a neat way of transporting data as a single file.

*The main advantage of this script is that it enables custom processing functions to be integrated in the code
without modification of the rest of the code. The outoup of processing function should be a dict with desired size of keys.*

### Instructions ###

**General**
1. clone the repo
2. install dependancies
3. run *"python main.py"* to generate sample hdf5 dataset file
4. run *"python inspect_file.py"* to get summary from the hdf5 dataset file


**In terminal**
> git clone https://github.com/noblerabbit/hdf5-dataset-builder.git

> cd noblerabbit/hdf5-dataset-builder

> pip install requirements.txt

> python main.py

> python inspect_file.py


### Arguments ###
**main.py (python main.py args):**
* **-x** (Path to image folder; default:"test_images")
* **-d** (tupple of width and height of the resized image; default: (256, 256)
* **-func** (name of the processing function defined in customxy.py; default: "prepare_x_and_y")
* **-img** (which image type to include. ie. ".jpg"; default: "" - all images)
* **-sf** (path where to store hdf5 datafile; default: "test_hdf5_data/test_data.hdf5")

    > python main.py -x "test_images/"

**inspect_file.py (python inspect_file.py)**
* -f (provide path to hdft file for analysis: default: "test_hdf5_data/test_data.hdf5")

    > python inspect_file.py -f "test_hdf5_data/test_data.hdf5"


### TODO ###
- [ ] Add option to parse subfolders
- [ ] Custom function example to parse category from filename and store it as Y
