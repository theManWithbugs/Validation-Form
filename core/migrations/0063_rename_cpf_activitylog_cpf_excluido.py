# Generated by Django 5.1.1 on 2024-10-07 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_rename_cpf_excluido_activitylog_cpf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitylog',
            old_name='cpf',
            new_name='cpf_excluido',
        ),
    ]