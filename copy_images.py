import glob
from math import nan
import shutil
import os
import pandas as pd
from PIL import Image
from find_shutterstock import *

def start():
    input_folder = 'C://Users//marcelh//Downloads//OneDrive_2022-02-10//afbeeldingen shutterstock'
    new_image_folder = os.path.join(input_folder, 'Bewerkt_Gereed')
    
    csv = os.path.join(input_folder, 'images_shutterstock.csv')
    df = pd.read_csv(csv, sep=';')
    rows = []
    for i, row in df.iterrows():
        rows.append(row)
    
    for row in rows:
        if not row['org_location']  == None and not row['org_location'] == '' and not row['shutterstock_filename']  == None and  isinstance(row['shutterstock_filename'], str):
            org =  os.path.join(input_folder, row['org_location'])
            new = os.path.join(new_image_folder, row['shutterstock_filename'])
            f = row['shutterstock_filename']
            if os.path.exists(new):
                im = Image.open(new)
                if not int(row['width']) == im.width:
                    org_width = row['width']
                    print(f'width not correct: {f} org: {org_width} new: {im.width}')
                if not int(row['height']) == im.height:
                    org_height = row['height']
                    print(f'height not correct: {f} org: {org_height} new: {im.height}')
                shutil.copyfile(new, org)
                hash = row['hash']
                copied_images = filter(lambda r: r['hash'] == hash and not r['org_location'] == row['org_location'], rows)
                for copied_image in copied_images:
                    other_org =  os.path.join(input_folder, copied_image['org_location'])
                    shutil.copyfile(new, other_org)
            else:
                print(f'file not found: {f}')
        else:
            shutterstock_image = not row['shutterstock_filename']  == None and  isinstance(row['shutterstock_filename'], str)
            file_name_available = not row['filename'] == '## already exists ##'
            if file_name_available and not shutterstock_image:
                print(f'missing shutterstock image: {f}')


start()
