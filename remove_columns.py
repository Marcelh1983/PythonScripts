"""
  Remove columns from csv file
"""
import pandas as pd

data = pd.read_csv("c://TMP//results-Molenven A-2021-12-07T164618.csv", sep=';')

columns = ['GroupName','StartCode','Status', 'ModuleId']
columns_to_delete = []
for column_name, j in data.head(1).iteritems():
    if not column_name in columns and not 'score' in column_name:
        columns_to_delete.append(column_name)
        #data..pop(column_name)
data = data.drop(columns_to_delete,axis=1)
data.to_csv("c://TMP//results-Molenven A-2021-12-07T164618_new.csv", sep=';')

