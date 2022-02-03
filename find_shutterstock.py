import json
import os
from typing import Dict
import urllib.request
from playwright.sync_api import Browser
def find_shutterstock_id(image_name: str):
    image_name = get_file_name(image_name)
    for image_part in image_name.split('-'):
        possible_int = (int(image_part) if image_part.isdigit() else None)
        if not possible_int == None and len(str(possible_int)) > 4:
            if (possible_int > 0):
                return possible_int
    for image_part in image_name.split('_'):
        possible_int = (int(image_part) if image_part.isdigit() else None)
        if not possible_int == None and len(str(possible_int)) > 4:
            if (possible_int > 0):
                return possible_int
    return None


def get_shutterstock_image_by_image(image_location: str, output_dir: str, browser: Browser = None):
    page = browser.new_page()
    page.goto("https://www.shutterstock.com/")
    listbox = page.locator(
        "[aria-haspopup=\"listbox\"][aria-label=\"Image\"]")
    listbox.click()
    listbox_item = page.locator("[data-value=\"reverseImageSearch\"]")
    listbox_item.click()
    file_input = page.locator("input[type=\"file\"]")
    file_input.set_input_files(image_location)
    imageLink = page.locator("a[data-track-label=\"gridItem\"]").first
    image_info = imageLink.get_attribute('data-track-value')
    id = json.loads(image_info)['id']
    src = imageLink.locator('img').first.get_attribute('src')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    file_location = os.path.join(output_dir, os.path.basename(src))
    urllib.request.urlretrieve(src, file_location)
    page.close()
    return ImageInfo(id, file_location)


def get_shutterstock_image_by_id(id: str, output_dir: str, browser: Browser = None):
    page = browser.new_page()
    page.goto("https://www.shutterstock.com/")
    search_input = page.locator("input[type=\"search\"]")
    search_input.fill(str(id))
    search_button = page.locator("button[aria-label=\"Search\"]")
    search_button.click()
    div_a_wrapper = page.locator(
        "div[data-automation=\"AssetGrids_MosaicAssetGrid_div\"]").first
    src = div_a_wrapper.locator('img').first.get_attribute('src')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    file_location = os.path.join(output_dir, os.path.basename(src))
    urllib.request.urlretrieve(src, file_location)
    page.close()
    return ImageInfo(id, file_location)


def get_file_name(path):
    if not os.path.isdir(path):
        return os.path.splitext(os.path.basename(path))[0].split(".")[0]


def get_file_extension(path):
    extensions = []
    copy_path = path
    while True:
        copy_path, result = os.path.splitext(copy_path)
        if result != '':
            extensions.append(result)
        else:
            break
    extensions.reverse()
    return "".join(extensions)


class ImageInfo:
    def __init__(self, image_id: str, location: str):
        self.id = image_id
        self.location = location

    id = ''
    location = ''


# get_shutterstock_image_by_image('C:\\TMP\\diggel_shutterstock\\shutterstock_1257452734.png', 'C:\\TMP\\diggel_shutterstock\\output')
