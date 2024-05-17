# totp-qr-backup

Python CLI script to scan and printer-friendly backups of your TOTP QR codes to print out and store somewhere safe.

## Quick start

```shell
# Install
pip install git+https://github.com/jakekara/totp-qr-backup

# Start the webcam QR code scanner (press Q to quit when you're done)
# This examples tores in a directory called `out`
qr-backup scan out

# Create an HTML digest and store it in digest.html
qr-backup digest out > digest.html

# Now you can open digest.html in a browser and print it out.
```

## Sample output

You can see the digest created in the quickstart example [here](https://htmlpreview.github.io/?https://github.com/jakekara/totp-qr-backup/blob/main/demo/digest.html), and the source is in the[demo/digest.html](demo/digest.html) file.

The input QR codes came from [this gist](https://gist.github.com/kcramer/c6148fb906e116d84e4bde7b2ab56992) 

## Project status

This is pretty much good enough for my own usage, but I don't think I'll do much in the way of supporting this unless people end up using it, in which case I'll be glad to make some improvements.

The code could be a lot better organized, but meh. I was learning all of this as I went: How to scan QR codes, how to use the web cam from Python, how to generate QR codes, how to parse TOTP URIs.

## Why?

Losing all my two-factor codes, like, by losing my phone, would suck. Paper is a good way to keep backups of important information.