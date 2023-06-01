# Script to quantitatively analyse the datapresent in the original flow cytometry images dataset
import os
import numpy as np

PATH = "/home/abeer/Downloads/Training_Test2_Canada_Swiss/Training_Canada_Swiss" # Path to the original training dataset
folders = ["Canadian","Swiss","Swiss_additional"]
cell_types =  ["CrenatedDisc", "CrenatedDiscoid", "CrenatedSphere", "CrenatedSpheroid", "Side", "SmoothDisc", "Undecidable"]
num_cell_types = np.zeros(7)

for folder in folders:
    folder_path = os.path.join(PATH,folder)
    subdirectories = [x[0] for x in os.walk(folder_path)]
    # print(subdirectories)
    for subdirectory in subdirectories:
        for i in range(7):    
            if subdirectory.endswith(cell_types[i]):
                img_paths = [] # Initialize an empty list of image files in the subdirectory
                for x in os.walk(subdirectory): # Get list of image files present in the directory
                    img_paths.extend(x[2])
                num_cell_types[i] += len(img_paths)

# Print the no. of different cell types

for i in range(7):
    print(cell_types[i] + ": " + str(num_cell_types[i]))
