import tkinter as tkin
from tkinter import filedialog as fd
import os
import encryption as e
import decryption as d
import threading as thread
import keygen as k
import socket
import time
from _thread import *
from PIL import ImageTk,Image
class EncrytAndDecryptWindow:
    
    def img_chooser(self):
        file = fd.askopenfilenames(title='Choose images')
        for i in file:
            self.files.append(i)
            self.choose_entry.config(state=tkin.NORMAL)
            self.choose_entry.insert(tkin.INSERT, i+'\n')
            self.choose_entry.config(state=tkin.DISABLED)

    def dest_chooser(self):
        dest = fd.askdirectory(title='Select output destination')
        self.op_entry.config(state=tkin.NORMAL)
        self.op_entry.delete(0, tkin.END)
        self.op_entry.insert(tkin.INSERT, dest)
        self.op_entry.config(state=tkin.DISABLED)
    
    def mode_changer(self):
        if self.selected_type.get() == 1:
            self.key2_label.config(text="Input receiver's public key: ")
            self.encrypt_text.set("Encrypt & send")
            self.choose_label.config(text="Select images to be encrypted")
        else:
            self.encrypt_text.set("Decrypt")
            self.choose_label.config(text="Select images to be decrypted")
            self.key2_label.config(text="Enter shared key2: ")

    def prog_show(self, filename, index, length):
        self.progText.set(self.encrypt_text.get()+"ing "+os.path.basename(filename)+" ("+str(index)+"/"+str(length)+")")
        self.window.update_idletasks()

    def encryptAndSend(self, listFilenames, private_key, public_key):
        key = k.Key(private_key, public_key)
        self.disable(tkin.DISABLED)
        for i in listFilenames:
            self.prog_show(i, listFilenames.index(i), len(listFilenames))
            nam=(str(i).split('/'))[-1]
            msg="\n\nimage_name: "+(nam)
            print("image_name: ",(nam))
            if self.selected_type.get() == 1:
                f_size_old=os.stat(i)
                msg+="\nimage size in MB before encryption is: "+str(f_size_old.st_size/(1024*1024))
                print(f'image size in MB before encryption is: "{f_size_old.st_size/(1024*1024)}')
                with open("analysis.txt",'a') as fl:
                    fl.write(msg)
                e.encryption(i, self.op_entry.get(), key)
                print(self.op_entry.get()+"/"+(nam))
                f_size_new=(os.stat(str(self.op_entry.get())+"/"+(nam.split('.')[0])+".png"))
                msg="\nimage size in MB after encryption is: "+str(f_size_new.st_size/(1024*1024))
                print(f'image size in MB after encryption is: "{f_size_new.st_size/(1024*1024)}')
                change_size=f_size_new.st_size/(1024*1024)-f_size_old.st_size/(1024*1024)
                msg+="\nchange in size: "+str(change_size)
                with open("analysis.txt",'a') as fl:
                    fl.write(msg)
            if self.selected_type.get() == 2:
                f_size_old=os.stat(i)
                msg+="\nimage size in MB before decryption is: "+str(f_size_old.st_size/(1024*1024))
                print(f'image size in MB before decryption is: "{f_size_old.st_size/(1024*1024)}')
                with open("analysis.txt",'a') as fl:
                    fl.write(msg)
                d.decryption(i, self.op_entry.get(), key)
                f_size_new=(os.stat(str(self.op_entry.get())+"/"+(nam.split('.')[0])+".png"))
                msg="\nimage size in MB after decryption is: "+str(f_size_new.st_size/(1024*1024))
                print(f'image size in MB after decryption is: "{f_size_new.st_size/(1024*1024)}')
                change_size=f_size_new.st_size/(1024*1024)-f_size_old.st_size/(1024*1024)
                msg+="\nchange in size: "+str(change_size)
                with open("analysis.txt",'a') as fl:
                    fl.write(msg)
        self.progText.set(self.encrypt_text.get()+"ion finished. ("+str(len(listFilenames))+"/"+str(len(listFilenames))+")")
        #
        #
        #
        #
        if self.selected_type.get() == 1:
            def mt_clients(c,tc,):
                dirs = os.listdir(self.op_entry.get())
                c.send(tc.to_bytes(2,'big'))
                time.sleep(0.5)
                for file in dirs:
                    c.send(b'next')
                    i = open(self.op_entry.get()+"/"+file , 'rb')
                    for j in i:
                        c.send(j)
                    print(file + " Sent")
                    msg="\n"+str(file) + " Sent"
                    with open("analysis.txt",'a') as fl:
                        fl.write(msg)
                    time.sleep(0.5)
                c.send(b'end')
                labelop.config(text="sent all files.",font=('Supreme', 9))
            def sendFiles():
                tc=1
                s = socket.socket()
                try:
                    s.bind(('',int(port_entered.get())))
                except socket.error as e:
                    print(str(e))
                s.listen(10)
                while True:
                    c , address = s.accept()
                    print('client Number: ' , str(tc)) 
                    msg='\n\nclient Number: ' + str(tc)
                    print('Connected with: ', address)
                    msg+='\nConnected with: '+ str(address)
                    with open("analysis.txt",'a') as fl:
                        fl.write(msg)
                    labelop.config(text=("connection established with "+str(address)+" and sending....."),font=('Supreme', 9))
                    start_new_thread(mt_clients, (c,tc ))
                    tc+=1 
                    print("connection closed with ",address) 
                    msg="\nconnection closed with "+str(address)
                    with open("analysis.txt",'a') as fl:
                        fl.write(msg)

            sender=tkin.Tk()
            sender.title("server IP input")
            sender.minsize(400,200)
            sender.configure(bg='#7DE5ED')
            labelport=tkin.Label(sender,text="Enter the port number: ",bg='#7DE5ED',font=('Supreme', 9))
            labelop=tkin.Label(sender,text="",bg='#7DE5ED',font=('Supreme', 9))
            port_text=tkin.StringVar()
            port_entered=tkin.Entry(sender,width=15,textvariable=port_text)
            button = tkin.Button(sender, text = "Send",bg='#5DA7DB', command = sendFiles,font=('Supreme', 10))
            labelop.grid(column = 0, row = 2,pady=3,sticky=tkin.W)
            labelport.grid(column = 0, row = 0,pady=3,sticky=tkin.W)
            port_entered.grid(column=1,row=0,pady=3,sticky=tkin.W)
            button.grid(column= 0, row = 1,pady=20,sticky=tkin.W)
            sender.mainloop()
            #
            #
            #
            #
        self.clear_ip()
        self.disable(tkin.NORMAL)
    def clear_ip(self):
        self.files.clear()
        self.choose_entry.delete(1.0, tkin.END)
        self.op_entry.delete(0, tkin.END)
        self.key2_entry.config(state=tkin.NORMAL)
        
    def disable(self, mode):
        self.button.config(state=mode)
        self.choose_entry.config(state=mode)
        self.op_entry.config(state=mode)
        self.clear_button.config(state=mode)
        self.op_dest_button.config(state=mode)
        self.select_button.config(state=mode)
        self.key2_entry.config(state=mode)
    
    def __init__(self, app, key):

        self.window = app
        self.window.minsize(600,350)
        self.window.title("Image Encryption and Decryption")
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

        self.files = []
        
        self.encrypt_text = tkin.StringVar()
        self.encrypt_text.set("Encrypt & Send")

        self.choose_label = tkin.Label(self.window, text="Select images to be encrypted",bg='#7DE5ED', font=('Supreme', 10))
        self.choose_label.grid(row=1, column=0, padx=(8,0), pady=(10,5), sticky='wn', columnspan=3)

        self.mode_label = tkin.Label(self.window, text="Select mode:",bg='#7DE5ED', font=('Supreme', 9))
        self.mode_label.grid(row=0, column=0, padx=(8,0), pady=(10,5), sticky='wn')

        self.selected_type = tkin.IntVar()
        self.selected_type.set(1)

        self.mode_e = tkin.Radiobutton(self.window, text="Encrypt", variable=self.selected_type, value=1,bg='#5DA7DB', command=self.mode_changer)
        self.mode_e.grid(row=0, column=1, padx=(4,0), pady=(10,0), sticky='wn')

        self.mode_d = tkin.Radiobutton(self.window, text="Decrypt",bg='#5DA7DB', variable=self.selected_type, value=2, command=self.mode_changer)
        self.mode_d.grid(row=0, column=2, padx=(4,0), pady=(10,0), sticky='wn')

        self.choose_entry = tkin.Text(self.window, width=0, height=0)
        self.choose_entry.config(state=tkin.DISABLED)
        self.choose_entry.grid(row=2, column=0, sticky='wens', padx=(10,5), rowspan=3, columnspan=3)

        self.op_label = tkin.Label(self.window, text="Select output destination folder",bg='#7DE5ED', font=('Supreme', 10))
        self.op_label.grid(row=5, column=0, padx=(8,0), pady=(10,5), sticky='wn', columnspan=3)

        self.select_button = tkin.Button(self.window, text ="Select",bg='#5DA7DB', command=self.img_chooser)
        self.select_button.grid(row=2, column=3, sticky='wen', padx=(5,10))

        self.clear_button = tkin.Button(self.window, text ="Clear",bg='#5DA7DB', command=lambda:[self.choose_entry.config(state=tkin.NORMAL), self.choose_entry.delete(1.0, tkin.END), self.choose_entry.config(state=tkin.DISABLED), self.files.clear()])
        self.clear_button.grid(row=3, column=3, sticky='wes', padx=(5,10), pady=(5,0))

        self.op_dest_button = tkin.Button(self.window,bg='#5DA7DB', text="Select", command=self.dest_chooser)
        self.op_dest_button.grid(row=6, column=3, sticky='wen', padx=(5,10))

        self.op_entry = tkin.Entry(self.window)
        self.op_entry.config(state=tkin.DISABLED)
        self.op_entry.grid(row=6, column=0, sticky='wen', padx=(10,5), columnspan=3)
        
        self.key1_label = tkin.Label(self.window, text="Shared key 1: ",bg='#7DE5ED', font=('Supreme', 10))
        self.key1_label.grid(row=7, column=0, padx=(8,0), pady=(5,5), sticky='wn', columnspan=3)

        self.key2_label = tkin.Label(self.window, text="Enter shared key2: ",bg='#7DE5ED', font=('Supreme', 10))
        self.key2_label.grid(row=9, column=0, padx=(8,0), pady=(5,5), sticky='wn', columnspan=3)
        
        self.key1_entry = tkin.Entry(app, width=0)
        self.key1_entry.insert(0, key)
        self.key1_entry.config(state=tkin.DISABLED)
        self.key1_entry.grid(row=8, column=0, sticky='wen', padx=10, columnspan=4)     

        self.key2_entry = tkin.Entry(app, width=0)
        self.key2_entry.grid(row=10, column=0, sticky='wen', padx=10, columnspan=4)
        
        self.button = tkin.Button(self.window, textvariable=self.encrypt_text,bg='#5DA7DB', command= lambda: thread._start_new_thread(self.encryptAndSend, (self.files, key, self.key2_entry.get())))
        self.button.grid(row=11, column=3, sticky='senw', padx=(0,10), pady=(20,10))

        self.progText = tkin.StringVar()
        self.prog_label = tkin.Label(self.window, textvariable=self.progText,bg='#7DE5ED', font=('Supreme', 9))
        self.prog_label.grid(row=11, column=0, sticky='swn', padx=(7,0), pady=(20,10), columnspan=3)

class loginpage:

    def new_key_gen(self):
        file_type = [('Text Document', '*.txt')]
        f = fd.asksaveasfile(title = "Select destination to save", initialfile='new_keypairs', filetypes=file_type, defaultextension=file_type)
        if f is None:
            return
        [key1, key2] = k.genKeyPairs()
        inf = "shared key1 = "+str(key1)+"\nshared key2 = "+str(key2)
        f.write(inf)
        f.close()

    def start_intro(self, key):
        self.window.destroy()
        tk_app = tkin.Tk()
        tk_app.configure(bg='#7DE5ED')
        func_app = EncrytAndDecryptWindow(tk_app, key)
        tk_app.mainloop()

    def __init__(self, app):
        self.window = app
        self.window.minsize(600,350)
        self.window.title("Ramalingam's chaos based Encrypter & Decrypter Login")

        self.image1 = Image.open("download.png")
        self.img1 = ImageTk.PhotoImage(self.image1)
        self.label1 = tkin.Label(self.window,image=self.img1)
        self.label1.place(x=0, y=0)

        self.frame = tkin.Frame(self.window,bg='#7DE5ED')
        self.frame.place(relx=.5, rely=.5, anchor="c")

        self.t_label = tkin.Label(self.frame, text="chaos based image encrypter and decrypter", font=('Supreme', 10, 'bold'), bg='#7DE5ED')
        self.t_label.grid(pady=(0,5))

        self.login_label = tkin.Label(self.frame, text="Login with shared key1", font=('Supreme', 10, 'bold'),bg='#7DE5ED')
        self.login_label.grid(pady=(5,8))

        self.login_entry = tkin.Entry(self.frame)
        self.login_entry.grid(pady=(0,5), sticky='enw')
        
        self.login_button = tkin.Button(self.frame, text="Login", font=('Supreme', 9),bg='#5DA7DB', command=lambda:self.start_intro(self.login_entry.get()))
        self.login_button.grid(pady=(5,5), ipadx=5, sticky='enw')

        self.gen_bt = tkin.Button(self.frame, text="generate new key pairs", font=('Supreme', 8),bg='#5DA7DB', command=self.new_key_gen)
        self.gen_bt.grid(pady=(5,0), sticky='enw')

        self.by_label = tkin.Label(self.frame, text="By, Ramalingam A", font=('Supreme', 10, 'bold'), bg='#7DE5ED')
        self.by_label.grid(pady=(5,5))

        self.reg_label = tkin.Label(self.frame, text="124003242", font=('Supreme', 10, 'bold'), bg='#7DE5ED')
        self.reg_label.grid(pady=(5,8))