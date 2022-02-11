from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from django.db.models import Count, Sum, F, Func, IntegerField, FloatField
from datetime import date, time, datetime
from django.db.models.deletion import PROTECT
from django.utils import timezone

from masterdata.models import MasterKapasitasMesin, MasterGroup
from form_maintenance.models import BreakdownEvent
from django.contrib.auth.models import Group as UserGroup

from django.urls import reverse
from django.core.mail import send_mail

import threading
from django.core.mail import EmailMessage

# id
id_foreman = 2
id_operator = 1

id_scrap = [2, 3, 36, 100, 113, 152, 159, 165]
id_rm = 1
id_fg = 2
id_wip = 3
id_pkg = 4
id_not_dark_grey = 2
id_common_user_group = 9999

id_downtime_istirahat = "IS"
id_downtime_idle = "ID"

id_user_pc = 1
id_user_kd = 2
id_user_acp = 3
id_user_upc_delta = 4
id_user_als = 5
id_user_oci = 6
id_user_upc_cpd = 41
id_user_upc_lc = 42
id_user_upc_g = 43
id_user_upc_r = 44

id_mesin_nok = [71, 72]

std_out_err_val = 0.00000000001


# Detail Table

class KK(models.Model):
    """Model for master table of WO number."""

    no_kk = models.CharField(
        max_length=20, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateField(default = timezone.now, verbose_name="Effective Date")
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    aktif = models.CharField(
        max_length=1,
        choices=(("0", "Closed"), ("1", "Aktif")),
        default=1,
    )
    is_export = models.CharField(
        max_length=1,
        choices=(("0", "Lokal"), ("1", "Eksport")),
    )
    item_example = models.ForeignKey("masterdata.MasterBarang", null=True, blank=True, on_delete=PROTECT,
        help_text="One example of product that is being produced")
    trial = models.BooleanField(default=False)
    cleaning = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "A1. Daftar KK"

    def __str__(self):
        return self.no_kk

    # KK UPC = 10 digit
    def clean(self):
        if "WOL" in  self.no_kk.upper() and len(self.no_kk) != 10:
            raise ValidationError("KK Harus 10 digit")

    def save(self, *args, **kwargs):
        if self.aktif == "0":
            self.split_rm(self)
        super().save(*args, **kwargs)

    def split_rm(self, kk):
        form_qs = kk.productionform_set.all()
        weight_factor = form_qs.aggregate(factor = Sum("raw_material") / (Sum("fg") + Sum("reject") + Sum("waste")))["factor"]
        fg_machine = form_qs.order_by().values("machine_id").annotate(fg=(Sum("fg") + Sum("reject") + Sum("waste")))
        for i in fg_machine:
            form = form_qs.filter(machine_id=i["machine_id"]).last()
            form.rm_split = i["fg"] * weight_factor
            form.save()

class DetailKKFinishedGood(models.Model):
    """Model representing the FG order in WO."""

    # Header
    no_kk = models.ForeignKey("KK", on_delete=models.CASCADE)

    # Detail
    produk = models.ForeignKey(
        "masterdata.MasterBarang",
        on_delete=models.PROTECT,
        limit_choices_to={"tipe__in": [id_fg, id_wip], "aktif": 1},
    )
    order_qty = models.FloatField(verbose_name="Order QTY (Sheet/ Pcs)")

    def __str__(self):
        return self.produk.nama

class DetailKKRawMaterial(models.Model):
    """Model representing the planned RM in WO."""

    # Header
    no_kk = models.ForeignKey("KK", on_delete=models.CASCADE)

    # Detail
    bahan = models.ForeignKey(
        "masterdata.MasterBarang",
        on_delete=models.PROTECT,
        limit_choices_to={"tipe__in": [id_rm, id_wip], "aktif": 1},
    )
    qty = models.FloatField(verbose_name="WO QTY")

class DetailMaterialConsumption(models.Model):
    """Model representing the detail of each material consumption."""

    # Header
    laporan = models.ForeignKey("ProductionForm", on_delete=models.CASCADE)

    # Detail
    bahan = models.ForeignKey(
        "masterdata.MasterBarang",
        on_delete=models.PROTECT,
        limit_choices_to={"tipe__in": [id_rm, id_wip], "aktif": 1},
    )
    batch_no = models.CharField(max_length=20, null=True, blank=True)
    qty_awal = models.FloatField(default=0, verbose_name="Awal (kg)")
    qty_tambahan = models.FloatField(default=0, verbose_name="Tambahan (kg)")
    qty_akhir = models.FloatField(default=0, verbose_name="Sisa (kg)")
    qty_pakai = models.FloatField(null=True, blank=True, verbose_name="Pakai (kg)")

    def save(self, *args, **kwargs):
        self.qty_pakai = self.qty_awal + self.qty_tambahan - self.qty_akhir
        self.qty_pakai = round(self.qty_pakai, 2)
        super(DetailMaterialConsumption, self).save(*args, **kwargs)

    def __str__(self):
        return self.laporan.tanggal_shift_kk()
'''
    def clean(self):
        self.save()
        laporan = self.laporan
        laporan.save()
        if abs(laporan.fg + laporan.reject + laporan.trimming + laporan.waste + laporan.hold - laporan.raw_material) > 20 :
            raise ValidationError("Selisih material dan hasil terlalu besar")
'''

class DetailProductionResults(models.Model):
    """Model representing the detail of production process."""

    # Header
    laporan = models.ForeignKey("ProductionForm", on_delete=models.CASCADE)

    # Detail
    produk = models.ForeignKey(
        "masterdata.MasterBarang",
        on_delete=models.PROTECT,
        limit_choices_to={"tipe__in": [id_fg, id_wip], "aktif": 1},
    )
    batch_no = models.CharField(max_length=20, null=True, blank=True)
    hasil_jadi_qty = models.FloatField()
    hold_qc_qty = models.FloatField(validators=[MinValueValidator(0)], default=0)
    berat_unit_sample = models.FloatField(
        default=0,
        verbose_name="Berat Per Unit",
        help_text="per lembar/ per kaleng/ dst",
    )
    reject = models.FloatField(default=0, verbose_name="Reject (kg)")
    trimming = models.FloatField(default=0, verbose_name="Trimming (kg)")
    waste = models.FloatField(default=0, verbose_name="Waste (kg)")

    fg_mass = models.FloatField(null=True, blank=True, default=0)
    hold_mass = models.FloatField(null=True, blank=True, default=0)
    total_output = models.FloatField(null=True, blank=True, default=0)
    fg_m2 = models.FloatField(null=True, blank=True, default=0)
    fg_lm = models.FloatField(null=True, blank=True, default=0)
    fg_mass_std = models.FloatField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        
        self.fg_mass = self.berat_unit_sample * self.hasil_jadi_qty
        self.hold_mass = self.berat_unit_sample * self.hold_qc_qty
        self.total_output = self.fg_mass + self.hold_mass + self.reject + self.trimming + self.waste

        self.fg_mass = round(self.fg_mass, 2)
        self.hold_mass = round(self.hold_mass, 2)
        self.total_output = round(self.total_output, 2)
        try:
            self.fg_lm = self.hasil_jadi_qty * self.produk.panjang / 1000
        except:
            self.fg_lm = 0
        
        try:
            self.fg_m2 = self.fg_lm * self.produk.lebar / 1000
        except:
            self.fg_m2 = 0
         
        try:
            self.fg_mass_std = self.hasil_jadi_qty * self.produk.berat_standar_fg
        except:
            self.fg_mass_std = 0
        super(DetailProductionResults, self).save(*args, **kwargs)

    def __str__(self):
        return self.laporan.tanggal_shift_kk()
    
    class Meta:
        verbose_name_plural = "Detail Production Results"


class DetailDowntime(models.Model):
    """Model representing the detail of downtime dan kejadian tertentu."""

    # Header
    laporan = models.ForeignKey("ProductionForm", on_delete=models.CASCADE)

    # Header
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    kategori = models.CharField(
        max_length=2,
        choices=[
            ("PU", "Production"),
            ("PS", "Set up"),
            ("PC", "Cleaning Color/ Machine"),
            ("TM", "Technic: Mechanic"),
            ("TE", "Technic: Electrical"),
            ("UT", "Utility Devices"),
            ("ML", "Mati Listrik/ Blackout"),
            ("LL", "Lain-lain/ Others"),
            ("IS", "Istirahat/ Break Time"),
            ("ID", "Idle/ Tunggu Order")
        ],
    )
    notes = models.TextField()
    durasi = models.FloatField(null=True, blank=True)
    form_breakdown = models.ForeignKey(BreakdownEvent, on_delete=PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.durasi = calc_duration(self.waktu_mulai, self.waktu_selesai)
        super(DetailDowntime, self).save(*args, **kwargs)

    def __str__(self):
        return self.laporan.tanggal_shift_kk()

    def clean(self):
        self.laporan.clean()
        if self.waktu_mulai is None or self.waktu_selesai is None  :
            raise ValidationError("WAKTU SALAH")
        
        durasi_form = calc_duration_from_dt(self.laporan.start_time, self.laporan.end_time)
        durasi_dt = calc_duration(self.waktu_mulai, self.waktu_selesai)
        if durasi_form < durasi_dt :
            raise ValidationError("Durasi Downtime lebih dari Durasi Form, cek start time dan end time header")


class DetailPackagingUsage(models.Model):
    """Model representing the detail of packaging rejects."""

    # Header
    laporan = models.ForeignKey("ProductionForm", on_delete=models.CASCADE)

    # Detail
    packaging = models.ForeignKey(
        "masterdata.MasterBarang",
        on_delete=models.PROTECT,
        limit_choices_to={
            "tipe__in": [
                id_pkg,
            ],
            "aktif": 1,
        },
    )
    terpakai = models.FloatField()
    reject = models.FloatField()

class ProductionForm(models.Model):
    """Model for representing the recap of daily production."""
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    shift = models.CharField(
        max_length=1,
        choices=(("1", "Shift 1"), ("2", "Shift 2"), ("3", "Shift 3")),verbose_name="# Shift"
    )
    machine = models.ForeignKey("masterdata.MasterMesin", on_delete=models.PROTECT)
    foreman = models.ForeignKey(
        "masterdata.MasterWorker",
        on_delete=models.PROTECT,
        limit_choices_to={"aktif": "1", "status": id_foreman},
        related_name="foreman",
        null=True,
        blank=True,
    )
    operator = models.ForeignKey(
        "masterdata.MasterWorker",
        on_delete=models.PROTECT,
        limit_choices_to={"aktif": "1", "status": id_operator},
        related_name="operator",
        null=True,
        blank=True,
        verbose_name="Operator Extruder"
    )
    no_kk = models.ForeignKey("KK", on_delete=models.PROTECT, limit_choices_to={"aktif": 1})
    dl_avail = models.FloatField(verbose_name="Jml Man Pwr")
    catatan = models.TextField(null=True, blank=True)

    ##### Calculated
    normalized_date = models.DateTimeField(null=True, blank=True)
    group_barang = models.ForeignKey(
        "masterdata.MasterGroup", null=True, blank=True, on_delete=models.PROTECT
    )
    tipe_barang = models.ForeignKey(
        "masterdata.MasterTipe", null=True, blank=True, on_delete=models.PROTECT
    )
    fg = models.FloatField(null=True, blank=True, default=0, verbose_name="FG (kg)")
    fg_mass_std = models.FloatField(null=True, blank=True, default=0, verbose_name="FG std (kg)")
    fg_lm = models.FloatField(null=True, blank=True, default=0)
    fg_m2 = models.FloatField(null=True, blank=True, default=0)
    fg_qty = models.FloatField(null=True, blank=True, default=0)
    hold = models.FloatField(null=True, blank=True, default=0, verbose_name="Hold (kg)")
    reject = models.FloatField(null=True, blank=True, default=0, verbose_name="Rj (kg)")
    waste = models.FloatField(null=True, blank=True, default=0, verbose_name="Wst (kg)")
    trimming = models.FloatField(null=True, blank=True, default=0, verbose_name="Trim (kg)")
    total_output = models.FloatField(null=True, blank=True, default=0, verbose_name="Rj (kg)")
    rm_split = models.FloatField(null=True, blank=True, default=0, verbose_name="RM Split By Machine (kg)")
    raw_material = models.FloatField(null=True, blank=True, default=0, verbose_name="RM (kg)")
    scrap_hasil = models.FloatField(null=True, blank=True, default=0, verbose_name="Scr Hsl (kg)")
    scrap_usage = models.FloatField(null=True, blank=True, default=0, verbose_name="Scr Usg (kg)")
    total_hour = models.FloatField(null=True, blank=True, default=0, verbose_name="Ttl Jam")
    effective_hour = models.FloatField(null=True, blank=True, default=0, verbose_name="Jam Eff")
    planned_down_hour = models.FloatField(null=True, blank=True, default=0, verbose_name="Jam Eff")
    downtime = models.FloatField(null=True, blank=True, default=0, verbose_name="Jam DwTm")
    earn_hour = models.FloatField(null=True, blank=True, default=0, verbose_name="Earn Hr")
    reject_eqv = models.FloatField(null=True, blank=True, default=0, verbose_name="Rj Eqv")
    output_std = models.FloatField(null=True, blank=True, verbose_name='Out Std')
    byproduct = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        #========================= TIME =========================#
        self.normalized_date = self.start_time - self.user_group.groupprofile.shift_hour

        planned_downtime_set = self.detaildowntime_set.filter(kategori__in=[id_downtime_istirahat, id_downtime_idle])
        durasi = planned_downtime_set.aggregate(total=Sum("durasi"))['total']
        if durasi is None:
            durasi = 0
        self.planned_down_hour = durasi
        self.planned_down_hour = round(self.planned_down_hour, 2)
        
        self.total_hour = calc_duration_from_dt(self.start_time, self.end_time) - self.planned_down_hour
        self.total_hour = round(self.total_hour, 2)
        
        downtime_set = self.detaildowntime_set.exclude(kategori__in=[id_downtime_istirahat, id_downtime_idle])
        durasi = downtime_set.aggregate(total=Sum("durasi"))['total']
        if durasi is None:
            durasi = 0
        self.downtime = durasi
        self.downtime = round(self.downtime, 2)
        
        self.effective_hour = self.total_hour - self.downtime
        self.effective_hour = round(self.effective_hour, 2)
        
        #========================= HASIL JADI =========================#
        production_result = self.detailproductionresults_set.all()

        metrics = {
            "fg_qty": Sum("hasil_jadi_qty", output_field=FloatField(),),
            "fg": Sum("fg_mass"),
            "fg_mass_std": Sum("fg_mass_std"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "reject": Sum("reject"),
            "trimming": Sum("trimming"),
            "waste": Sum("waste"),
            "hold": Sum("hold_mass"),
        }

        hasil = production_result.aggregate(**metrics)
        self.fg_qty = hasil["fg_qty"]
        self.fg = round_2(hasil["fg"])
        self.fg_mass_std = round_2(hasil["fg_mass_std"])
        self.fg_lm = round_2(hasil["fg_lm"])
        self.fg_m2 = round_2(hasil["fg_m2"])
        self.reject = round_2(hasil["reject"])
        self.trimming = round_2(hasil["trimming"])
        self.waste = round_2(hasil["waste"])
        self.hold = round_2(hasil["hold"])
        self.total_output = round_2(self.fg + self.hold + self.reject + self.trimming + self.waste)
        self.byproduct = round_2(self.reject + self.trimming + self.waste)

        if self.user_group_id in [id_user_als, id_user_oci]:
            self.waste += self.reject + self.trimming
            self.reject = 0
            self.trimming = 0

        production_result = self.detailproductionresults_set.first()

        if production_result:
            self.group_barang = production_result.produk.group
            self.tipe_barang = production_result.produk.tipe

        #========================= MATERIAL USAGE =========================#
        material_consumption = self.detailmaterialconsumption_set.all()

        metrics = {
            "raw": Sum("qty_pakai"),
        }
        if material_consumption:
            raw_material = material_consumption.aggregate(**metrics)
            self.raw_material = round_2(raw_material["raw"])
        else:
            self.raw_material = 0

        #========================= SCRAP =========================#
        scrap_instance = material_consumption.filter(bahan__group__kategori_rm__in=('scr', 'rpl'))

        metrics = {
            "raw": Sum("qty_pakai"),
        }
        
        if scrap_instance:
            scrap = scrap_instance.aggregate(**metrics)
            self.scrap_usage = scrap["raw"]
        else:
            self.scrap_usage = 0
        
        self.scrap_hasil = self.reject + self.trimming

        kk_item = self.no_kk.item_example
        if kk_item:
            if kk_item.group.kategori_rm == "rpl":
                self.scrap_hasil += self.fg
        
        #========================= EARN HOUR =========================#
        hasil = self.detailproductionresults_set.first()
        prev_output_std = self.output_std
        if hasil:
            produk = hasil.produk
            group = produk.group
            warna = produk.warna
            tebal = produk.tebal1
            dimensi_aux = produk.tebal2
            mesin = self.machine

            if self.user_group_id == id_user_acp:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(
                        mesin=mesin,
                        group=group,
                        tebal=tebal,
                        dimensi_aux=dimensi_aux,
                    )
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.filter(
                            mesin=mesin,
                            group=group,
                            tebal=tebal,
                        ).first()
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                        
                    except:
                        kapasitas_mesin = std_out_err_val

            if self.user_group_id == id_user_pc:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(
                        mesin=mesin, group=group, tebal=tebal, warna=warna
                    )
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(
                            mesin=mesin, group=group, tebal__isnull=True, warna=warna
                        )
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        try:
                            kapasitas_mesin = MasterKapasitasMesin.objects.get(
                                mesin=mesin,
                                group=group,
                                tebal__isnull=True,
                                warna=id_not_dark_grey,
                            )
                            kapasitas_mesin = kapasitas_mesin.output_ideal
                        except:
                            kapasitas_mesin = std_out_err_val

            if self.user_group_id == id_user_kd:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(
                        mesin=mesin, group=group, tebal=round(tebal)
                    )
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    kapasitas_mesin = std_out_err_val

            if self.user_group_id == id_user_als:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val

            if self.user_group_id == id_user_oci:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    kapasitas_mesin = std_out_err_val
            
            if self.user_group_id == id_user_upc_delta:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val
            
            if self.user_group_id == id_user_upc_cpd:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val
            
            if self.user_group_id == id_user_upc_lc:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val
            
            if self.user_group_id == id_user_upc_g:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val

            if self.user_group_id == id_user_upc_r:
                try:
                    kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group=group)
                    kapasitas_mesin = kapasitas_mesin.output_ideal
                except:
                    try:
                        kapasitas_mesin = MasterKapasitasMesin.objects.get(mesin=mesin, group__isnull=True)
                        kapasitas_mesin = kapasitas_mesin.output_ideal
                    except:
                        kapasitas_mesin = std_out_err_val
            
            if self.user_group_id in [id_user_oci, id_user_als] or self.machine_id in id_mesin_nok: 
                self.earn_hour = self.fg_qty / kapasitas_mesin
            else:
                self.earn_hour = self.fg / kapasitas_mesin
            self.earn_hour = round(self.earn_hour, 2)

            if kapasitas_mesin == std_out_err_val and kapasitas_mesin != prev_output_std:
                error_mail_message = "Dear Bapak/ Ibu,\nSistem OEE mencatat ada kesalahan pengisian pada form berikut ini:\n\nLink = {link}\nKK = {kk}\nMesin = {mesin}\nProduk = {produk} \n\n\nSehingga output standar yang tercatat diisi dengan nilai lain. Mohon konfirmasinya pada divisi IT yang memelihara sistem OEE.\n\nSalam"

                url = reverse('admin:%s_%s_change' % ("form_produksi", "productionform"), args=[self.id])
                url = "http://36.94.100.6" + url
                error_mail_message = error_mail_message.format(link=url, kk=self.no_kk.no_kk, mesin=self.machine.mesin, produk=produk.nama)

                send_html_mail(
                    "Possible Input Mistake on Impack Production Information System",
                    error_mail_message,
                    [self.user_group.groupprofile.admin_email],
                    "oee.notification@impack-pratama.com",)
        else:
            kapasitas_mesin = 0
            self.earn_hour = 0
        #========================= Item of WO =========================#
        if self.no_kk.item_example is None and hasil:
            self.no_kk.item_example_id = hasil.produk_id
            self.no_kk.save()

        

        self.output_std = kapasitas_mesin
        
        #========================= REJECT EQUIVALENT =========================#
        if self.user_group_id == id_user_oci:
            packaging_instances = self.detailpackagingusage_set.all()
            metrics1 = {
                "pkg_eqv": Sum(
                    F("reject") * F("packaging__bobot_reject"), output_field=FloatField()
                ),
            }
            production_instances = self.detailproductionresults_set.all()
            metrics2 = {
                "rm_eqv": Sum(
                    F("reject") * F("produk__bobot_reject"), output_field=FloatField()
                ),
            }

            if packaging_instances:
                agregat = packaging_instances.aggregate(**metrics1)
                pkg_eqv = agregat["pkg_eqv"]
            else:
                pkg_eqv = 0
            
            if production_instances:
                agregat = production_instances.aggregate(**metrics2)
                rm_eqv = agregat["rm_eqv"]
            else:
                rm_eqv = 0
            self.reject_eqv = round(pkg_eqv + rm_eqv, 2)


        super(ProductionForm, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-start_time"]
        verbose_name_plural = "A2. Form dan Report by Shift"

    def tanggal_shift_kk(self):
        return "{} {} {}".format(str(self.start_time), self.shift, self.no_kk)

    def __str__(self):
        return self.tanggal_shift_kk()
    
    def clean(self):
        if self.start_time is None or self.end_time is None  :
            raise ValidationError("WAKTU SALAH")

        if self.start_time > self.end_time :
            raise ValidationError("WAKTU MULAI MENDAHULUI WAKTU SELESAI")

        # dt = none_as_zero(self.downtime) + none_as_zero(self.planned_down_hour)
        # if dt > self.total_hour:
        #     raise ValidationError("DOWNTIME LEBIH BESAR DARI WAKTU START-END FORM")

'''
        if ProductionForm.objects.filter(machine=self.machine, start_time=self.start_time).exclude(id=self.id).exists():
            raise ValidationError("LAPORAN DENGAN MESIN DAN JAM SAMA SUDAH ADA, CARI LAPORAN DI DAFTAR FORM")
'''

def none_as_zero(a):
    if type(a) == None:
        return 0
    else:
        return a


def calc_duration(mulai, selesai):
    durasi = datetime(1, 1, 10)
    dummy = date(1, 1, 1)
    awal = datetime.combine(dummy, mulai)
    akhir = datetime.combine(dummy, selesai)

    durasi += akhir - awal
    h = durasi.hour
    m = durasi.minute
    time = h + (m / 60.0)
    time = round(time, 2)
    return time

def calc_duration_from_dt(mulai, selesai):
    time = selesai - mulai
    time = time.total_seconds() / 3600
    time = round(time, 2)
    return time

def round_2(angka):
    if angka is None:
        return 0
    else:
        return round(angka, 2)

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()

def send_html_mail(subject, html_content, recipient_list, sender):
    EmailThread(subject, html_content, recipient_list, sender).start()