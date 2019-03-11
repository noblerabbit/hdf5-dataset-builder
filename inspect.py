# Script that returns a short summary of HDF5 dataset created with
# HDF5 Dataset Image Builder

import h5py
import os

DATASET_PATH = "test_hdf5_data/test_data.hdf5"

EXCLUDE_DATASETS = ["hdf5-image-dataset-builder-signature", "original_filenames_mapping"]
PROP_DATASETS = len(EXCLUDE_DATASETS)

def inspect(DATASET=DATASET_PATH):
    line = "============================================="
    d = {}

    with h5py.File(DATASET_PATH, 'r') as f:
        #check for signature
        dataset_keys = f.keys()
        if not f[EXCLUDE_DATASETS[0]]:
            print("Dataset was not created with the tool.")
            return -1
        print(line)
        print("HDF5 Dataset Image Builder\nSignature found.")
        print("Dataset name: {}".format(DATASET_PATH.split("/")[-1]))
        print("Dataset size: {} MB".format(os.path.getsize(DATASET_PATH)/1000000))
        print(line)

        #loook all datasets and sort them
        
        for key in f.keys():
            if key not in EXCLUDE_DATASETS:
                k, nr = key.split("_")
                if k not in d.keys():
                    d[k] = [nr]
                else:
                    d[k].append(nr)
                    
        for key in d.keys():
            print("| {}\t : {} files |".format(key, len(d[key])))
            
        print("Total number of image datasets: {}".format(len(dataset_keys)-PROP_DATASETS))
        print("One example of dataset name: '{}' ".format(list(dataset_keys)[int(len(dataset_keys)/2)]))
        print(line)
                
            
if __name__ == '__main__':
    inspect()