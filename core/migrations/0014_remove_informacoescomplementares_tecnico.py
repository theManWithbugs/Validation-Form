# Generated by Django 5.0.7 on 2024-08-22 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_informacoescomplementares_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informacoescomplementares',
            name='tecnico',
        ),
    ]