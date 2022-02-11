
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import include, path
from datetime import datetime

admin.site.site_header = 'Impack Manufacturing & Reporting Information System'
admin.site.site_title = "Impack Manufacturing & Reporting Information System"
admin.site.index_title = "Menu List"
now = datetime.now()
redirect_path = 'admin/form_produksi/reportperunit/?normalized_date__month={}&normalized_date__year={}'.format(now.month, now.year)

urlpatterns = [
            path('admin/', admin.site.urls),

            ]

urlpatterns += [
             path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
             path('', RedirectView.as_view(url=redirect_path )),
             ]


