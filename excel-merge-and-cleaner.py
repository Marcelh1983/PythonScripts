import pandas as pd
import numpy as np
import glob
import re
import unicodedata

# CONFIGURE THIS
excel_folder = "C:/TMP/TOM/*.xlsx"
columns_to_clean = []
# columns_to_clean = ['Body', 'Tekst en interacties', 'Vraag', 'Keuze (A)', \
# 'Keuze (B)', 'Keuze (C)', 'Keuze (D)', 'Keuze (E)', 'Keuze (F)', 'Keuze (G)', \
# 'Keuze (H)', 'Keuze (I)']
new_excel_file_name = 'newExcel.xlsx'
# END CONFIGURING

# clean up all the string value
def clean(s):
    s = replaceTabSpacesNewLineBySpaces(s)
    s = replaceNewLineBySpaces(s)
    s = removeWeirdSpaces(s)
    s = removeDoubleSpaces(s)
    s = removeInlineInteractionCrap(s)
    s = removeInlineImageCrapButKeepImage(s)
    s = removeDoubleSpaces(s)
    s = s.strip()
    return s

def removeDoubleSpaces(s):
    return re.sub(' +',' ',s)

def replaceTabSpacesNewLineBySpaces(s):
    return re.sub(r'\s+',' ',s)

def replaceNewLineBySpaces(s):
    return s.replace('\n', ' ').replace('\r', '')

def removeWeirdSpaces(s):
    s = unicodedata.normalize("NFKD", s)
    return s

# removes inline Interaction crap
def removeInlineInteractionCrap(s):
    # find first, split on space and join from where we know the parameters end
    inlineElementParameters = 8
    guidFinder = re.compile('I[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', re.I)
    while isFound(guidFinder.search(s)):
        s = s[:guidFinder.search(s).regs[0][0]] + ' '.join(s[guidFinder.search(s).regs[0][0]:].split(' ')[inlineElementParameters:])
    return s

# removes inline Image crap
def removeInlineImageCrapButKeepImage(s):
    inlineElementParameters = 10
    imageFinder = re.compile(r'( ?.*\.(?:png|jpg))', re.I)
    imageFinderStart = re.compile('(png|jpg)', re.I)
    while isFound(imageFinder.search(s)) and len(s[imageFinder.search(s).regs[0][0]:].split(' ')) > inlineElementParameters:
        s = s[:imageFinder.search(s).regs[0][1]] + ' '.join(s[imageFinder.search(s).regs[0][0]:].split(' ')[inlineElementParameters:])
        s = s.replace('.jpg', '-image').replace('.png', '-image')
    # check above matches only if there is a space before the inline image.
    while isFound(imageFinderStart.search(s)):
        s = s[:imageFinderStart.search(s).regs[0][1]]+ ' '.join(s[imageFinderStart.search(s).regs[0][0]:].split(' ')[inlineElementParameters:])
        s = s.replace('.jpg', '-image').replace('.png', '-image')
    return s

def isFound(searched):
    return not searched is None and not \
    searched.regs is None and not  \
    len(searched.regs) == 0

def getColumns(header_names, frames):
    return [getColumn(header_name, frames) for header_name in header_names]

def getColumn(header_name, frames):
    column = np.where(combined.iloc[0].values == header_name)
    if not column is None:
        return frames[column[0][0]]

excel_names = glob.glob(excel_folder)

# read them in
excels = [pd.ExcelFile(name) for name in excel_names]

# turn them into dataframes
frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]

# delete the first row for all frames except the first
# i.e. remove the header row -- assumes it's the first
frames[1:] = [df[1:] for df in frames[1:]]

# concatenate them..
combined = pd.concat(frames)

# clean up columns
columns = getColumns(columns_to_clean, combined)
for column_index, column in enumerate(columns):
    for row_index, row_value in enumerate(columns[column_index]):
        if isinstance(row_value, str):
            newValue = clean(row_value)
            columns[column_index].values[row_index] =  newValue

# write it out
combined.to_excel(new_excel_file_name, header=False, index=False)
