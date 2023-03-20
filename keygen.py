import secrets
import math
#generator = 243658791110131217141915231629
#prime = 691701709719727733739743751757
generator = 24365879
prime = 6917017

class start_arnold:
    def __init__(self, para):
        para = str(para)
        l_iter = para[-6:]
        self.iter = sum(int(digit) for digit in l_iter)
        self.p = para[:math.floor(len(para)/2)]
        self.q = para[math.floor(len(para)/2):]
        print("p: ",self.p)
        print("q: ",self.q)
        print("iteration: ",self.iter)
        msg="\np: "+str(self.p)+"\nq: "+str(self.q)+"\niteration: "+str(self.iter)
        with open("analysis.txt",'a') as fl:
            fl.write(msg)
        with open("analysis.txt",'a') as fl:
            fl.write(msg)

class start_henon:
    def __init__(self, para):
        para = str(para)
        if len(para) > 28:
            para = para[:28]
        y = float("0."+para[math.floor(len(para)/2):])
        x = float("0."+para[:math.floor(len(para)/2)])
        if(y>0.97):
            y=0.97-(y-0.97)
        if(x>0.97):
            x=0.97-(x-0.97)
        self.y = min(x,y)
        self.x = max(x,y)
        print("x: ",self.x)
        print("y: ",self.y)
        msg="\nx: "+str(self.x)+"\ny: "+str(self.y)
        with open("analysis.txt",'a') as fl:
            fl.write(msg)
        with open("analysis.txt",'a') as fl:
            fl.write(msg)

class Key:
    def __init__(self, privatekey, publickey):
        self.prime = prime
        self.genrator = generator
        self.shared_key1 = int(privatekey)
        self.shared_key2 = int(publickey)
        self.shared_key = pow(self.shared_key2,self.shared_key1,self.prime)
        print("shared_key: ",self.shared_key)
        self.henon = start_henon(self.shared_key)
        self.arnold = start_arnold(self.shared_key)
        
def genKeyPairs():
    key = secrets.randbits(100)
    pub = pow(generator,key,prime)
    return key, pub