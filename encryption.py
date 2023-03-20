import os
import diffuse as dif
import confuse as con
import reshape as res
import cv2
import img as image
import time

def encryption(file_path, dest_path, key):
    st1 = time.perf_counter()
    img = image.IMG(file_path, image.classify.ORIGINAL, cv2.imread(file_path), key)
    dest = os.path.join('.', 'images')
    print("image_dimensions: ",img.dim)
    st = time.perf_counter()
    img_reshaped = image.IMG(dest+"\\reshaped\\"+img.f_name.split('.')[0]+".png", image.classify.RESHAPED, res.resize_toSquare(img), key)
    et = time.perf_counter() - st
    msg="\nimage_dimensions: "+str(img.dim) +"\nTime taken for changing_size_to_square: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    print(f"Time taken for changing_size_to_square: {et:0.4f} seconds")
    st = time.perf_counter()
    img_confused = image.IMG(dest+"\\confused\\"+img.f_name.split('.')[0]+".png", image.classify.CONFUSED, con.con_arnold(img_reshaped), key)
    et = time.perf_counter() - st
    print(f"Time taken for confusion: {et:0.4f} seconds")
    msg="\nTime taken for confusion: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    st = time.perf_counter()
    img_diffused = image.IMG(dest_path+"\\"+img.f_name.split('.')[0]+".png", image.classify.ENCRYPTED, dif.pxl_change(img_confused), key)
    et = time.perf_counter() - st
    msg="\nTime taken for diffusion: "+str(et)+" seconds"
    et1 = time.perf_counter() - st1
    msg="\nTime taken for ecryption: "+str(et1)+" seconds"
    print(f"Time taken for encryption: {et1:0.4f} seconds")
    cv2.imwrite(img_diffused.f_path, img_diffused.mat)
    with open("analysis.txt",'a') as fl:
        fl.write(msg)