import cv2
import numpy as np
from pyzbar.pyzbar import decode
import qrgenerator 
import tkinter
from tkinter import *                                       # type: ignore
from PIL import ImageTk, Image
from tkinter import ttk

def windowqrgen():

    newwind = Toplevel(root)
    newwind.geometry("500x600")
        
    def save_text():
        text_file =  open("test.txt", "w")
        content = ""
        inputtxt.insert(END, content)
        text_file.write(inputtxt.get(1.0, END))
        text_file.close()

        text_file = open("test.txt", "r")
        content = text_file.read()
        text_file.close()

        content = content[:len(content)-1]

        qrgenerator.qrgen(content)
        if(content != ""):
            b = tkinter.Label(newwind, text= "Generated and saved as 'qr-img1.jpg'",
                                                pady=10, padx=10, font=10, fg = "green")                      # type: ignore
            b.pack()
            canvas = tkinter.Canvas(newwind, width = 500, height = 325)  
            canvas.pack()  
            img = ImageTk.PhotoImage(Image.open("qr-img1.jpg"))      # type: ignore
            canvas.create_image(100, 20, anchor = NW,image = img)


        elif(content == ""):
            b = tkinter.Label(newwind, text= "NO DATA TO GENERATE QR", 
                                            pady=10, padx=10, font=10, fg = "red")                          # type: ignore
            b.pack()
    
    inputtxt = Text(newwind, height=10, width=50)
    inputtxt.pack()
    
    
    qrendbtn = Button(newwind, text="Generate QR", command=save_text)
    qrendbtn.pack(ipadx = 5,ipady = 5, expand = True)
    
    newwind.mainloop()
    
def qrscan():
    def decoder(image):
        gray_img = cv2.cvtColor(image,0)  
        qrcode = decode(gray_img)
        for obj in qrcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 255, 0), 3)  
    
            global barcodeData
            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            string = "Data " + str(barcodeData)
            cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)  
            print("Barcode: "+barcodeData +" | Type: "+barcodeType)
 
    cap = cv2.VideoCapture(0)  
    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow('Image', frame)  
        code = cv2.waitKey(1)  

        if code == 27:
            break

        elif code == ord('q'):
            newwind2 = Toplevel(root)
            newwind2.geometry("500x100")
            def save_info():
                try:
                    
                    a = tkinter.Label(newwind2, text= "Saved !!!", 
                                        pady=10, padx=10, font=10, fg = "green")                    # type: ignore
                    a.pack()
                    text_file = open("test.txt", "w")
                    s = ""
                    savetxt.insert(END, s)
                    text_file.write(savetxt.get(1.0, END))
                    text_file.close()
                    with open("test.txt","r") as f1:
                        s = f1.read()
                    with open(s[:len(s)-1]+".txt","w") as f1:
                        f1.write(barcodeData)
                    
                    
                except NameError:
                    a = tkinter.Label(newwind2, text= "No QR code",
                                     pady=10, padx=10, font=10, fg = "red")                         # type: ignore
            savetxt = Text(newwind2, height=2, width=40)
            qrendbtn = ttk.Button(newwind2, text="Save file", command=save_info)

            savetxt.pack()
            qrendbtn.pack(ipadx = 5,ipady = 5, expand = True)
            newwind2.mainloop()
            break

root = Tk()
root.geometry("1000x750")	

root.configure(bg='light blue')
btn1 = ttk.Button(root, text = 'QR CODE SCANNER',command = qrscan)
btn2 = ttk.Button(root, text = 'QR CODE GENERATOR',command = windowqrgen)
Label(root, text = "Project QR Code \n",font = ("Bahnschrift",75,"bold") ,
                                        fg = "blue", bg = "light blue").pack()
Label(root, text = "By Priyatham Konda",font = ("Helvetica",25,"italic") ,
                                        fg = "blue", bg = "light blue").pack()
Label(root, text = "version 0.0.2",font = ("Helvetica",15) ,
                                        fg = "blue", bg = "light blue").pack()
btn1.pack(side = 'left',ipadx = 50,ipady = 50,expand = True)
btn2.pack(side = 'right',ipadx = 50,ipady = 50, expand = True)
root.mainloop()