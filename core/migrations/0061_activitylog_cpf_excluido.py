# Generated by Django 5.1.1 on 2024-10-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_remove_activitylog_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='cpf_excluido',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]