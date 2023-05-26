This file will be used to track all the changes made to the original code.

**First iteration**

**25th May 2023**

1. Successfully cloned the ASGIT repo

2. Installed requirements.txt

3. Downloaded a dataset of flow cytometry images: https://figshare.com/articles/figure/URL7_Annotated_Data/12432506?file=22926995
   Found this from the following research paper: https://www.pnas.org/doi/pdf/10.1073/pnas.2001227117
   Description of the dataset:
      - The letters A to J and CE47 to CE49in the canadian dataset denote collection bag no.

4. Downloaded rotatingRBC.mov

5. Created a file cytometry_rbc_preprocess.py 
   - Deleted all RBC images that were not CrenatedDisc or SmoothDisc
   - Some images were blacked out, deleted those.
   - Deleted Swiss_additional folder
   - Generated 1405 images cytometry images
   - Combined all of them into a single training folder 

6. Deleted half of all the folders in order to reduce the no. of images

7. Created a file rbc_video_preprocess.py
   - Resized the flipping rbc video online at clideo.com since direct resize using python was leading to low quality. 
   - Generated 1640 rotating RBC images

8. Default mask size might need to be changed in attn_cycle_gan_v2_model.py. Changed it to 32 from 128.

9. Separated 200 images from the RBC_simulation dataset to create a test dataset in testA folder. Renamed the folders containing the RBC_simulation and 
   Training_Canada_Swiss to trainA and trainB as per the base_dataset.py file. 

10. Ran train.py with PHA + RHP, resnet6 generator.
    Got RuntimeError: No CUDA GPUs are available
    Installed pytorch version based on advice from stackoverflow. Went to pytorch.org and installed with command copied from there: 
    pip3 install torch torchvision torchaudio
    Didn't work, added a print statement to base_options to see the gpu_ids printed.
    Couldn't sort it out, doing cpu training for now.

11. Set the default value of --gpu_ids in base_options.py to -1 to shift to cpu training from gpu.  

IndexError: self.aux_data = aux_dataset.AuxAttnDataset(3000, 3000, self.gpu_ids[0], mask_size=opt.mask_size) list index out of range 

12. Changed default mask_size in aux_dataset.py to 64 from 256. Still got the same error. 

13. Figured out the problem. In line 57 of attn_cycle_gan_model.py made the following change to handle the problem of self.gpu_ids being an empty:
        if len(self.gpu_ids) > 0:
            self.aux_data = aux_dataset.AuxAttnDataset(3000, 3000, self.gpu_ids[0], mask_size=opt.mask_size)
        else: # Made this modification since gpu-id was an empty list
            self.aux_data = aux_dataset.AuxAttnDataset(3000, 3000, -1, mask_size=opt.mask_size)

14. This leads to problems downstream. The right solution is to set device to "cpu". In base_options.py made the following modification:

        if len(opt.gpu_ids) > 0:
            torch.cuda.set_device(opt.gpu_ids[0])
        else:
            opt.gpu_ids = ["cpu"]

15. Sorted this out with:
        if len(self.gpu_ids) > 0:
            self.aux_data = aux_dataset.AuxAttnDataset(3000, 3000, self.gpu_ids[0], mask_size=opt.mask_size)
        else: # Made this modification since gpu-id was an empty list
            self.aux_data = aux_dataset.AuxAttnDataset(3000, 3000, "cpu", mask_size=opt.mask_size)

16. Ran into new error: 

        model.optimize_parameters()  # calculate loss functions, get gradients, update network weights
          File "/home/abeer/Documents/GitHub/ASGIT/models/attn_cycle_gan_model.py", line 232, in optimize_parameters
            self.forward()      # compute fake images and reconstruction images.
          File "/home/abeer/Documents/GitHub/ASGIT/models/attn_cycle_gan_model.py", line 125, in forward
            self.fake_B = self.netG_A(self.real_A * (1. + self.attn_A))
        RuntimeError: The size of tensor a (256) must match the size of tensor b (128) at non-singleton dimension 3

**26th May 2023**

1. Printed the shapes of self.real_A and self.attn_A:

   Real A shape:  torch.Size([1, 3, 256, 256])
   A attention shape:  torch.Size([1, 1, 128, 128])

2. Problem of unable to start Visdom server solved. Just run python -m visdom.server -p 8098 in another terminal in the same directory. 

3. In attn_cycle_gan_model.py, set --mask_size default value to 64 in the def modfiy_command_line() to change size of attention masks to 64 x 64.
   Still doesn't solve the problem of why A is a 256 x 256 tensor

4. Added print(self.real_A.shape) at line 101 in attn_cycle_gan_model.py for debugging

5. Ran the training file with:
    python3 train_attn.py --netG resnet_6blocks --netD posthoc_attn --model attn_cycle_gan --concat rmult --dataroot "datasets" --name sim2synthetic --preprocess "none"
   Did this since preprocess by default is to resize and crop which changes the image size to 256 x 256 
   Also deleted the debug line print(self.real_A.shape) at line 101 in attn_cycle_gan_model.py

6. Ran into the following error:

    File "/home/abeer/Documents/GitHub/ASGIT/models/attn_cycle_gan_model.py", line 244, in optimize_parameters
    self.aux_data.update_attn_map(self.attn_A_index, self.tmp_attn_A.detach_(), True)
  File "/home/abeer/Documents/GitHub/ASGIT/data/aux_dataset.py", line 29, in update_attn_map
    self.A_attns[idx] = tgt_tensor
    RuntimeError: shape mismatch: value tensor of shape [256, 256] cannot be broadcast to indexing result of shape [1, 1, 64, 64]

7. Added the following debug lines at line 110 in attn_cycle_gan_model.py:

        print("Real_A shape ", self.real_A.shape)
        print("Real_B shape ", self.real_B.shape)
        print("Attention A shape", self.attn_A.shape)
        print("Attention B shape", self.attn_B.shape)

8. Shapes are fine for these arrays 64,64 only

9. Changed self.mask_shape in class PHADiscriminator() to 64 from 256 at line 1006 in networks.py 

10. All errors resolved. Will now try to look at the live web display of training results.

11. Error: ListIndex out of range. Will try to resume training with --continue_training option in the command line



 