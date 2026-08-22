from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.painel_relatorios, name='painel'),
    path('carteira/', views.carteira_cliente, name='carteira_cliente'),
    path('investimentos-tipo/', views.investimentos_por_tipo, name='investimentos_tipo'),
    path('evolucao-saldo/', views.evolucao_saldo, name='evolucao_saldo'),
    path('produtividade/', views.produtividade_funcionarios, name='produtividade'),
    path('reativacao/', views.clientes_sem_contato, name='reativacao'),
    path('qualidade-dados/', views.qualidade_dados, name='qualidade_dados'),
    # Exportação para Excel
    path('exportar/investimentos/', views.exportar_investimentos_xlsx, name='exportar_investimentos'),
    path('exportar/reativacao/', views.exportar_reativacao_xlsx, name='exportar_reativacao'),
    path('exportar/produtividade/', views.exportar_produtividade_xlsx, name='exportar_produtividade'),
]
