from django.contrib import admin
from django.contrib.auth.models import Group

from masterdata.models import MasterWorker, MasterStatus, MasterMesin
from masterdata.models import (
    MasterBarang,
    MasterGroup,
    MasterTipe,
    MasterWarna,
    MasterUOM,
    MasterKapasitasMesin,
    MasterItemProperty,
    DayOffList
)
from form_produksi.models import KK

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.apps import apps

from django.db import models
from django import forms
from django.contrib.admin import widgets, SimpleListFilter

from django.contrib.auth.models import Group as UserGroup

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User
from masterdata.models import UserProfile, GroupProfile

from urllib.parse import parse_qs, urlparse

id_fg = 2
id_wip = 3
id_unit_group = "1"
# ============================ Custom Auth ============================#
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Additional User Data'
    filter_horizontal = ('factory_group',)

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'Additional Group Data'

# Define a new User admin
class UserGroupAdmin(BaseGroupAdmin):
    inlines = (GroupProfileInline,)
    list_filter = ['groupprofile__group_type']

# Re-register UserAdmin
admin.site.unregister(Group)
admin.site.register(Group, UserGroupAdmin)

# ============================ Custom Filter ============================#
class ItemGroupFilter(SimpleListFilter):
    title = "Item Group"
    parameter_name = "group_id"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        get_params = request.GET
        try:
            selected_user = get_params["user_group__id__exact"]
        except:
            return None

        daftar_group = MasterGroup.objects.filter(user_group__id=selected_user).all().order_by('group')
        return [(group.id, group.group) for group in daftar_group]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group__id=self.value())
        else:
            return queryset

class UserGroupFilter(SimpleListFilter):
    title = "Unit Pabrik"
    parameter_name = "user_group__id__exact"
    template = "admin/aux_dropdown_filter.html"

    def lookups(self, request, model_admin):
        daftar_unit = UserGroup.objects.filter(
            id__in=request.user.userprofile.factory_group.filter(groupprofile__group_type=id_unit_group)).order_by('name')
        return [(unit.id, unit.name) for unit in daftar_unit]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_group__id=self.value())
        else:
            return queryset

# ============================ Actions ============================#

def make_item_inactive(modeladmin, request, queryset):
    queryset.update(aktif='0')

make_item_inactive.allowed_permissions = ('change',)


# ============================ Standar ============================#

for i in [
    MasterStatus,
    MasterTipe,
    MasterWarna,
    MasterUOM,
]:
    try:
        admin.site.register(i)
    except:
        pass



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user__groups',
        'user',
        'content_type',
        'action_flag',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ug_list = list(request.user.userprofile.factory_group.all())
        return qs.filter(user__groups__in=ug_list)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
    
admin.site.register(MasterItemProperty)

class UnitSpecificModelAdmin(admin.ModelAdmin):
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
        ug_list = list(request.user.userprofile.factory_group.all())
        return qs.filter(user_group__in=ug_list)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        ug_list = list(request.user.userprofile.factory_group.all())
        if db_field.name == "machine" or db_field.name == "mesin":
            kwargs["queryset"] = MasterMesin.objects.filter(user_group__in=ug_list)
        if db_field.name == "group":
            kwargs["queryset"] = MasterGroup.objects.filter(
                user_group__in=ug_list
            )
        if db_field.name == "foreman":
            kwargs["queryset"] = MasterWorker.objects.filter(user_group__in=ug_list)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "team":
                kwargs["queryset"] = MasterWorker.objects.filter(
                    user_group__in=request.user.userprofile.factory_group.all()
                )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(MasterBarang)
class MasterBarangAdmin(UnitSpecificModelAdmin):
    search_fields = ["nama", "kode_barang"]
    list_filter = [UserGroupFilter, ItemGroupFilter, "group__kategori_rm", "tipe", 'profil']
    actions = [make_item_inactive, ]
    list_display = [
        "id",
        "nama",
        "kode_barang",
        "tipe",
        "group",
        "panjang",
        "tebal1",
        "lebar",
        "berat_standar_fg",
        "warna",
        "uom",
        "profil",
        "tebal2",
        "aktif",
    ]

    def get_queryset(self, request):
        qs = super(UnitSpecificModelAdmin, self).get_queryset(request)
        ug_list = request.user.userprofile.factory_group.all()
        ug_list = ug_list.values_list('id', flat=True)
        ug_list = list(ug_list)
        return qs.filter(user_group__id__in=ug_list)

    def get_search_results(self, request, queryset, search_term):
        if search_term == "":
            url = request.META.get('HTTP_REFERER')
            no_kk = parse_qs(urlparse(url).query).get('no_kk')
            if no_kk and request.GET["field_name"] == 'bahan':
                no_kk = int(no_kk[0])
                kk = KK.objects.filter(id=no_kk)
            elif 'prefilledform' in url and 'change' in url:
                object_id = url.split("/")
                object_id = object_id[object_id.index('change') - 1]
                object_id = int(object_id)
                kk = KK.objects.filter(productionform=object_id)
            else:
                kk = None
                
            if kk:
                item_list = kk.values_list("detailkkrawmaterial__bahan__id", flat=True)
                item_list = MasterBarang.objects.filter(id__in=item_list)
                queryset = item_list

        return super().get_search_results(request, queryset, search_term)

@admin.register(MasterMesin)
class MasterMesinAdmin(UnitSpecificModelAdmin):
    search_fields = ["mesin"]
    list_display = ["id", "mesin", "user_group"]
    list_filter = [UserGroupFilter]
    readonly_fields = ["id"]

@admin.register(MasterWorker)
class MasterWorkerAdmin(UnitSpecificModelAdmin):
    readonly_fields = ["id"]
    list_display = ["id", "nama", "status", "aktif", "user_group"]
    list_filter = [UserGroupFilter]

@admin.register(MasterGroup)
class MasterGroupAdmin(UnitSpecificModelAdmin):
    readonly_fields = ["id"]
    list_filter = [UserGroupFilter]
    list_display = ["id", "group", "user_group", "tipe", "kategori_rm"]

@admin.register(MasterKapasitasMesin)
class MasterKapasitasMesinAdmin(UnitSpecificModelAdmin):
    search_fields = ["mesin__mesin", "group__group"]
    readonly_fields = ["id"]
    list_display = [
        "mesin",
        "user_group",
        "group",
        "warna",
        "tebal",
        "dimensi_aux",
        "item_property",
        "output_ideal",
        "dl_standar",
    ]
    autocomplete_fields = ['mesin']
    
    list_filter = [UserGroupFilter]

@admin.register(DayOffList)
class MasterGroupAdmin(UnitSpecificModelAdmin):
    date_hierarchy = "off_day"
    readonly_fields = ["id"]
    list_filter = ["off_day"]
    list_display = ["user_group", "off_day", "notes"]