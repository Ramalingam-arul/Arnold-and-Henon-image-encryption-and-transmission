import os
import diffuse as dif
import confuse as con
import reshape as res
import cv2
import img as image
import time

def decryption(file_path, dest_path, key):
    st1 = time.perf_counter()
    img_encrypted = image.IMG(file_path, image.classify.ENCRYPTED, cv2.imread(file_path, cv2.IMREAD_UNCHANGED), key)
    path = os.path.join('.', 'images')
    st = time.perf_counter()
    img_undiffused = image.IMG(path+"\\undiffused\\"+img_encrypted.f_name.split('.')[0]+".png", image.classify.UNDIFFUSED, dif.pxl_change(img_encrypted), key)
    et = time.perf_counter() - st
    print(f"Time taken for undiffusion: {et:0.4f} seconds")
    msg="\nTime taken for undiffusion: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    print("encrypted_filename: ",img_encrypted.f_name)
    st = time.perf_counter()
    img_unconfused = image.IMG(path+"\\unconfused\\"+img_encrypted.f_name.split('.')[0]+".png", image.classify.UNCONFUSED, con.uncon_arnold(img_undiffused), key)
    et = time.perf_counter() - st
    print(f"Time taken for unconfusion: {et:0.4f} seconds")
    msg="\nTime taken for unconfusion: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    st = time.perf_counter()
    img_decrypted = image.IMG(dest_path+"\\"+img_encrypted.f_name.split('.')[0]+".png", image.classify.DECRYPTED, res.border_croper(img_unconfused), key)
    et = time.perf_counter() - st
    print(f"Time taken for border_croping: {et:0.4f} seconds")
    msg="\nTime taken for border_croping: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    et1 = time.perf_counter() - st1
    msg="\nTime taken for decryption: "+str(et1)+" seconds"
    print(f"Time taken for decryption: {et1:0.4f} seconds")
    cv2.imwrite(img_decrypted.f_path, img_decrypted.mat)
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
        time.sleep(0.3)