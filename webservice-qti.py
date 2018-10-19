from flask import Flask, request, make_response
from qti_model import *
from helper_functions import *
import xml.etree.ElementTree as ET
import zipfile
import io
import time
import os
import csv
import json
import pandas as pd

app = Flask(__name__)


def get_interaction_type(element_name):
    switcher = {
        'textEntryInteraction': interaction_type.TextEntry,
        'choiceInteraction': interaction_type.Choice
    }
    return switcher.get(element_name, interaction_type.NotDetermined)


@app.route("/uploadQtiPackage", methods=['GET', 'POST'])
def upload_packagefile():
    # get file from request
    f = request.files['file']
    if not f:
        return "No file"
    # copy file to working directory
    filename = 'working-directory/qti-package' + \
        time.strftime("%Y%m%d-%H%M%S") + '.zip'
    with open(filename, 'wb') as new_file:
        new_file.write(f.stream.read())
    package_folder = os.path.splitext(filename)[0]
    # unzip package
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(package_folder)
    zip_ref.close()

    # open manifest file
    manifest = ET.parse(package_folder + '/imsmanifest.xml').getroot()
    ns = {'d': 'http://www.imsglobal.org/xsd/imscp_v1p1'}
    # xpath to get all items in package
    items = []
    item_refs = manifest.findall(
        ".//d:resource[@type='imsqti_item_xmlv2p1']", ns)
    item_codes = [item_ref.attrib['href'] for item_ref in item_refs]
    # loop through all item references
    for item_ref in item_codes:
        # open item xml file
        item = ET.parse(package_folder + '/' + item_ref).getroot()
        item_ns = {'d': 'http://www.imsglobal.org/xsd/imsqti_v2p1'}
        # get item body
        item_body = item.find('.//d:itemBody', item_ns)
        interactions = []
        body = ''
        item_type = interaction_type.NotDetermined
        alternatives = []
        # loop through elements of item body to get body text and interaction info
        for elem in item_body.findall(".//*"):
            elem_name = elem.tag.replace(
                '{http://www.imsglobal.org/xsd/imsqti_v2p1}', '')
            if elem_name.endswith('Interaction'):
                interactions.append(elem)
                if item_type == '' or item_type == interaction_type.NotDetermined:
                    item_type = get_interaction_type(elem_name)
                    if item_type == interaction_type.Choice:
                        alternatives = [alternative(choice.attrib['identifier'], clean(' '.join([get_end_clean(
                            c_el) for c_el in choice.findall('.//*')]))) for choice in elem.findall('.//d:simpleChoice', item_ns)]
            else:
                if elem.text is not None and not is_child_of(interactions, elem):
                    body = body + ' ' + clean(elem.text)
        body = clean(body)
        res_e = [get_end_clean(cr_elem) for cr_elem in item.find(
            './/d:correctResponse', item_ns).findall('.//*')]
        correct_response = '#'.join(res_e)
        base_item = multiple_choice_item(item.attrib['identifier'], item_type, body, correct_response, alternatives) \
            if item_type == interaction_type.Choice \
            else item_base(item.attrib['identifier'], item_type, body, correct_response)
        items.append(base_item)
    choice_items = [itm for itm in items if type(itm) is multiple_choice_item]
    if len(choice_items) > 0:
        with open('muliple_choice_items.csv', mode='w', encoding="utf-8", newline='') as csv_file:
            # sort on max alternatives so we get the item with max columns
            sorted = choice_items[:]
            sorted.sort(reverse=True, key=alt_count)
            # get column headers from item with most alternatives
            fieldnames = sorted[0].to_dict().keys()
            writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames,  delimiter=';')
            writer.writeheader()
            for choice in choice_items:
                writer.writerow(choice.to_dict())
    itm_dict = [itm.to_dict() for itm in items]
    response = make_response(json.dumps(
        itm_dict, sort_keys=True, indent=4, separators=(',', ': ')))
    return response


def alt_count(itm):
    return len(itm.alternatives)


if __name__ == "__main__":
    app.run()
