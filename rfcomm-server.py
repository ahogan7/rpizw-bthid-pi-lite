# -*- coding: utf-8 -*-
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

### Dependence ###############
# pip install pycrypto==2.6.1
##############################
import base64
import hashlib

from bluetooth import *
from Crypto import Random
from Crypto.Cipher import AES

import time
import string
import random

import qrcode
import os

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation


def password_generator(length=64):
    '''
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    '''
    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    if random_password == '': return None
    return random_password


class AESCipher:
    bs = AES.block_size

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(message)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

# characters

NUC = chr(0)
SHF = chr(32)+NUC
RET = chr(40)
REG = NUC*2
DN = NUC*5
FRE = NUC*8
map = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
regular = ["", "", "", "", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
                       "2", "3", "4", "5", "6", "7", "8", "9", "0", "ENTER", "ESCAPE", "\b", "\t", " ", "-", "=", "[", "]", "\\", "", ";", "'", "`", ",", ".", "/",
                       "CAPSLOCK", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "printscreen", "Scroll Lock", "Pause",
                       "Insert", "Home", "PageUp", "Delete", "End", "PageDown", "RightArrow", "LeftArrow", "DownArrow", "UpArrow",
                       "Num Lock ", "/1", "*", "-", "+", "ENTER", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ""]
shifted = ["", "", "", "", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                      "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "", "", "", "", "", "_", "+", "{", "}", "|", "", ":", "\"", "~", "<", ">", "?", "", "", "", "", "", "", "",
                      "", "", "", "", "", "", "insert", "", "", "", "", "", "Forward", "", "", "", "", "", "", "Clear", "", "", "", "", "", "End", "Down Arrow", "PageDn",
                      "Left Arrow", "", "Rigth Arrow", "Home", "Up Arrow", "PageUp", "Insert", "Delete", ""]
num = """0123456789"""
alphlor = """abcdefghijklmnopqrstuvwxyz"""
alphupr = """ABCDEFGHIJKLMNOPQRSTUVWXYZ"""
punc = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
space = " "
format = """\n\r\x0b\x0c"""

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def mpwd(mpwd):
    try:
        if len(mpwd) <= 0:
            print("Not enough information")
            return
        hasNum = False
        hasAlphlor = False
        hasAlphupr = False
        hasPunc = False
        hasSpace = False
        hasFormat = False
        hasOther = False
        contains = "["
        if len(mpwd) < 21:
            print("Consider increasing password length above 20 if possible.")
        for c in mpwd:
            if c in num:
                hasNum = True
            elif c in alphlor:
                hasAlphlor = True
            elif c in alphupr:
                hasAlphupr = True
            elif c in punc:
                hasPunc = True
            elif c in space:
                hasSpace = True
            elif c in format:
                hasFormat = True
            else:
                hasOther = True

        if hasNum:
            contains = contains + "0-9"
        if hasAlphlor:
            contains = contains + "a-z"
        if hasAlphupr:
            contains = contains + "A-Z"
        if hasPunc:
            contains = contains + ":punc:"
        if hasSpace:
            contains = contains + "\s"
        if hasFormat:
            contains = contains + "\\ntr"
            print("WARNING has non-printable ascii.")
        if hasOther:
            contains = contains + ":utf8:"
            print("WARNING has uncicode..")
        print("Pwd has some "+repr(contains+"]"))
        print("Potential is "+repr("[0-9a-zA-Z:punc:\\s\\ntr] and possibly UTF-8"))
        for c in mpwd:
            try:
               dex = regular.index(c)
               code = REG + chr(dex) + DN
            except:
               dex = -1
            if dex < 0:
                try:
                    dex = shifted.index(c)
                    code = SHF + chr(dex) + DN
                except:
                    dex = -1
            if dex > 0:
                write_report(code)
                write_report(FRE)
            else:
                print("Unknown character!")
            time.sleep(0.1)
        #write_report(REG + RET + DN)
        #write_report(FRE)
    except EOFError:
        print("Done...")
    except Exception as e:
        print(e)
        logging.error(traceback.format_exc())
        return



if __name__ == '__main__':
    fn = "key.txt"
    key = None
    if os.path.isfile(fn):
        with open(fn,"r") as f:
            key = f.readline().rstrip()
            f.close()
    else:
        with open(fn,"w") as f:
            key = password_generator()
            f.write(key)
            f.write("\n")
            f.close()

    assert key != None

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(key)
    qr.make(fit=True)

    qr.print_ascii()

    img = qr.make_image(fill_color="black", back_color="white")

    img.save('key.png')

    aes_cipher = AESCipher(key)

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            ciph_str=data.decode("utf-8")
            print("ciph: " + ciph_str)
            pt_str=aes_cipher.decrypt(ciph_str)
            print("pt: " + pt_str)
            mpwd(pt_str)
    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")
