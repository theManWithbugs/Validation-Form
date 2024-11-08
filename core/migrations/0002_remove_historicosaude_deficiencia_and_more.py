# Generated by Django 5.0.7 on 2024-08-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicosaude',
            name='Deficiencia',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='Deficiencia_just',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='drogas_jus',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='medica_ctL',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='medica_ctL_jus',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='saude_just',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='tratmentPS',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='tratmentPS_just',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='tratmento',
        ),
        migrations.RemoveField(
            model_name='historicosaude',
            name='tratmento_jus',
        ),
        migrations.AddField(
            model_name='historicosaude',
            name='medicacao_controlada',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicosaude',
            name='tratamento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicosaude',
            name='tratamento_psiquiatrico',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='drogas_uso',
            field=models.CharField(blank=True, choices=[('Álcool', 'Álcool'), ('Cigarro', 'Cigarro'), ('Maconha', 'Maconha'), ('Pasta Base', 'Pasta Base'), ('Cocaína', 'Cocaína'), ('Merla', 'Merla'), ('Crack', 'Crack'), ('Outras drogas', 'Outras drogas')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='saude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicosaude',
            name='deficiencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
