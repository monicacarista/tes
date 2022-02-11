from form_produksi.models import ReportShiftPerKK, KK, DetailProductionResults, DetailMaterialConsumption, DetailDowntime
import csv
import pandas as pd
from datetime import datetime, timedelta, time
from tqdm import tqdm
from masterdata.models import MasterBarang

csv_file_path = "/home/Vieri/upload_pma/masterdata_masterbarang (3).csv"
null_code = -100

df = pd.read_csv(csv_file_path)

df['berat_standar_fg'] = df['berat_standar_fg'].fillna(null_code)

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        barang = MasterBarang.objects.get(id=row['id'])
    except:
        print(row['id'])
        continue
    brt_std = row['berat_standar_fg']
    # kode = row['kode_barang']
    # if barang.kode_barang != kode:
    #     barang.kode_barang = kode
    if brt_std != null_code:
        barang.berat_standar_fg = brt_std
    else:
        barang.berat_standar_fg = None
    barang.save()
