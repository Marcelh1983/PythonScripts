from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import zipfile
import io
import time
import os
import re
import unicodedata
import json
import ntpath
import html


app = Flask(__name__)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def clean(s):
    if s is not None:
        s = html.unescape(s)
        s = replaceTabSpacesNewLineBySpaces(s)
        s = replaceNewLineBySpaces(s)
        s = removeWeirdSpaces(s)
        s = removeDoubleSpaces(s)
        s = removeDoubleSpaces(s)
        s = s.strip()
        return s
    return ''


def get_end_clean(elem):
    if elem is not None:
        elem_name = elem.tag.replace('{http://www.imsglobal.org/xsd/imsqti_v2p1}', '')
        if elem_name == 'img':
            return path_leaf(elem.attrib['src'])
        else:
            return clean(elem.text)


def removeDoubleSpaces(s):
    return re.sub(' +', ' ', s)


def replaceTabSpacesNewLineBySpaces(s):
    return re.sub(r'\s+', ' ', s)


def replaceNewLineBySpaces(s):
    return s.replace('\n', ' ').replace('\r', '')


def removeWeirdSpaces(s):
    s = unicodedata.normalize("NFKD", s)
    return s


def get_interaction_type(element_name):
    switcher = {
        'textEntryInteraction': "SA",
        'choiceInteraction': "MC"
    }
    return switcher.get(element_name, "INFO")


def is_child_of(parents, child):
    for parent in parents:
        for elem in parent.findall(".//*"):
            if elem == child:
                return True
    return False


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
        interactionType = ''
        alternatives = []
        # loop through elements of item body to get body text and interaction info
        for elem in item_body.findall(".//*"):
            elem_name = elem.tag.replace(
                '{http://www.imsglobal.org/xsd/imsqti_v2p1}', '')
            if elem_name.endswith('Interaction'):
                interactions.append(elem)
                if interactionType == '' or interactionType == 'Info':
                    interactionType = get_interaction_type(elem_name)
                    if interactionType == 'MC':
                        alternatives = [{
                            u'id': choice.attrib['identifier'],
                            u'text': clean(' '.join([get_end_clean(c_el) for c_el in choice.findall('.//*')]))
                        } for choice in elem.findall('.//d:simpleChoice', item_ns)]
            else:
                if elem.text is not None and not is_child_of(interactions, elem):
                    body = body + ' ' + clean(elem.text)
        body = clean(body)
        res_e = [get_end_clean(cr_elem) for cr_elem in item.find(
            './/d:correctResponse', item_ns).findall('.//*')]
        correct_response = '#'.join(res_e)
        items.append({
            'id': item.attrib['identifier'],
            'body': body,
            'interactionType': interactionType,
            'alternatives': alternatives,
            'correct_response': correct_response
        })
    # TODO : loop through items, remove xml-elements
    response = make_response(json.dumps(
        items, sort_keys=True, indent=4, separators=(',', ': ')))
    return response


if __name__ == "__main__":
    app.run()
