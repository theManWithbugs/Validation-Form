# Generated by Django 5.0.7 on 2024-09-09 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_acompcentral_data_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acompcentral',
            name='evolucao_percepcoes',
            field=models.CharField(max_length=400, verbose_name='Evolução/ Demanda/ Percepções:'),
        ),
        migrations.AlterField(
            model_name='acompcentral',
            name='tecnico_responsavel',
            field=models.CharField(max_length=80, verbose_name='Técnico responsavel:'),
        ),
        migrations.AlterField(
            model_name='historicocriminal',
            name='numero_do_processo',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='ArmTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('cidadao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time', to='core.cidadao')),
            ],
        ),
    ]
