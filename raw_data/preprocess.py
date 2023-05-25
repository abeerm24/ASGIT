# File to perform all the preprocessing options
import os
import shutil
import cv2
import numpy as np

# Get all the folders in a directory
avail_folders = ["Canadian", "Swiss"]

'''
*******************************************************************************************************************************

                                        DATA CLEANING SECTION
                                        
*******************************************************************************************************************************
'''


# Delete all the non CrenatedDisc and Smooth Disc folders 
for folder in avail_folders:
    folder_path = os.path.join("Training_Canada_Swiss",folder)
    subdirectories = [x[0] for x in os.walk(folder_path)]
    for subdirectory in subdirectories:
        if subdirectory.count('/')==4:
            if subdirectory.endswith("CrenatedDisc") or subdirectory.endswith("SmoothDisc"):
                continue
            else:
                print(subdirectory + " deleted")
                shutil.rmtree(subdirectory) # Remove all the subdirectories that don't contain Disc shaped RBCs

# Delete all the black images and the non-opening images from the dataset from the dataset
for folder in avail_folders:
    folder_path = os.path.join("Training_Canada_Swiss",folder)
    subdirectories = [x[0] for x in os.walk(folder_path)]
    for subdirectory in subdirectories:
        if subdirectory.endswith("CrenatedDisc") or subdirectory.endswith("SmoothDisc"): # Enter the folder where images are stored
            img_paths = []
            for x in os.walk(folder_path): # Get list of image files present in the directory
                img_paths.extend(x[2])
            for img_path in img_paths:
                img_path = os.path.join(subdirectory,img_path)
                img = cv2.imread(img_path, 0) # Load the image in grayscale
                try:
                    if np.average(img[0:5,0:5])<20:
                        os.remove(img_path) # Delete image file if top left corner is mostly black
                        print(img_path + " deleted")
                except: # Some image paths listed are already deleted. To handle that try and except statements were used
                    continue
            

                


            