# Generated by Django 5.0.7 on 2024-08-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_historicosaude_deficiencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='cidadao',
            name='moradia_situacao',
            field=models.CharField(blank=True, choices=[('PROPIA', 'Propia'), ('ALUGADO', 'Alugado'), ('CEDIDO', 'Cedido'), ('OCUPACAO', 'Ocupação'), ('IRREGULAR', 'Irregular'), ('SITUACAO DE RUA', 'Situação de rua')], max_length=15, null=True, verbose_name='Situação de moradia, tipo de ocupação'),
        ),
        migrations.AddField(
            model_name='cidadao',
            name='moradia_tipo',
            field=models.CharField(blank=True, choices=[('ALVENARIA', 'Alvenaria'), ('MADEIRA', 'Madeira'), ('MISTA', 'Mista')], max_length=9, null=True, verbose_name='Tipo de moradia'),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='endereco',
            field=models.CharField(max_length=80, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='idade',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='nome',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='nome_social',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='deficiencia',
            field=models.CharField(choices=[('', 'Selecione'), ('SIM', 'Sim'), ('NAO', 'Não')], max_length=3, verbose_name='É portador de alguma deficiência'),
        ),
        migrations.AlterField(
            model_name='informacoescomplementares',
            name='idade_familiar',
            field=models.CharField(blank=True, max_length=3, verbose_name='Idade do familiar'),
        ),
        migrations.AlterField(
            model_name='informacoescomplementares',
            name='quantas_pessoas',
            field=models.CharField(max_length=2, verbose_name='Quantas pessoas moram com você ? (inclua você na contagem)'),
        ),
        migrations.AlterField(
            model_name='informacoescomplementares',
            name='tecnico_responsavel',
            field=models.CharField(max_length=200, verbose_name='Técnico responsavel'),
        ),
    ]