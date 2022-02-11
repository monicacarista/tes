import csv
import pandas as pd
from datetime import datetime, timedelta, time
from tqdm import tqdm
from form_produksi.models import ProductionForm, KK, DetailProductionResults, DetailMaterialConsumption, DetailDowntime
from masterdata.models import MasterBarang
from django.db.models import Count, Sum, F, Func, IntegerField, FloatField

csv_file_path = "/home/Vieri/project_dir/oee_impc/tools/RM UPC AUG.csv"
df = pd.read_csv(csv_file_path)

df['qty'] = df['qty'].str.replace('.', '')
df['qty'] = df['qty'].str.replace(',', '.')

convert_dict = {'kk': str, 'kode': str, 'bahan': str, 'qty': float}
df = df.astype(convert_dict)

# Check whether the KK is in DB or not

kk_list = df['kk'].unique()
kk_available = KK.objects.filter(no_kk__in=kk_list)
print(kk_available)

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    kk = KK.objects.get(no_kk = row.kk)
    laporan = kk.productionform_set.all()
    out_summary = laporan.values("machine").annotate(out = Sum("total_output")).order_by()
    out_total = laporan.aggregate(out = Sum("total_output"))
    barang = MasterBarang.objects.get(kode_barang=row.kode)
    for i in out_summary:
        factor = i["out"] / out_total["out"]
        this_form = laporan.filter(machine_id=i["machine"]).first()
        this_form.detailmaterialconsumption_set.create(bahan=barang, qty_awal=row.qty * factor, qty_tambahan=0, qty_akhir=0)
    

row = df.iloc[0]
kk = KK.objects.get(no_kk = row.kk)
laporan = kk.productionform_set.all()
out_summary = laporan.values("machine").annotate(out = Sum("total_output")).order_by()
out_total = laporan.aggregate(out = Sum("total_output"))
barang = MasterBarang.objects.get(kode_barang=row.kode)
for i in out_summary:
    factor = i["out"] / out_total["out"]
    this_form = laporan.filter(machine_id=i["machine"]).first()
    this_form.detailmaterialconsumption_set.create(bahan=barang, qty_awal=row.qty * factor, qty_tambahan=0, qty_akhir=0)


DetailMaterialConsumption.objects.filter(laporan__no_kk__creation_date__month=8, laporan__user_group_id=4)
