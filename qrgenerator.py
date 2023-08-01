import qrcode 
def qrgen(s):  
    qr_img = qrcode.make(s)
    qr_img.save("qr-img1.jpg")
