from django.contrib import admin
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
from django.contrib.admin.options import ModelAdmin, StackedInline
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

from form_maintenance.models import (
    BreakdownEvent,
    BreakdownFix,
    MasterMachineSection,
    MasterMachinePart,
    MasterTechnician
)

from masterdata.models import (
    MasterMesin
)

# Register your models here.
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
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class BreakdownFixInline(StackedInline):
    model = BreakdownFix
    autocomplete_fields = ["technician", "broken_part", "broken_section"]
    extra = 0

@admin.register(BreakdownEvent)
class BreakdownEventAdmin(UnitSpecificModelAdmin):
    search_fields = ["no_form"]
    list_display = ["machine", "user_group"]
    autocomplete_fields = ["machine"]
    inlines = [BreakdownFixInline]
    #list_filter = [UserGroupFilter]

@admin.register(MasterMachineSection)
class MasterMachinePartAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(MasterMachinePart)
class MasterSparepartAdmin(ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(MasterTechnician)
class MasterTechnicianAdmin(UnitSpecificModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    #list_filter = [UserGroupFilter]