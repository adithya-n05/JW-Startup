import pandas as pd 

file_name = 'Jeff_Wilson_Sources.xlsx'
df = pd.read_excel(file_name)

print(df.head())

json_data = df.to_json(orient='records')
print(json_data)

for index, row in df.iterrows():
    url = row['Source']
    description = row['Description']
    