from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "XPTO Investimentos — Administração"
admin.site.site_title = "XPTO Investimentos"
admin.site.index_title = "Gestão Operacional e Financeira"

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('relatorios/', include('apps.relatorios.urls')),
]

