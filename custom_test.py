import torch
from models.networks import define_G
from collections import OrderedDict
import numpy as np
import os
import cv2

model_dict = torch.load("checkpoints/sim2synthetic_ssim/10_net_G_A.pth")
new_dict = OrderedDict()
# for k, v in model_dict.items():
#     # load_state_dict expects keys with prefix 'module.'
#     new_dict["module." + k] = v

# make sure you pass the correct parameters to the define_G method
generator_model = define_G(input_nc=3,output_nc=3,ngf=64,netG="resnet_6blocks",
                            norm="batch",use_dropout=True,init_gain=0.02,gpu_ids=[]) # Empty gpu_ids since there is no gpu to train on 
generator_model.load_state_dict(model_dict)

# Directory to save test results
save_dir = "test_results/test_results_sim2synthetic_ssim"

# Test on all the images in the test directory

# Load test files
test_dir = "datasets/testA"     # Path to directory containing test files
test_files = []
for x in os.walk(test_dir):
    test_files.extend(x[2])

# Run on test_files
for test_file in test_files:
    img = cv2.imread(os.path.join(test_dir,test_file))
    img = torch.tensor(img)     # Convert to tensor
    cytometry_img = generator_model(img)
    cv2.imwrite(os.path.join(save_dir,test_file),np.uint8(cytometry_img))