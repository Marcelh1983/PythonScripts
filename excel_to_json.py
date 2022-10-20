import os
import pandas as pd
import json
from pathlib import Path

def get_file_name(path):
    if not os.path.isdir(path):
        return os.path.splitext(os.path.basename(path))[0].split(".")[0]

excel_file = 'C://TMP//woordmars_vast.xlsx'
output_folder_name = 'c://tmp//'

excel_data_fragment = pd.read_excel(excel_file)
json_str = excel_data_fragment.to_json(orient='records')
thisisjson_dict = json.loads(json_str)

json_file = os.path.join(output_folder_name, get_file_name(excel_file) + '.json')

# import pandas as pd
# from googletrans import Translator
# import os
# from api.convert import convert_from_file

with open(json_file, 'w') as json_file:
    json.dump(thisisjson_dict, json_file)
print('done')
# output_file_nl = 'AnalyseModelBeeldverhaal_nl.json'
# output_file_en = 'AnalyseModelBeeldverhaal_en.json'

# excel_file = 'C://repos//woordmars//apps//functions//items.xlsx'

# excel_file_en = 'C://repos//beeldverhaal-web//frontend-teacher//tour_EN.xlsx'


# convert_from_file(excel_file, output_folder_name)
# read from an excel file
# df = pd.read_excel(excel_file)

# def localTranslate(value): 
#     if isinstance(value, str) and value.strip():
#         return getattr(translator.translate(value, src='nl',dest='en'), 'text')
#     else:
#         return ''

# # translate the columns
# translator = Translator()         
# df['Aspect'] = df['Aspect'].apply(localTranslate)
# df['observatie'] = df['observatie'].apply(localTranslate)
# df['Korte omschrijving'] = df['Korte omschrijving'].apply(localTranslate)
# df['Toelichting -i-'] = df['Toelichting -i-'].apply(localTranslate)

# # output new excel file
# df.to_excel(excel_file_en, index=False)


# # export json files and rename to more meaninfull name
# excel2json.convert_from_file(excel_file, output_folder_name)
# os.rename(os.path.join(output_folder_name, 'Sheet1.json'),os.path.join(output_folder_name, output_file_nl))

# excel2json.convert_from_file(excel_file_en, 'C://TMP//')
# os.rename(os.path.join(output_folder_name, 'Sheet1.json'),os.path.join(output_folder_name, output_file_en))

