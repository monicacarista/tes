from datetime import date, datetime
from email.mime import application
import inspect
from django.db import models
from django.utils.timezone import now
from masterdata.models import MasterBarang, MasterMesin, MasterGroup
from form_produksi.models import KK
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

# Create your models here.
class QCForm(models.Model):
    shift_choices=(
    ('1','1'),
    ('2', '2'),
    ('3','3'),
    )
    n_choices=(
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10'),
        (11,'11'),
        (12,'12'),
        (13,'13'),
        (14,'14'),
    )
    item_group = models.ForeignKey(MasterGroup, default=None, on_delete = models.CASCADE,  verbose_name="Grup Produk",null=True)
    no_kk = models.ForeignKey(KK, default=None, on_delete = models.CASCADE,  verbose_name="No KK")
    user_group = models.ForeignKey(Group,default=None, on_delete=models.CASCADE,  verbose_name="Unit")
    item =models.ForeignKey(MasterBarang,default=None, on_delete=models.CASCADE, verbose_name="Kode Barang")
    shift = models.CharField(max_length=1, default="pilih salah satu", choices=shift_choices)
    qc_inspector= models.ForeignKey('QCInspector', default=None, on_delete=models.CASCADE)
    inspection_date = models.DateField('Tanggal Pengecekan',default=now, blank=True)
    inspection_time = models.DateTimeField('Waktu Pengecekan', default=now,blank=True, null=True)
    customer = models.CharField(max_length=30,default=None, blank=True, null=True)
    machine = models.ForeignKey(MasterMesin,max_length=30, default=None, on_delete=models.CASCADE)
    pengecekan_ke=models.IntegerField(max_length=2,default=0, choices=n_choices)
    
    def save(self, *args, **kwargs):
        self.inspection_date = self.inspection_time.date()
        self.clean()
        return super().save()
    
    def __str__(self):
         return '{} {}'.format(self.shift, self.inspection_date)
    class Meta:
       
        verbose_name = 'Form Pengecekan'
        unique_together = [("pengecekan_ke", "inspection_date", "machine","shift")]

class QCInspector(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = 'OperatorQC'
    def __str__(self):
         return self.name

class RejectFormSelection(models.Model):
    aspek_fungsional=  (
        ('fungsional','Fungsional'), 
        ('estetika', 'Estetika')
    )
    aspek_parameter =(
        ('dimensi','Dimensi'),
        ('atribut','Atribut')
    )
    aspek_critical=(
        ('critical','Critical'),
        ('non_critical','Non Critical')
    )

    item_group = models.ForeignKey(MasterGroup, default=None, on_delete=models.CASCADE,  verbose_name="Grup Produk")
    reject_type = models.ForeignKey('MasterReject', default=None, on_delete=models.CASCADE,  verbose_name="Jenis Reject")
    aspekFungsional = models.CharField(max_length=50, default="pilih salah satu", choices=aspek_fungsional, verbose_name= "Aspek Fungsional")
    aspekParameter = models.CharField(max_length=50, default="pilih salah satu", choices=aspek_parameter, verbose_name= "Aspek Parameter")
    aspekCritical = models.CharField(max_length=50, default="pilih salah satu", choices=aspek_critical, verbose_name= "Aspek Critical")
    def __str__(self):
        return self.reject_type.__str__()

class MasterReject(models.Model):
   
    item_group = models.ForeignKey(MasterGroup, verbose_name="Grup Produk",default=None, on_delete=models.CASCADE)
    reject_type = models.CharField(max_length=50, default=None, verbose_name = "Jenis Reject")
   
  
    class Meta:
        verbose_name = 'Master Reject'
    def __str__(self):
         return self.reject_type

class MasterFormParameter(models.Model):
    qc_parameter = models.CharField(max_length= 100,default=None,  verbose_name="Parameter Pengecekan")
    
    def __str__(self):
         return self.qc_parameter


class ParameterFormSelection(models.Model):
      item_group = models.ForeignKey(MasterGroup, default=None, on_delete=models.CASCADE,  verbose_name="Grup Produk")
      selected_field = models.ForeignKey('MasterFormParameter',  verbose_name="Parameter yang Dipilih", default=None, on_delete=models.CASCADE)
      note = models.CharField(max_length=100, default=None,  verbose_name= "Keterangan")
      kategori = models.CharField(max_length=100, default=None,  verbose_name= "Kategori")

      def __str__(self):
         return self.selected_field.__str__()
         

class DetailQCInspection(models.Model):
    qc_form=models.ForeignKey('QCForm',null=True, default=None, on_delete=models.CASCADE)
    selected_fields=models.ForeignKey('ParameterFormSelection',null=True, default=None, on_delete=models.CASCADE)
    dimensi1=models.FloatField(default=0,max_length=4)
    dimensi2=models.FloatField(default=0,max_length=4)
    dimensi3=models.FloatField(default=0,max_length=4)
    dimensi4=models.FloatField(default=0,max_length=4)
    dimensi5=models.FloatField(default=0,max_length=4)
    dimensi6=models.FloatField(default=0,max_length=4)
    dimensi7=models.FloatField(default=0,max_length=4)
    dimensi8=models.FloatField(default=0,max_length=4)
    dimensi9=models.FloatField(default=0,max_length=4)
    dimensi10=models.FloatField(default=0,max_length=4)
    dimensi11=models.FloatField(default=0,max_length=4)
    dimensi12=models.FloatField(default=0,max_length=4)
    dimensi13=models.FloatField(default=0,max_length=4)
    dimensi14=models.FloatField(default=0,max_length=4)
    dimensi15=models.FloatField(default=0,max_length=4)
    dimensi16=models.FloatField(default=0,max_length=4)
    dimensi17=models.FloatField(default=0,max_length=4)
    dimensi18=models.FloatField(default=0,max_length=4)
    dimensi19=models.FloatField(default=0,max_length=4)
    dimensi20=models.FloatField(default=0,max_length=4)
    dimensi21=models.FloatField(default=0,max_length=4)
    dimensi22=models.FloatField(default=0,max_length=4)
    dimensi23=models.FloatField(default=0,max_length=4)
    dimensi24=models.FloatField(default=0,max_length=4)
    dimensi25=models.FloatField(default=0,max_length=4)
    dimensi26=models.FloatField(default=0,max_length=4)
    dimensi27=models.FloatField(default=0,max_length=4)
    dimensi28=models.FloatField(default=0,max_length=4)
    dimensi29=models.FloatField(default=0,max_length=4)
    dimensi30=models.FloatField(default=0,max_length=4)
    dimensi31=models.FloatField(default=0,max_length=4)
    dimensi32=models.FloatField(default=0,max_length=4)
    dimensi33=models.FloatField(default=0,max_length=4)
    dimensi34=models.FloatField(default=0,max_length=4)
    dimensi35=models.FloatField(default=0,max_length=4)
    dimensi36=models.FloatField(default=0,max_length=4)
    dimensi37=models.FloatField(default=0,max_length=4)
    dimensi38=models.FloatField(default=0,max_length=4)
    dimensi39=models.FloatField(default=0,max_length=4)
    dimensi40=models.FloatField(default=0,max_length=4)
    dimensi41=models.FloatField(default=0,max_length=4)
    dimensi42=models.FloatField(default=0,max_length=4)
    dimensi43=models.FloatField(default=0,max_length=4)
    dimensi44=models.FloatField(default=0,max_length=4)
    dimensi45=models.FloatField(default=0,max_length=4)
    dimensi46=models.FloatField(default=0,max_length=4)
    dimensi47=models.FloatField(default=0,max_length=4)
    dimensi48=models.FloatField(default=0,max_length=4)
    dimensi49=models.FloatField(default=0,max_length=4)
    dimensi50=models.FloatField(default=0,max_length=4)
    dimensi51=models.FloatField(default=0,max_length=4)
    dimensi52=models.FloatField(default=0,max_length=4)
    dimensi53=models.FloatField(default=0,max_length=4)
    dimensi54=models.FloatField(default=0,max_length=4)
    dimensi55=models.FloatField(default=0,max_length=4)
    dimensi56=models.FloatField(default=0,max_length=4)
    dimensi57=models.FloatField(default=0,max_length=4)
    dimensi58=models.FloatField(default=0,max_length=4)
    dimensi59=models.FloatField(default=0,max_length=4)
    dimensi60=models.FloatField(default=0,max_length=4)
    light_transmission =models.FloatField(default=0)
    squareness1 =models.FloatField(default=0)
    squareness2 =models.FloatField(default=0)
    kelengkungan = models.FloatField(default=0)
    bowing_max=models.FloatField(default=0)
    uji_lock=models.FloatField(default=0)
    gsm =models.FloatField(default=0)
    machine_rpm = models.FloatField(default=0)
    machine_pressure =models.FloatField(default=0)
    machine_torque = models.FloatField(default=0)
    uv_pinggir = models.FloatField(default=0)
    uv_tengah = models.FloatField(default=0)
    uv_inkjet = models.FloatField(default=0)
    corona_treatment_atas = models.FloatField(default=0)
    corona_treatment_bawah = models.FloatField(default=0)
    tekanan_maks_hidrostatik = models.FloatField(default=0)
    tekanan_maks_burst = models.FloatField(default=0)
    viskositas_atas = models.FloatField(default=0)
    viskositas_bawah = models.FloatField(default=0)
    solid_content = models.FloatField(default=0)
    ph = models.FloatField(default=0)
    rheovis_qty = models.FloatField(default=0)
    fineness_pre_adjusting = models.FloatField(default=0)
    fineness_post_adjusting = models.FloatField(default=0)
    bonding_strength_coil_atas = models.FloatField(default=0)
    bonding_strength_coil_bwh =models.FloatField(default=0)
    speed_extruder_adhesive = models.FloatField(default=0)
    berat1 =models.FloatField(default=0)
    berat2 =models.FloatField(default=0)
    berat3 =models.FloatField(default=0)
    berat4 =models.FloatField(default=0)
    berat5 =models.FloatField(default=0)
    skin_time = models.FloatField(default=0)
    uv_absorber =  models.FloatField(default=0)
    lembar = models.IntegerField(default=0)
    reject_indecisive = models.ManyToManyField('RejectFormSelection', related_name='ragu')
    reject = models.ManyToManyField('MasterReject', related_name='reject')
    komentar = models.CharField(max_length=250,default=None, blank=True, null=True)
    class Meta:
        verbose_name = 'Detail Pengecekan'
        verbose_name_plural = 'DetailQCInspection'
    def get_reject(self):
         return ",".join([str(p) for p in self.reject.all()])
    # def __str__(self):
    #      return self.dimensi1
