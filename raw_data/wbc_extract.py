import cv2
import numpy as np
import os

def split_nuc_and_cyto(img_gt):
    """
    This function split the nucleus and cytoplasm

    :param img_gt: groundtruth image in *.bmp format and shape of 575*575
    :return: nucleus, cytoplasm
    """

    # Extracting the nucleus
    img_nuc = np.zeros_like(img_gt)
    img_nuc[img_gt == 100] = 100

    # Extracting the cytoplasm
    img_cyt = np.zeros_like(img_gt)
    img_cyt[img_gt == 255] = 255

    return img_nuc, img_cyt


if __name__ == '__main__':
    orig_folder_path = "GrTh/Original/"
    mask_folder_path = "GrTh/Ground Truth/"
    wbc_types = ["Basophil","Eosinophil","Lymphocyte","Monocyte","Neutrophil"]
    img_name = "95-5-4-1_45_1.jpg"
    orig_img_path = os.path.join(orig_folder_path + wbc_types[1],img_name)
    mask_img_path = os.path.join(mask_folder_path + wbc_types[1],img_name)
    orig_img = cv2.imread(orig_img_path, cv2.IMREAD_GRAYSCALE)
    mask_img = cv2.threshold(cv2.imread(mask_img_path,cv2.IMREAD_GRAYSCALE), 20, 255, cv2.THRESH_BINARY)[1]
    mask_img = mask_img/255.0 # Convert to a scale of 1

    cell_img = np.uint8(np.multiply(orig_img,mask_img))
    #cell_img = cv2.threshold(cv2.imread(mask_img_path,cv2.IMREAD_GRAYSCALE), 50, 255, cv2.THRESH_TRUNC)[1]

    for i in range(cell_img.shape[0]):
        for j in range(cell_img.shape[1]):
            if (not cell_img[i][j]):
                cell_img[i][j] += 150 + int(10*np.random.normal())
    
    cell_img = cv2.GaussianBlur(cell_img,(5,5),cv2.BORDER_DEFAULT)
    cv2.imshow('orig_img', orig_img)
    cv2.imshow('mask',mask_img)
    cv2.imshow('masked_cell', cell_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()