from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import Group, User

id_foreman = 1
id_operator = 2
id_scrap = 2
id_rm = 1
id_fg = 2
id_wip = 3
id_not_dark_grey = 2
id_group_type_unit = '1'

#================ AUTH MODELS =================#

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_group = models.ForeignKey(Group, on_delete=models.PROTECT, blank=True, null=True, related_name="main_ug", limit_choices_to={'groupprofile__group_type': id_group_type_unit}, help_text="Grup Pabrik yang akan menjadi identitas form yang diisi user")
    factory_group = models.ManyToManyField(Group, related_name="other_ug", limit_choices_to={'groupprofile__group_type': id_group_type_unit}, help_text="Grup Pabrik yang bisa dipakai untuk filter laporan")

class GroupProfile(models.Model):
    user_group = models.OneToOneField(Group, on_delete=models.CASCADE)
    group_type = models.CharField(
        max_length=1,
        choices=(
            ("1", "Unit"),
            ("0", "Jabatan"),
        ),
    )
    shift_hour = models.DurationField(help_text="Jam mulai kerja shift pertama, mis: 07:00:00")
    daily_work_hour = models.FloatField(help_text="Lama jam kerja dari unit dalam sehari")
    weekly_days = models.CharField(max_length=7, help_text="Isi dengan 1111111 jika grup aktif senin-minggu, 1111100 jika grup aktif senin-jumat, dst (1=Kerja, 0=Libur)")
    admin_email = models.CharField(max_length=256, blank=True, null=True)

class DayOffList(models.Model):
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    off_day = models.DateField()
    notes = models.CharField(
        max_length=50,
    )
    def __str__(self):
        return "{}: {} - {}".format(self.user_group, self.off_day, self.notes)

    class Meta:
        ordering = ['-off_day']


#================ MASTERDATA MODELS =================#

class MasterWorker(models.Model):
    """Model for master table of Operator Names."""

    nama = models.CharField(
        max_length=50,
    )
    status = models.ForeignKey("MasterStatus", on_delete=models.PROTECT)
    aktif = models.CharField(
        max_length=1,
        choices=(
            ("1", "Aktif"),
            ("0", "Inaktif"),
        ),
    )
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Master Workers"
        ordering = ['nama']


class MasterStatus(models.Model):
    """Model for master table of Worker Status."""

    # status_id = models.CharField(max_length=2, unique=True)
    status = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Master Worker Status"


class MasterKapasitasMesin(models.Model):
    """Model for master table of Machine Output Capacity."""

    user_group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        limit_choices_to={'groupprofile__group_type': id_group_type_unit}
    )
    mesin = models.ForeignKey(
        "MasterMesin",
        on_delete=models.PROTECT,
    )
    group = models.ForeignKey(
        "MasterGroup", on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={"tipe__in": [2,3]}, verbose_name="Item Group"
    )
    warna = models.ForeignKey(
        "MasterWarna", on_delete=models.PROTECT, null=True, blank=True
    )
    tebal = models.FloatField(blank=True, null=True, verbose_name="Thickness (mm)")
    dimensi_aux = models.FloatField(blank=True, null=True, verbose_name="Other Dimension (mm)")
    item_property = models.ForeignKey(
        "MasterItemProperty", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Property Lain"
    )
    output_ideal = models.FloatField(default=0, verbose_name="Output Standar (kg/h or pcs/h)")
    dl_standar = models.FloatField(verbose_name="DL Standar (Person)")

    def __str__(self):
        return "{} {}".format(self.mesin, self.group)

    class Meta:
        verbose_name_plural = "Master Machine Capacity"


class MasterMesin(models.Model):
    """Model for master table of Machine Names."""

    # mesin_id = models.CharField(max_length=5, unique=True)
    mesin = models.CharField(
        max_length=30,
    )
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT, limit_choices_to={'groupprofile__group_type': id_group_type_unit})
    add_date = models.DateField()
    priority = models.CharField(
        max_length=1,
        choices=(
            ("1", "Main Machine"),
            ("2", "Secondary Machine"),
        ),
    )

    def __str__(self):
        return self.mesin

    class Meta:
        verbose_name_plural = "Master Machine"
        ordering = ['mesin']


class MasterItemProperty(models.Model):
    """Model for master table of Profil or ACP Core."""

    item_property = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name_plural = "Master Item Property"

    def __str__(self):
        return self.item_property


class MasterBarang(models.Model):
    """Model for master table of Product Names and Part Number."""

    nama = models.CharField(
        max_length=70,
    )
    kode_barang = models.CharField(max_length=50, unique=True)
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT, limit_choices_to={'groupprofile__group_type': id_group_type_unit})
    tipe = models.ForeignKey("MasterTipe", on_delete=models.PROTECT)
    group = models.ForeignKey("MasterGroup", on_delete=models.PROTECT, verbose_name="Item Group")
    berat_standar_fg = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Berat Standar (FG)", help_text="Jika RM, isi 0")
    panjang = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Panjang (mm)"
    )
    tebal1 = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Tebal Utama (mm)")
    tebal2 = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True,
        verbose_name="Tebal Lain (mm)", help_text="Untuk ACP: tebal Aluminum Layer")
    lebar = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Lebar Efektif (mm) / Diameter (inch)", 
        help_text="Lebar dalam keadaan Korugasi (Misal lebar efektif Alderon 830 = 830MM). \nJika Pipa, isikan diameter Pipa dalam Inch")
    lebar_ext = models.FloatField(
        validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="Lebar Bentang (mm)", 
        help_text="Lebar barang jika dibentangkan, seharusnya lebih besar dari lebar utama (Misal lebar bentang Alderon 830 = 892MM)"
    )
    gsm = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="GSM (gram/m^2)")
    bobot_reject = models.FloatField(default=1000, blank=True, null=True, verbose_name="Bobot Reject (OCI only)")
    warna = models.ForeignKey(
        "MasterWarna", on_delete=models.PROTECT, blank=True, null=True
    )
    profil = models.ForeignKey("MasterItemProperty", on_delete=models.PROTECT)
    uom = models.ForeignKey("MasterUOM", on_delete=models.PROTECT)
    aktif = models.CharField(
        max_length=1,
        choices=(
            ("1", "Aktif"),
            ("0", "Inaktif"),
        ),
    )

    class Meta:
        verbose_name_plural = "Master Barang"

    def __str__(self):
        return self.nama + " - " + self.kode_barang + " - Wt: " + str(self.berat_standar_fg)

    class Meta:
        verbose_name_plural = "Master Item"


class MasterTipe(models.Model):
    """Model for master table of Item Type."""

    tipe = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name_plural = "Master Tipe"

    def __str__(self):
        return self.tipe

    class Meta:
        verbose_name_plural = "Master Item Type"
        ordering = ['tipe']


class MasterGroup(models.Model):
    """Model for master table of Item group."""

    group = models.CharField(
        max_length=40, verbose_name="Item Group"
    )
    tipe = models.ForeignKey("MasterTipe", on_delete=models.PROTECT)
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT, limit_choices_to={'groupprofile__group_type': id_group_type_unit})
    kategori_rm = models.CharField(null=True, blank=True, 
        max_length=3,
        choices=(
            ("frs", "Fresh"),
            ("scr", "Scrap"),
            ("pgm", "Pigment"),
            ("adt", "Aditif"),
            ("flr", "Filler"),
            ("adk", "Adukan"),
            ("rpl", "Repellet"),
            ("msk", "Masking"),
            
        ),
    )

    def __str__(self):
        return self.group

    class Meta:
        verbose_name_plural = "Master Item Group"
        ordering = ['group']


class MasterWarna(models.Model):
    """Model for master table of Item Colour."""

    warna = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name_plural = "Master Item Color"

    def __str__(self):
        return self.warna


class MasterUOM(models.Model):
    """Model for master table of Unit of Measurements."""

    uom = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return self.uom

    class Meta:
        verbose_name_plural = "Master UOM"
        ordering = ['uom']

