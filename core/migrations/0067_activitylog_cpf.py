# Generated by Django 5.1.1 on 2024-10-09 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_armtime_process_equal'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='cpf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='log_atividades', to='core.cidadao'),
            preserve_default=False,
        ),
    ]
