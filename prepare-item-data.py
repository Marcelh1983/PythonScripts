import pandas as pd
import numpy as np

# read excel with item definitions
item_data = pd.read_excel("/alle-items-opgeschoond.xlsx")

# add new columns for analysis
item_data['optellen'] = item_data['Vraag'].apply(lambda vraag: (
    "+" in vraag) or ("erbij" in vraag) or ("plus" in vraag))



# item_data['aftrekken'] = item_data['Vraag'].apply(
#     lambda vraag: ("-" in vraag) or ("min" in vraag))

# item_data['vermenigvuldigen'] = item_data['Vraag'].apply(
#     lambda vraag: ("x" in vraag))

# item_data['aantal_karakters_in_vraag_en_body'] = item_data['Vraag'].apply(
#     lambda vraag: (len(vraag))) + item_data['Body'].apply(lambda body: (len(body)))

# item_data['vraag_of_body_bevat_plaatje'] = item_data['Vraag'].apply(lambda vraag: (
#     "-image" in vraag)) or item_data['Body'].apply(lambda body: ("-image" in body))

# item_data['kort_antwoord']
# item_data['multiple_choice']
# item_data['aantal_alternatieven']

# read item responses

# combine item response and item data

# remove items that probably have the wrong solution.

item_data.head(10)
