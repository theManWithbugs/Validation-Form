# Generated by Django 5.1.1 on 2024-10-08 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_remove_activitylog_nome_excluido'),
    ]

    operations = [
        migrations.AddField(
            model_name='armtime',
            name='process_equal',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]