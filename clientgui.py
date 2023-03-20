import socket
import tkinter as tkin
import time
def receiveFiles():
    c = socket.socket()
    r = ".jpg"
    m = 0
    condition = True
    print("server_ip: ",ip_entered.get(),"port_num: ",int(port_entered.get()))
    msg="\nserver_ip: "+ip_entered.get()+"\nport_num: "+port_entered.get()
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    c.connect((ip_entered.get(),int(port_entered.get())))
    labelop.config(text=("connection established with "+ip_entered.get()+"and receiving....."),font=('Supreme', 9))
    msg=''
    a=c.recv(1024)
    while condition:
        l = c.recv(1024)
        if l == b'next':
            m = m + 1
            name="client received images/client"+str(int.from_bytes(a,"big"))+" image"+str(m)
            i = open((name + r) , "wb")
            print("client"+str(int.from_bytes(a,"big"))+" image"+str(m) + " received")
            msg+="\nclient"+str(int.from_bytes(a,"big"))+" image"+str(m) + " received"
        if l !=b'next':
            i.write(l)
        if l == b'end':
            condition = False
    labelop.config(text="received all files.",font=('Supreme', 9))
    with open("analysis.txt",'a') as fl:
        fl.write(msg)
    c.close()

def decryptFiles():
    receiver.destroy()
    import gui as ma
    app = tkin.Tk()
    app.configure(bg='#7DE5ED')
    login_app = ma.loginpage(app)
    app.mainloop()

receiver=tkin.Tk()
receiver.title("Receiver IP input")
receiver.configure(bg='#7DE5ED')
receiver.minsize(400,200)
labelip=tkin.Label(receiver,text="Enter sender's ip address: ",bg='#7DE5ED',font=('Supreme', 9))
labelop=tkin.Label(receiver,text="",bg='#7DE5ED',font=('Supreme', 9))
labelport=tkin.Label(receiver,text="Enter the port number: ",bg='#7DE5ED',font=('Supreme', 9))
labeltxt=tkin.Label(receiver,text="To decrypt received files press Decrypt.",bg='#7DE5ED',font=('Supreme', 9))
ip_text=tkin.StringVar()
ip_entered=tkin.Entry(receiver,width=15,textvariable=ip_text)
port_text=tkin.StringVar()
port_entered=tkin.Entry(receiver,width=15,textvariable=port_text)
button_rec = tkin.Button(receiver, text = "Receive",bg='#5DA7DB', command = receiveFiles,font=('Supreme', 10))
button_dec = tkin.Button(receiver, text = "Decrypt",bg='#5DA7DB', command = decryptFiles,font=('Supreme', 10))
labelip.grid(column = 0, row = 0,sticky=tkin.W,pady=3)
labelop.grid(column = 0, row = 3,pady=3,sticky=tkin.W)
labelport.grid(column = 0, row = 1,pady=3,sticky=tkin.W)
labeltxt.grid(column = 0, row = 4,pady=3,sticky=tkin.W)
ip_entered.grid(column=1,row=0,pady=3,sticky=tkin.W)
port_entered.grid(column=1,row=1,pady=3,sticky=tkin.W)
button_rec.grid(column= 0, row = 2,pady=3,sticky=tkin.W)
button_dec.grid(column= 0, row = 5,pady=3,sticky=tkin.W)
receiver.mainloop()