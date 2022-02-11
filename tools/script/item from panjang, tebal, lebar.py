from masterdata.models import MasterBarang
import csv
import pandas as pd
from tqdm import tqdm
from django.db.models import Value, F, Func

# Constants MUST CHECK
csv_file_path = "/home/Vieri/project_dir/oee_impc/tools/KD to OEE.csv"
convert_dict = {"panjang": float, "tebal": float, "lebar": float, "berat": float}

df1 = pd.read_csv(csv_file_path)
df1 = df1.astype(convert_dict)

with open('/home/Vieri/project_dir/oee_impc/tools/item.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for index, row in tqdm(df1.iterrows(), total=df1.shape[0]):
        berat = row['berat']
        tebal = row['tebal']
        lebar = row['lebar']
        panjang = row['panjang']
        s_or_g = row['s_or_g']
        data = [tebal, lebar, panjang]
        if s_or_g == "S":
            items = MasterBarang.objects.filter(group_id=196, panjang=panjang, lebar=lebar) | MasterBarang.objects.filter(group_id=196, panjang=lebar, lebar=panjang)
        else:
            items = MasterBarang.objects.filter(group_id=96, panjang=panjang, lebar=lebar) | MasterBarang.objects.filter(group_id=96, panjang=lebar, lebar=panjang)
        if len(items) > 0:
            items = items.annotate(delta=Func(F("berat_standar_fg")-berat, function='ABS')).values_list("id", "nama", "berat_standar_fg", "delta").order_by('delta')[0]
            item = list(items)
            data += item
        writer.writerow(data)