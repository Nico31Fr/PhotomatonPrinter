#!/usr/bin/env python3
import io
import os
from PIL import Image, ImageOps

_IMAGE_CADRE1_L_: int = 2241
_IMAGE_CADRE1_H_: int = 1298
_IMAGE_CADRE4_L_: int = 1012
_IMAGE_CADRE4_H_: int = 733
_OFFSET_FF_: int = 19
_OFFSET4_FF_: int = 18
_RATIO4_: float = 1.38


def get_4_image_as_data_with_border(filename, deffilter, width=None, height=None):

    im1 = Image.open(filename[0])
    im2 = Image.open(filename[1])
    im3 = Image.open(filename[2])
    im4 = Image.open(filename[3])
    cadre = Image.open("./Graphics/cadre4.png")

    iwidth, iheight = im1.size
    # change ratio to 1.35 (reduce width)
    crop = int((iwidth - int(float(iheight)*_RATIO4_))/2)

    im1 = im1.crop((crop, 0, iwidth - crop, iheight))
    im2 = im2.crop((crop, 0, iwidth - crop, iheight))
    im3 = im3.crop((crop, 0, iwidth - crop, iheight))
    im4 = im4.crop((crop, 0, iwidth - crop, iheight))
    im1 = im1.resize((_IMAGE_CADRE4_L_, _IMAGE_CADRE4_H_))
    im2 = im2.resize((_IMAGE_CADRE4_L_, _IMAGE_CADRE4_H_))
    im3 = im3.resize((_IMAGE_CADRE4_L_, _IMAGE_CADRE4_H_))
    im4 = im4.resize((_IMAGE_CADRE4_L_, _IMAGE_CADRE4_H_))

    cadre.paste(im1, (_OFFSET4_FF_, _OFFSET4_FF_))
    cadre.paste(im2, (_OFFSET4_FF_+_IMAGE_CADRE4_L_+_OFFSET4_FF_, _OFFSET4_FF_))
    cadre.paste(im3, (_OFFSET4_FF_, _OFFSET4_FF_+_IMAGE_CADRE4_H_+_OFFSET4_FF_))
    cadre.paste(im4, (_OFFSET4_FF_+_IMAGE_CADRE4_L_+_OFFSET4_FF_, _OFFSET4_FF_+_IMAGE_CADRE4_H_+_OFFSET4_FF_))
    cadre = cadre.resize((width, height))

    if deffilter == 'nb':
        cadre = ImageOps.grayscale(cadre)

    im_bytes = io.BytesIO()
    cadre.save(im_bytes, format="PNG")

    im1.close()
    im2.close()
    im3.close()
    im4.close()
    cadre.close()

    return im_bytes.getvalue()


def get_image_as_data_with_border(filename, deffilter, width=None, height=None):

    im = Image.open(filename)
    im = im.resize((_IMAGE_CADRE1_L_, _IMAGE_CADRE1_H_))
    cadre = Image.open("./Graphics/cadre.png")
    cadre.paste(im, (_OFFSET_FF_, _OFFSET_FF_))
    cadre = cadre.resize((width, height))

    if deffilter == 'nb':
        cadre = ImageOps.grayscale(cadre)

    im_bytes = io.BytesIO()
    cadre.save(im_bytes, format="PNG")

    im.close()
    cadre.close()

    return im_bytes.getvalue()


def get_image_as_data(filename, width=None, height=None):
    im = Image.open(filename)
    if isinstance(width, int) and isinstance(height, int):  # Resize if dimensions provided
        im = im.resize((width, height))
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="PNG")
    im.close()
    return im_bytes.getvalue()


def get_image_files_list(folder, default_pic):
    all_files = os.listdir(folder)
    image_files = []
    for file in all_files:
        extension = file.lower().split(".")[-1]
        if extension in ["jpg", "png", "jpeg", "jpe"] and not file == default_pic:
            image_files.append(file)
    image_files.sort()
    return image_files
