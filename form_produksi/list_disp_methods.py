from datetime import datetime, date
from django.db.models import Count, Sum, F, Func, IntegerField
from django.utils.html import format_html
from django.urls import reverse

# ======== Table Columns dict
col = {
    "kk_aktif" : "KK Status",
    "month_executed" : "Month Executed",
    "item" : "Item Name",
    "item_group" : "Item Group",
    "item_code" : "Item Code",
    "eff_hour" : "Eff Hour (hr)",
    "dt" : "Downtime (hr)",
    "idle" : "Idle Time (hr)",
    "rm" : "Raw Material (kg)",
    "fg" : "FG (kg)",
    "fg_lm" : "FG (LM)",
    "fg_m2" : "FG (M2)",
    "fg_qty" : "FG Qty",
    "fg_theory" : "FG Theory (kg)",
    "tr" : "Trimming (kg)",
    "rj" : "Reject (kg)",
    "ws" : "Waste (kg)",
    "scrap_chg" : "Scrap Chg (kg)",
    "scrap_use" : "Scrap Used (kg)",
    "scrap_prod" : "Scrap Created (kg)",
    "mat_diff" : "Material Differences (kg)",
    "mat_eff" : "Material Efficiency",
    "fty" : "FTY",
    "avail" : "Avail",
    "perf" : "Perf",
    "oee" : "OEE",
    "FTY" : "FTY%",
    "weight" : "Weight (kg)",
    "qty" : "Qty",
    "wo" : "WO Number",
    "machine" : "Machine Name",
    "date" : "Date",
    "category" : "Category",
    "date" : "Date"
}
# ======== Table Columns dict

class KKReportMethod():
    def get_laporan_filtered(self, obj):
        mesin_id = self.request.GET.get("machine__id")
        if mesin_id:
            reports = obj.productionform_set.filter(machine=mesin_id)
        else:
            reports = obj.productionform_set.all()
        return reports

    def bulan_pengerjaan(self, obj):
        reports = self.get_laporan_filtered(obj)
        bulan = set()
        for report in reports:
            bulan.add(report.start_time.strftime("%B - %Y"))
        return ', '.join(bulan)
    
    def produk(self, obj):
        try:
            reports = self.get_laporan_filtered(obj)
            jenis_barang = reports.values_list('detailproductionresults__produk__group__group', flat=True)
            jenis_barang = list(set(jenis_barang))
            jenis_barang = [i for i in jenis_barang if i]
        except: 
            return '-' 
        return jenis_barang
    produk.short_description = col['item_group']
    
    def rm(self, obj):
        reports = self.get_laporan_filtered(obj)
        pemakaian = reports.aggregate(total = Sum('raw_material'))['total']
        return round_2(pemakaian)
    rm.short_description = col['rm']

    def fg_unit(self, obj):
        reports = self.get_laporan_filtered(obj)
        fg_unit = reports.aggregate(total = Sum('fg_qty'))['total']
        return round_2(fg_unit)
    fg_unit.short_description = col['fg_qty']

    def fg_lm(self, obj):
        reports = self.get_laporan_filtered(obj)
        fg_lm = reports.aggregate(total = Sum('fg_lm'))['total']
        return round_2(fg_lm)
    fg_lm.short_description = col['fg_lm']
        
    def fg_m2(self, obj):
        reports = self.get_laporan_filtered(obj)
        fg_m2 = reports.aggregate(total = Sum('fg_m2'))['total']
        return round_2(fg_m2)
    fg_m2.short_description = col['fg_m2']

    def fg(self, obj):
        reports = self.get_laporan_filtered(obj)
        total_fg = reports.aggregate(total = Sum('fg'))['total']
        return round_2(total_fg)
    fg.short_description = col['fg']

    def fg_teori(self, obj):
        reports = self.get_laporan_filtered(obj)
        total_fg = reports.aggregate(total = Sum('fg_mass_std'))['total']
        return round_2(total_fg)
    fg_teori.short_description = col['fg_theory']

    def reject(self, obj):
        reports = self.get_laporan_filtered(obj)
        reject = reports.aggregate(total = Sum('reject') )['total']
        if reject == None: reject = 0
        return round_2(reject)
    reject.short_description = col['rj']

    def trimming(self, obj):
        reports = self.get_laporan_filtered(obj)
        reject = reports.aggregate(total = Sum('trimming') )['total']
        if reject == None: reject = 0
        return round_2(reject)
    trimming.short_description = col['tr']
    
    def waste(self, obj):
        reports = self.get_laporan_filtered(obj)
        reject = reports.aggregate(total = Sum('waste') )['total']
        if reject == None: reject = 0
        return round_2(reject)
    waste.short_description = col['ws']
    
    def selisih_material(self, obj):
        reports = self.get_laporan_filtered(obj)

        rm = reports.aggregate(total = Sum('raw_material'))['total']
        t_out = reports.aggregate(total = Sum('total_output'))['total']
        try:
            eff = t_out/rm
        except:
            eff = 0

        selisih = reports.aggregate(total = Sum('raw_material') - Sum('total_output'))['total']
        if selisih is None: selisih = 0 

        msg = '{:,.2f} ({:.2%})'.format(selisih, eff)
        
        if eff > 1 or eff < 0.8:
            msg = format_html('<mark>' + msg + '</mark>')
        return msg
    selisih_material.short_desciption = col['mat_diff']

    def scrap_used(self, obj):
        reports = self.get_laporan_filtered(obj)
        scrap_usage = reports.aggregate(total = Sum('scrap_usage'))['total']
        scrap_usage = none_to_0(scrap_usage)
        return scrap_usage
    scrap_used.short_description = col['scrap_use']

    def scrap_created(self, obj):
        reports = self.get_laporan_filtered(obj)
        scrap_created = reports.aggregate(total = Sum('scrap_hasil'))['total']
        scrap_created = none_to_0(scrap_created)
        return scrap_created
    scrap_created.short_description = col['scrap_prod']

    def scrap_chg(self, obj):
        reports = self.get_laporan_filtered(obj)
        scrap_usage = reports.aggregate(total = Sum('scrap_usage'))['total']
        scrap_created = reports.aggregate(total = Sum('scrap_hasil'))['total']
        scrap_usage = none_to_0(scrap_usage)
        scrap_created = none_to_0(scrap_created)
        
        scrap_chg = scrap_created - scrap_usage
        return warna_limit(scrap_chg, -4000, 0)
    scrap_chg.short_description = col['scrap_chg']

    def eff_rm(self,obj):
        reports = self.get_laporan_filtered(obj)
        rm = reports.aggregate(total = Sum('raw_material'))['total']
        t_out = reports.aggregate(total = Sum('total_output') - Sum('waste'))['total']
        try:
            fty = t_out/rm
        except:
            fty = 0
        return warna_persen(fty)
    eff_rm.short_description = col['mat_eff']
        
    def eff_hour(self, obj):
        reports = self.get_laporan_filtered(obj)
        durasi = reports.aggregate(total = Sum('effective_hour'))['total']
        return round_2(durasi)
    eff_hour.short_description = col['eff_hour']

    def downtime(self, obj):
        reports = self.get_laporan_filtered(obj)
        durasi = reports.aggregate(total = Sum('downtime'))['total']
        return round_2(durasi)
    downtime.short_description = col['dt']

    def durasi_downtime(self, obj):
        reports = self.get_laporan_filtered(obj)
        durasi = reports.aggregate(total = Sum('downtime'))['total']
        try:
            return round_2(durasi)
        except:
            return 0

    def fty(self,obj):
        reports = self.get_laporan_filtered(obj)
        fg = reports.aggregate(total = Sum('fg'))['total']
        t_out = reports.aggregate(total = Sum('total_output'))['total']
        try:
            fty = fg/t_out
        except:
            fty = 0
        return warna_persen(fty)
    fty.short_description = col['fty']

    def availability(self,obj):
        reports = self.get_laporan_filtered(obj)
        durasi_total = reports.aggregate(total = Sum('total_hour'))['total']
        durasi_efektif = reports.aggregate(total = Sum('effective_hour'))['total']
        try:
            avail = durasi_efektif/durasi_total
        except:
            avail = 0
        return warna_persen(avail)
    availability.short_description = col['avail']
    
    def performance(self, obj):
        reports = self.get_laporan_filtered(obj)
        earn_hour = reports.aggregate(total = Sum('earn_hour'))['total']
        effective_hour = reports.aggregate(total = Sum('effective_hour'))['total']
        try:
            performa = earn_hour/effective_hour
        except:
            return 0
        return warna_persen(performa)
    performance.short_description = col['perf']

    def oee(self,obj):
        reports = self.get_laporan_filtered(obj)
        earn_hour = reports.aggregate(total = Sum('earn_hour'))['total']
        durasi_total = reports.aggregate(total = Sum('total_hour'))['total']
        durasi_efektif = reports.aggregate(total = Sum('effective_hour'))['total']
        fg = reports.aggregate(total = Sum('fg'))['total']
        total_output = reports.aggregate(total = Sum('total_output'))['total']
        try:
            oee_value = fg / total_output * earn_hour / durasi_efektif * durasi_efektif / durasi_total
        except:
            return 'Error'
        return warna_persen(oee_value)
    oee.short_description = col['oee']

class ShiftReportMethod():
    def produk(self, obj):
        try:
            produk = obj.detailproductionresults_set.first().produk.nama
        except: 
            return '-' 
        return produk
    produk.short_description = "Produk pertama form"
    
    def material_usage(self, obj):
        return round_2(obj.raw_material)
    material_usage.short_description = col['rm']
    
    def finished_goods(self, obj):
        return round_2(obj.fg)
    finished_goods.short_description = col['fg']

    def fg_teori(self, obj):
        return round_2(obj.fg_mass_std)
    fg_teori.short_description = col['fg_theory']
    
    def fg_unit(self, obj):
        return round_2(obj.fg_qty)
    fg_unit.short_description = col['fg_qty']

    def fg_lm_(self, obj):
        return round_2(obj.fg_lm)
    fg_lm_.short_description = col['fg_lm']
        
    def fg_m2_(self, obj):
        return round_2(obj.fg_m2)
    fg_m2_.short_description = col['fg_m2']

    def hold_qc(self, obj):
        return round_2(obj.hold)
    hold_qc.short_description = "Hold (kg)"

    def byproduct(self, obj):
        try:
            obj.reject = none_to_0(obj.reject)
            obj.trimming = none_to_0(obj.trimming)
            obj.waste = none_to_0(obj.waste)
            return round_2(obj.reject + obj.trimming + obj.waste)
        except:
            return 0
    byproduct.short_description = 'Rj+Ws (kg)'

    def reject_(self, obj):
        try:
            return round_2(obj.reject)
        except:
            return 0
    reject_.short_description = col['rj']
    reject_.admin_order_field = 'reject'

    def trimming_(self, obj):
        try:
            return round_2(obj.trimming )
        except:
            return 0
    trimming_.short_description = col['tr']

    def waste_(self, obj):
        try:
            return round_2(obj.waste)
        except:
            return 0
    waste_.short_description = col['ws']
    
    def selisih_material(self, obj):
        try:
            obj.raw_material = none_to_0(obj.raw_material)
            obj.total_output = none_to_0(obj.total_output)
            selisih = obj.raw_material - obj.total_output
        except:
            selisih = 0
        return warna_limit(selisih, -1, 1)
    selisih_material.short_description = col['mat_diff']

    def pemakaian_scrap(self, obj):
        try:
            obj.scrap_usage = none_to_0(obj.scrap_usage)
            obj.scrap_hasil = none_to_0(obj.scrap_hasil)
            return round_2(obj.scrap_hasil - obj.scrap_usage)
        except:
            return 0
    pemakaian_scrap.short_description = col['scrap_chg']

    def pkg_reject(self, obj):
        try:
            obj.reject_eqv = none_to_0(obj.reject_eqv)
            obj.fg_qty = none_to_0(obj.fg_qty)
            return round_2(obj.reject_eqv / obj.fg_qty)
        except:
            return 0
    pkg_reject.short_description = 'Reject Eqv%'
        
    def durasi_pengerjaan(self, obj):
        try:
            return round_2(obj.effective_hour)
        except:
            return 0
    durasi_pengerjaan.short_description = col['eff_hour']

    def durasi_downtime(self, obj):
        try:
            return round_2(obj.downtime)
        except:
            return 0
    durasi_downtime.short_description = col['dt']

    def earn_hour(self, obj):
        return round_2(obj.earn_hour)

    def fty(self,obj):
        fg = none_to_0( obj.fg)
        t_out = none_to_0(obj.total_output)
        try:
            fty = fg / t_out
        except:
            fty = 0
        return warna_persen(fty)
    fty.short_description = col['fty']

    def availability(self,obj):
        efektif = none_to_0(obj.effective_hour)
        total = none_to_0(obj.total_hour)
        try:
            avail = efektif/total
        except:
            avail = 0
        return warna_persen(avail)
    availability.short_description = col['avail']
    
    def performance(self, obj):
        durasi_efektif = none_to_0(obj.effective_hour)
        earn_hour = none_to_0(obj.earn_hour)

        if type(earn_hour) == str:
            return 'Output Mesin Ideal tidak terdata'

        if durasi_efektif == 0:
            performa = 0
        else:
            try:
                performa = earn_hour / durasi_efektif
            except:
                return "Error"

        return warna_persen(performa)
    performance.short_description = col['perf']

    def oee(self,obj):
        fg = none_to_0(obj.fg)
        t_out = none_to_0(obj.total_output)
        efektif = none_to_0(obj.effective_hour)
        durasi_total = none_to_0(obj.total_hour)
        earn_hour = none_to_0(obj.earn_hour)
        
        try:
            oee = fg / t_out * earn_hour / efektif * efektif / durasi_total
        except:
            return 'Error'
        return warna_persen(oee)
    oee.short_description = col['oee']

class DowntimeReportMethod():
    def durasi_downtime(self, obj):
        downtime_list = []
        downtime_detail_inst = obj.detaildowntime_set.all()
        for inst in downtime_detail_inst:
            downtime_list.append(str(round_2(inst.durasi)))
        
        printout = format_html('<br>'.join(downtime_list))
        return printout
    durasi_downtime.short_description = col['dt']

    def penyebab_downtime(self, obj):
        downtime_list = []
        downtime_detail_inst = obj.detaildowntime_set.all()
        for inst in downtime_detail_inst:
            kategori = inst.get_kategori_display()
            notes = inst.notes
            penyebab = "{}\t: {}".format(kategori, notes)
            downtime_list.append(penyebab)

        printout = format_html('<br>'.join(downtime_list))
        return printout

class MaterialConsumptionMethod():
    id_aditif = [162, 161, 155, 154, 142, 141, 107, 105, 101, 5, 52, 7]
    id_filler = []
    id_pigment = [157, 149, 106, 99, 54, 9, ]

    def finished_good(self, obj):
        return round_2(obj.fg)
    finished_good.short_description = 'FG (kg)'

    def pemakaian_fresh(self, obj):
        return round_2(obj.raw_material - obj.scrap_usage)
    pemakaian_fresh.short_description = 'Fresh (kg)'

    def pemakaian_scrap(self, obj):
        return round_2(obj.scrap_usage)
    pemakaian_scrap.short_description = 'Scrap (kg)'

    def pemakaian_pigment(self, obj):
        records = obj.detailmaterialconsumption_set.filter(bahan__group__in=self.id_pigment)
        pigment = records.aggregate(usage = Sum("qty_pakai"))
        return round_2(pigment["usage"])
    pemakaian_pigment.short_description = 'Pigment (kg)'

    def pemakaian_aditif(self, obj):
        records = obj.detailmaterialconsumption_set.filter(bahan__group__in=self.id_aditif)
        aditif = records.aggregate(usage = Sum("qty_pakai"))
        return round_2(aditif["usage"])
    pemakaian_aditif.short_description = 'Aditif (kg)'
    
    def persentase_scrap(self, obj):
        try:
            total_usage = obj.raw_material
            scrap_usage = obj.scrap_usage
            persen_scrap = scrap_usage/total_usage
        except:
            persen_scrap = 0
        return to_percent(persen_scrap)
    persentase_scrap.short_description = 'Scrap%'

class ProductionResultsMethod():
    def produk(self, obj):
        #detail = obj.detailproductionresults_set.all()
        #jenis_barang = '<br>'.join([i.produk.nama for i in detail])
        #jenis_barang = format_html(jenis_barang)
        try:
            detail = obj.detailproductionresults_set.first()
            jenis_barang = detail.produk
        except: 
            return None

        return jenis_barang
    
    def finished_good(self, obj):
        return round_2(obj.fg)
    finished_good.short_description = 'FG (kg)'

    def hold(self, obj):
        return round_2(obj.hold)
    hold.short_description = 'QC Hold (kg)'

    def reject(self, obj):
        return round_2(obj.reject)
    reject.short_description = 'Reject (kg)'
    
    def trimming(self, obj):
        return round_2(obj.trimming)
    trimming.short_description = 'Trimming (kg)'
    
    def waste(self, obj):
        return round_2(obj.waste)
    waste.short_description = 'Waste (kg)'


class RejectPackagingReportMethod():
    def daftar_reject(self, obj):
        daftar = []
        reject_packaging_inst = obj.detailpackagingusage_set.filter(reject__gt=0)
        for inst in reject_packaging_inst:
            pkg = inst.packaging.nama
            reject_qty = inst.reject
            isi = "{}\t\t\t: {}".format(pkg, reject_qty)
            daftar.append(isi)

        printout = format_html('<br>'.join(daftar))
        return printout

    
def hm_to_h(time_string):
    hm = time_string
    h = int(hm[:2])
    m = int(hm[3:])
    time = h+(m/60.0)
    return (time)

def calc_duration(mulai, selesai):
    durasi = datetime(1,1,10)
    dummy = date(1,1,1)
    awal = datetime.combine(dummy, mulai)
    akhir = datetime.combine(dummy, selesai)
    
    durasi += akhir - awal
    h = durasi.hour
    m = durasi.minute
    time = h+(m/60.0)
    return time

def none_to_0(num):
    if num is None:
        return 0
    else:
        return num

def round_2(num):
    if num is not None:
        return '{:,.2f}'.format(num)

def to_percent(data):
    if data == None: return "0 %"
    return "{0:.2%} ".format(data)

def warna_angka(angka):
    if angka < 0:
        return format_html('<mark>' + '{:,.2f}'.format(angka) + '</mark>')
    else: 
        return '{:,.2f}'.format(angka)

def warna_persen(angka):
    if angka <= .3 or angka > 1:
        return format_html('<mark>' + '{0:.2%}'.format(angka) + '</mark>')
    else: 
        return '{0:.2%}'.format(angka)

def warna_limit(angka, limit_bawah, limit_atas):
    if angka < limit_bawah or angka > limit_atas:
        return format_html('<mark>' + '{:,.2f}'.format(angka) + '</mark>')
    else: 
        return '{:,.2f}'.format(angka)
