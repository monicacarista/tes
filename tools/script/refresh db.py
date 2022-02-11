from form_produksi.models import ProductionForm, DetailProductionResults
from form_produksi.models import DetailMaterialConsumption, DetailDowntime
from form_produksi.models import DetailPackagingUsage, KK
from tqdm import tqdm

data = ProductionForm.objects.all()
for i in tqdm(data):
    i.save()

data = DetailMaterialConsumption.objects.all()
for i in tqdm(data):
    i.save()

data = DetailProductionResults.objects.all()
for i in tqdm(data):
    i.save()

data = DetailDowntime.objects.all()
for i in tqdm(data):
    i.save()

data = ProductionForm.objects.filter(user_group_id=6)
for i in tqdm(data):
    i.save()

data = KK.objects.filter(user_group_id=4)
for i in tqdm(data):
    i.save()