# Generated by Django 5.0.7 on 2024-08-19 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_historicosaude_deficiencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicocriminal',
            name='prisao_familiar_justificativa',
        ),
        migrations.AddField(
            model_name='cidadao',
            name='idade',
            field=models.CharField(default='0', max_length=3),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='grau_de_parentesco',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='ja_esteve_preso',
            field=models.CharField(blank=True, choices=[('', 'Selecione'), ('S', 'Sim'), ('N', 'Não')], max_length=3),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='juiz_de_origem',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='medida_aplicada',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='numero_do_processo',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='reincidencia',
            field=models.CharField(blank=True, choices=[('', 'Selecione'), ('S', 'Sim'), ('N', 'Não')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='sugest_encaminhamento',
            field=models.CharField(blank=True, choices=[('SASDH', 'SASDH'), ('NATERA-MP', 'NATERA-MP'), ('GRUPO NAA OU AA', 'GRUPO NAA OU AA'), ('INTERNAÇÃO EM COMUNIDADE TERAPÊUTICA', 'INTERNAÇÃO EM COMUNIDADE TERAPÊUTICA'), ('RETIRADA DE DOCUMENTOS-IML', 'RETIRADA DE DOCUMENTOS-IML'), ('CAPS-AD |||/CAPS-SAMAUMA', 'CAPS-AD |||/CAPS-SAMAUMA'), ('OUTROS', 'OUTROS')], max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='sugestao_de_trabalho',
            field=models.CharField(blank=True, choices=[('DEPENDENCIA QUIMICA', 'DEPENDENCIA QUIMICA'), ('MULHERES', 'MULHERES'), ('OUTRO DELITOS', 'OUTROS DELITOS'), ('PRESTAÇÃO DE SERVÇOS A COMUNIDADE', 'PRESTAÇÃO DE SERVÇOS A COMUNIDADE'), ('TRAFICO DE DROGAS', 'TRAFICO DE DROGAS'), ('TRANSITO', 'TRANSITO'), ('VIOLÊNCIA DOMESTICA', 'VIOLÊNCIA DOMESTICA')], max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='tipo_penal',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='violencia_dome_nome_vitima',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='historicocriminal',
            name='violencia_domestica',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicocriminal',
            name='cidadao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cidadao'),
        ),
        migrations.AlterField(
            model_name='historicocriminal',
            name='prisao',
            field=models.CharField(blank=True, default='Desconhecida', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicocriminal',
            name='prisao_familiar',
            field=models.CharField(blank=True, choices=[('', 'Selecione'), ('S', 'Sim'), ('N', 'Não')], max_length=3),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='cidadao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historicos_saude', to='core.cidadao'),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='deficiencia',
            field=models.CharField(default='Desconhecida', max_length=100),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='medicacao_controlada',
            field=models.CharField(default='Não especificado', max_length=100),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='saude',
            field=models.CharField(default='default_value', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='tratamento',
            field=models.CharField(default='Não especificado', max_length=100),
        ),
        migrations.AlterField(
            model_name='historicosaude',
            name='tratamento_psiquiatrico',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.CreateModel(
            name='InformacoesComplementares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantas_pessoas', models.CharField(max_length=100)),
                ('nome_familiar', models.CharField(max_length=70)),
                ('parentesco', models.CharField(max_length=100)),
                ('idade_familiar', models.CharField(default='0', max_length=3)),
                ('escolaridade_familiar', models.CharField(max_length=100)),
                ('ocupacao', models.CharField(max_length=100)),
                ('analise_descritiva', models.CharField(max_length=300)),
                ('cidadao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informacoes_complementares', to='core.cidadao')),
            ],
        ),
        migrations.DeleteModel(
            name='InformacoesTecnicas',
        ),
    ]