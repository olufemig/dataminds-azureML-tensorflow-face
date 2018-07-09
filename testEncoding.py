import cv2 
import pickle
import numpy as np
import myImageLibrary
import os
import base64

img = myImageLibrary.resize_crop(cv2.imread("images/images_all/pieter/img_1.jpg"),96)
img = np.expand_dims(img,axis=0) #reference

img_base64 = myImageLibrary.preprocess(img,transpose=False)
input_bytes = base64.b64decode(img_base64) 
img_decoded = np.loads(input_bytes)

check = np.sum(img-img_decoded)
if (img == img_decoded).all():
    print("ok")