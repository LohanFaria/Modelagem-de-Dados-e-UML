import apps.clientes.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome completo')),
                ('cpf', models.CharField(help_text='Formato: 000.000.000-00', max_length=14, unique=True, validators=[apps.clientes.validators.validar_cpf], verbose_name='CPF')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ContaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=60, verbose_name='Banco')),
                ('agencia', models.CharField(max_length=10, verbose_name='Agência')),
                ('conta', models.CharField(max_length=20, verbose_name='Conta')),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas', to='clientes.cliente')),
            ],
            options={
                'verbose_name': 'Conta bancária',
                'verbose_name_plural': 'Contas bancárias',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('principal', models.BooleanField(default=False, verbose_name='Principal?')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='clientes.cliente')),
            ],
            options={
                'verbose_name': 'E-mail',
                'verbose_name_plural': 'E-mails',
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20, verbose_name='Número')),
                ('tipo', models.CharField(choices=[('CELULAR', 'Celular'), ('FIXO', 'Fixo'), ('COMERCIAL', 'Comercial'), ('OUTRO', 'Outro')], default='CELULAR', max_length=10, verbose_name='Tipo')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to='clientes.cliente')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
        ),
        migrations.CreateModel(
            name='SaldoHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_saldo', models.DateField(verbose_name='Data do saldo')),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Saldo (R$)')),
                ('registrado_em', models.DateTimeField(auto_now_add=True)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saldos', to='clientes.contabancaria')),
            ],
            options={
                'verbose_name': 'Histórico de saldo',
                'verbose_name_plural': 'Históricos de saldo',
                'ordering': ['-data_saldo'],
            },
        ),
        migrations.AddConstraint(
            model_name='contabancaria',
            constraint=models.UniqueConstraint(fields=('banco', 'agencia', 'conta'), name='unique_banco_agencia_conta'),
        ),
        migrations.AddConstraint(
            model_name='saldohistorico',
            constraint=models.UniqueConstraint(fields=('conta', 'data_saldo'), name='unique_conta_data_saldo'),
        ),
    ]
