from form_produksi.models import ReportShiftPerKK, KK, DetailProductionResults, DetailMaterialConsumption, DetailDowntime
import csv
import pandas as pd
from datetime import datetime, timedelta, time
from tqdm import tqdm

# Constants MUST CHECK
csv_file_path = "/home/Vieri/project_dir/oee_impc/tools/hollow3.csv"

user_id = 4

col_kk = "kk"
col_date = "tanggal"
col_machine = "mesin"
col_dl = "dl"
col_fg = "fg"
col_berat_unit = "berat_unit"
col_item = "fg_item"
col_fg_qty = "fg_qty"
col_reject = "reject"
col_trimming = "trimming"
col_waste = "waste"
col_eff_hour = "eff_hour"
col_shift = "shift"


convert_dict = {col_kk: str, col_date: str, col_machine: int, col_dl: float, 
                col_fg: float, col_berat_unit: float, col_shift: int,
                col_item: int, col_fg_qty: float, col_reject: float, 
                col_waste: float, col_eff_hour: float}

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
    try:
        entry = KK(no_kk=kk, creation_date=tanggal, user_group_id=user_id)
        entry.save()
    except:
        pass

# Create form based on excel file

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    # form header
    total_hr = row[col_eff_hour]
    shift = row[col_shift]
    kk_used = row[col_kk]
    start_ = datetime.strptime(row[col_date], '%d/%m/%Y')
    if total_hr > 0:
        total_hr = timedelta(hours=total_hr)
        end_ = start_ + total_hr
        kk_ = KK.objects.get(no_kk=kk_used)
        mesin_ = row[col_machine]
        dl_ = row[col_dl]
        the_form = ReportShiftPerKK(user_group_id=user_id, start_time=start_,
                                    end_time=end_, shift=shift, machine_id=mesin_, no_kk=kk_, dl_avail=dl_)
        the_form.save()
    else:
        the_form = ReportShiftPerKK.objects.get(shift=shift, no_kk_id=kk_used, start_time=start_)
    # fg details
    fg_item_ = row[col_item]
    fg_qty_ = row[col_fg_qty]
    berat_unit_ = row[col_berat_unit]
    reject_ = row[col_reject]
    trimming_ = row[col_trimming]
    waste_ = row[col_waste]
    finished_good_obj = DetailProductionResults(produk_id=fg_item_, hasil_jadi_qty=fg_qty_, hold_qc_qty=0,
                                                berat_unit_sample=berat_unit_, reject=reject_, trimming=trimming_,
                                                waste=waste_, laporan=the_form)
    finished_good_obj.save()