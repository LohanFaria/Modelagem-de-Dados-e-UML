from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from apps.clientes.views_api import ClienteViewSet
from apps.investimentos.views_api import TipoInvestimentoViewSet, InvestimentoViewSet
from apps.relacionamento.views_api import FuncionarioViewSet, ContatoViewSet, ContatoQuarentenaViewSet

admin.site.site_header = "XPTO Investimentos — Administração"
admin.site.site_title = "XPTO Investimentos"
admin.site.index_title = "Gestão Operacional e Financeira"

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='api-cliente')
router.register(r'tipos-investimento', TipoInvestimentoViewSet, basename='api-tipo-investimento')
router.register(r'investimentos', InvestimentoViewSet, basename='api-investimento')
router.register(r'funcionarios', FuncionarioViewSet, basename='api-funcionario')
router.register(r'contatos', ContatoViewSet, basename='api-contato')
router.register(r'quarentena', ContatoQuarentenaViewSet, basename='api-quarentena')

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('relatorios/', include('apps.relatorios.urls')),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
