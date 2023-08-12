from datetime import date, datetime
import pandas as pd

df = pd.read_csv('project/manitoba_covid_data_2020-2021.csv')
#print(df)

print(df.columns)
# Index(['Date', 'RHA', 'Daily_Cases', 'Cumulative_Cases', 'Active_Cases',
#        'Recoveries', 'Deaths', 'ObjectId'],
#       dtype='object')

for row in df.iterrows():
    # row is a tuple
    row = row[1]
    name = row['RHA']
    d = row['Date']

    # ex: '1/5/20'
    fmt = '%d/%m/%y'

    d = datetime.strptime(d, fmt)

    cases = row['Daily_Cases']
    cases = int(cases)

    p = root.get_child(name)
    p.add_case(d, cases)
