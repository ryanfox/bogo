import hashlib
import sys
from collections import Counter

from PIL import Image


MODES = {'1': 0, 'L': 1, 'RGB': 2}


def rle_encode(pixel_counts):
    array = bytearray()

    for pixel_value, count in sorted(pixel_counts.items()):
        array.extend(count.to_bytes(2, 'big'))
        for channel in pixel_value:
            array.extend(channel.to_bytes(1, 'big'))

    return array


in_filename = sys.argv[1]
img = Image.open(in_filename)

img.thumbnail((256, 256))
width, height = img.size

pixels = []
for row in range(height):
    for col in range(width):
        pixels.append(img.getpixel((col, row)))

counter = Counter(pixels)
rle_encoded_data = rle_encode(counter)

md5 = hashlib.md5()
for pixel in pixels:
    for channel in pixel:
        md5.update(channel.to_bytes(1, 'big'))
checksum = md5.digest()

out_filename = sys.argv[2]
with open(out_filename, 'wb') as f:
    f.write(b'BOGO')
    f.write(width.to_bytes(1, 'big'))
    f.write(height.to_bytes(1, 'big'))
    f.write(MODES[img.mode].to_bytes(1, 'big'))
    f.write(checksum)
    f.write(rle_encoded_data)
