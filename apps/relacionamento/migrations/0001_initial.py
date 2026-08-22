from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60, unique=True, verbose_name='Assunto / Produto')),
            ],
            options={
                'verbose_name': 'Assunto',
                'verbose_name_plural': 'Assuntos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ContatoQuarentena',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linha_origem', models.JSONField(verbose_name='Linha bruta da planilha')),
                ('motivo', models.CharField(choices=[('CLIENTE_INEXISTENTE', 'CPF não encontrado na base de clientes'), ('CPF_INVALIDO', 'CPF com dígito verificador inválido'), ('DADO_FALTANTE', 'Campo obrigatório ausente')], max_length=30, verbose_name='Motivo')),
                ('detalhe', models.TextField(blank=True, verbose_name='Detalhe do problema')),
                ('importado_em', models.DateTimeField(auto_now_add=True, verbose_name='Importado em')),
                ('resolvido', models.BooleanField(default=False, verbose_name='Resolvido?')),
            ],
            options={
                'verbose_name': 'Contato em quarentena',
                'verbose_name_plural': 'Contatos em quarentena',
                'ordering': ['-importado_em'],
            },
        ),
        migrations.CreateModel(
            name='FormaContato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30, unique=True, verbose_name='Forma de contato')),
            ],
            options={
                'verbose_name': 'Forma de contato',
                'verbose_name_plural': 'Formas de contato',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do funcionário')),
                ('matricula', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Matrícula')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_contato', models.DateField(verbose_name='Data do contato')),
                ('observacao', models.TextField(blank=True, verbose_name='Observação')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('assunto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='relacionamento.assunto', verbose_name='Assunto')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contatos', to='clientes.cliente', verbose_name='Cliente')),
                ('forma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='relacionamento.formacontato', verbose_name='Forma de contato')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contatos', to='relacionamento.funcionario', verbose_name='Funcionário')),
            ],
            options={
                'verbose_name': 'Contato',
                'verbose_name_plural': 'Contatos',
                'ordering': ['-data_contato'],
                'indexes': [models.Index(fields=['cliente', '-data_contato'], name='relacioname_cliente_b428d0_idx')],
            },
        ),
    ]
