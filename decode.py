import hashlib
import sys

import numpy as np
import random

from PIL import Image

MODES = {0: '1', 1: 'L', 2: 'RGB'}
CHANNELS = {'1': 1, 'L': 1, 'RGB': 3}


def decode(f, mode, filesize):
    decoded = []

    while f.tell() < filesize:
        if mode in ('1', 'L'):  # 2 byte count followed by 1 byte values
            pixel = f.read(3)

        else:  # 2 byte count followed by 3 byte values
            pixel = f.read(5)

        count = pixel[:2]
        value = pixel[2:]
        decoded.append((count, value))

    return decoded


in_filename = sys.argv[1]

with open(in_filename, 'rb') as f:
    f.seek(0, 2)
    filesize = f.tell()
    f.seek(0)

    magic_number = f.read(4)
    assert magic_number == b'BOGO'

    width = int.from_bytes(f.read(1), 'big')
    height = int.from_bytes(f.read(1), 'big')
    mode = MODES[int.from_bytes(f.read(1), 'big')]
    checksum = f.read(16)

    counts = decode(f, mode, filesize)

pixel_values = []
for count, value in counts:
    pixel_values.extend([value] * int.from_bytes(count, 'big'))

while True:
    random.shuffle(pixel_values)

    md5 = hashlib.md5()
    md5.update(b''.join(pixel_values))

    if checksum == md5.digest():
        break

# now we have the correct pixel value ordering, need to convert bytes to actual brightnesses
pixels = []

if mode in ('1', 'L'):
    for pixel in pixel_values:
        pixels.append(int.from_bytes(pixel, 'big'))

else:
    for pixel in pixel_values:
        rgb = (pixel[0], pixel[1], pixel[2])
        pixels.append(rgb)

ndarray = np.asarray(pixels).astype(np.uint8)
ndarray = ndarray.reshape((height, width, CHANNELS[mode]))

img = Image.fromarray(ndarray, mode=mode)
img.save(sys.argv[2])
