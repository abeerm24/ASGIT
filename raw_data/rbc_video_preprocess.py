# This script is for generating a dataset of images from the rotating RBC video

import os
import cv2
import numpy as np

vid_path = "flippingrbc_wYIzq73f.mp4"

cap = cv2.VideoCapture(vid_path)

def random_rotate_image(image, angle):
  ''',255
  Function to rotate an image by a certain angle 
  '''
  image_center = tuple(np.array(image.shape[1::-1]) / 2) 
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(238,232,239)) # Video background color
  return result

# Check if camera opened successfully
if (cap.isOpened()== False): 
  raise Exception("Error opening video stream or file")

count =  0

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    
    angle = int(90*np.random.rand())

    # Display the resulting frame
    cv2.imshow('Frame',frame)

    img = frame
    cv2.imwrite('RBC_simulation/img' + str(count) + '.png', cv2.resize(img,(64,64),cv2.INTER_AREA))
    count += 1

    img = random_rotate_image(frame, angle)
    cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
    count += 1

    img = cv2.flip(img,-1)
    cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
    count += 1

    img = cv2.flip(img,0)
    cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
    count += 1

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break

# Read until video is completed
# pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
# while(cap.isOpened()):
#   # Capture frame-by-frame
#   ret, frame = cap.read()
#   count = 0
#   if ret == True:
#     # Rotate each image by a random angle
#     angle = int(90*np.random.rand())
    
#     img = frame
#     cv2.imwrite('RBC_simulation/img' + str(count) + '.png', cv2.resize(img,(64,64),cv2.INTER_AREA))
#     count += 1

#     img = random_rotate_image(frame, angle)
#     cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
#     count += 1

#     img = cv2.flip(img,-1)
#     cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
#     count += 1

#     img = cv2.flip(img,0)
#     cv2.imwrite('RBC_simulation/img' + str(count) + '.png',cv2.resize(img,(64,64),cv2.INTER_AREA))
#     count += 1
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break

#   else:
#     break

cap.release()