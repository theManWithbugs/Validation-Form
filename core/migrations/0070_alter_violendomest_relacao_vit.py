# Generated by Django 5.1.1 on 2024-10-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_remove_armtime_process_equal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violendomest',
            name='relacao_vit',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Que tipo de relação mantém atualmente com a vitima?'),
        ),
    ]