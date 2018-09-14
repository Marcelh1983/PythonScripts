import pandas as pd
import numpy as np
from collections import Counter

# read the csv
df = pd.read_csv("C:/TMP/Python/itemresponse.csv", ';', usecols=['ItemCode', 'Score', 'Response', 'CorrectResponse']).fillna(value = '')
# function to determine if a item is answered correct
def is_correct(x):
    if x > 0:
        return 1
    else:
        return 0

# add column with that indicates if the item is answered correctly.
df['correct'] = df['Score'].apply(is_correct)
# add column with counts to see how many candidates did answer this item
df["count"] = df.groupby(["ItemCode"])["ItemCode"].transform("count")

df['MostGivenResponse'] = df.groupby('ItemCode')["Response"].transform(lambda x : x.mode().iloc[0])
# print top 10 to show results
df.head(10)
# group by itemcode and calculate the percentage that is answered correctly
group = df.groupby(['ItemCode', "count", "MostGivenResponse", "CorrectResponse"]).apply(lambda x: x['correct'].sum()/len(x)).reset_index(name='percentage')
# filter out items that are answered less than 10 times
group = group[(group['count'] > 10)]
# print result
group.head(10)
# sort by percentage
group = group.sort_values(by=['percentage'])
# the top 10 could indicate a wrong key
group.head(10)
# sort ascending
group = group.sort_values(by=['percentage'], ascending=False)
# these items are probably too easy
group.head(10)
