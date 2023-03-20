import numpy as np
import cv2
import math
from PIL import ImageTk, Image

def border_croper(img):
    try:
        [h_old, w_old, dimension] = img.dim
        w = (img.mat[math.floor(h_old/2),:,3] == 255).sum()
        h = (img.mat[:,math.floor(w_old/2),3] == 255).sum()
        print("height: ",h)
        print("width: ",w)
        msg="\nheight: "+str(h)+"\nwidth: "+str(w)
        with open("analysis.txt",'a') as fl:
            fl.write(msg)
        img_new = np.empty([h,w,3])
        for i in range(3):
            img_temp = img.mat[:,:,[i,3]]
            img_temp = img_temp[img_temp[:,:,1] == 255]
            img_new[:,:,i] = np.reshape(img_temp[:,0], [h,w])
        return img_new
    except:
        return img.mat

def resize_toSquare(image):    
    [h, w, dimension] = image.dim
    size_new = max(h, w)
    resized_img = np.uint8(np.random.randint(0, 256, size=(size_new, size_new, 4)))
    resized_img[:,:,3] = 254
    x_off = math.floor((size_new-w)/2)
    y_off = math.floor((size_new-h)/2)
    img_mat = cv2.cvtColor(image.mat, cv2.COLOR_BGR2BGRA)
    resized_img[y_off:y_off+h, x_off:x_off+w] = img_mat.copy()
    return resized_img