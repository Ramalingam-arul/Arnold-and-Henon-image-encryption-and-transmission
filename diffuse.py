import numpy as np
import cv2
import time
def henon_gen(img):
    [row, column, dim] = img.dim
    seq_size = row * column * 8
    y = img.key.henon.y
    x = img.key.henon.x
    bitseq = []
    byte_arr = []
    for i in range(seq_size):
        x_new = y + 1 - 1.4 * x**2
        y_new = 0.3 * x
        x = x_new
        y = y_new
        if x_new <= 0.3992:
            bit = 0
        else:
            bit = 1
        try:
            bitseq.append(bit)
        except:
            bitseq = [bit]
        if i % 8 == 7:
            decimal = dec(bitseq)
            try:
                byte_arr.append(decimal)
            except:
                byte_arr = [decimal]
            bitseq = []
    byte_arr = np.asarray(byte_arr)
    henon_map = np.reshape(byte_arr, [row, column])
    return henon_map

def dec(bit_seq):
    deci = 0
    for bit in bit_seq:
        deci = deci * 2 + int(bit)
    return deci

def pxl_change(image):
    print("started diffusion...")
    msg="\nstarted diffusion..."
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    [row, col, dim] = image.dim
    al = image.mat[:,:,3]
    st = time.perf_counter()
    henon = henon_gen(image)
    et = time.perf_counter() - st
    print(f"Time taken for henon_map generation: {et:0.4f} seconds")
    msg="\nTime taken for henon_map generation: "+str(et)+" seconds"
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    st = time.perf_counter()
    res_mat = []
    img_mat = []
    henon_flatten = henon.flatten()
    for i in range(3):
        img_mat.append(image.mat[:,:,i].flatten())
    for i in range(3):
        res_mat.append(np.bitwise_xor(henon_flatten, img_mat[i]))
    res_mat = np.asarray(res_mat)
    re_mat_g = np.reshape(res_mat[1], [row,col])
    res_mat_r = np.reshape(res_mat[2], [row,col])
    res_mat_b = np.reshape(res_mat[0], [row,col])
    res_mat = np.dstack((res_mat_b, re_mat_g, res_mat_r, al))
    et = time.perf_counter() - st
    print(f"Time taken for reshaping: {et:0.4f} seconds")
    return res_mat
