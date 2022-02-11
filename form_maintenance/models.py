from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from django.db.models import Count, Sum, F, Func, IntegerField, FloatField
from django.db.models.deletion import CASCADE, PROTECT
from django.utils import timezone

from datetime import date, time, datetime

from masterdata.models import MasterMesin, MasterGroup
from django.contrib.auth.models import Group as UserGroup

from django.urls import reverse
from django.core.mail import send_mail

class BreakdownEvent(models.Model):
    """Model representing the form for maintenance documentation."""
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=1,
        choices=(("1", "Active"), ("0", "Closed")),
        default="1"
    )
    no_form = models.CharField(
        max_length=32
    )
    machine = models.ForeignKey(MasterMesin, on_delete=models.PROTECT)
    report_time = models.DateTimeField()
    breakdown_note = models.TextField(help_text="Divisi Produksi isi sampai sini")

    def __str__(self):
        return "{}: {}".format(self.no_form, self.machine)

class BreakdownFix(models.Model):
    breakdown_event = models.OneToOneField("BreakdownEvent", on_delete=CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    breakdown_type = models.CharField(
        max_length=1,
        choices=(("1", "Mechanical"), ("2", "Electrical"))
    )
    technician = models.ForeignKey("MasterTechnician", on_delete=models.PROTECT)
    broken_section = models.ForeignKey("MasterMachineSection", on_delete=models.PROTECT)
    broken_part = models.ManyToManyField("MasterMachinePart")
    fixing_note = models.TextField()

class MasterMachineSection(models.Model):
    """Model representing the form for maintenance documentation."""
    name = models.CharField(
        max_length=64
    )
    def __str__(self):
        return self.name

class MasterMachinePart(models.Model):
    """Model representing the form for maintenance documentation."""
    name = models.CharField(
        max_length=64
    )
    def __str__(self):
        return self.name

class MasterTechnician(models.Model):
    """Model representing the form for maintenance documentation."""
    user_group = models.ForeignKey(Group, on_delete=models.PROTECT)
    name = models.CharField(
        max_length=32,
    )
    status = models.CharField(
        max_length=1,
        choices=(("1", "Active"), ("0", "Inactive")),
        default="1"
    )
    def __str__(self):
        return self.name