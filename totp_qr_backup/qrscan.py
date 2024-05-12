import argparse
from hashlib import sha256
import os
from urllib.parse import parse_qs, unquote, urlparse

import cv2
from pyzbar.pyzbar import decode
import qrcode

def add_arguments(parser:argparse.ArgumentParser):
    parser.add_argument("out_dir")
    
def watch_for_qr_codes():

    vid = cv2.VideoCapture(0) 

    last_qr = None
    while(True):
        ret, frame = vid.read()
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

    parsed_url = urlparse(totp_str)
    data = parse_qs(parsed_url.query)
    issuer = data["issuer"][0]
    path = unquote(parsed_url.path).strip().strip("/").replace("/","_").replace(":","_")

    fname = f"{issuer} - {path} - {hash}"

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

        # Write the png
        img = qrcode.make(qr_text)
        full_img_file_path = os.path.join(out_dir, f"{file_name}.png")
        img.save(full_img_file_path)
