import glob
import shutil
import os
import pandas as pd
from PIL import Image
import hashlib
import requests
from find_shutterstock import *
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser


def get_unique_file(filename: str, output_folder, seq=0):
    filename = os.path.basename(filename)
    new_filename = filename
    if (not seq == 0):
        new_filename = get_file_name(new_filename) + "_" + \
            str(seq) + get_file_extension(new_filename)
    dst = os.path.join(output_folder, new_filename)
    if (os.path.isfile(dst)):
        print('already exists')
        return get_unique_file(filename, output_folder, seq + 1)
    else:
        return dst


def get_hash(filename: str):
    m = hashlib.md5()
    data = open(filename, 'rb').read()
    m.update(data)
    return m.hexdigest()


def get_item(collection, key, target):
    return next((item for item in collection if item[key] == target), None)


def handle_image(filename: str, images: list, output_folder: str, hashes: list):
    dst = get_unique_file(os.path.basename(filename), output_folder)
    hash = get_hash(filename)
    if (not hash in hashes):
        mapped = get_item(images, "hash", hash)
        name = os.path.basename(dst)
        shutterstock_id = 0
        shutterstock_image_guess = False
        shutterstock_info: ImageInfo = None
        def Round(x, n): return eval('"%.'+str(int(n))+'f" % ' +
                                     repr(int(x)+round(float('.'+str(float(x)).split('.')[1]), n)))
        if (not mapped is None):
            name = "## already exists ##"
            shutil.copyfile(filename, dst)
        else:
            shutil.copyfile(filename, dst)
            shutterstock_id = find_shutterstock_id(filename)
        im = Image.open(filename)
        im_shutterstock: Image = None
        aspect_shutterstock = ''
        if not im_shutterstock == None:
            im_shutterstock = Image.open(shutterstock_info.location)
            aspect_shutterstock = Round(
                im_shutterstock.width / im_shutterstock.height, 4)
        file = {
            "org_location": filename,
            "filename": name,
            "width": im.width,
            "height": im.height,
            "aspect": Round(im.width / im.height, 4),
            "hash": hash,
            "shutterstock_image_guess": shutterstock_image_guess,
            "shutterstock_id": shutterstock_id,
            "shutterstock_aspect":  aspect_shutterstock
        }
        return file
    else:
        return None


def get_images_hashes_folder():
    other_folder = 'c://tmp//diggel_shutterstock_old'
    hashes = []
    for filename in glob.iglob(other_folder + '/**/*.png', recursive=True):
        hash = get_hash(filename)
        hashes.append(hash)
    for filename in glob.iglob(other_folder + '/**/*.jpg', recursive=True):
        hash = get_hash(filename)
        hashes.append(hash)
    return hashes


def start():
    # from api.convert import convert_from_file
    ext = ['png', 'jpg', 'gif']    # Add image formats here
    output_folder = 'c://tmp//diggel_shutterstock_final'
    input_folder = 'c://repos//diggel2//frontend//apps'
    hashes = get_images_hashes_folder()
    if (os.path.isdir(output_folder)):
        shutil.rmtree(output_folder)
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
        images = []
    for filename in glob.iglob(input_folder + '/**/*.png', recursive=True):
        file = handle_image(filename, images, output_folder, hashes)
        if (not file == None):
            images.append(file)
    for filename in glob.iglob(input_folder + '/**/*.jpg', recursive=True):
        file = handle_image(filename, images, output_folder,  hashes)
        if (not file == None):
            images.append(file)
    df = pd.DataFrame(images)
    df.to_csv(os.path.join(output_folder, 'images.csv'), ";")
    print('done')


start()
