from gettext import find
import glob
import os
import re
from typing import Dict
import lxml.etree as ET
import pandas as pd
import hashlib
from pathlib import Path
# md5_to_crack = '012638432aa13300e065933d868a8cf9'

item_ids = ['item-21', 'item-22', 'item-23', 'item-43', 'item-41']
# item_ids['item-23'] = 'Verhoudingen'

# Boekje 01 - item-23 - Getallen
# Boekje 02 - item-22 - Meetkunde
# Boekje 03 - item-43 - Verbanden
# Boekje 04 - item-23 - Verhoudingen
# Boekje 05 - item-23 - Getallen
# Boekje 06 - item-23 - Meetkunde
# Boekje 07 - item-21 - Verbanden
# Boekje 08 - item-21 - Verhoudingen
# Boekje 09 - item-21 - Getallen
# Boekje 10 - item-21 - Meetkunde
# Boekje 11 - item-21 - Verbanden
# Boekje 12 - item-41 - Verhoudingen
booklet = {}
booklet['Booklet01'] = 'Getallen'
booklet['Booklet02'] = 'Meetkunde'
booklet['Booklet03'] = 'Verbanden'
booklet['Booklet04'] = 'Verhoudingen'
booklet['Booklet05'] = 'Getallen'
booklet['Booklet06'] = 'Meetkunde'
booklet['Booklet07'] = 'Verbanden'
booklet['Booklet08'] = 'Verhoudingen'
booklet['Booklet09'] = 'Getallen'
booklet['Booklet10'] = 'Meetkunde'
booklet['Booklet11'] = 'Verbanden'
booklet['Booklet12'] = 'Verhoudingen'
# 'https://lutpr01twp.eu.premium.taocloud.org/#i61e8188ecaf3e1423052040aabcc9aa89',
# '#i61e8188ecaf3e1423052040aabcc9aa89',
# 'i61e8188ecaf3e1423052040aabcc9aa89',
# 'Verhoudingen'


input_folder_student_info = 'C://TMP//tao-state//results'
input_folder_results = 'C://TMP//tao-state//state-filtered'

logs = {}
sessions = []

for filename in glob.iglob(input_folder_student_info + '/*.csv', recursive=True):
    df = pd.read_csv(filename)
    rows = []
    for i, row in df.iterrows():
        rows.append(row)
    for row in rows:
        if not row['Test Taker ID'] == None:
            sessions.append(
                {'TestTakerId': row['Test Taker ID'], 'TestTaker': row['Test Taker'],'Group': row['Group'], 'Delivery': row['Delivery Execution Id']})
for filename in glob.iglob(input_folder_results + '/*', recursive=True):
    md5_state_file = os.path.basename(filename)
    if not '_' in md5_state_file:
        for item_id in item_ids:
            for session in sessions:
                user_id_full = str(session['TestTakerId'])
                session_id_full = str(session['Delivery'])
                group = str(session['Group'])
                item_identifier = booklet[group]
                test_taker = str(session['TestTaker'])
                # STRING TO HASH = '{USER_ID}{CALL_ID}'
                ## CALL_ID = '{SESSION_ID}{ITEM_IDENTIFIER}'

                # md5 with full url
                md5 = hashlib.md5(
                    f'{user_id_full}{session_id_full}{item_id}'.encode('utf-8')).hexdigest()
                if md5 == md5_state_file:
                    if os.path.exists(filename):
                        os.rename(filename, os.path.join(Path(filename).resolve().parent, f'{test_taker}_{item_identifier}_{md5}.json'))


# encoding GeeksforGeeks using md5 hash
# function

# student_ids = []
# for description in descriptions:

#     arr = about.split('#')
#     student_ids.append(arr[len(arr) -1])
