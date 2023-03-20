import numpy as np

def uncon_arnold(image):
    print("started to unconfuse...")
    msg="\nstarted to unconfuse..."
    dim = image.dim[0]
    iteration = image.key.arnold.iter
    q_whole = image.key.arnold.q
    p_whole = image.key.arnold.p
    x,y = np.meshgrid(range(dim),range(dim))
    a_map = image.mat
    for i in reversed(range(iteration)):
        q = int(q_whole[i%len(q_whole)]+q_whole[(i+1)%len(q_whole)])
        p = int(p_whole[i%len(p_whole)]+p_whole[(i+1)%len(p_whole)])
        x_new = (x+y*p) % dim
        y_new = (x*q+y*(p*q+1)) % dim
        a_map[x,y] = a_map[x_new,y_new]
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    return a_map

def con_arnold(image):
    print("started to confuse...")
    msg="\nstarted to confuse..."
    dim = image.dim[0]
    iteration = image.key.arnold.iter
    q_whole = image.key.arnold.q
    p_whole = image.key.arnold.p
    x,y = np.meshgrid(range(dim),range(dim))
    a_map = image.mat
    for i in range(iteration):
        q = int(q_whole[i%len(q_whole)]+q_whole[(i+1)%len(q_whole)])
        p = int(p_whole[i%len(p_whole)]+p_whole[(i+1)%len(p_whole)])
        x_new = (x+y*p) % dim
        y_new = (x*q+y*(p*q+1)) % dim
        a_map[x_new,y_new] = a_map[x,y]
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    return a_map