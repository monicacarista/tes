import re
import csv
import pandas as pd

df = pd.read_csv("C:/Users/Owner/Downloads/masterdata_masterbarang (5).csv")
ds = df['nama']

with open('extracted_number.csv', 'w', encoding='UTF8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
    
    for i in ds:
        extracted = re.findall(r"[-+]?\d*\.\d+|\d+", i)
        csv_writer.writerow([i] + extracted)