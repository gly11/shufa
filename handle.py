import pandas as pd
from tqdm import tqdm

from_csv = './data/csv_files/data_100.csv'
df = pd.read_csv('./data/csv_files/raw_data.csv')
df1 = pd.read_csv(from_csv)
li = []
for row in df.values:
    if row[2].split('.')[-1] == 'pn':
        li.append(row[0])

for index, row in tqdm(df1.iterrows()):
    n = row['No.']
    if n in li:
        try:
            df1.drop(index, inplace=True)
        except Exception as err:
            print(f'Error: {err} NO. {n}')

df1.to_csv(f'{from_csv.split("/")[-1].split(".")[0]}_removed.csv', encoding='utf-8-sig', index=False)
