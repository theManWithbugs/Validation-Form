# Generated by Django 5.0.7 on 2024-08-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_historicosaude_tratamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicosaude',
            name='deficiencia',
            field=models.CharField(choices=[('', 'Selecione'), ('SIM', 'Sim'), ('NAO', 'Não')], default='Selecione', max_length=100, verbose_name='É portador de alguma deficiência'),
        ),
    ]
