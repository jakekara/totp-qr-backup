import argparse
from totp_qr_backup import qrscan
from totp_qr_backup import qrdigest

def main():

    parser = argparse.ArgumentParser(
                    prog='qr-backup',
                    description='Backup TOTP QR codes')
    
    subparsers = parser.add_subparsers()

    scan_parser = subparsers.add_parser("scan")
    scan_parser.set_defaults(func=qrscan.main)
    qrscan.add_arguments(scan_parser)

    digest_parser = subparsers.add_parser("digest")
    digest_parser.set_defaults(func=qrdigest.main)
    qrdigest.add_arguments(digest_parser)
    
    args = parser.parse_args()
    args.func(args)