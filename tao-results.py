"""
  Read csv file, remove columsn
"""
import glob
import math
import re
from typing import Dict
import numpy as np
import pandas as pd

# 1.1 choice_2
# 1.2 choice_17
# 1.3 - choice_1
# 1.4 -choice_1
# 2.1 = [choice_2 choice_5; choice_2 choice_6; choice_2 choice_7; choice_3 choice_8; choice_2 choice_9; choice_2 choice_10; choice_3 choice_11; choice_3 choice_12; choice_2 choice_13]
# 2.2 = [choice_2 choice_5; choice_1 choice_6; choice_1 choice_7; choice_1 choice_8; choice_1 choice_9; choice_1 choice_10; choice_2 choice_11; choice_4 choice_12; choice_1 choice_13]
# 2.3 = choice_2
# 2.4 = [choice_2 choice_5; choice_2 choice_6; choice_2 choice_7; choice_2 choice_8; choice_1 choice_9; choice_4 choice_10; choice_3 choice_11; choice_2 choice_12]
# 2.5 = [choice_2 choice_5; choice_3 choice_6; choice_2 choice_7; choice_2 choice_8; choice_4 choice_9; choice_2 choice_10; choice_3 choice_11; choice_3 choice_12; choice_2 choice_13]
# 2.6 = [choice_2 choice_5; choice_1 choice_6; choice_1 choice_7; choice_1 choice_8; choice_1 choice_9; choice_1 choice_10]

def add_value(col_name: str, value: str, df: pd.DataFrame):
    if col_name not in df:
      df[col_name] = ''  
    df.iloc[index, list(pd_total.columns).index(col_name)] = value

pd_total: pd.DataFrame = None
for filename in glob.iglob('c://TMP//tao/*.csv', recursive=True):
    data = pd.read_csv(filename, sep=',')

    # columns = ['GroupName','StartCode','Status', 'ModuleId']
    
    columns = ['Test Taker','Item1.1-RESPONSE', 'Item1.2-RESPONSE', 'Item1.2-RESPONSE_1', 'Item1.3-RESPONSE',
               'Item1.4-RESPONSE', 'Item2.1-RESPONSE', 'Item2.1-RESPONSE_1', 'Item2.2-RESPONSE', 'Item2.3-RESPONSE',
               'Item2.4-RESPONSE', 'Item2.5-RESPONSE', 'Item2.6-RESPONSE']
    items = dict()
    items['Item1.1-RESPONSE'] = {'label': 'omschrijf jezelf',
                                 'responses': [{'choice_1': 'jongen'}, {'choice_2': 'meisje'}, {'choice_3', 'anders'}]}

    columns_to_delete = []
    for column_name, j in data.head(1).iteritems():
        if not column_name in columns: #and (not '-RESPONSE' in column_name or 'correct' in column_name):
            columns_to_delete.append(column_name)
            # data..pop(column_name)
    data = data.drop(columns_to_delete, axis=1)
    if data.columns.size > 1:
      if pd_total is None:
        pd_total = data
      else:
        pd_total = pd.concat([pd_total, data])
pd_org = pd_total.copy(True)
# cols_to_add = ['Item1.1-RESPONSE-geslacht', 'Item1.2-RESPONSE-maand', 'Item1.2-RESPONSE-jaar',
# 'Item1.3-RESPONSE-nederlands-praten-thuis', 'Item1.4-RESPONSE-boeken', 'Item2.3-RESPONSE-zelfstandig', 'leuk_leren_rekenen', 'willen_geen_rekenen_leren', 'rekenen_is_saai',
#               'leer_interessant_rekenen', 'rekenen_leuk', 'school_taken_getallen_leuk',
#               'leuk_rekensommen_oplossen', 'verheug_rekenles', 'rekenen_favoriet',
#               'ik_weet_moet_doen_van_meester_juf', 'begrijp_meester_juf',
#               'meester_juf_duidelijk_antwoord_mijn_vraag', 'meester_juf_goed_uitleggen',
#               'meester_juf_helper', 'meester_juf_nog_een_keer_uitleggen', 'meester_juf_commentaar',
#               'meester_juf_vraagt_laten_zien_geleerd', 'meester_juf_vraagt_mij_antwoorden_uitleggen',
#               'meestal_goed_in_rekenen', 'moeilijker_dan_klasgenoot', 'ik_ben_gewoon_niet_goed', 'makkelijk_voor_mij',
#               'goed_in_oplossen_moeilijke_sommen', 'goed_uitleggen', 'moeilijker_andere_vakken', 'moeilijk_te_snappen',
#               'goed_mijn_best', 'niet_veranderen', 'hard_gewerkt', 'niet_slim_kan_goed_worden',
#               'niet_veranderen_slim_rekenen', 'goed_door_opletten', 'goed_geboren', 'iedereen_kan_rekenen',
#               'zelf_veranderen_rekenen',
#               'leerling_luisteren', 'te_onrustig', 'lang_wachten_stil', 'onderbreken_juf_meester',
#               'niet_aan_regels_houden', 'moeilijk_concentreren_door_andere'
# ]
# for col_to_add in cols_to_add:
#   pd_total[col_to_add] = ''
pd_total = pd_total.fillna('')
pd_total.replace('nan', '', inplace=True)
columns_to_delete = []
for name, values in pd_total.iteritems():
    for index, value in enumerate(values):
        new_value = ''
        if not pd_total.iloc[index][name] == value:
          print('wrong!')
        v = -1
        num_value:int = None
        try:
          num_value = int(''.join(filter(str.isdigit, str(value))))
        except:
          print('error')
          # ignore
        if not num_value is None:
          v = int(num_value)
        if (name == 'Item1.1-RESPONSE' and not v == -1):
          new_value = ['meisje', 'jongen', 'anders'][v-1]
          add_value('Item1.1-RESPONSE-geslacht', new_value, pd_total)
        if (name == 'Item1.2-RESPONSE' and not v == -1):
          new_value = ['Januari', 'Februari','Maart', 'April', 'Mei', 'Juni', 'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December'][v-1]
          add_value('Item1.2-RESPONSE-maand', new_value, pd_total)
        if (name == 'Item1.2-RESPONSE_1' and not v == -1):
          new_value = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', 'anders'][v-13]
          add_value('Item1.2-RESPONSE-jaar', new_value, pd_total)
        if (name == 'Item1.3-RESPONSE' and not v == -1):
          new_value = ['altijd', 'bijna_altijd', 'soms', 'nooit' ][v-1]
          add_value('Item1.3-RESPONSE-nederlands-praten-thuis', new_value, pd_total)
        if (name == 'Item1.4-RESPONSE' and not v == -1):
          new_value = ['0-tot-10', '11-tot-25', '26-tot-100', '101-tot-200', '200-plus' ][v-1]
          add_value('Item1.4-RESPONSE-boeken', new_value, pd_total)
        if (name == 'Item2.3-RESPONSE' and not v == -1):
          new_value = ['elk_bijna_elke_les', 'helft_lessen', 'sommige_lessen', 'nooit' ][v-1]
          add_value('Item2.3-RESPONSE-zelfstandig', new_value, pd_total)
          columns_to_delete.append(name)
        if '[choice' in str(value) and ';' in str(value):
          splitted = value.replace('[', '').strip().replace(']', '').split(';')
          for split_col in splitted:
            [answer, question] = split_col.strip().split(' ')
            num_value_answer = int(''.join(filter(str.isdigit, str(answer))))
            num_value_col = int(''.join(filter(str.isdigit, str(question))))
            matrix_values = ['z_eens', 'b_eens', 'b_oneens', 'z_oneens']
            if (name == 'Item2.1-RESPONSE'):
              cols = ['leuk_leren_rekenen', 'willen_geen_rekenen_leren', 'rekenen_is_saai',
              'leer_interessant_rekenen', 'rekenen_leuk', 'school_taken_getallen_leuk',
              'leuk_rekensommen_oplossen', 'verheug_rekenles', 'rekenen_favoriet']
              if not num_value_col is None and not num_value_answer is None:
                new_col_name = cols[num_value_col - 5]
                add_value(f'{name}-{new_col_name}', matrix_values[num_value_answer -1], pd_total)
            if (name == 'Item2.2-RESPONSE'):
              cols = ['ik_weet_moet_doen_van_meester_juf', 'begrijp_meester_juf',
              'meester_juf_duidelijk_antwoord_mijn_vraag', 'meester_juf_goed_uitleggen',
              'meester_juf_helper', 'meester_juf_nog_een_keer_uitleggen', 'meester_juf_commentaar',
              'meester_juf_vraagt_laten_zien_geleerd', 'meester_juf_vraagt_mij_antwoorden_uitleggen']
              if not num_value_col is None and not num_value_answer is None:
                new_col_name = cols[num_value_col - 5]
                add_value(f'{name}-{new_col_name}', matrix_values[num_value_answer -1], pd_total)
            if (name == 'Item2.4-RESPONSE'):
              cols = ['meestal_goed_in_rekenen', 'moeilijker_dan_klasgenoot', 'ik_ben_gewoon_niet_goed', 'makkelijk_voor_mij',
              'goed_in_oplossen_moeilijke_sommen', 'goed_uitleggen', 'moeilijker_andere_vakken', 'moeilijk_te_snappen']
              if not num_value_col is None and not num_value_answer is None:
                new_col_name = cols[num_value_col - 5]
                add_value(f'{name}-{new_col_name}', matrix_values[num_value_answer -1], pd_total)
            if (name == 'Item2.5-RESPONSE'):
              cols = ['goed_mijn_best', 'niet_veranderen', 'hard_gewerkt', 'niet_slim_kan_goed_worden',
              'niet_veranderen_slim_rekenen', 'goed_door_opletten', 'goed_geboren', 'iedereen_kan_rekenen',
              'zelf_veranderen_rekenen']
              if not num_value_col is None and not num_value_answer is None:
                new_col_name = cols[num_value_col - 5]
                add_value(f'{name}-{new_col_name}', matrix_values[num_value_answer -1], pd_total)
            if (name == 'Item2.6-RESPONSE'):
              cols = ['leerling_luisteren', 'te_onrustig', 'lang_wachten_stil', 'onderbreken_juf_meester',
              'niet_aan_regels_houden', 'moeilijk_concentreren_door_andere']
              matrix_values = ['elk', 'helft', 'sommige', 'nooit']
              if not num_value_col is None and not num_value_answer is None:
                new_col_name = cols[num_value_col - 5]
                add_value(f'{name}-{new_col_name}', matrix_values[num_value_answer -1], pd_total)
            if not name in columns_to_delete:
              columns_to_delete.append(name)

pd_total = pd_total.astype(str)
pd_total = pd_total.replace(to_replace = "\.0+$",value = "", regex = True)


pd_total = pd_total.drop(columns_to_delete, axis=1)
pd_total.to_csv('c:\\tmp\\tao_vragenlijst.csv', index=False, sep=';')
pd_org.to_csv('c:\\tmp\\tao_vragenlijst-org.csv', index=False, sep=';')
# now loop through dataframa and modify columns
    
