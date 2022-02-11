from form_produksi.models import ReportShiftPerKK, KK, DetailProductionResults, DetailMaterialConsumption, DetailDowntime
import csv
import pandas as pd
from datetime import datetime, timedelta, time
from tqdm import tqdm

# Constants MUST CHECK
csv_file_path = "/home/Vieri/project_dir/oee_impc/tools/UPC-Tobeuploaded.csv"

id_fresh = 27680
id_caco3 = 27717
id_scrap = 27654

user_id = 4
shift = 1

col_kk = "kk"
col_date = "tanggal"
col_machine = "mesin"
col_dl = "dl"
col_scrap_usage = "scrap_usage"
col_fg = "fg"
col_fresh = "fresh"
col_hold = "hold"
col_berat_unit = "berat_unit"
col_item = "fg_item"
col_fg_qty = "fg_qty"
col_reject = "reject"
col_trimming = "trimming"
col_waste = "waste"
col_eff_hour = "eff_hour"
col_dt_produksi = "dt_produksi"
col_dt_teknik = "dt_teknik"
col_kk_cleaning = "cleaning"
kat_teknik = "PU"
kat_produksi = "TM"


convert_dict = {col_kk: str, col_kk_cleaning: bool, col_date: str, col_machine: int, col_dl: float, 
                col_fresh: float, col_scrap_usage: float, col_fg: float, col_hold: float, col_berat_unit: float,
                col_item: int, col_fg_qty: float, col_reject: float, col_trimming: float, 
                col_waste: float, col_eff_hour: float, col_dt_produksi: float, col_dt_teknik: float}

fields = ["kk", "fresh", "cleaning", "tanggal", "mesin", "dl", "scrap_usage", "fg", "hold", "berat_unit",
          "fg_item", "fg_qty", "reject", "trimming", "waste", "eff_hour", "dt_produksi", "dt_teknik"]

# Verify CSV Format

df = pd.read_csv(csv_file_path)
for i in fields:
    if i not in df:
        print(i, "not in CSV, check header")

df = df.astype(convert_dict)

# Check whether the KK is in DB or not

kk_list = df[col_kk].unique()
kk_available = KK.objects.filter(no_kk__in=kk_list)
print(kk_available)

# Create KK based on excel D Column

for kk in kk_list:
    tanggal = df[df[col_kk] == kk][col_date]
    tanggal = tanggal.min()
    tanggal = datetime.strptime(tanggal, '%d/%m/%Y')
    is_cleaning = df[df[col_kk] == kk][col_kk_cleaning]
    is_cleaning = is_cleaning.iloc[0]
    try:
        entry = KK(no_kk=kk, cleaning=is_cleaning, creation_date=tanggal, user_group_id=user_id)
        entry.save()
    except:
        pass

# Create form based on excel file

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    # form header
    start_ = datetime.strptime(row[col_date], '%d/%m/%Y')
    total_hr = row[col_eff_hour] + row[col_dt_produksi] + row[col_dt_teknik]
    total_hr = timedelta(hours=total_hr)
    end_ = start_ + total_hr
    kk_ = KK.objects.get(no_kk=row[col_kk])
    mesin_ = row[col_machine]
    dl_ = row[col_dl]
    the_form = ReportShiftPerKK(user_group_id=user_id, start_time=start_,
                                end_time=end_, shift=shift, machine_id=mesin_, no_kk=kk_, dl_avail=dl_)
    the_form.save()
    # rm details
    fresh = row[col_fresh]
    scrap_ = row[col_scrap_usage]
    fresh_ = fresh / 2
    fresh_obj = DetailMaterialConsumption(
        bahan_id=id_fresh, qty_awal=fresh_, laporan=the_form)
    caco3_obj = DetailMaterialConsumption(
        bahan_id=id_caco3, qty_awal=fresh_, laporan=the_form)
    scrap_obj = DetailMaterialConsumption(
        bahan_id=id_scrap, qty_awal=scrap_, laporan=the_form)
    fresh_obj.save()
    scrap_obj.save()
    caco3_obj.save()
    # fg details
    fg_item_ = row[col_item]
    fg_qty_ = row[col_fg_qty]
    hold_qty_ = row[col_hold] / row[col_berat_unit]
    berat_unit_ = row[col_berat_unit]
    reject_ = row[col_reject]
    trimming_ = row[col_trimming]
    waste_ = row[col_waste]
    finished_good_obj = DetailProductionResults(produk_id=fg_item_, hasil_jadi_qty=fg_qty_, hold_qc_qty=hold_qty_,
                                                berat_unit_sample=berat_unit_, reject=reject_, trimming=trimming_,
                                                waste=waste_, laporan=the_form)
    finished_good_obj.save()
    # downtime
    dt_start_ = datetime(1, 1, 1, 0, 0, 0)
    dt_produksi = row[col_dt_produksi]
    dt_produksi = timedelta(hours=dt_produksi)
    dt_produksi_ = dt_start_ + dt_produksi
    dt_produksi_ = dt_produksi_.time()
    dt_teknik = row[col_dt_teknik]
    dt_teknik = timedelta(hours=dt_teknik)
    dt_teknik_ = dt_start_ + dt_teknik
    dt_teknik_ = dt_teknik_.time()
    dt_start_ = dt_start_.time()
    dt_produksi_obj = DetailDowntime(waktu_mulai=dt_start_, waktu_selesai=dt_produksi_,
                                     kategori=kat_produksi, notes="Produksi", laporan=the_form)
    dt_teknik_obj = DetailDowntime(waktu_mulai=dt_start_, waktu_selesai=dt_teknik_,
                                   kategori=kat_teknik, notes="Teknik", laporan=the_form)
    dt_produksi_obj.save()
    dt_teknik_obj.save()
