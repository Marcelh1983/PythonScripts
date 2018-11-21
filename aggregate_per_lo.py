import pandas as pd

# read csv
df = pd.read_csv("C:/TMP/sessions_pilot_leerlijn-2018-11-20_10-33-35.csv", ';').fillna(value = '')

# add leerdoel by stripping ITM- and the last part of the item_code: ITM-G5_HG7_11 to G5_HG7
df['leerdoel'] = df['ItemCode'].replace({'ITM-' : ''}, regex=True).apply(lambda x: "_".join(x.split("_")[:2]))

# group by CandidateId and leerdoel and add a new column leerdoel_score
group = df.groupby(['CandidateId', 'leerdoel'])['ItemScore'].sum().reset_index(name='leerdoel_score')

# if score > 5 then the candidate passed
group['gehaald'] = group['leerdoel_score'] > 5
# write to csv
group.to_csv('C:/TMP/per_learning_objective.csv', ';', index=False)