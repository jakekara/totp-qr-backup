"""
Subcommand to scan QR codes by camera and write them to a directory
"""

import argparse
from hashlib import sha256
import os

import cv2
import pyotp
from pyzbar.pyzbar import decode

def add_arguments(parser:argparse.ArgumentParser):
    parser.add_argument("out_dir")
    
def watch_for_qr_codes():

    vid = cv2.VideoCapture(0) 

    last_qr = None
    while(True):
        _, frame = vid.read()
        cv2.imshow('frame', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

        try:
            decoded_qr = decode(frame)
            qr_text = decoded_qr[0].data.decode('ascii')
        except:
            continue

        if qr_text == last_qr:
            continue
        
        last_qr = qr_text
        yield qr_text
        
def get_filename_from_totp(totp_str: str):
    
    hash = sha256(totp_str.encode("utf-8")).hexdigest()[:8]

    otp = pyotp.parse_uri(totp_str)

    fname = f"{otp.issuer} - {otp.name} - {hash}"

    return fname

def main(args):
    
    out_dir = args.out_dir

    # Create the output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    for qr_text in watch_for_qr_codes():
        file_name = get_filename_from_totp(qr_text)

        # Write the text file
        full_file_path = os.path.join(out_dir, f"{file_name}.txt")
        with open(full_file_path, "w") as fh:
            fh.write(qr_text)
        
        print(f"* Wrote QR code to {full_file_path}")

