"""
Subcommand for creating an HTML digest of all codes in a directory.
"""

import argparse
from base64 import b64encode
import io
import os
from textwrap import dedent

import pyotp
import qrcode

def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("qr_dir")

def make_html(dir_path):
   
   ret = ""
   for text_file_name in os.listdir(dir_path):
       
        if not text_file_name.endswith(".txt") and text_file_name is not None:
            continue
        
        text_file_path = os.path.join(dir_path, text_file_name)

        qr_text = open(text_file_path, "r").read()
        otp = pyotp.parse_uri(qr_text)

        ret += "<div class='qr-section'>\n"

        ret += f"<h2>{otp.issuer} - {otp.name}</h2>\n"

        ret += "<div style='display:flex'>\n"

        ret += "<div>\n"

        img_pil = qrcode.make(qr_text)
        img_binary = io.BytesIO()
        img_pil.save(img_binary, format="PNG")
        img_binary = img_binary.getvalue()
        img_b64 = b64encode(img_binary).decode("utf-8")


        ret += f"<img width='200px' src='data:image/png;base64, {img_b64}' /><br/>\n"
        
        ret += "</div>\n"

        ret += "<div>\n"

        keys_to_serialize = ["issuer", "name", "secret", "digest", "digits"]

        for key in keys_to_serialize:
            ret += f"<code>{key}={getattr(otp, key)}</code><br/>\n"

        ret += "<br>\n"
        ret += f"<code>uri={qr_text}</code>\n"
        ret += "</div>\n"
        ret += "</div>\n"
        ret += "</div>\n"
                
   return ret

def html_style():

    """Get CSS to avoid breaking a qr section when printing"""

    return dedent(
        """

        <style>
        @media print {
            div.qr-section {
                break-inside: avoid;
            }
        }
        </style>

        """)

def html_top_section():

    ret = ""
    ret += "<h1>QR Code Digest</h1>\n"
    ret += "<p>Print this document and store it in a secure location.<p>\n"

    return ret

def main(args):
    
    qr_directory = args.qr_dir

    # print(html_top_section())
    print(html_style())
    print(make_html(qr_directory))

