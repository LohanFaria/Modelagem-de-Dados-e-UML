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
]
