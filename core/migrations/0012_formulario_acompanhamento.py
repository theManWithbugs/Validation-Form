# Generated by Django 5.0.7 on 2024-08-22 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_user_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='formulario_acompanhamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=12)),
                ('tecnico', models.CharField(max_length=100)),
                ('evolucao_percepcoes', models.CharField(max_length=255)),
                ('cidadao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formulario_acompanhamento', to='core.cidadao')),
            ],
        ),
    ]
