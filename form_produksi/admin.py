import time
import calendar
import numbers
import numpy as np
from calendar import Calendar, monthrange
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

from django.contrib import admin
from django.contrib.admin import widgets, SimpleListFilter
from django.contrib.auth.models import Group as UserGroup
from django.contrib.admin.options import ModelAdmin, TabularInline
from django.apps import apps

from django import forms
from django.forms import Textarea, TextInput, ModelForm

from django.urls import reverse
from django.template.response import SimpleTemplateResponse
from django.urls import path

from django.utils.html import format_html
from django.utils.http import urlencode

from django.db import models
from django.db.models.functions import Trunc
from django.db.models import Sum, F, Q, Min, Max
from django.db.models.aggregates import Count

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from rangefilter.filters import DateRangeFilter

from masterdata.models import MasterWorker, MasterStatus, MasterMesin

from masterdata.models import (
    MasterBarang,
    MasterGroup,
    DayOffList
)
from form_produksi.models import (
    KK,
    ProductionForm,
    DetailKKFinishedGood,
    DetailKKRawMaterial,
    DetailDowntime,
    DetailMaterialConsumption,
    DetailProductionResults,
    DetailPackagingUsage,
)
from .list_disp_methods import KKReportMethod, ShiftReportMethod, DowntimeReportMethod
from .list_disp_methods import MaterialConsumptionMethod, ProductionResultsMethod, RejectPackagingReportMethod


# ============================ Dict of ids ============================ #
id_scrap = 2
id_rm = 1
id_fg = 2
id_wip = 3
id_pkg = 4
id_oci_user = 6
list_need_packaging_inline = [1, 2, 3, 4, 5, 6]
id_unit_group = "1"
n_report = 20

# ============================ Dict of table columns ============================ #
col = {
    "kk_aktif": "KK Status",
    "month_executed": "Month Executed",
    "item": "Item Name",
    "item_group": "Item Group",
    "item_code": "Item Code",
    "eff_hour": "Eff Hour (hr)",
    "dt": "Downtime (hr)",
    "idle": "Idle Time (hr)",
    "rm": "Raw Material (kg)",
    "fg": "FG (kg)",
    "fg_lm": "FG (LM)",
    "fg_m2": "FG (M2)",
    "fg_qty": "FG Qty",
    "fg_theory": "FG Theory (kg)",
    "tr": "Trimming (kg)",
    "rj": "Reject (kg)",
    "ws": "Waste (kg)",
    "scrap_chg": "Scrap Chg (kg)",
    "scrap_use": "Scrap Used (kg)",
    "scrap_prod": "Scrap Created (kg)",
    "mat_diff": "Material Differences (kg)",
    "mat_eff": "Material Efficiency",
    "fty": "FTY",
    "avail": "Avail",
    "perf": "Perf",
    "oee": "OEE",
    "FTY": "FTY",
    "weight": "Weight (kg)",
    "qty": "Qty",
    "wo": "WO Number",
    "machine": "Machine Name",
    "date": "Date",
    "category": "Category",
    "date": "Date"
}

# ============================ Signals ============================#
# region


@receiver(post_delete, sender=DetailMaterialConsumption)
def delete_mat_con(sender, instance, using, **kwargs):
    try:
        instance.laporan.save()
    except:
        pass


@receiver(post_delete, sender=DetailProductionResults)
def delete_prod_res(sender, instance, using, **kwargs):
    try:
        instance.laporan.save()
    except:
        pass


@receiver(post_delete, sender=DetailDowntime)
def delete_downtime(sender, instance, using, **kwargs):
    try:
        instance.laporan.save()
    except:
        pass


@receiver(post_delete, sender=DetailPackagingUsage)
def delete_pkg_usg(sender, instance, using, **kwargs):
    try:
        instance.laporan.save()
    except:
        pass


@receiver(post_save, sender=DetailMaterialConsumption)
def save_mat_con(sender, instance, created, raw, using, update_fields, **kwargs):
    instance.laporan.save()


@receiver(post_save, sender=DetailProductionResults)
def save_prod_res(sender, instance, created, raw, using, update_fields, **kwargs):
    instance.laporan.save()


@receiver(post_save, sender=DetailDowntime)
def save_downtime(sender, instance, created, raw, using, update_fields, **kwargs):
    instance.laporan.save()


@receiver(post_save, sender=DetailPackagingUsage)
def save_pkg_usg(sender, instance, created, raw, using, update_fields, **kwargs):
    instance.laporan.save()
# endregion


# ============================ Actions ============================#
# region

def make_closed(modeladmin, request, queryset):
    queryset.update(aktif='0')


make_closed.allowed_permissions = ('change',)


def make_closed_and_split_rm(modeladmin, request, queryset):
    for i in queryset:
        i.aktif = '0'
        i.save()


make_closed_and_split_rm.allowed_permissions = ('change',)


def make_active(modeladmin, request, queryset):
    queryset.update(aktif='1')


make_active.allowed_permissions = ('change',)


def duplicate(modeladmin, request, queryset):
    for self in queryset:
        fks_to_copy = list(self.detailmaterialconsumption_set.all())

        self.pk = None
        self.start_time = datetime(1945, 8, 17, 10, 30)

        self.save()

        new_pk = self.pk

        foreign_keys = {}
        for fk in fks_to_copy:
            fk.pk = None
            fk.laporan = ProductionForm.objects.get(id=new_pk)

            try:
                foreign_keys[fk.__class__].append(fk)
            except KeyError:
                foreign_keys[fk.__class__] = [fk]

        for cls, list_of_fks in foreign_keys.items():
            cls.objects.bulk_create(list_of_fks)


duplicate.allowed_permissions = ('change',)


def refresh_fg_calculation(modeladmin, request, queryset):
    production_list = queryset.values("detailproductionresults")
    production_list = DetailProductionResults.objects.filter(id__in=production_list)
    for obj in production_list:
        obj.save()

refresh_fg_calculation.allowed_permissions = ('change',)

def refresh(modeladmin, request, queryset):
    queryset.values
    for obj in queryset:
        obj.save()


refresh.allowed_permissions = ('change',)
# endregion

# ============================ Auto Complete Select ============================#
# region
# Used to do a filter by limit choices to in the fields line


class AutocompleteSelect(widgets.AutocompleteSelect):
    def __init__(
        self, rel, admin_site, attrs=None, choices=(), using=None, for_field=None
    ):
        super().__init__(rel, admin_site, attrs=attrs, choices=choices, using=using)
        self.for_field = for_field

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.update({"data-ajax--delay": 500})
        if "style" not in base_attrs:
            attrs.update({"style": "width: 350px;"})
        return attrs
# endregion

# ============================ Custom Filter ============================#

# region


class UserGroupFilter(SimpleListFilter):
    title = "Factory Unit"
    parameter_name = "user_group__id__exact"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        daftar_unit = request.user.userprofile.factory_group.filter(
            groupprofile__group_type=id_unit_group).order_by('name')
        return [(unit.id, unit.name) for unit in daftar_unit]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_group__id=self.value())
        else:
            return queryset


class MesinFilter(SimpleListFilter):
    title = "Mesin"
    parameter_name = "machine__id__exact"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_mesin = MasterMesin.objects.filter(
            user_group__id=selected_user).order_by('mesin')
        return [(mesin.id, mesin.mesin) for mesin in daftar_mesin]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(machine__id=self.value())
        else:
            return queryset


class WorkerFilter(SimpleListFilter):
    title = "Worker"
    parameter_name = "worker__id"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_worker = MasterWorker.objects.filter(
            user_group__id=selected_user).order_by('nama')
        return [(worker.id, worker.nama) for worker in daftar_worker]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(foreman__id=self.value()) | Q(operator__id=self.value()))
        else:
            return queryset


class ProductFilter(SimpleListFilter):
    title = "Product"
    parameter_name = "produk_id"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_group = MasterGroup.objects.filter(user_group__id=selected_user).filter(
            tipe__in=[id_wip, id_fg]
        ).order_by('group')
        return [(group.id, group.group) for group in daftar_group]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(no_kk__item_example__group_id=self.value())
        else:
            return queryset


class KKItemGroupFilter(SimpleListFilter):
    title = "Product Group"
    parameter_name = "item_example__group"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_group = MasterGroup.objects.filter(user_group__id=selected_user).filter(
            tipe__in=[id_wip, id_fg]
        ).order_by('group')
        return [(group.id, group.group) for group in daftar_group]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(item_example__group_id=self.value())
        else:
            return queryset


class ItemGroupFilter(SimpleListFilter):
    title = "Item Group"
    parameter_name = "barang_id"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_group = MasterGroup.objects.filter(user_group__id=selected_user).all(
        ).order_by('group')
        return [(group.id, group.group) for group in daftar_group]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(no_kk__item_example__group_id=self.value())
        else:
            return queryset


class WIPFilter(SimpleListFilter):
    title = "WIP / FG"
    parameter_name = "tipe__id"

    def lookups(self, request, model_admin):
        tipe = (
            (3, "WIP Only"),
            (2, "FG Only"),
        )
        return tipe

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(no_kk__item_example__tipe_id=self.value())
        else:
            return queryset


class WIPCustomFilter(SimpleListFilter):
    title = "WIP / FG"
    parameter_name = "tipe__id"

    def lookups(self, request, model_admin):
        tipe = (
            (3, "WIP Only"),
            ('all', "All"),
        )
        return tipe

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() != None:
            return queryset.filter(no_kk__item_example__tipe_id=self.value())
        else:
            return queryset.filter(no_kk__item_example__tipe_id=2)

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'FG Only'
        return choices


'''
class KKFilter(SimpleListFilter):
    title = "KK"
    parameter_name = "no_kk__id__exact"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_mesin = MasterMesin.objects.filter(user_group__id=selected_user)
        return [(mesin.id, mesin.mesin) for mesin in daftar_mesin]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(machine__id=self.value())
        else:
            return queryset
'''


class ExportFilter(SimpleListFilter):
    title = "Export"
    parameter_name = "is_export__id"

    def lookups(self, request, model_admin):
        is_eksport = (
            (0, "Local"),
            (1, "Export"),
        )
        return is_eksport

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(no_kk__is_export=self.value())
        else:
            return queryset


class ClosedCustomFilter(SimpleListFilter):
    title = "WO Status"
    parameter_name = "no_kk__aktif"

    def lookups(self, request, model_admin):
        trial = (
            ("0", "WO Closed"),
            ('all', "All"),
        )
        return trial

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() != None:
            return queryset.filter(no_kk__aktif=self.value())
        else:
            return queryset.filter(no_kk__aktif="1")

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'WO Active'
        return choices


class TrialFilter(SimpleListFilter):
    title = "Trial"
    parameter_name = "trial"

    def lookups(self, request, model_admin):
        trial = (
            (False, "Non Trial"),
            (True, "Trial"),
        )
        return trial

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(no_kk__trial=self.value())
        else:
            return queryset


class TrialCustomFilter(SimpleListFilter):
    title = "Trial"
    parameter_name = "trial"

    def lookups(self, request, model_admin):
        trial = (
            (True, "Trial"),
            ('all', "All"),
        )
        return trial

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() != None:
            return queryset.filter(no_kk__trial=self.value())
        else:
            return queryset.filter(no_kk__trial=False)

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'Non Trial'
        return choices


class CleaningFilter(SimpleListFilter):
    title = "Cleaning"
    parameter_name = "cleaning"

    def lookups(self, request, model_admin):
        trial = (
            (True, "Cleaning"),
            ('all', "All"),
        )
        return trial

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() != None:
            return queryset.filter(no_kk__cleaning=self.value())
        else:
            return queryset.filter(no_kk__cleaning=False)

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'Non Cleaning'
        return choices


class KKMesinFilter(SimpleListFilter):
    title = "Mesin"
    parameter_name = "machine__id"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_mesin = MasterMesin.objects.filter(
            user_group__id=selected_user).order_by('mesin')
        return [(mesin.id, mesin.mesin) for mesin in daftar_mesin]

    def queryset(self, request, queryset):
        return queryset


class KKTrialCustomFilter(SimpleListFilter):
    title = "Trial"
    parameter_name = "trial"

    def lookups(self, request, model_admin):
        trial = (
            (True, "Trial"),
            ('all', "All"),
        )
        return trial

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() != None:
            return queryset.filter(trial=self.value())
        else:
            return queryset.filter(trial=False)

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'Non Trial'
        return choices


class KKWIPFilter(SimpleListFilter):
    title = "WIP / FG"
    parameter_name = "tipe__id"

    def lookups(self, request, model_admin):
        tipe = (
            (3, "WIP Only"),
            (2, "FG Only"),
        )
        return tipe

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(item_example__tipe_id=self.value())
        else:
            return queryset


class HiddenItemMode(SimpleListFilter):
    title = ''
    parameter_name = 'item_mode'
    template = 'admin/hidden_filter_for_qparam.html'

    def lookups(self, request, model_admin):
        return None

    def queryset(self, request, queryset):
        return queryset


class HiddenRMSplitFilter(SimpleListFilter):
    title = 'Mode: RM Auto Calculation'
    parameter_name = 'rm_split'

    def lookups(self, request, model_admin):
        tipe = (
            (1, "RM Auto Split"),
        )
        return tipe

    def queryset(self, request, queryset):
        return queryset

    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices[0]['display'] = 'Normal'
        return choices

# endregion

# ============================ Method for Admin Calc Field ============================#

# region


class UnitSpecificModelAdmin(admin.ModelAdmin):
    list_max_show_all = 1000

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append("user_group")
        return super(UnitSpecificModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user_group = request.user.userprofile.main_group
        obj.save()

    def get_queryset(self, request):
        qs = super(UnitSpecificModelAdmin, self).get_queryset(request)
        ug_list = request.user.userprofile.factory_group.all()
        return qs.filter(user_group__in=ug_list)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user_group_list = request.user.userprofile.factory_group.all()
        if db_field.name == "machine" or db_field.name == "mesin":
            kwargs["queryset"] = MasterMesin.objects.filter(
                user_group__in=user_group_list
            )
        if db_field.name == "foreman":
            kwargs["queryset"] = MasterWorker.objects.filter(
                user_group__in=user_group_list
            )
        if db_field.name == "operator":
            kwargs["queryset"] = MasterWorker.objects.filter(
                user_group__in=user_group_list
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DetailAdmin(ModelAdmin):
    list_max_show_all = 1000
    list_display = [
        "start_time",
        "shift",
        "no_kk",
        "machine",
    ]
    fields = [
        ("start_time", "end_time", "shift", "machine",),
        ("no_kk", ),
        ("dl_avail", "foreman", "operator"),
        "catatan"
    ]
    readonly_fields = ["start_time", "end_time", "shift",
                       "machine", "no_kk", "dl_avail", "foreman", "operator", "catatan"]

    def get_queryset(self, request):
        qs = super(DetailAdmin, self).get_queryset(request)
        return qs.filter(user_group__in=request.user.userprofile.factory_group.all())

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReportAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CustomTabularInline(TabularInline):
    pass

class ProductionFormInline(CustomTabularInline):

    def has_add_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_add_permission(request, obj)
        return super().has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_change_permission(request, obj)
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_delete_permission(request, obj)
        return super().has_delete_permission(request, obj)


class CustomModelAdmin(ModelAdmin):
    list_max_show_all = 1000

# endregion

# ============================ Inlines ============================#

# region


class KKFinishedGoodInline(CustomTabularInline):
    model = DetailKKFinishedGood
    autocomplete_fields = ["produk"]
    extra = 0


class KKRawMaterialInline(CustomTabularInline):
    model = DetailKKRawMaterial
    autocomplete_fields = ["bahan"]
    extra = 0


class DowntimeInline(ProductionFormInline):
    model = DetailDowntime
    exclude = ["durasi"]
    autocomplete_fields = ["form_breakdown"]
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(
                attrs={
                    "rows": 2,
                    "cols": 25
                }
            ),
        }
    }
    extra = 0



class MaterialConsumptionInline(ProductionFormInline):
    model = DetailMaterialConsumption
    extra = 0
    exclude = ["qty_pakai"]
    autocomplete_fields = ["bahan"]
    formfield_overrides = {
        models.FloatField: {"widget": TextInput(attrs={"size": "5"})},
        models.CharField: {
            "widget": TextInput(
                attrs={
                    "size": 15,
                }
            ),
        },
    }


class ProductionResultsInline(ProductionFormInline):
    model = DetailProductionResults
    extra = 0
    fields = [
        "produk",
        "batch_no",
        "hasil_jadi_qty",
        "hold_qc_qty",
        "berat_unit_sample",
        "reject",
        "trimming",
        "waste",
    ]
    autocomplete_fields = ["produk"]
    formfield_overrides = {
        models.IntegerField: {"widget": TextInput(attrs={"size": "5"})},
        models.FloatField: {"widget": TextInput(attrs={"size": "5"})},
        models.CharField: {
            "widget": TextInput(
                attrs={
                    "size": 15,
                }
            ),
        },
    }


class ProductionResultsPrefilledInline(ProductionFormInline):
    model = DetailProductionResults
    extra = 0
    fields = [
        "produk",
        "batch_no",
        "hasil_jadi_qty",
        "hold_qc_qty",
        "berat_unit_sample",
        "reject",
        "trimming",
        "waste",
    ]
    formfield_overrides = {
        models.IntegerField: {"widget": TextInput(attrs={"size": "5"})},
        models.FloatField: {"widget": TextInput(attrs={"size": "5"})},
        models.CharField: {
            "widget": TextInput(
                attrs={
                    "size": 15,
                }
            ),
        },
    }

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ProductionResultsPrefilledInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        if db_field.name == 'produk':
            query_kk = request.GET.get("no_kk")
            object_id = request.path
            if query_kk:
                kk = KK.objects.filter(id=query_kk)
            elif 'change' in object_id:
                object_id = object_id.split("/")
                object_id = object_id[object_id.index('change') - 1]
                object_id = int(object_id)
                kk = KK.objects.filter(productionform=object_id)
            else:
                kk = None

            if kk:
                produk_list = kk.values_list(
                    "detailkkfinishedgood__produk__id", flat=True)
                field.queryset = MasterBarang.objects.filter(
                    id__in=produk_list)
            else:
                field.queryset = MasterBarang.objects.none()
        return field


class ReportListKKInline(TabularInline, ShiftReportMethod):
    model = ProductionForm
    ordering = ["-start_time"]
    fields = [
        "start_time",
        "shift",
        "machine",
        "item_group",
        "daftar_fg",
        "durasi",
        "durasi_downtime",
        "raw_material",
        "finished_goods",
        "byproduct"
    ]
    readonly_fields = [
        "start_time",
        "shift",
        "machine",
        "item_group",
        "daftar_fg",
        "durasi",
        "durasi_downtime",
        "raw_material",
        "finished_goods",
        "byproduct"
    ]
    show_change_link = True
    extra = 0

    def has_change_permission(self, request, obj=None):
        if obj.aktif == 1:
            return True
        else:
            return False

    def durasi(self, obj):
        pk = obj.id
        report = ProductionForm.objects.get(id=pk)
        return ShiftReportMethod.durasi_pengerjaan(self, report)

    def daftar_fg(self, obj):
        barang = DetailProductionResults.objects.filter(laporan_id=obj.id)
        barang = barang.values_list("produk__nama", "hasil_jadi_qty",
                                    "fg_mass", "berat_unit_sample", "produk__berat_standar_fg")
        barang = ["{}: {} - {} kg - {} ({})".format(i, j, k, l, m)
                  for i, j, k, l, m in barang]
        daftar = "<br>".join(barang)
        return format_html(daftar)

    def item_group(self, obj):
        barang = obj.no_kk.item_example.group
        return barang


class RejectPackagingInline(ProductionFormInline):
    model = DetailPackagingUsage
    autocomplete_fields = ["packaging"]
    extra = 0


# endregion

# ============================ KK ============================#
# region


class ReportByKK(KK):
    class Meta:
        proxy = True
        verbose_name_plural = "SMW1. Report By WO"


@admin.register(ReportByKK)
class ReportByKKModelAdmin(UnitSpecificModelAdmin, KKReportMethod):
    date_hierarchy = "creation_date"
    change_list_template = "admin/report_w_total.html"
    change_form_template = "admin/report_by_kk_change_form.html"
    ordering = ["-creation_date"]
    actions = [make_closed, make_active]
    search_fields = ["no_kk"]
    inlines = [ReportListKKInline]
    list_filter = (UserGroupFilter, KKMesinFilter, ('creation_date', DateRangeFilter), "aktif",
                   "is_export", "cleaning", "trial")
    list_per_page = n_report
    list_display = (
        "no_kk",
        "aktif",
        "bulan_pengerjaan",
        "produk",
        "eff_hour",
        "downtime",
        "rm",
        "fg_unit",
        "fg_lm",
        "fg_m2",
        "fg_teori",
        "fg",
        "reject",
        "trimming",
        "waste",
        "scrap_used",
        "scrap_created",
        "scrap_chg",
        "selisih_material",
        "eff_rm",
        "fty",
        "availability",
        "performance",
        "oee",
    )
    total_functions = {
        "eff_hour": [Sum('productionform__effective_hour'), 'f', 'productionform'],
        "downtime": [Sum('productionform__downtime'), 'f', 'productionform'],
        'rm': [Sum('productionform__raw_material'), 'f', 'productionform'],
        'fg': [Sum('productionform__fg'), 'f', 'productionform'],
        'fg_teori': [Sum('productionform__fg_mass_std'), 'f', 'productionform'],
        "fg_unit": [Sum('productionform__fg_qty'), 'f', 'productionform'],
        "fg_lm": [Sum('productionform__fg_lm'), 'f', 'productionform'],
        "fg_m2": [Sum('productionform__fg_m2'), 'f', 'productionform'],
        'reject': [Sum('productionform__reject'), 'f', 'productionform'],
        'trimming': [Sum('productionform__trimming'), 'f', 'productionform'],
        'waste': [Sum('productionform__waste'), 'f', 'productionform'],
        'scrap_used': [Sum('productionform__scrap_usage'), 'f', 'productionform'],
        'scrap_created': [Sum('productionform__scrap_hasil'), 'f', 'productionform'],
        'scrap_chg': [Sum('productionform__scrap_hasil') - Sum('productionform__scrap_usage'), 'f', 'productionform'],
        'selisih_material': [Sum('productionform__raw_material') - Sum('productionform__total_output'), 'f', 'productionform'],
        'eff_rm': [Sum('productionform__total_output') / Sum('productionform__raw_material'), '%', 'productionform'],
        'fty': [Sum('productionform__fg') / (Sum('productionform__total_output')), '%', 'productionform'],
        'availability': [Sum('productionform__effective_hour') / Sum('productionform__total_hour'), '%', 'productionform'],
        'performance': [Sum('productionform__earn_hour') / Sum('productionform__effective_hour'), '%', 'productionform'],
        'oee': [Sum('productionform__fg')
                / (Sum('productionform__total_output'))
                * Sum('productionform__earn_hour') / Sum('productionform__effective_hour')
                * Sum('productionform__effective_hour') /
                Sum('productionform__total_hour'),
                '%'],
    }

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        mesin_id = request.GET.get("machine__id")
        if mesin_id:
            queryset = queryset.filter(
                productionform__machine=mesin_id).distinct()
        queryset = queryset.prefetch_related("productionform_set")
        return queryset

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        # ----------------- QUERYSET EXTRACTION
        dict_dt_cat = DetailDowntime._meta.get_field('kategori').choices
        dict_dt_cat = dict(dict_dt_cat)
        kk = KK.objects.get(id=object_id)
        form_shift = kk.productionform_set.all().order_by('machine_id')
        data_rm = form_shift.values('machine__mesin', bahan__nama=F('detailmaterialconsumption__bahan__nama')).annotate(
            rm=Sum('detailmaterialconsumption__qty_pakai')).order_by('machine')

        data_fg = form_shift.values('machine__mesin', produk__nama=F('detailproductionresults__produk__nama'), produk__kode_barang=F('detailproductionresults__produk__kode_barang')).annotate(qty=Sum("detailproductionresults__hasil_jadi_qty"), fg=Sum(
            F("detailproductionresults__hasil_jadi_qty") * F("detailproductionresults__berat_unit_sample"))).order_by('machine', '-detailproductionresults__produk__panjang', 'produk__kode_barang')
        data_bp = form_shift.values('machine__mesin').annotate(reject=Sum(
            'reject'), trimming=Sum("trimming"), waste=Sum("waste")).order_by('machine')
        data_mesin = form_shift.order_by().values_list(
            'machine__mesin', flat=True).order_by('machine_id').distinct()
        data_summary = form_shift.values('machine__mesin').annotate(rm=Sum("raw_material"), fg_piece=Sum(
            "fg_qty"), fg_weight=Sum('fg'), bp=Sum('reject') + Sum("trimming") + Sum("waste")).order_by('machine')
        data_downtime = form_shift.values('machine__mesin', 'start_time', 'shift', dt_notes=F('detaildowntime__notes'), dt_durasi=F('detaildowntime__durasi')).annotate(
            dt_kategori=F('detaildowntime__kategori'), dt_start=F('detaildowntime__waktu_mulai'), dt_end=F('detaildowntime__waktu_selesai')).order_by('-start_time')

        data_jadi = {}

        for i in data_mesin:
            data_jadi[i] = {'fg': [], 'rm': [], 'dt': []}

        for i in data_rm:
            if i["bahan__nama"] is not None:
                data_jadi[i['machine__mesin']]['rm'].append(i)

        for i in data_fg:
            if i["produk__nama"] is not None:
                data_jadi[i['machine__mesin']]['fg'].append(i)

        for i in data_bp:
            mesin = i.pop('machine__mesin')
            data_jadi[mesin]['bp'] = i

        for i in data_downtime:
            if i["dt_kategori"] is not None:
                data_jadi[i['machine__mesin']]['dt'].append(i)

        for i in data_summary:
            data_jadi[i['machine__mesin']]['summary'] = i

        dict_dt = DetailDowntime._meta.get_field('kategori').choices
        dict_dt = dict(dict_dt)
        try:
            response.context_data['field_rm'] = ['item', 'Weight']
            response.context_data['field_fg'] = ['Item', 'QTY', 'Weight']
            response.context_data['field_bp'] = ['Reject', 'Trimming', 'Waste']
            response.context_data['field_dt'] = [
                'Date', 'Shift', "Start", "End", 'Category', 'Notes', 'Duration (Hr)']
            response.context_data['dict_dt'] = dict_dt
            response.context_data['dataset'] = data_jadi
        except:
            pass

        return response

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# ============================ SMW2 ============================#


class ReportPerWaktuVsKK(KK):
    class Meta:
        proxy = True
        verbose_name = "SMW2. Report By WO Date"
        verbose_name_plural = "SMW2. Report By WO Date"


@admin.register(ReportPerWaktuVsKK)
class ReportPerWaktuWOBasedAdmin(ReportAdmin):

    change_list_template = "admin/report_by_waktu_kk_change_list.html"
    date_hierarchy = "creation_date"
    list_filter = [UserGroupFilter, "aktif", KKWIPFilter, 
                   "is_export", "trial", "cleaning"]
    date_grouping = "normalized_date"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
            qs = ProductionForm.objects.filter(no_kk__in=qs)
        except (AttributeError, KeyError):
            return response

        # ===== if something in query params
        is_machine_query = any("machine" in query for query in request.GET)

        # ================= Check date format
        period = self.get_next_in_date_hierarchy(
            request,
            self.date_hierarchy,
        )

        # ================= What to calculate
        metrics = {
            "availibility": Sum("effective_hour") / Sum("total_hour"),
            "performance": Sum("earn_hour") / Sum("effective_hour"),
            "fg_qty": Sum("fg_qty"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "fg_theory": Sum("fg_mass_std"),
            "fty": Sum("fg") / (Sum("total_output")),
            "scrap_dipakai": Sum("scrap_usage"),
            "scrap_dihasilkan": Sum("scrap_hasil"),
            "scrap_selisih": Sum("scrap_hasil") - Sum("scrap_usage"),
            "finished_goods": Sum("fg"),
            "oee": Sum("fg")
            / (Sum("total_output"))
            * Sum("earn_hour") / Sum("effective_hour")
            * Sum("effective_hour") / Sum("total_hour"),
            "raw_material": Sum("raw_material"),
            "waste": Sum("waste"),
            "downtime": Sum("downtime"),
            "effective_time": Sum("effective_hour")
        }

        # ================= Make the qs
        period_query = "no_kk__" + self.date_hierarchy
        summary_data = (
            qs.annotate(
                period=Trunc(
                    period_query,
                    period,
                ),
            )
            .values("period")
            .annotate(**metrics)
            .order_by("period")
        )

        # ================= Processing the context data
        summary_data = list(summary_data)

        for d in summary_data:
            d["period"] = self.format_time(
                d, period)

        # ================== Rekap seluruh QS
        summary_total = qs.aggregate(**metrics)

        response.context_data["table_fields"] = [
            col["date"],
            col["rm"],
            col["fg"],
            col["fg_theory"],
            col["fg_qty"],
            col["fg_lm"],
            col["fg_m2"],
            col["FTY"],
            col["avail"],
            col["perf"],
            col["oee"],
            col["scrap_use"],
            col["scrap_prod"],
            col["scrap_chg"],
            col["ws"],
            col["eff_hour"],
            col["dt"],
            col["idle"],
        ]
        response.context_data["summary"] = summary_data
        response.context_data["summary_total"] = summary_total

        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__day" in request.GET:
            return "kk"
        if date_hierarchy + "__month" in request.GET:
            return "day"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
    ):
        if period == "day":
            return data["period"].strftime("%d %b %Y")
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")

# A1


@admin.register(KK)
class KKModelAdmin(UnitSpecificModelAdmin, CustomModelAdmin):
    date_hierarchy = "creation_date"
    search_fields = ["no_kk"]
    autocomplete_fields = ["item_example"]
    actions = [make_closed, make_closed_and_split_rm, make_active]
    ordering = ["-creation_date"]
    list_display = ["no_kk", "creation_date",
                    "aktif", "is_export", "cleaning", "trial", "item_example"]
    list_filter = (UserGroupFilter, KKItemGroupFilter,
                   "aktif", "is_export", "cleaning", "trial")
    inlines = [KKFinishedGoodInline, KKRawMaterialInline]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append("user_group")
        return super(KKModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user_group = request.user.userprofile.main_group
        obj.save()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if not request.user.is_superuser:
            queryset = queryset.filter(
                user_group__in=request.user.userprofile.factory_group.all()
            )
            queryset, use_distinct = super().get_search_results(
                request, queryset, search_term
            )

        if (
            "app_label" in request.GET
            and "model_name" in request.GET
            and "field_name" in request.GET
        ):
            model_class = apps.get_model(
                request.GET["app_label"], request.GET["model_name"]
            )
            limit_choices_to = model_class._meta.get_field(
                request.GET["field_name"]
            ).get_limit_choices_to()
            if limit_choices_to:
                queryset = queryset.filter(**limit_choices_to)

        return queryset, use_distinct

# endregion

# ============================ Report ============================#

# # Form specific To each report
# # Downtime


# class ReportDowntime(ProductionForm):
#     class Meta:
#         proxy = True
#         verbose_name_plural = "DT3. Report Downtime"


# @admin.register(ReportDowntime)
# class DowntimeReportAdmin(DetailAdmin, DowntimeReportMethod):
#     change_list_template = "admin/report_table.html"
#     list_display = DetailAdmin.list_display + \
#         ["durasi_downtime", "penyebab_downtime"]
#     list_per_page = n_report
#     list_filter = [UserGroupFilter, MesinFilter,
#                    ProductFilter, WIPFilter, ExportFilter, TrialFilter, CleaningFilter, WorkerFilter]
#     inlines = [
#         ProductionResultsInline,
#         MaterialConsumptionInline,
#         DowntimeInline,
#         RejectPackagingInline,
#     ]
#     date_hierarchy = "normalized_date"
#     search_fields = ["no_kk__no_kk"]


# # Production Results
# class ReportProductionResults(ProductionForm):
#     class Meta:
#         proxy = True
#         verbose_name_plural = "FG1. Report Production Results"


# # @admin.register(ReportProductionResults)
# class ProductionResultsReportAdmin(ProductionResultsMethod, DetailAdmin):
#     change_list_template = "admin/report_w_total.html"
#     list_display = DetailAdmin.list_display + [
#         "produk",
#         "finished_good",
#         "hold",
#         "reject",
#         "trimming",
#         "waste",
#     ]
#     inlines = [
#         ProductionResultsInline,
#         MaterialConsumptionInline,
#         DowntimeInline,
#         RejectPackagingInline,
#     ]
#     list_filter = [UserGroupFilter, MesinFilter,
#                    ProductFilter, WIPFilter, ExportFilter, TrialFilter, CleaningFilter, WorkerFilter]
#     list_per_page = n_report
#     date_hierarchy = "normalized_date"
#     total_functions = {
#         'finished_good': [Sum('fg'), 'f'],
#         'hold': [Sum('hold'), 'f'],
#         'reject': [Sum('reject'), 'f'],
#         'trimming': [Sum('trimming'), 'f'],
#         'waste': [Sum('waste'), 'f'],
#     }
#     search_fields = ["no_kk__no_kk"]

# # Material Consumption


# class ReportMaterialConsumption(ProductionForm):
#     class Meta:
#         proxy = True
#         verbose_name_plural = "RM2. Report Material Consumption"


# # @admin.register(ReportMaterialConsumption)
# class MaterialConsumptionReportAdmin(DetailAdmin, MaterialConsumptionMethod):
#     change_list_template = "admin/report_w_total.html"
#     list_display = DetailAdmin.list_display + [
#         "finished_good",
#         "pemakaian_fresh",
#         "pemakaian_scrap",
#         "persentase_scrap",
#         "pemakaian_pigment",
#         "pemakaian_aditif",
#     ]
#     inlines = [
#         ProductionResultsInline,
#         MaterialConsumptionInline,
#         DowntimeInline,
#         RejectPackagingInline,
#     ]
#     list_filter = [UserGroupFilter, MesinFilter,
#                    ProductFilter, WIPFilter, ExportFilter, TrialFilter, CleaningFilter, WorkerFilter]
#     list_per_page = n_report
#     date_hierarchy = "normalized_date"
#     search_fields = ["no_kk__no_kk"]

# Packaging Reject


class ReportRejectPacakging(ProductionForm):
    class Meta:
        proxy = True
        verbose_name_plural = "PKG1. Packaging Reject Report"


@admin.register(ReportRejectPacakging)
class PackagingRejectReportAdmin(DetailAdmin, RejectPackagingReportMethod):
    change_list_template = "admin/report_w_total.html"
    inlines = [
        ProductionResultsInline,
        MaterialConsumptionInline,
        DowntimeInline,
        RejectPackagingInline,
    ]
    total_functions = {'fg_qty': [Sum('fg_qty'), 'f']}
    list_display = DetailAdmin.list_display + \
        ["fg_qty", "reject_eqvl", "daftar_reject"]
    list_per_page = n_report
    list_filter = [UserGroupFilter, MesinFilter,
                   ProductFilter, WIPFilter, ExportFilter, TrialFilter, CleaningFilter, WorkerFilter]
    date_hierarchy = "normalized_date"

    def reject_eqvl(self, obj):
        if not obj.fg_qty:
            return "No FG"
        return to_percent(obj.reject_eqv / obj.fg_qty)
    reject_eqvl.admin_order_field = 'reject_eqv'

# ============================ Form ============================#


class PrefilledForm(ProductionForm):
    class Meta:
        proxy = True
        verbose_name_plural = "A3. Prefilled Form"


@admin.register(PrefilledForm)
class FormPraisiAdmin(CustomModelAdmin, ShiftReportMethod):
    search_fields = ["no_kk__no_kk"]
    change_form_template = "admin/prefilled_form.html"
    change_list_template = "admin/prefilled_form_changelist.html"
    inlines = [
        ProductionResultsPrefilledInline,
        MaterialConsumptionInline,
        DowntimeInline,
        RejectPackagingInline,
    ]
    list_display = ['start_time', 'shift', 'no_kk', 'machine', 'produk']

    # Modifying based on get param

    def get_fields(self, request, obj=None):
        self.request = request
        main_form_field = [
            ("start_time", "end_time", "shift", "machine",),
            ("no_kk", ),
            ("dl_avail", "foreman", "operator"),
            "catatan"
        ]
        if not request.user.is_superuser:
            fields = main_form_field
        else:
            fields = ["user_group"] + main_form_field
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user_group = request.user.userprofile.main_group
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            ug_list = request.user.userprofile.factory_group.all()
            return qs.filter(user_group__in=ug_list)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            ug_list = request.user.userprofile.factory_group.all()
            if db_field.name == "machine":
                kwargs["queryset"] = MasterMesin.objects.filter(
                    user_group__in=ug_list
                )
            if db_field.name == "foreman":
                kwargs["queryset"] = MasterWorker.objects.filter(
                    user_group__in=ug_list
                )
            if db_field.name == "operator":
                kwargs["queryset"] = MasterWorker.objects.filter(
                    user_group__in=ug_list
                )
                
        if db_field.name == "no_kk":
            query_kk = request.GET.get("no_kk")
            object_id = request.path
            if query_kk:
                kk = KK.objects.filter(id=query_kk)
            elif 'change' in object_id:
                object_id = object_id.split("/")
                object_id = object_id[object_id.index('change') - 1]
                object_id = int(object_id)
                kk = KK.objects.filter(productionform=object_id)
            else:
                kk = KK.objects.none()
            kwargs["queryset"] = kk

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        query_params = request.GET
        q_expression = Q(
            aktif=1, user_group__in=request.user.userprofile.factory_group.all())

        if query_params.get("q"):
            queries = query_params.get("q")
            queries = queries.split()

            for wo in queries:
                q_expression &= Q(no_kk__icontains=wo)

            qs = KK.objects.filter(
                q_expression).order_by('-id')[:5]

        else:
            qs = KK.objects.filter(q_expression).order_by('-id')[:5]

        qs = qs.prefetch_related('detailkkfinishedgood_set')

        table_content = [
            {
                'no_kk': data.no_kk,
                'id': data.id,
                'creation_date': data.creation_date,
                'link': link_prefilled_form(data.id, data.no_kk),
                'barang': data.detailkkfinishedgood_set.first()
            } for data in qs
        ]

        try:
            response.context_data["table_content"] = table_content
            response.context_data["table_fields"] = [
                col["wo"], col["month_executed"], "Barang yang diproduksi"]
        except:
            pass

        return response

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_change_permission(request, obj)
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_delete_permission(request, obj)
        return super().has_delete_permission(request, obj)


def link_prefilled_form(id_kk, no_kk):
    url = reverse('admin:form_produksi_prefilledform_add')
    q_param = 'no_kk=' + str(id_kk)
    link = "{}?{}".format(url, q_param)
    return format_html("<a href='{}'>{}</a>", link, no_kk)

# A2


@admin.register(ProductionForm)
class ReportShiftAdmin(CustomModelAdmin, ShiftReportMethod):
    change_list_template = "admin/report_w_total.html"
    change_form_template = "admin/shift_form_w_calc.html"
    date_hierarchy = "normalized_date"
    actions = [duplicate, refresh, refresh_fg_calculation]
    list_max_show_all = 1000
    list_display = [
        "start_time",
        "shift",
        "link_kk",
        "machine",
        "produk",
        "durasi_pengerjaan",
        "durasi_downtime",
        "material_usage",
        "fg_unit",
        "fg_lm_",
        "fg_m2_",
        "finished_goods",
        "fg_teori",
        "hold_qc",
        "reject_",
        "trimming_",
        "waste_",
        "selisih_material",
        "pemakaian_scrap",
        "pkg_reject",
        "output_std",
        "fty",
        "availability",
        "performance",
        "oee",
        "foreman",
        "operator"
    ]
    list_filter = [UserGroupFilter, MesinFilter, ProductFilter, WorkerFilter,
                   ('normalized_date', DateRangeFilter), WIPFilter, ExportFilter, TrialFilter, CleaningFilter, ClosedCustomFilter]
    inlines = [
        ProductionResultsInline,
        MaterialConsumptionInline,
        DowntimeInline,
        RejectPackagingInline,
    ]
    autocomplete_fields = ["no_kk", "machine"]
    search_fields = ["no_kk__no_kk"]
    ordering = ["-created_at"]
    list_per_page = n_report
    total_functions = {
        "material_usage": [Sum("raw_material"), 'f'],
        "fg_unit": [Sum("fg_qty"), 'f'],
        "fg_lm_": [Sum("fg_lm"), 'f'],
        "fg_m2_": [Sum("fg_m2"), 'f'],
        'fg_teori': [Sum('fg_mass_std'), 'f'],
        "finished_goods": [Sum("fg"), 'f'],
        "hold_qc": [Sum("hold"), 'f'],
        "reject_": [Sum("reject"), 'f'],
        "trimming_": [Sum("trimming"), 'f'],
        "waste_": [Sum("waste"), 'f'],
        "selisih_material": [Sum("raw_material") - Sum('total_output'), 'f'],
        "pemakaian_scrap": [Sum('scrap_hasil') - Sum('scrap_usage'), 'f'],
        "pkg_reject": [Sum('reject_eqv') / Sum('fg_qty'), '%'],
        "durasi_pengerjaan": [Sum('effective_hour'), 'f'],
        "durasi_downtime": [Sum('downtime'), 'f'],
        "fty": [Sum('fg') / (Sum('total_output')), '%'],
        "availability": [Sum('effective_hour') / Sum('total_hour'), '%'],
        "performance": [Sum('earn_hour') / Sum('effective_hour'), '%'],
    }

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(
                attrs={
                    "rows": 2,
                    "cols": 60
                }
            ),
        }
    }

    def get_fields(self, request, obj=None):
        if not request.user.is_superuser:
            fields = [
                ("start_time", "end_time", "shift", "machine",),
                ("no_kk", ),
                ("dl_avail", "foreman", "operator"),
                "catatan"
            ]
        else:
            fields = [
                "user_group",
                ("start_time", "end_time", "shift", "machine",),
                ("no_kk", ),
                ("dl_avail", "foreman", "operator"),
                "catatan"
            ]
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user_group = request.user.userprofile.main_group
        obj.save()

    def get_queryset(self, request):
        qs = super(ReportShiftAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            ug_list = request.user.userprofile.factory_group.all()
            return qs.filter(user_group__in=ug_list)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            ug_list = request.user.userprofile.factory_group.all()
            if db_field.name == "machine":
                kwargs["queryset"] = MasterMesin.objects.filter(
                    user_group__in=ug_list
                )
            if db_field.name == "foreman":
                kwargs["queryset"] = MasterWorker.objects.filter(
                    user_group__in=ug_list
                )
            if db_field.name == "operator":
                kwargs["queryset"] = MasterWorker.objects.filter(
                    user_group__in=ug_list
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def link_kk(self, obj):
        url = reverse("admin:form_produksi_reportbykk_change",
                      args=(obj.no_kk.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.no_kk)
    link_kk.short_description = "KK"

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_change_permission(request, obj)
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.no_kk.aktif == "1" and super().has_delete_permission(request, obj)
        return super().has_delete_permission(request, obj)

    def get_rangefilter_normalized_date_title(self, request, field_path):
        return 'Date Range'

# ============================ Summary by Period ============================#


class ReportPerWaktu(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "SMT2. Report By Form Date"
        verbose_name_plural = "SMT2. Report By Form Date"


@admin.register(ReportPerWaktu)
class ReportPerWaktuAdmin(ReportAdmin):
    change_list_template = "admin/report_by_waktu_change_list.html"
    date_hierarchy = "normalized_date"
    list_filter = [UserGroupFilter, "machine__priority", MesinFilter,
                   ProductFilter, ('normalized_date', DateRangeFilter), WIPCustomFilter, ExportFilter, TrialCustomFilter, CleaningFilter, WorkerFilter]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        # ===== if something in query params
        is_machine_query = any("machine" in query for query in request.GET)

        # ================ Check date query for KK page
        cl_ = response.context_data["cl"]
        field_name_ = cl_.date_hierarchy
        year_field_ = '%s__year' % field_name_
        month_field_ = '%s__month' % field_name_
        day_field_ = '%s__day' % field_name_
        year_lookup_ = cl_.params.get(year_field_)
        month_lookup_ = cl_.params.get(month_field_)
        day_lookup_ = cl_.params.get(day_field_)

        filters = {year_field_: year_lookup_, month_field_: month_lookup_}

        # ================= Check date format
        period = self.get_next_in_date_hierarchy(
            request,
            self.date_hierarchy,
        )

        # ================= What to calculate
        metrics = {
            "availibility": Sum("effective_hour") / Sum("total_hour"),
            "performance": Sum("earn_hour") / Sum("effective_hour"),
            "fg_qty": Sum("fg_qty"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "fg_theory": Sum("fg_mass_std"),
            "fty": Sum("fg") / (Sum("total_output")),
            "scrap_dipakai": Sum("scrap_usage"),
            "scrap_dihasilkan": Sum("scrap_hasil"),
            "scrap_selisih": Sum("scrap_hasil") - Sum("scrap_usage"),
            "finished_goods": Sum("fg"),
            "oee": Sum("fg")
            / (Sum("total_output"))
            * Sum("earn_hour") / Sum("effective_hour")
            * Sum("effective_hour") / Sum("total_hour"),
            "raw_material": Sum("raw_material"),
            "waste": Sum("waste"),
            "downtime": Sum("downtime"),
            "effective_time": Sum("effective_hour")
        }

        # ================= Make the qs
        if period == "kk":
            summary_data = (
                qs.values("no_kk", "no_kk__no_kk", "id")
                .annotate(**metrics)
            )
        else:
            summary_data = (
                qs.annotate(
                    period=Trunc(
                        self.date_hierarchy,
                        period,
                    ),
                )
                .values("period")
                .annotate(**metrics)
                .order_by("period")
            )

        total_time = get_total_time_time_row(
            summary_data, period, self.date_hierarchy, is_machine_query)

        # ================= Processing the context data
        summary_data = list(summary_data)

        if period == "kk":
            for d in summary_data:
                d["period"] = self.format_time(
                    d, period, cl_, filters, day_field_)
                d["form"] = self.link_to_form(d)
        else:
            for d in summary_data:
                d["idle_time"] = total_time[d["period"]] - \
                    d["downtime"] - d["effective_time"]
                d["period"] = self.format_time(
                    d, period, cl_, filters, day_field_)

        # ================== Rekap seluruh QS
        summary_total = qs.aggregate(**metrics)

        if period != "kk":
            summary_total["idle_time"] = sum(
                [data["idle_time"] for data in summary_data])

        if period == "kk":
            response.context_data["table_fields"] = [
                col["wo"],
                "Form",
            ]
        else:
            response.context_data["table_fields"] = [
                "Production Date",
            ]

        response.context_data["table_fields"] += [
            col["rm"],
            col["fg"],
            col["fg_theory"],
            col["fg_qty"],
            col["fg_lm"],
            col["fg_m2"],
            col["FTY"],
            col["avail"],
            col["perf"],
            col["oee"],
            col["scrap_use"],
            col["scrap_prod"],
            col["scrap_chg"],
            col["ws"],
            col["eff_hour"],
            col["dt"],
            col["idle"],
        ]
        response.context_data["summary"] = summary_data
        response.context_data["summary_total"] = summary_total

        # ----------------- JUDUL MESIN DAN USER
        get_params = request.GET
        if "machine__id__exact" in get_params:
            response.context_data["selected_machine"] = (
                " - "
                + MasterMesin.objects.get(id=get_params["machine__id__exact"]).mesin
            )

        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__day" in request.GET:
            return "kk"
        if date_hierarchy + "__month" in request.GET:
            return "day"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
        cl=None,
        filters=None,
        day_field=None
    ):
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")
        if period == "day":
            filters[day_field] = data["period"].strftime("%-d")
            return format_html("<a href='{}'>{}</a>", link_date(cl, filters, self.date_hierarchy), data["period"].strftime("%d %b %Y"))
        if period == "kk":
            idx = data["no_kk"]
            url = reverse(
                'admin:form_produksi_reportbykk_change', args=[idx])
            return format_html("<a href='{}'>{}</a>", url, data["no_kk__no_kk"])

    def link_to_form(self, data):
        idx = data["id"]
        url = reverse('admin:form_produksi_productionform_change', args=[idx])
        return format_html("<a href='{}'>{}</a>", url, "To Form")

    def get_rangefilter_normalized_date_title(self, request, field_path):
        return 'Date Range'


def get_total_time_time_row(form_qs, period, date_hierarchy, is_machine_query):
    if period != "kk":
        now = datetime.now()
        group_list = form_qs.order_by().values('user_group')
        group_time_list = group_list.distinct().annotate(daily_hour=F(
            'user_group__groupprofile__daily_work_hour'), week_mask=F('user_group__groupprofile__weekly_days'))
        day_off_list = DayOffList.objects.filter(user_group__in=group_list)
        period_list = form_qs.order_by().values('period').distinct()
        time_dict = {}

        if not is_machine_query:
            machine_list = MasterMesin.objects.values("user_group", "add_date")

        for i in period_list:
            if period == "year":
                first = i['period']
                if first.year == now.year:
                    last = now
                else:
                    last = first + relativedelta(years=1)
            elif period == "month":
                first = i['period']
                if first.year == now.year and first.month == now.month:
                    last = now
                else:
                    last = first + relativedelta(months=1)
            elif period == "day":
                first = i['period']
                last = first + relativedelta(days=1)

            first_str = first.strftime('%Y-%m-%d')
            last_str = last.strftime('%Y-%m-%d')

            day_off_dict = {}
            day_off_filtered = day_off_list.filter(off_day__gte=first, off_day__lte=last).order_by(
            ).values('user_group').annotate(day_off_count=Count('id'))
            for j in day_off_filtered:
                day_off_dict[j['user_group']] = j['day_off_count']

            total_hour = 0

            for k in group_time_list:
                default_business_day = np.busday_count(
                    first_str, last_str, k['week_mask']) - day_off_dict.get(k['user_group'], 0)
                if is_machine_query:
                    machine_add_date = form_qs.order_by().values(
                        'machine__add_date')[0]['machine__add_date']

                    if first.date() > machine_add_date:
                        work_day = default_business_day
                    else:
                        work_day = np.busday_count(
                            machine_add_date, last_str, k['week_mask']) - day_off_dict.get(k['user_group'], 0)
                    total_hour = work_day * k['daily_hour']
                else:
                    machine_count = machine_list.filter(
                        user_group=k['user_group'], add_date__lte=first).count()
                    adt_machine_day = 0
                    for machine in machine_list.filter(user_group=k['user_group'], add_date__gt=first):
                        machine_busday = np.busday_count(
                            machine['add_date'], last_str, k['week_mask'])
                        if machine_busday > 0:
                            adt_machine_day += machine_busday
                    total_hour += (default_business_day *
                                   machine_count + adt_machine_day) * k['daily_hour']
            time_dict[i['period']] = total_hour

        return time_dict

#============================ Report By Unit ============================#


class ReportPerUnit(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "SMT1. Report By Unit"
        verbose_name_plural = "SMT1. Report By Unit"


@admin.register(ReportPerUnit)
class ReportPerUnitAdmin(ReportAdmin):
    change_list_template = "admin/report_by_unit_change_list.html"
    date_hierarchy = "normalized_date"
    list_filter = [('normalized_date', DateRangeFilter), "machine__priority", WIPCustomFilter, ExportFilter,
                   TrialCustomFilter, CleaningFilter]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        # ================= What to calculate
        metrics = {
            "availibility": Sum("effective_hour") / Sum("total_hour"),
            "performance": Sum("earn_hour") / Sum("effective_hour"),
            "fg_qty": Sum("fg_qty"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "fg_theory": Sum("fg_mass_std"),
            "fty": Sum("fg") / (Sum("total_output")),
            "scrap_dipakai": Sum("scrap_usage"),
            "scrap_dihasilkan": Sum("scrap_hasil"),
            "scrap_selisih": Sum("scrap_hasil") - Sum("scrap_usage"),
            "finished_goods": Sum("fg"),
            "oee": Sum("fg")
            / (Sum("total_output"))
            * Sum("earn_hour") / Sum("effective_hour")
            * Sum("effective_hour") / Sum("total_hour"),
            "raw_material": Sum("raw_material"),
            "waste": Sum("waste"),
        }

        # ================= Make the qs
        summary_data = (
            qs.values("user_group__name", "user_group__id")
            .annotate(**metrics)
            .order_by("user_group")
        )

        # ================= Processing the context data
        summary_data = list(summary_data)

        for d in summary_data:
            d["unit"] = link_unit(d["user_group__id"],
                                  d["user_group__name"], request.GET)

        # ================== Rekap seluruh QS
        summary_total = qs.aggregate(**metrics)

        response.context_data["table_fields"] = [
            "Unit",
            col["rm"],
            col["fg"],
            col["fg_theory"],
            col["fg_qty"],
            col["fg_lm"],
            col["fg_m2"],
            col["FTY"],
            col["avail"],
            col["perf"],
            col["oee"],
            col["scrap_use"],
            col["scrap_prod"],
            col["scrap_chg"],
            col["ws"]
        ]
        response.context_data["summary"] = summary_data
        response.context_data["summary_total"] = summary_total

        # ----------------- JUDUL MESIN DAN USER
        get_params = request.GET
        if "machine__id__exact" in get_params:
            response.context_data["selected_machine"] = (
                " - "
                + MasterMesin.objects.get(id=get_params["machine__id__exact"]).mesin
            )
        return response

    def get_rangefilter_normalized_date_title(self, request, field_path):
        return 'Date Range'


def link_date(cl, filters, date_hierarchy):
    return cl.get_query_string(filters, [date_hierarchy])


def link_unit(unit_id, unit_name, queries):
    url = reverse('admin:form_produksi_reportperwaktu_changelist')
    q_param = '&'.join(['{}={}'.format(i, queries[i]) for i in queries])
    q_param += '&user_group__id__exact=' + str(unit_id)
    link = "{}?{}".format(url, q_param)
    return format_html("<a href='{}'>{}</a>", link, unit_name)

# link = cl_.get_query_string(filters, [field_generic]) # output = link
# format_html("<a href='{}'>{}</a>", url, obj.no_kk)

#============================ Downtime by Mesin ============================#


class ReportDowntimePerMesin(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "DT1. Report Downtime By Mesin"
        verbose_name_plural = "DT1. Report Downtime By Mesin"


@admin.register(ReportDowntimePerMesin)
class ReportDowntimePerMesinAdmin(ReportAdmin):
    date_hierarchy = "normalized_date"
    list_filter = [UserGroupFilter, WorkerFilter]
    change_form_template = "admin/downtime_by_mesin_change_form.html"
    change_list_template = "admin/downtime_by_mesin_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/detail/', self.admin_site.admin_view(self.detail_view),
                 name='form_produksi_reportdowntimepermesin_detail'),
        ]
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response
        # GET TOTAL DAY
        period = get_current_in_date_hierarchy(request, self.date_hierarchy)
        year, month = get_date_from_request(request, self.date_hierarchy)
        total_days = get_total_time_machine_row(
            qs, period, self.date_hierarchy, year=year, month=month)

        # ================================

        mesin_list = qs.values_list('machine__mesin', 'machine__id').order_by(
            'machine__mesin').distinct()
        mesin_list = list(mesin_list)
        kategori_list = DetailDowntime._meta.get_field('kategori').choices
        kategori_list = [('NAN1', col["machine"]),
                         ('NAN2', col["eff_hour"]), ('NAN3', col["dt"]), ('NAN3', col["idle"])] + kategori_list
        kode_list = [i[0] for i in kategori_list]
        nama_list = [i[1] for i in kategori_list]

        kode_idx = enumerate(kode_list)
        mesin_idx = enumerate(mesin_list)
        kode_idx = dict((j, i) for i, j in kode_idx)
        mesin_idx = dict((j[0], i) for i, j in mesin_idx)

        downtime_data = qs.values('machine__mesin', 'detaildowntime__kategori').annotate(
            downtime=Sum('detaildowntime__durasi')).order_by("machine__mesin")
        summary_data = qs.values('machine__mesin', 'machine', 'user_group').annotate(
            uptime=Sum('effective_hour'), downtime=Sum('downtime'), daily_hour=F('user_group__groupprofile__daily_work_hour')).order_by("machine__mesin")

        for i in downtime_data:
            if i['downtime'] == None:
                i['downtime'] = 0

            i['y'] = mesin_idx.get(i['machine__mesin'])
            i['x'] = kode_idx.get(i['detaildowntime__kategori'])

        td = [[0]*len(nama_list) for _ in range(len(mesin_list))]

        for i, j in enumerate(mesin_list):
            td[i][0] = self.link_mesin_downtime(j, request)

        for i in downtime_data:
            try:
                td[i['y']][i['x']] = round(i['downtime'], 2)
            except:
                pass

        for i in summary_data:
            td[mesin_idx.get(i['machine__mesin'])][1] = round(i['uptime'], 2)
            td[mesin_idx.get(i['machine__mesin'])][2] = round(i['downtime'], 2)
            td[mesin_idx.get(i['machine__mesin'])][3] = round(
                total_days[i['machine']]['total_hour'] - i['uptime'] - i['downtime'], 2)

        sum_kode = list(zip(*td))
        try:
            sum_kode.pop(0)
            sum_kode = [map(float, content) for content in sum_kode]
            sum_kode = map(sum, sum_kode)
        except:
            pass
        sum_kode = list(sum_kode)
        sum_kode = [round(i, 2) for i in sum_kode]

        td = [list(map(td_mapper, data)) for data in td]

        response.context_data["table_fields"] = nama_list
        response.context_data["summary"] = td
        response.context_data["summary_total"] = sum_kode

        return response

    def detail_view(self, request, object_id, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        response.template_name = self.change_form_template

        # ----------------- QUERYSET EXTRACTION
        q_params = request.GET.copy()
        q_params = dict(q_params)
        mesin = MasterMesin.objects.get(id=object_id)

        if 'produk_id' in q_params:
            q_params['no_kk__item_example__group_id'] = q_params['produk_id']
            q_params.pop('produk_id')

        if 'normalized_date__range__gte' in q_params:
            string = q_params['normalized_date__range__gte'][0].split("/")
            string = ["{:s}-{:s}-{:s}".format(string[2], string[1], string[0])]
            q_params['normalized_date__gte'] = string
            q_params.pop('normalized_date__range__gte')

        if 'normalized_date__range__lte' in q_params:
            string = q_params['normalized_date__range__lte'][0].split("/")
            string = ["{:s}-{:s}-{:s}".format(string[2], string[1], string[0])]
            q_params['normalized_date__lte'] = string
            q_params.pop('normalized_date__range__lte')

        for i in q_params:
            try:
                q_params[i] = q_params[i][0]
                q_params[i] = int(q_params[i])
            except:
                pass

        form_shift = ProductionForm.objects.filter(machine=mesin)
        form_shift = form_shift.filter(**q_params)

        id_dt = form_shift.values_list('detaildowntime', flat=True)
        downtime_set = DetailDowntime.objects.filter(id__in=id_dt)
        downtime_set = downtime_set.values('laporan__start_time', 'laporan__id', 'laporan__start_time',
                                           'laporan__no_kk__no_kk', 'durasi', 'notes', 'kategori').order_by('-durasi')
        downtime_kategori = DetailDowntime._meta.get_field('kategori').choices
        downtime_kategori = dict(downtime_kategori)

        summary_data = []
        for i in downtime_set:
            if i['durasi'] != None:
                row_data = []
                row_data.append(i['laporan__start_time'].strftime('%d %b %Y'))
                row_data.append(self.link_mesin_downtime_form(
                    i['laporan__no_kk__no_kk'], i['laporan__id']))
                row_data.append(i['durasi'])
                row_data.append(downtime_kategori[i['kategori']])
                row_data.append(i['notes'])
                summary_data.append(row_data)

        field = [col["date"], col["wo"], col["dt"], col["category"], 'Notes']

        all_machine_link = "{}?{}".format(reverse(
            "admin:form_produksi_reportdowntimepermesin_changelist"), request.GET.urlencode())
        all_machine_link = format_html(
            "<a href='{}'>{}</a>", all_machine_link, "Back To All Machine")

        response.context_data['table_fields'] = field
        response.context_data['all_machine_link'] = all_machine_link
        response.context_data['title'] = mesin.mesin
        response.context_data['table_data'] = summary_data

        return response

    def get_rangefilter_normalized_date_title(self, request, field_path):
        return 'Date Range'

    def link_mesin_downtime(self, obj, req):
        url = "{}?{}".format(reverse("admin:form_produksi_reportdowntimepermesin_detail",
                                     args=(obj[1],)), req.GET.urlencode())
        return format_html("<a href='{}'>{}</a>", url, obj[0])

    def link_mesin_downtime_form(self, form_date, form_id):
        url = "{}".format(reverse("admin:form_produksi_productionform_change",
                                  args=[form_id]))
        return format_html("<a href='{}'>{}</a>", url, form_date)


def get_total_time_machine_row(form_qs, period, date_hierarchy, year=None, month=None):
    if form_qs.exists():
        now = datetime.now()
        time_data = form_qs.order_by().values('machine').annotate(daily_hour=F(
            'user_group__groupprofile__daily_work_hour'), week_mask=F('user_group__groupprofile__weekly_days'), machine_add_date=F('machine__add_date'), ).distinct()
        exclude_key = 'machine'
        time_dict = {}
        for i in time_data:
            time_dict[i['machine']] = {
                k: v for k, v in i.items() if k not in exclude_key}

        day_off_list = DayOffList.objects.filter(user_group__in=time_dict)
        day_off_dict = {}

        if period == "year":
            if year == now.year:
                first = date(year, 1, 1)
                last = now
            else:
                first = date(year, 1, 1)
                last = first + relativedelta(years=1)
        elif period == "month":
            if year == now.year and month == now.month:
                first = date(year, month, 1)
                last = now
            else:
                first = date(year, month, 1)
                last = first + relativedelta(months=1)
        elif period == "days":
            first = date(2021, 8, 16)
            last = date(2021, 8, 17)
        else:
            first = form_qs.aggregate(Min(date_hierarchy))[
                date_hierarchy+'__min'].date()
            last = now

        last_str = last.strftime('%Y-%m-%d')

        for k, v in time_dict.items():
            if first > v['machine_add_date']:
                v['first_date'] = first.strftime('%Y-%m-%d')
            else:
                v['first_date'] = v['machine_add_date'].strftime('%Y-%m-%d')

        day_off_list = day_off_list.filter(off_day__gte=first, off_day__lt=last).values(
            'user_group').annotate(total=Count('id'))
        for i in day_off_list:
            day_off_dict[i['user_group']] = i['total']

        for k, v in time_dict.items():
            business_day = np.busday_count(
                v['first_date'], last_str, v['week_mask']) - day_off_dict.get(k, 0)

            v['total_hour'] = business_day * v['daily_hour']

        return time_dict


def get_current_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + "__day" in request.GET:
        return "day"
    if date_hierarchy + "__month" in request.GET:
        return "month"
    if date_hierarchy + "__year" in request.GET:
        return "year"
    return "all"


def get_date_from_request(request, date_hierarchy):
    year = request.GET.get(date_hierarchy+"__year")
    month = request.GET.get(date_hierarchy+"__month")
    if year:
        year = int(year)
    if month:
        month = int(month)
    return year, month

# ======================== DT by Waktu


class ReportDowntimePerWaktu(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "DT2. Report Downtime By Time"
        verbose_name_plural = "DT2. Report Downtime By Time"


@admin.register(ReportDowntimePerWaktu)
class ReportDowntimePerWaktuAdmin(ReportAdmin):
    date_hierarchy = "normalized_date"
    list_filter = [UserGroupFilter,
                   "machine__priority", MesinFilter, WorkerFilter]
    change_list_template = "admin/downtime_by_mesin_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ===== if something in query params
        is_machine_query = any("machine" in query for query in request.GET)

        # ================= Check date format
        period = self.get_next_in_date_hierarchy(
            request,
            self.date_hierarchy,
        )

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        downtime_data = qs.annotate(
            period=Trunc(
                self.date_hierarchy,
                period,
            )
        ).values("period", 'detaildowntime__kategori'
                 ).annotate(downtime=Sum('detaildowntime__durasi')
                            ).order_by("period")

        summary_data = qs.annotate(
            period=Trunc(
                self.date_hierarchy,
                period,
            ),
        ).values("period"
                 ).annotate(uptime=Sum('effective_hour'), downtime=Sum('downtime')
                            ).order_by("period")

        # ================= Processing the context data
        total_time = get_total_time_time_row(
            summary_data, period, self.date_hierarchy, is_machine_query)
        downtime_data = downtime_data

        for d in downtime_data:
            d["period"] = self.format_time(d, period)

        for d in summary_data:
            d["idle_time"] = total_time[d["period"]] - \
                d["uptime"] - d["downtime"]
            d["period"] = self.format_time(d, period)

        tanggal_list = {i["period"] for i in downtime_data}
        tanggal_list = list(tanggal_list)

        if period == "day":
            tanggal_list.sort()

        kategori_list = DetailDowntime._meta.get_field('kategori').choices
        kategori_list = [('NAN1', col["date"]),
                         ('NAN2', col["eff_hour"]), ('NAN3', col["dt"]), ('NAN3', col["idle"])] + kategori_list
        kode_list = [i[0] for i in kategori_list]
        nama_list = [i[1] for i in kategori_list]

        kode_idx = enumerate(kode_list)
        tanggal_idx = enumerate(tanggal_list)
        kode_idx = dict((j, i) for i, j in kode_idx)
        tanggal_idx = dict((j, i) for i, j in tanggal_idx)

        for i in downtime_data:
            if i['downtime'] == None:
                i['downtime'] = 0

        for i in downtime_data:
            i['y'] = tanggal_idx.get(i['period'])
            i['x'] = kode_idx.get(i['detaildowntime__kategori'])

        td = [[0]*len(nama_list) for _ in range(len(tanggal_list))]

        for i, j in enumerate(tanggal_list):
            td[i][0] = j

        for i in downtime_data:
            try:
                td[i['y']][i['x']] = round(i['downtime'], 2)
            except:
                pass

        for i in summary_data:
            td[tanggal_idx.get(i['period'])][1] = round(i['uptime'], 2)
            td[tanggal_idx.get(i['period'])][2] = round(i['downtime'], 2)
            td[tanggal_idx.get(i['period'])][3] = round(i['idle_time'], 2)

        sum_kode = list(zip(*td))
        try:
            sum_kode.pop(0)
            sum_kode = [map(float, content) for content in sum_kode]
            sum_kode = map(sum, sum_kode)
        except:
            pass
        sum_kode = list(sum_kode)
        sum_kode = [round(i, 2) for i in sum_kode]

        td = [list(map(td_mapper, data)) for data in td]

        response.context_data["table_fields"] = nama_list
        response.context_data["summary"] = td
        response.context_data["summary_total"] = sum_kode

        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__day" in request.GET:
            return "kk"
        if date_hierarchy + "__month" in request.GET:
            return "day"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
    ):
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")
        if period == "day":
            return data["period"].strftime("%d %b %Y")

#============================ RM by KK ============================#


class ReportRawMaterialPerKK(KK):
    class Meta:
        proxy = True
        verbose_name = "RM1. Raw Material Report"
        verbose_name_plural = "RM1. Raw Material Report"


@admin.register(ReportRawMaterialPerKK)
class ReportRawMaterialPerKKAdmin(ReportAdmin):
    date_hierarchy = "creation_date"
    inlines = [ReportListKKInline]
    change_list_template = "admin/report_rm_change_list.html"
    list_filter = (UserGroupFilter, KKMesinFilter, "aktif",
                   "is_export", "cleaning", "trial", HiddenItemMode)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        query = request.GET.copy()
        url = request.build_absolute_uri(request.path)

        if 'item_mode' in query:
            query.pop('item_mode')
            link_str = "Item Code"
            mode = "group"
        else:
            query.appendlist('item_mode', 'group')
            link_str = "Item Group"
            mode = "code"

        query = query.urlencode()
        switch_path = "{}?{}".format(url, query)
        switch_link = format_html("<a href='{}'>{}</a>", switch_path, link_str)
        response.context_data["itemgroup_switch"] = switch_link

        # ----------------- QUERYSET EXTRACTION
        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        ids = qs.values_list('id', flat=True)
        qs = KK.objects.filter(id__in=ids)

        ids = qs.values("productionform")
        qs = ProductionForm.objects.filter(id__in=ids)

        if "machine__id" in request.GET:
            qs = qs.filter(machine=request.GET["machine__id"])

        metrics = {
            "rm_usage": Sum('detailmaterialconsumption__qty_pakai'),
            # "fg" : Sum('fg'),
            # "reject" : Sum('reject') + Sum('trimming') + Sum('hold'),
            # "waste" : Sum('waste')
        }

        if mode == "group":
            period = self.get_next_in_date_hierarchy(
                request, self.date_hierarchy)
            if period == "kk":
                data = qs.values(period=F("no_kk__no_kk"), bahan=F('detailmaterialconsumption__bahan__group__group'),
                                 ).annotate(**metrics).order_by('period')
            else:
                data = qs.annotate(
                    period=Trunc(
                        "no_kk__" + self.date_hierarchy,
                        period,
                    )
                ).values("period", bahan=F('detailmaterialconsumption__bahan__group__group')
                         ).annotate(**metrics).order_by('period')

            daftar_y = data.order_by('bahan').values_list(
                'bahan', flat=True).distinct()
            daftar_y = list(daftar_y)

            try:
                daftar_y.remove(None)
            except:
                pass

            if period == "kk":
                daftar_x = data.values_list('period', flat=True).distinct()
                daftar_x = list(daftar_x)
                produk = data.values('no_kk__no_kk', produk=F(
                    'detailproductionresults__produk__nama'))
            else:
                daftar_x = data.values('period').distinct()
                daftar_x = [self.format_time(i, period) for i in daftar_x]

            # SUSUN ARRAY
            daftar_x = ["Raw Material Group"] + daftar_x

            data = list(data)

            data = [i for i in data if i['bahan'] != None]

            if period != "kk":
                for i in data:
                    i["period"] = self.format_time(i, period)

            idx_x = enumerate(daftar_x)
            idx_y = enumerate(daftar_y)
            idx_x = dict((j, i) for i, j in idx_x)
            idx_y = dict((j, i) for i, j in idx_y)

            for i in data:
                i['x'] = idx_x.get(i['period'])
                i['y'] = idx_y.get(i['bahan'])

            td = [["-"]*len(daftar_x) for _ in range(len(daftar_y))]

            for i, j in enumerate(daftar_y):
                td[i][0] = j

            for i in data:
                td[i['y']][i['x']] = round(i['rm_usage'], 2)

            td = [list(x) for x in zip(*td)]

            del td[0]
            del daftar_x[0]

            if period == "kk":
                for i in produk:
                    i['x'] = idx_x.get(i['no_kk__no_kk']) - 1

                daftar_produk = ["-" for i in range(len(daftar_x))]
                for i in produk:
                    daftar_produk[i['x']] = i['produk']

                for i, kk in enumerate(daftar_x):
                    td[i] = [kk, daftar_produk[i]] + td[i]
                daftar_x = ["Period", col["item"]] + daftar_y
            else:
                for i, kk in enumerate(daftar_x):
                    td[i] = [kk] + td[i]
                daftar_x = ["Period"] + daftar_y

        elif mode == "code":
            period = self.get_next_in_date_hierarchy(
                request, self.date_hierarchy)
            if period == "kk":
                data = qs.values(period=F("no_kk__no_kk"), bahan=F('detailmaterialconsumption__bahan__nama'),
                                 ).annotate(**metrics).order_by('period')
            else:
                data = qs.annotate(
                    period=Trunc(
                        "no_kk__" + self.date_hierarchy,
                        period,
                    )
                ).values("period", bahan=F('detailmaterialconsumption__bahan__nama')
                         ).annotate(**metrics).order_by('period')

            daftar_y = data.order_by('bahan').values_list(
                'bahan', flat=True).distinct()
            daftar_y = list(daftar_y)

            try:
                daftar_y.remove(None)
            except:
                pass

            if period == "kk":
                daftar_x = data.values_list('period', flat=True).distinct()
                daftar_x = list(daftar_x)
            else:
                daftar_x = data.values('period').distinct()
                daftar_x = [self.format_time(i, period) for i in daftar_x]

            # SUSUN ARRAY
            daftar_x = [col["item"], "Subtotal"] + daftar_x

            data = list(data)

            data = [i for i in data if i['bahan'] != None]

            if period != "kk":
                for i in data:
                    i["period"] = self.format_time(i, period)

            idx_x = enumerate(daftar_x)
            idx_y = enumerate(daftar_y)
            idx_x = dict((j, i) for i, j in idx_x)
            idx_y = dict((j, i) for i, j in idx_y)

            for i in data:
                i['x'] = idx_x.get(i['period'])
                i['y'] = idx_y.get(i['bahan'])

            td = [["-"]*len(daftar_x) for _ in range(len(daftar_y))]

            for i, j in enumerate(daftar_y):
                td[i][0] = j

            for i in data:
                td[i['y']][i['x']] = round(i['rm_usage'], 2)

            for i, td_row in enumerate(td):
                td[i][1] = sum(
                    val for val in td_row if isinstance(val, numbers.Number))
                td[i][1] = round(td[i][1], 2)

        response.context_data["table_fields"] = daftar_x
        response.context_data["summary"] = td

        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__month" in request.GET:
            return "kk"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
    ):
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")
        if period == "kk":
            idx = data["no_kk"]
            url = reverse(
                'admin:form_produksi_reportbykk_change', args=[idx])
            return format_html("<a href='{}'>{}</a>", url, data["no_kk__no_kk"])

#============================ Report By Mesin vs TIme ============================#


class ReportPerMesin(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "SMT3. Report Machine vs Time"
        verbose_name_plural = "SMT3. Report Machine vs Time"


@admin.register(ReportPerMesin)
class ReportPerMesinAdmin(ReportAdmin):
    date_hierarchy = "normalized_date"
    change_list_template = "admin/report_by_mesin_vs_waktu_change_list.html"
    list_filter = [UserGroupFilter, "machine__priority", ProductFilter,
                   WIPFilter, ExportFilter, TrialFilter, CleaningFilter]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        query = request.GET.copy()
        ug_list = request.user.userprofile.factory_group.all()
        period = self.get_next_in_date_hierarchy(request, self.date_hierarchy)

        # ----------------- QUERYSET EXTRACTION

        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(user_group__in=ug_list)
        except (AttributeError, KeyError):
            return response

        ids = qs.values_list('id', flat=True)
        qs = ProductionForm.objects.filter(id__in=ids)

        data = qs.annotate(period=Trunc(self.date_hierarchy, period)).values(
            "period", "machine__mesin")
        data = data.annotate(fg_=Sum("fg"),
                             fty=Sum("fg")/Sum("total_output"),
                             performance=Sum("earn_hour") /
                             Sum("effective_hour"),
                             availibility=Sum("effective_hour") /
                             Sum("total_hour"),
                             oee=Sum("fg")/Sum("total_output") *
                             Sum("earn_hour")/Sum("total_hour")
                             ).order_by('period')

        daftar_y = MasterMesin.objects.filter(
            user_group__in=ug_list).values_list('mesin', flat=True).distinct()

        if "user_group__id__exact" in query:
            daftar_y = daftar_y.filter(
                user_group=query["user_group__id__exact"])

        daftar_y = list(daftar_y)

        if period == "day":
            year = query[self.date_hierarchy + "__year"]
            year = int(year)
            month = query[self.date_hierarchy + "__month"]
            month = int(month)
            day = monthrange(year, month)[1]
            day = list(range(1, day + 1))
            daftar_x = [date(year, month, i) for i in day]
        else:
            daftar_x = data.values('period').distinct()
            daftar_x = [self.format_time(i, period) for i in daftar_x]

        data = list(data)

        for i in data:
            i["period"] = self.format_time(i, period)

        idx_x = enumerate(daftar_x)
        idx_y = enumerate(daftar_y)
        idx_x = dict((j, i) for i, j in idx_x)
        idx_y = dict((j, i) for i, j in idx_y)

        for i in data:
            i['x'] = idx_x.get(i['period'])
            i['y'] = idx_y.get(i['machine__mesin'])

        td = [{"mesin": mesin, "fg": ["-" for _ in range(len(daftar_x))], "fty": ["-" for _ in range(len(daftar_x))],
               "performance": ["-" for _ in range(len(daftar_x))], "availibility": ["-" for _ in range(len(daftar_x))],
               "oee": ["-" for _ in range(len(daftar_x))]} for mesin in daftar_y]

        for i in data:
            try:
                td[i['y']]["fg"][i['x']] = "{:,.2f}".format(i['fg_'])
            except:
                td[i['y']]["fg"][i['x']] = 0

            try:
                td[i['y']]["performance"][i['x']
                                          ] = "{:.2%}".format(i['performance'])
            except:
                td[i['y']]["performance"][i['x']] = "{:.2%}".format(0)

            try:
                td[i['y']]["availibility"][i['x']
                                           ] = "{:.2%}".format(i['availibility'])
            except:
                td[i['y']]["availibility"][i['x']] = "{:.2%}".format(0)

            try:
                td[i['y']]["fty"][i['x']] = "{:.2%}".format(i['fty'])
            except:
                td[i['y']]["fty"][i['x']] = "{:.2%}".format(0)

            try:
                td[i['y']]["oee"][i['x']] = "{:.2%}".format(i['oee'])
            except:
                td[i['y']]["oee"][i['x']] = "{:.2%}".format(0)

        response.context_data["table_fields"] = daftar_x
        response.context_data["summary"] = td
        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__month" in request.GET:
            return "day"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
    ):
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")
        if period == "day":
            return data["period"].date()

    def none_to_zero(i):
        if i == None:
            return "-"
        else:
            return i

#============================ Report By Mesin Detailed ============================#


class ReportPerMesinDetailed(KK):
    class Meta:
        proxy = True
        verbose_name = "SMW3. Report By Machine"
        verbose_name_plural = "SMW3. Report By Machine"


@admin.register(ReportPerMesinDetailed)
class ReportPerMesinDetailedAdmin(ReportAdmin):
    date_hierarchy = "creation_date"
    change_list_template = "admin/report_by_mesin_detailed_change_list.html"
    list_filter = (UserGroupFilter, ('creation_date', DateRangeFilter), HiddenRMSplitFilter, KKWIPFilter,
                   KKTrialCustomFilter, "cleaning")

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        q_params = request.GET.copy()

        # ----------------- QUERYSET EXTRACTION

        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        ids = qs.values_list('id', flat=True)
        qs = KK.objects.filter(id__in=ids)

        ids = qs.values("productionform")
        qs = ProductionForm.objects.filter(id__in=ids)

        metrics = {
            "eff_hour": Sum("effective_hour"),
            "downtime": Sum("downtime"),
            "rm": Sum("raw_material"),
            "finished_goods": Sum("fg"),
            "reject": Sum("reject"),
            "trimming": Sum("trimming"),
            "waste": Sum("waste"),
            "scrap_dipakai": Sum("scrap_usage"),
            "scrap_dihasilkan": Sum("scrap_hasil"),
            "scrap_selisih": Sum("scrap_hasil") - Sum("scrap_usage"),
            "availibility": Sum("effective_hour") / Sum("total_hour"),
            "performance": Sum("earn_hour") / Sum("effective_hour"),
            "fty": Sum("fg") / (Sum("total_output")),
            "oee": Sum("fg")
            / (Sum("total_output"))
            * Sum("earn_hour") / Sum("effective_hour")
            * Sum("effective_hour") / Sum("total_hour"),
            "fg_qty": Sum("fg_qty"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "fg_theory": Sum("fg_mass_std"),
        }

        if "rm_split" in q_params:
            metrics["rm"] = Sum("rm_split")

        data = qs.values(mesin=F("machine__mesin")).annotate(
            **metrics).order_by('mesin')

        daftar_y = data.values_list('mesin', flat=True).distinct()
        daftar_y = list(daftar_y)

        metrik = [("rm", "f"), ("finished_goods", "f"), ("fg_theory", "f"), ("fg_qty", "f"), ("fg_lm", "f"), ("fg_m2", "f"), ("fty", "p"), ("availibility", "p"), ("performance", "p"),
                  ("oee", "p"), ("scrap_dipakai", "f"), ("scrap_dihasilkan", "f"), ("scrap_selisih", "f"), ("reject", "f"), ("trimming", "f"), ("waste", "f"), ("eff_hour", "f"), ("downtime", "f"), ]

        daftar_x = [col["machine"],
                    col["rm"],
                    col["fg"],
                    col["fg_theory"],
                    col["fg_qty"],
                    col["fg_lm"],
                    col["fg_m2"],
                    col["FTY"],
                    col["avail"],
                    col["perf"],
                    col["oee"],
                    col["scrap_use"],
                    col["scrap_prod"],
                    col["scrap_chg"],
                    col["rj"], col["tr"],
                    col["ws"],
                    col["eff_hour"],
                    col["dt"],
                    ]
        data = list(data)

        td = []

        for i in data:
            buffer = []
            buffer.append(i["mesin"])
            for key in metrik:
                buffer.append(format_table_content(i[key[0]], key[1]))

            td.append(buffer)

        total_data = qs.aggregate(**metrics)

        summary_total = []
        for key in metrik:
            summary_total.append(format_table_content(total_data[key[0]], key[1]))

        response.context_data["table_fields"] = daftar_x
        response.context_data["summary"] = td
        response.context_data["summary_total"] = summary_total
        return response

#============================ Report By Product Group ============================#


class ReportPerProductGroup(KK):
    class Meta:
        proxy = True
        verbose_name = "SMW4. Report By Product Group"
        verbose_name_plural = "SMW4. Report By Product Group"


@admin.register(ReportPerProductGroup)
class ReportPerProductGroupAdmin(ReportAdmin):
    date_hierarchy = "creation_date"
    change_list_template = "admin/report_by_product_group_change_list.html"
    list_filter = (UserGroupFilter, ('creation_date', DateRangeFilter), KKWIPFilter, "is_export",
                   KKTrialCustomFilter, "cleaning")

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        # ----------------- QUERYSET EXTRACTION

        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(
                user_group__in=request.user.userprofile.factory_group.all())
        except (AttributeError, KeyError):
            return response

        ids = qs.values_list('id', flat=True)
        qs = KK.objects.filter(id__in=ids)

        ids = qs.values("productionform")
        qs = ProductionForm.objects.filter(id__in=ids)

        metrics = {
            "eff_hour": Sum("effective_hour"),
            "downtime": Sum("downtime"),
            "rm": Sum("raw_material"),
            "finished_goods": Sum("fg"),
            "reject": Sum("reject"),
            "trimming": Sum("trimming"),
            "waste": Sum("waste"),
            "scrap_dipakai": Sum("scrap_usage"),
            "scrap_dihasilkan": Sum("scrap_hasil"),
            "scrap_selisih": Sum("scrap_hasil") - Sum("scrap_usage"),
            "availibility": Sum("effective_hour") / Sum("total_hour"),
            "performance": Sum("earn_hour") / Sum("effective_hour"),
            "fty": Sum("fg") / (Sum("total_output")),
            "oee": Sum("fg")
            / (Sum("total_output"))
            * Sum("earn_hour") / Sum("effective_hour")
            * Sum("effective_hour") / Sum("total_hour"),
            "fg_qty": Sum("fg_qty"),
            "fg_lm": Sum("fg_lm"),
            "fg_m2": Sum("fg_m2"),
            "fg_theory": Sum("fg_mass_std"),
        }

        data = qs.values("no_kk__item_example__group__group").annotate(
            **metrics).order_by('no_kk__item_example__group__group')

        daftar_y = data.values_list(
            'no_kk__item_example__group__group', flat=True).distinct()
        daftar_y = list(daftar_y)

        daftar_y = ['Unspecified' if v == None else v for v in daftar_y]

        metrik = [("rm", "f"), ("finished_goods", "f"), ("fg_theory", "f"), ("fg_qty", "f"), ("fg_lm", "f"), 
                  ("fg_m2", "f"), ("fty", "p"), ("availibility", "p"), ("performance", "p"),
                  ("oee", "p"), ("scrap_dipakai", "f"), ("scrap_dihasilkan", "f"), ("scrap_selisih", "f"), 
                  ("reject", "f"), ("trimming", "f"), ("waste", "f"), ("eff_hour", "f"), ("downtime", "f"), ]

        daftar_x = [col["item_group"],
                    col["rm"],
                    col["fg"],
                    col["fg_theory"],
                    col["fg_qty"],
                    col["fg_lm"],
                    col["fg_m2"],
                    col["FTY"],
                    col["avail"],
                    col["perf"],
                    col["oee"],
                    col["scrap_use"],
                    col["scrap_prod"],
                    col["scrap_chg"],
                    col["rj"], col["tr"],
                    col["ws"],
                    col["eff_hour"],
                    col["dt"],
                    ]

        data = list(data)

        td = []

        for i in data:
            buffer = []
            if i["no_kk__item_example__group__group"] == None:
                buffer.append("Unspecified")
            else:
                buffer.append(i["no_kk__item_example__group__group"])
            for key in metrik:
                buffer.append(format_table_content(i[key[0]], key[1]))

            td.append(buffer)

        total_data = qs.aggregate(**metrics)

        summary_total = []
        for key in metrik:
            summary_total.append(format_table_content(total_data[key[0]], key[1]))

        response.context_data["table_fields"] = daftar_x
        response.context_data["summary"] = td
        response.context_data["summary_total"] = summary_total
        return response

# ============================ Checking active time =======================#


class MachineDailyTime(ProductionForm):
    class Meta:
        proxy = True
        verbose_name = "CK1. Machine Daily Time"
        verbose_name_plural = "CK1. Machine Daily Time"


@admin.register(MachineDailyTime)
class MachineDailyTimeAdmin(ReportAdmin):
    date_hierarchy = "normalized_date"
    change_list_template = "admin/machine_daily_time_change_list.html"
    list_filter = [UserGroupFilter]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        query = request.GET.copy()
        ug_list = request.user.userprofile.factory_group.all()
        period = self.get_next_in_date_hierarchy(request, self.date_hierarchy)

        # ----------------- QUERYSET EXTRACTION

        try:
            qs = response.context_data["cl"].queryset
            qs = qs.filter(user_group__in=ug_list)
        except (AttributeError, KeyError):
            return response

        data = qs.annotate(period=Trunc(self.date_hierarchy, period)).values(
            "period", "machine__mesin", "machine__id", "user_group__id")
        data = data.annotate(total_time=Sum("total_hour"), time_percent=Sum(
            "total_hour")/F("user_group__groupprofile__daily_work_hour")).order_by('period')

        daftar_y = MasterMesin.objects.filter(
            user_group__in=ug_list).values_list('mesin', flat=True).distinct()

        if "user_group__id__exact" in query:
            daftar_y = daftar_y.filter(
                user_group=query["user_group__id__exact"])

        daftar_y = list(daftar_y)

        if period == "day":
            year = query[self.date_hierarchy + "__year"]
            year = int(year)
            month = query[self.date_hierarchy + "__month"]
            month = int(month)
            day = monthrange(year, month)[1]
            day = list(range(1, day + 1))
            daftar_x = [date(year, month, i) for i in day]
        else:
            daftar_x = data.values('period').distinct()
            daftar_x = [self.format_time(i, period) for i in daftar_x]

        daftar_x = ["Mesin"] + daftar_x

        data = list(data)

        for i in data:
            i["period"] = self.format_time(i, period)

        idx_x = enumerate(daftar_x)
        idx_y = enumerate(daftar_y)
        idx_x = dict((j, i) for i, j in idx_x)
        idx_y = dict((j, i) for i, j in idx_y)

        for i in data:
            i['x'] = idx_x.get(i['period'])
            i['y'] = idx_y.get(i['machine__mesin'])

        td = [[[0, 0, [0, 0, 0]] for _ in daftar_x] for mesin in daftar_y]

        for idx, name in enumerate(daftar_y):
            td[idx][0] = name

        for i in data:
            if period == "day":
                link_date = daftar_x[i['x']]
                if i['time_percent'] > 1:
                    td[i['y']][i['x']][1] = 1
                try:
                    td[i['y']][i['x']][0] = "{:.2f} ({:.2%})".format(
                        i['total_time'], i['time_percent'])
                except:
                    td[i['y']][i['x']][0] = 0
                url = reverse('admin:form_produksi_reportperwaktu_changelist')
                query = ("machine__id__exact={}&normalized_date__day={}&normalized_date__month={}&normalized_date__year={}&user_group__id__exact={}").format(
                    i['machine__id'], link_date.day, link_date.month, link_date.year, i['user_group__id'])
                td[i['y']][i['x']][2] = url + "?" + query
            else:
                try:
                    td[i['y']][i['x']][0] = "{:.2f}".format(i['total_time'])
                except:
                    td[i['y']][i['x']][0] = 0

        response.context_data["table_fields"] = daftar_x
        response.context_data["summary"] = td
        return response

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + "__month" in request.GET:
            return "day"
        if date_hierarchy + "__year" in request.GET:
            return "month"
        return "year"

    def format_time(
        self,
        data,
        period,
    ):
        if period == "month":
            return data["period"].strftime("%B")
        if period == "year":
            return data["period"].strftime("%Y")
        if period == "day":
            return data["period"].date()

    def none_to_zero(i):
        if i == None:
            return "-"
        else:
            return i

# ============================ Custom Function ============================#


def hm_to_h(time_string):
    hm = time_string
    h = int(hm[:2])
    m = int(hm[3:])
    time = h + (m / 60.0)
    return time


def calc_duration(mulai, selesai):
    durasi = datetime(1, 1, 10)
    dummy = date(1, 1, 1)
    awal = datetime.combine(dummy, mulai)
    akhir = datetime.combine(dummy, selesai)

    durasi += akhir - awal
    h = durasi.hour
    m = durasi.minute
    time = h + (m / 60.0)
    return time


def to_percent(data):
    try:
        return "{:.2%}".format(data)
    except:
        return "{:.2%}".format(0)


def td_mapper(data):
    if data == 0:
        return '-'
    elif isinstance(data, int) or isinstance(data, float):
        return "{:,.2f}".format(data)
    else:
        return data


def format_table_content(data, format):
    if format == "f":
        if data == 0:
            return '-'
        else:
            try:
                return "{:,.2f}".format(data)
            except:
                return "Error"
    elif format == "p":
        try:
            return "{:.2%}".format(data)
        except:
            return "Error"
    else:
        return data


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=admin.widgets.AdminDateWidget())
    end_date = forms.DateField(widget=admin.widgets.AdminDateWidget())
