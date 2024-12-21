import pyotp
import qrcode
from PIL import Image
import time
import os
import base64


def authy(key):
    #Authenticator section
    totp = pyotp.TOTP(key)
    while True:     
        verify = totp.verify(input("Enter your code from your Google Authenticator App: "))
        if verify:
            print("Access granted.")
            break
        else:
            print("Wrong code. Try again.")

def authy_creator(key):
    ID = input('''
Signing up...
What is your name?: ''')
            
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=ID, issuer_name="Personal Passwords")
    qrcode.make(uri).save("totp.png")
    print("Please scan the QR Code with Google Authenthicator")
    time.sleep(2)
    qr = Image.open('totp.png')
    qr.show()





