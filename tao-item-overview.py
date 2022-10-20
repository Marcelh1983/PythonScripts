from gettext import find
import glob
import os
import re
from typing import Dict
import lxml.etree as ET
import pandas as pd

input_folder = 'C://TMP//TAO_BOEKJES'
ns = {'d': 'http://www.imsglobal.org/xsd/imsqti_v2p2'}

rows = []

for filename in glob.iglob(input_folder + '/**/qti.xml', recursive=True):
    item_dom: ET.ElementBase = ET.parse(filename).getroot()
    title = item_dom.get('title')
    identifier = item_dom.get('identifier')
    # next(item for item in dicts if item["name"] == "Pam")
    matching = next((item for item in rows if item["title"] == title), None)
    # matching = next(filter(lambda item: item["title"] == title , rows))
    if matching == None:
        # row = { 'title': title, 'identifier', identifier, 'text': ''.join(item_dom.itertext()}
        text = re.sub('\s+', ' ', ''.join(item_dom.itertext()).rstrip("\n"))
        map_keys = item_dom.findall(".//d:*[@mapKey]", ns)
        keys = [*map(lambda map_key: map_key.get('mapKey'), map_keys)]
        key = '#'.join(keys)
        if key == '':
            correct_responses = item_dom.findall(".//d:correctResponse/d:value", ns)
            if len(correct_responses) > 0:
                values = [*map(lambda correct_response: correct_response.text.rstrip().replace(
                    'choice_', ''), correct_responses)]
                # test = ''.join(values)
                choices = ['', 'A', 'B', 'C', 'D']
                keys = []
                for value in values:
                    if value.isnumeric() and int(value) < len(choices):
                        keys.append(choices[int(value)])
                    else:
                        keys.append(value)
                # key = '#'.join(test)

        new_row = {'title': title, 'identifier': identifier,
                   'key': '#'.join(keys), 'text': text}
        rows.append(new_row)
column_names = ["title", "identifier", "key", "text"]
df = pd.DataFrame(rows)
df.to_excel(os.path.join(input_folder, 'items.xlsx'))
