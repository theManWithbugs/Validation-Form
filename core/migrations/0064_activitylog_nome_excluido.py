# Generated by Django 5.1.1 on 2024-10-07 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_rename_cpf_activitylog_cpf_excluido'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='nome_excluido',
            field=models.CharField(default=1, max_length=80),
            preserve_default=False,
        ),
    ]