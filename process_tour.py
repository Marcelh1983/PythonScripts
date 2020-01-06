
import excel2json
import pandas as pd
from googletrans import Translator
import os

output_folder_name = 'C://TMP//'
output_file_nl = 'tour_nl.json'
output_file_en = 'tour_en.json'

excel_file = '//tour_nl.xlsx'
excel_file_en = '//tour_en.xlsx'

# read from an excel file
df = pd.read_excel(excel_file)

def localTranslate(value): 
    if isinstance(value, str) and value.strip():
        return getattr(translator.translate(value, src='nl',dest='en'), 'text')
    else:
        return ''

# translate the columns
translator = Translator()         
df['content'] = df['content'].apply(localTranslate)
df['title'] = df['title'].apply(localTranslate)
df['nextBtnTitle'] = df['nextBtnTitle'].apply(localTranslate)
df['endBtnTitle'] = df['endBtnTitle'].apply(localTranslate)

# output new excel file
df.to_excel(excel_file_en, index=False)


# export json files and rename to more meaninfull name
excel2json.convert_from_file(excel_file, output_folder_name)
os.rename(os.path.join(output_folder_name, 'Sheet1.json'),os.path.join(output_folder_name, output_file_nl))

excel2json.convert_from_file(excel_file_en, 'C://TMP//')
os.rename(os.path.join(output_folder_name, 'Sheet1.json'),os.path.join(output_folder_name, output_file_en))
