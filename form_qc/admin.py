from cProfile import label
from dataclasses import field, fields
from datetime import datetime
from email.errors import FirstHeaderLineIsContinuationDefect
from faulthandler import disable
from pyexpat import model
from select import select
from tokenize import group
from urllib import request
from django.contrib import admin
from django.db import models
from django.contrib.admin import ModelAdmin
from form_qc.models import QCForm, QCInspector, RejectFormSelection, MasterReject, MasterFormParameter, ParameterFormSelection,DetailQCInspection
from masterdata.models import MasterBarang, MasterMesin, MasterGroup
from form_produksi.models import KK
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import widgets
from django.forms import CheckboxSelectMultiple
from django.forms.models import inlineformset_factory
from django import forms
from django.forms import Textarea, TextInput,NumberInput
from django.utils.timezone import now
admin.site.site_header = 'Quality Control'



class OperatorAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
	list_per_page = 10


class MasterPilihanAdmin(admin.ModelAdmin):
	
	fields = ['qc_parameter']
	list_display = ['qc_parameter']
	search_fields = ['qc_parameter']
	list_per_page = 10
	# inlines = [ChoiceInLine]



class MasterDipilihAdmin(admin.ModelAdmin):
	list_display = ['selected_field','note','item_group']
	search_fields = ['selected_field_id']
	list_per_page = 10


# ----------------------Class for Method ----------------------------#
class ForMethod(admin.ModelAdmin):
	list_max_show_all = 1000
#menghilangkan user group
	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_superuser:
			self.exclude.append("user_group")
			# print(Group.user_group)
		return super(ForMethod, self).get_form(request, obj, **kwargs)

#menampilkan sesuai filter
	def get_queryset(self, request):
		qs = super(ForMethod, self).get_queryset(request)
		ug_list = request.user.userprofile.factory_group.all()
		return qs.filter(user_group__in=ug_list)
	#menyimpan user group yang lagi login
	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			obj.user_group = request.user.userprofile.main_group
		obj.save()

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if not request.user.is_superuser:
			user_group_list = request.user.userprofile.factory_group.all()
			if db_field.name == "item_group":
				kwargs["queryset"] = MasterGroup.objects.filter(
				user_group__in=user_group_list
			)
			if db_field.name == "machine":
				kwargs["queryset"] = MasterMesin.objects.filter(
				user_group__in=user_group_list
			)
			if db_field.name == "item":
				kwargs["queryset"] = MasterBarang.objects.filter(
				user_group__in=user_group_list
			)
		if db_field.name == "item_group":
			query_item_group = request.GET.get("item_group")
			object_id = request.path
			if query_item_group:
				group = MasterGroup.objects.filter(id=query_item_group)
			elif 'change' in object_id:
				object_id = object_id.split("/")
				object_id = object_id[object_id.index('change') - 1]
				object_id = int(object_id)
				group = MasterGroup.objects.filter(qcform=object_id)
			else:
				group = MasterGroup.objects.none()
			kwargs["queryset"] = group


		return super().formfield_for_foreignkey(db_field, request, **kwargs)
# ----------------------Class for Method -----------------------------#
###############################################################################################################################################
#------------ParameterDipilih SET 1-----------------------------------#

class TagInLineAdmin(admin.StackedInline):
	model = ParameterFormSelection
	fields = [('selected_field','kategori','note',)]
	extra= 0


class SettingMasterGroupQC(MasterGroup):
	class Meta:
		proxy = True
		verbose_name = "SET 1. QC Parameter"
		verbose_name_plural = "SET 1. QC Paramater"


@admin.register(SettingMasterGroupQC)
class SettingMasterGroupQC(ForMethod):
   
	inlines = [TagInLineAdmin]
	fields = ('group',)
	list_display = ['group','tipe']
	readonly_fields = ('group',)
	search_fields = ["group"]
	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		queryset = queryset.filter(tipe = 2)
		return queryset
#------------ParameterDipilih/SET 1-----------------------------------#
##############################################################################################################################################
#-----------Dictionary-----------------------------------------------#
col1 = {
	1:"dimensi1",
	2:"dimensi2",
	3:"dimensi3",
	4:"dimensi4",
	5:"dimensi5",
	6:"dimensi6",
	7:"dimensi7",
	8:"dimensi8",
	9:"dimensi9",
	10:"dimensi10",
	11:"dimensi11",
	12:"dimensi12",
	13:"dimensi13",
	14:"dimensi14",
	15:"dimensi15",
	16:"dimensi16",
	17:"dimensi17",
	18:"dimensi18",
	19:"dimensi19",
	20:"dimensi20",
	21:"dimensi21",
	22:"dimensi22",
	23:"dimensi23",
	24:"dimensi24",
	25:"dimensi25",
	26:"dimensi26",
	27:"dimensi27",
	28:"dimensi28",
	29:"dimensi29",
	30:"dimensi30",
	31:"dimensi31",
	32:"dimensi32",
	33:"dimensi33",
	34:"dimensi34",
	35:"dimensi35",
	36:"dimensi36",
	37:"dimensi37",
	38:"dimensi38",
	39:"dimensi39",
	40:"dimensi40",
	41:"dimensi41",
	42:"dimensi42",
	43:"dimensi43",
	44:"dimensi44",
	45:"dimensi45",
	46:"dimensi46",
	47:"dimensi47",
	48:"dimensi48",
	49:"dimensi49",
	50:"dimensi50",
	51:"dimensi51",   
	52:"dimensi52",    
	53:"dimensi53",    
	54:"dimensi54",    
	55:"dimensi55",    
	56:"dimensi56",    
	57:"dimensi57",    
	58:"dimensi58",    
	59:"dimensi59",    
	60:"dimensi60",    
	61:"light_transmission",
	62:"squareness1",
	63:"squareness2",
	64:"kelengkungan",
	65:"bowing_max",
	66:"uji_lock",
	67:"gsm",
	68:"machine_rpm",
	69:"machine_pressure",
	70:"machine_torque",
	71:"uv_pinggir",
	72:"uv_tengah",
	73:"uv_inkjet",
	74:"corona_treatment_atas",
	75:"corona_treatment_bawah",
	76:"tekanan_maks_hidrostatik",
	77:"tekanan_maks_burst",
	78:"viskositas_atas",
	79:"viskositas_bawah",
	80:"solid_content",
	81 :"ph",
	82:"rheovis_qty",
	83:"fineness_pre_adjusting",
	84:"fineness_post_adjusting",
	85:"bonding_strength_coil_atas",
	86:"bonding_strength_coil_bwh",
	87:"speed_extruder_adhesive",
	88:"berat",
	89:"skin_time",
	90:"reject_indecisive",
	100:"reject",
	101:"komentar",
	102: "berat1",
	103: "berat2",
 	104: "berat3",
	105: "berat4",
	106: "berat5",
	107: "uv_absorber",
	108: "lembar",
	109: "komentar",
}
#-----------Dictionary-----------------------------------------------#
###############################################################################################################################################
#------------Pengecekan/Form Pengecekan Quality-----------------------#


class TagInLineDetail(admin.StackedInline):
	def get_fieldsets(self, request, obj=None):

		#klao add pke yg skrg edit baru yg baru
		if request.resolver_match.url_name == 'form_qc_qcform_change':
			if obj is not None:
				item_group_id = obj.item_group_id
				selected_param = ParameterFormSelection.objects.filter(item_group_id=item_group_id).values('selected_field', 'kategori','note')
				# select = ParameterFormSelection.objects.filter(item_group_id=change_id).values('selected_field', 'kategori','note')
				selected_fields = {}
				for i in selected_param:
					if i['kategori'] not in selected_fields:
						selected_fields[i['kategori']] = [col1[i['selected_field']]]
					else:
						selected_fields[i['kategori']].append(col1[i['selected_field']])
			
		elif request.resolver_match.url_name == 'form_qc_qcform_add':
			item_group_id = request.GET.get("item_group")
			selected_param = ParameterFormSelection.objects.filter(item_group_id=item_group_id).values('selected_field', 'kategori','note')
			# select = ParameterFormSelection.objects.filter(item_group_id=change_id).values('selected_field', 'kategori','note')
			selected_fields = {}
			for i in selected_param:
				if i['kategori'] not in selected_fields:
					selected_fields[i['kategori']] = [col1[i['selected_field']]]
				else:
					selected_fields[i['kategori']].append(col1[i['selected_field']])
		selected_fields_1 = []
		for k, v in selected_fields.items():
			selected_fields_1.append((k, {'fields':((v),)}))
  		
		fieldsets = (selected_fields_1)

		
		return fieldsets
	
	
	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			obj.user_group = request.user.userprofile.main_group
		obj.save()
		
	def get_formset(self, request, obj,**new_kwargs):
		if request.resolver_match.url_name == 'form_qc_qcform_change':
			if obj is not None:
				item_group_id = obj.item_group_id
				selected_param = ParameterFormSelection.objects.filter(item_group_id=item_group_id).values('selected_field', 'note')
				label = {}
				for i in selected_param:
					label[col1[i['selected_field']]] = i['note']
					new_kwargs = {'labels': label}
		
		elif request.resolver_match.url_name == 'form_qc_qcform_add':

				item_group_id = request.GET.get("item_group")
				selected_param = ParameterFormSelection.objects.filter(item_group_id=item_group_id).values('selected_field', 'note')
				label = {}
				for i in selected_param:
					label[col1[i['selected_field']]] = i['note']
					new_kwargs = {'labels': label}

		inline_formset = super().get_formset(request, obj, **new_kwargs)
		return inline_formset
	   

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		item_group_id = request.GET.get("item_group")
		if db_field.name == "reject" or db_field.name == "reject_indecisive":
			kwargs["queryset"] = MasterReject.objects.filter(item_group_id=item_group_id)
		return super().formfield_for_manytomany(db_field, request, **kwargs)
   
	model = DetailQCInspection

	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
		models.CharField: {'widget': TextInput(attrs={'width':'24'})},
		models.FloatField: {'widget': TextInput(attrs={'size':'5'})},
	}    
 

	extra= 0

col = {
	"it":"Item Group"
}

def link_customize_qc_form(id, item_group):
	url = reverse('admin:form_qc_qcform_add')
	q_param = 'item_group=' + str(id)
	link = "{}?{}".format(url, q_param)
	return format_html("<a href='{}'>{}</a>", link, item_group)

class PengecekanForm(forms.ModelForm):
	item_group = forms.CharField(disabled=False)
	
	class Meta:
		model = QCForm
		fields =['item_group']
   
	 
	# def __init__(self, *args, **kwargs):
	#     super(PengecekanForm, self).__init__(*args, **kwargs)
	#     self.fields['item_group'].queryset = MasterGroup.objects.filter(item_group = request.item_group)
	#     self.fields['item_group'].widget.attrs['disabled'] = 'disabled'
  

def duplicate(modeladmin, request, queryset):
	for self in queryset:
		# fks_to_copy = list(self.detailqcinspection_set.all())
		pengecekan = self.pengecekan_ke + 1
		self.pk = None
		self.inspection_date = datetime.now()
		self.pengecekan_ke = pengecekan
		self.save()

		new_pk = self.pk

		foreign_keys = {}
		# for fk in fks_to_copy:
		# 	fk.pk = None
		# 	fk.laporan = QCForm.objects.get(id=new_pk)

		# 	try:
		# 		foreign_keys[fk.__class__].append(fk)
		# 	except KeyError:
		# 		foreign_keys[fk.__class__] = [fk]

		for cls, list_of_fks in foreign_keys.items():
			cls.objects.bulk_create(list_of_fks)


duplicate.allowed_permissions = ('change',)


@admin.register(QCForm)
class AdminPengecekanQC(ForMethod):
	search_fields = ["item_group__group"]
	inlines = [TagInLineDetail]
	change_list_template = "admin/qc_form_change_list.html"
	autocomplete_fields = ["item","no_kk"]
	actions = [duplicate]
	list_display = ["item_group","no_kk","user_group","shift","qc_inspector","inspection_date","customer","machine","pengecekan_ke"]
	formfield_overrides = {

		models.CharField: {'widget': TextInput(attrs={'size':25})},
	
	}    

	def get_tipe(self,obj):
		# print(obj.operator.nama_operator)
		tipe= obj.item_group.tipe
		return tipe

	def changelist_view(self, request, extra_context=None):
		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		query_params = request.GET
		q_expression = Q(
		  tipe__in=[2,3], user_group__in=request.user.userprofile.factory_group.all())

		if query_params.get("q"):
			queries = query_params.get("q")
			queries = queries.split()

			for wo in queries:
				q_expression &= Q(group__icontains=wo)

			qs = MasterGroup.objects.filter(
				q_expression).order_by('group')

		else:
			qs = MasterGroup.objects.filter(q_expression).order_by('group')

		table_content = [
			{
				'item_group': data.group,
				'id': data.id,
				# 'creation_date': data.creation_date,
				'link': link_customize_qc_form(data.id, data.group),
			} for data in qs
		]

		try:
			response.context_data["table_content"] = table_content
			response.context_data["table_fields"] = [
			 "Item Group"]
		except:
			pass

		return response

#------------Detail Pengecekan/DetailAdmin----------------------------#
def getFieldsModel(model): # untuk menampilkan smua field di list display
	
	return [field.name for field in model._meta.get_fields()]


@admin.register(DetailQCInspection)
class DetailAdmin(ModelAdmin):

	list_display = ['dimensi1','dimensi30','get_reject']

#------------Detail Pengecekan/DetailAdmin----------------------------#
#------------Pengecekan/Form Pengecekan Quality-----------------------#
###############################################################################################################################################W
#------------Master Reject--------------------------------------------#
class MasterRejectAdmin(admin.ModelAdmin):
	list_display = ['item_group','reject_type']
	search_fields = ['reject_type']
	list_per_page = 10

#------------Master Reject--------------------------------------------#
################################################################################################################################################
#------------Reject Form Selection/ Reject dipilih--------------------#

class TagInLineReject(admin.StackedInline):
	model = RejectFormSelection
	fields = [('reject_type','aspekFungsional','aspekParameter','aspekCritical')]
	extra= 0

class SettingMasterGroupQC1(MasterGroup):
	class Meta:
		proxy = True
		verbose_name = "SET 2. QC Reject"
		verbose_name_plural = "SET 2. QC Reject"

@admin.register(SettingMasterGroupQC1)
class SettingMasterGroupQC1(ForMethod):
   
	inlines = [TagInLineReject]
	fields = ('group',)
	list_display = ['group','tipe']
	readonly_fields = ('group',)
	search_fields = ["group"]
	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		queryset = queryset.filter(tipe = 2)
		return queryset

#------------Reject Form Selection/ Reject dipilih--------------------#

admin.site.register(QCInspector, OperatorAdmin)
admin.site.register(MasterFormParameter,MasterPilihanAdmin)
admin.site.register(ParameterFormSelection,MasterDipilihAdmin)
admin.site.register(MasterReject,MasterRejectAdmin)

