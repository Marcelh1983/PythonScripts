from os import listdir
from os.path import isfile, join, basename, dirname, normpath
import pandas as pd


base_path = 'C://TMP//vlag'
folders = ['MijnDocumenten', 'ClipArt', 'EmbeddedMedia']

# map(lambda x : x['name'], dict_a)
file_array = []
full_folder_names = map(lambda folder: join(base_path, folder), folders)
for mypath in full_folder_names:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        filename = basename(f)
        type = 'Afbeeldingen'
        if filename.startswith('video'):
            type = 'Videos'  
        foldername = basename(normpath(mypath))
        file_array.append({ 'url': filename, 'title': filename, 'type': type, 'category': foldername })

df = pd.DataFrame(file_array).T
df = df.transpose()
df.to_excel(excel_writer = join(base_path, "images.xlsx"))