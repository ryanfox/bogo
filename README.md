# BOGO - Basically Optimal Graphics Ontology

BOGO (Basically Optimal Graphics Ontology) is a lossless image compression format. BOGO derives its name from [bogosort.](https://en.wikipedia.org/wiki/Bogosort) Unlike traditional computationally-wasteful
image formats that let your underutilized CPU sit around idle, BOGO maximizes your computer's time spent doing what it loves: computing.

Contrary to rumor, BOGO does not stand for Blockchain-Oriented Graphics Orifice. Why would you use a blockchain to store an image? That would be silly.

A proof-of-concept encoder and decoder are included in this repository. See
[the official documentation for more information.](https://foxrow.com/bogo-an-image-compression-format)

Usage:

    # encoding
    $ python encode.py input.jpg output.bogo
    
    # decoding
    $ python decode.py input.bogo output.jpg

## BOGO image spec v0.0.1

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
RFC 2119.

BOGO files should use the file extension ".bogo".

BOGO files must adhere to the following format:

Byte #  | Content
--------|--------
0-3     | Magic number containing the ASCII for "BOGO" (Decimal `66` `79` `71` `79`)
4       | Width of the image in pixels. Trust me, you don't want an image larger than 256x256
5       | Height of the image in pixels
6       | Image mode. 0 corresponds to black and white, 1 to grayscale, and 2 to RGB
7-22    | Image checksum
23-N    | Image data

All numerical values must be unsigned integers in big-endian format.

### Image mode

BOGO supports 3 image modes: black and white, grayscale, and RGB.

For black and white images, each pixel value is stored as 1 or 0.

For grayscale images, each pixel is stored as 0-255, with 8 bits per pixel.

For RGB images, each pixel is stored as a 3-tuple of 0-255 values. Red must be the 0th value in the tuple, followed by green, followed by blue.

### Checksum

A BOGO header contains a checksum to verify that the image has been correctly reconstructed. To compute the checksum of a given image, concatenate each pixel value in raster order and compute the MD5 of the result. For multi-channel images, data shall be concatenated per-pixel rather than per-channel. That is, concatenate the RGB values of the 0th pixel, followed by the RGB values of the 1st pixel, etc.

### Image data
To compress image data, BOGO pixel values are stored using run-length encoding. To maximize compression, pixel values must be sorted before encoding. An encoded pixel is stored using two bytes for the count, followed by the pixel value. For simplicity, black and white pixel values are stored using a full byte, rather than a single bit.

For black/white and grayscale images, this gives encoded pixels a width of 3 bytes. For RGB images, 2 bytes for count plus 3 bytes for value gives an encoded pixel width of 5 bytes.


### Decoding
1. Reconstruct the list of pixel values by decompressing the run-length encoded image data.
2. Randomly shuffle the pixel values.
3. Compute the MD5 checksum.
4. If it matches the checksum stored in the file header, you are done. If not, go to step 2. 

The BOGO reference implementation is [available on Github.](https://github.com/ryanfox/bogo)