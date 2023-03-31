# import pandas as pd
import json
import csv



# df = pd.read_json (r'C:\python310\json2csv\tags.json')
# df.to_csv (r'C:\python310\json2csv\tags.csv', index = None)


with open('C:\\python310\\json2csv\\tags.json', 'r') as f:
    data = json.load(f)

rows = []

for item in data:
    print(data[item])
    row = {}

    row['name'] = item['name']
    row['tagType'] = item['tagType']
    row['tags'] = item['tags']

    row['valueSource'] = item['valueSource']
    row['opcItemPath'] = item['opcItemPath']
    row['dataType'] = item['dataType']
    row['tagType'] = item['tagType']
    row['opcServer'] = item['opcServer']

    rows.append(row)

with open('C:\\python310\\json2csv\\tags.csv', 'w', newline='') as f:
    fieldnames = ['name', 'tagType', 'tags', 'valueSource', 'opcItemPath', 'dataType', 'tagType', 'opcServer']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)