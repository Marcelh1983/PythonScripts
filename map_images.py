import glob
import os
import shutil
from playwright.sync_api import sync_playwright, Browser
import pandas as pd
from PIL import Image
from find_shutterstock import *
from get_images import get_hash


def start():
    ext = ['png', 'jpg', 'gif']    # Add image formats here
    input_folder = 'c://tmp//diggel_shutterstock'
    csv = os.path.join(input_folder, 'images.csv')
    shutterstock_dir_compare = os.path.join(input_folder, 'shutter_compare')
    if not os.path.isdir(shutterstock_dir_compare):
        os.mkdir(shutterstock_dir_compare)
    df = pd.read_csv(csv, sep=';')
    files = []
    hashes = []
    rows = []
    for filename in glob.iglob(input_folder + '/**/*.png', recursive=True):
        files.append(os.path.basename(filename))
    for filename in glob.iglob(input_folder + '/**/*.jpg', recursive=True):
        files.append(os.path.basename(filename))
    for i, row in df.iterrows():
        file_name = row['filename']
        if (file_name in files):
            hashes.append(row['hash'])
            rows.append(row)
    # now check for double images
    double_items = []
    for i, row in df.iterrows():
        org_location = row['org_location']
        hash = row['hash']
        for new_row in rows:
            if new_row['hash']== hash and not org_location ==  new_row['org_location']:
                double_items.append(row)

    # find correspondin item
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        for row in rows:
            filename = row['filename']
            filepath = os.path.join(input_folder, filename)
            shutterstock_id = find_shutterstock_id(filename)
            shutterstock_dir = os.path.join(input_folder, 'shutterstock_org')
            shutterstock_info: ImageInfo = None
            if not os.path.isdir(shutterstock_dir):
                os.mkdir(shutterstock_dir)
            if not shutterstock_id == None:
                # Get image by id
                shutterstock_info = get_shutterstock_image_by_id(
                    shutterstock_id, shutterstock_dir, browser)
            if shutterstock_info == None:
                shutterstock_image_guess = True
                shutterstock_info = get_shutterstock_image_by_image(
                    filepath, shutterstock_dir, browser)
                # Copy downloaded image to dir to compare. add org name so sort both folder and compare the images.
                filename_to_compare = get_file_name(filename) + '___' + os.path.basename(shutterstock_info.location)
                shutil.copyfile(shutterstock_info.location, os.path.join(shutterstock_dir_compare, filename_to_compare))
            if not shutterstock_info == None:
                row.shutterstock_id = shutterstock_info.id
                im_shutterstock = Image.open(shutterstock_info.location)
                a = im_shutterstock.width / im_shutterstock.height
                aspect_shutterstock = f"{a:.2f}"
                a = int(row.width) / int(row.height)
                aspect = f"{a:.2f}"
                row.hash = get_hash(shutterstock_info.location)
                row.aspect = aspect
                row.shutterstock_aspect = aspect_shutterstock
        browser.close()
    for double_item in double_items:
        rows.append(double_item)

    new_df = pd.DataFrame(rows)
    new_df.to_csv(os.path.join(input_folder, 'images_shutterstock.csv'), ";")

# start()