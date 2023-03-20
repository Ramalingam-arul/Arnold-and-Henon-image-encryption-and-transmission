from enum import Enum
import os
import cv2

class classify(Enum):
    ORIGINAL = 1
    RESHAPED = 2
    CONFUSED = 3
    ENCRYPTED = 4
    UNDIFFUSED = 5
    UNCONFUSED = 6
    DECRYPTED = 7

class IMG:
    def __init__(self, f_path, type, mat, Key):
        self.f_path = f_path
        self.f_name = os.path.basename(f_path)
        self.type = type
        self.mat = mat
        self.dim = self.mat.shape
        self.key = Key