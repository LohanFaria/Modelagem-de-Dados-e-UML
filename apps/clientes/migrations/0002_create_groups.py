from django.db import migrations


def criar_grupos_e_permissoes(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Criar os 3 grupos
    consultor, _ = Group.objects.get_or_create(name='Consultor')
    gestor, _ = Group.objects.get_or_create(name='Gestor')
    auditor, _ = Group.objects.get_or_create(name='Auditor')

    # Permissões do Consultor: view e add nos modelos de domínio, sem delete
    perms_consultor = Permission.objects.filter(
        codename__in=[
            'view_cliente', 'add_cliente', 'change_cliente',
            'view_telefone', 'add_telefone', 'change_telefone',
            'view_email', 'add_email', 'change_email',
            'view_contabancaria', 'add_contabancaria', 'change_contabancaria',
            'view_saldohistorico', 'add_saldohistorico',
            'view_investimento', 'add_investimento', 'change_investimento',
            'view_tipoinvestimento',
            'view_contato', 'add_contato', 'change_contato',
            'view_funcionario', 'view_formacontato', 'view_assunto',
        ]
    )
    consultor.permissions.set(perms_consultor)

    # Permissões do Gestor: todas as permissões de domínio
    perms_gestor = Permission.objects.filter(
        content_type__app_label__in=['clientes', 'investimentos', 'relacionamento', 'importacao', 'relatorios']
    )
    gestor.permissions.set(perms_gestor)

    # Permissões do Auditor: somente leitura (view_*)
    perms_auditor = Permission.objects.filter(
        codename__startswith='view_'
    )
    auditor.permissions.set(perms_auditor)


def reverter_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Consultor', 'Gestor', 'Auditor']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(criar_grupos_e_permissoes, reverter_grupos),
    ]
