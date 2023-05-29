# File to perform all the preprocessing options
import os
import shutil
import cv2
import numpy as np

# Get all the folders in a directory
avail_folders = ["Canadian", "Swiss", "Swiss_additional"]

'''
*******************************************************************************************************************************

                                        DATA CLEANING SECTION
                                        
*******************************************************************************************************************************
'''


# #Delete all the folders except for SmoothDisc folders to select only smooth RBC images 
# for folder in avail_folders:
#     folder_path = os.path.join("Training_Canada_Swiss",folder)
#     subdirectories = [x[0] for x in os.walk(folder_path)]
#     for subdirectory in subdirectories:
#         if subdirectory.count('/')==4:
#             if subdirectory.endswith("SmoothDisc"):
#                 continue
#             else:
#                 shutil.rmtree(subdirectory) # Remove all the subdirectories that don't contain Disc shaped RBCs
#                 print(subdirectory + " deleted")
                
# #Delete all the black images and the non-opening images from the dataset from the dataset
# for folder in avail_folders:
#     folder_path = os.path.join("Training_Canada_Swiss",folder)
#     subdirectories = [x[0] for x in os.walk(folder_path)]
#     for subdirectory in subdirectories:
#         if subdirectory.endswith("CrenatedDisc") or subdirectory.endswith("SmoothDisc"): # Enter the folder where images are stored
#             img_paths = []
#             for x in os.walk(folder_path): # Get list of image files present in the directory
#                 img_paths.extend(x[2])
#             for img_path in img_paths:
#                 img_path = os.path.join(subdirectory,img_path)
#                 img = cv2.imread(img_path, 0) # Load the image in grayscale
#                 try:
#                     if np.average(img[0:5,0:5])<20:
#                         os.remove(img_path) # Delete image file if top left corner is mostly black
#                         print(img_path + " deleted")
#                 except: # Some image paths listed are already deleted. To handle that try and except statements were used
#                     continue

'''
*********************************************************************************************************************************

                                            IMAGE RESIZING AND SAVING

*********************************************************************************************************************************
'''
idx = 0
for folder in avail_folders:
    folder_path = os.path.join("Training_Canada_Swiss",folder)
    subdirectories = [x[0] for x in os.walk(folder_path)]
    for subdirectory in subdirectories:
        if subdirectory.endswith("SmoothDisc"): # Enter the folder where images are stored
            img_paths = []
            #folder_path = os.path.join(folder_path,subdirectory)
            for x in os.walk(subdirectory): # Get list of image files present in the directory
                img_paths.extend(x[2])
            for img_path in img_paths:
                # Randomly select 20 % of all images since the total dataset length was otherwise 6102 images
                if np.random.rand() < 0.20:
                    img_path = os.path.join(subdirectory,img_path)
                    img = cv2.imread(img_path) # Load the image in grayscale
                    cv2.imwrite('../datasets/Training_Canada_Swiss/img' + str(idx) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
                    idx += 1
                
                


            