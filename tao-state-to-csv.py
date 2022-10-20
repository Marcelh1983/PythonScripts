import json
import glob
import os
import pandas as pd
import shutil



input_folder_results = 'C://TMP//tao-state//state-filtered'
output_folder = 'C://TMP//tao-state//'

logs = {}
sessions = []

# max_sessions = 20

# getallen_index = 0
# meetkunde_index = 0

rows = dict()
# rows_meetkunde = []

# ts_getallen = []
# ts_meetkunde = []
for filename in glob.iglob(input_folder_results + '/*', recursive=True):
    name = os.path.basename(filename)
    if '_' in name:
        with open(filename) as f:
            # try:
            lines = f.read()
            splitted_name = name.split('_')
            student = splitted_name[0]
            item_id = splitted_name[1]
            full_doc = json.loads(lines)
            state = json.loads(full_doc['RESPONSE'])
            attempt = state['state']
            log = state['log']
            for log_row in log:
                if not item_id in rows:
                    rows[item_id] = []
                rows[item_id].append({'candidate_id': student,  'item': 'Verhoudingen',
                                    'type': log_row['type'], 'payload': log_row['payload']})
                # if 'vlakken' in lines:
                #     # shutil.copyfile(filename, os.path.join('C://TMP//tao-state//state-filtered', name))
                #     getallen_index += 1
                #     full_doc = json.loads(lines)
                #     state = json.loads(full_doc['RESPONSE'])
                #     attempt = state['state']
                #     log = state['log']
                #     if getallen_index <= max_sessions:
                #         ts_getallen.append(json.dumps(log))
                #     for log_row in log:
                #         rows_getallen.append({'candidate_id': name,  'item': 'Verhoudingen',
                #                             'type': log_row['type'], 'payload': log_row['payload']})

                # if 'cubes' in lines:
                #     # shutil.copyfile(filename, os.path.join('C://TMP//tao-state//state-filtered', name))
                #     full_doc = json.loads(lines)
                #     meetkunde_index += 1
                #     state = json.loads(full_doc['RESPONSE'])
                #     attempt = state['state']
                #     log = state['log']
                #     if getallen_index <= max_sessions:
                #         ts_meetkunde.append(json.dumps(log))
                #     for log_row in log:
                #         rows_meetkunde.append({'candidate_id': name,  'item': 'Meetkunde',
                #                             'type': log_row['type'], 'payload': log_row['payload']}) 
                # if 'attempts'  in lines and 'state' in lines:
                #     shutil.copyfile(filename, os.path.join('C://TMP//tao-state//state-filtered', name))                             
            # except :
            #     print("An exception occurred")
for item_id in rows.keys():
    df_getallen = pd.DataFrame(rows[item_id])
    df_getallen.to_csv(os.path.join(output_folder, f'Log-{item_id}.csv'), ";")
# df_meetkunde = pd.DataFrame(rows_meetkunde)
# df_meetkunde.to_csv(os.path.join(output_folder, 'log-meetkunde.csv'), ";")

# file_ts_getallen = open(os.path.join(output_folder, 'log-getallen.ts'), "w")
# file_ts_getallen.write(f'{",".join(ts_getallen)}')
# file_ts_getallen.close()

# file_ts_meetkunde = open(os.path.join(output_folder, 'log-meetkunde.ts'), "w")
# file_ts_meetkunde.write(f'{",".join(ts_meetkunde)}')
# file_ts_meetkunde.close()