from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoInvestimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, verbose_name='Nome do tipo')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Tipo de investimento',
                'verbose_name_plural': 'Tipos de investimento',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Investimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_investido', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Valor investido (R$)')),
                ('data_aplicacao', models.DateField(blank=True, null=True, verbose_name='Data de aplicação')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='investimentos', to='clientes.cliente', verbose_name='Cliente')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='investimentos', to='investimentos.tipoinvestimento', verbose_name='Tipo de investimento')),
            ],
            options={
                'verbose_name': 'Investimento',
                'verbose_name_plural': 'Investimentos',
                'ordering': ['-valor_investido'],
            },
        ),
    ]
