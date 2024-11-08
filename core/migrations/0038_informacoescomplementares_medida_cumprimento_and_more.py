# Generated by Django 5.0.7 on 2024-09-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_alter_cidadao_escolaridade'),
    ]

    operations = [
        migrations.AddField(
            model_name='informacoescomplementares',
            name='medida_cumprimento',
            field=models.CharField(choices=[('', 'Selecione'), ('COMPARECIMENTO BIMESTRAL', 'COMPARECIMENTO BIMESTRAL'), ('COMPARECIMENTO MENSAL', 'COMPARECIMENTO MENSAL'), ('COMPARECIMENTO QUINZENAL', 'COMPARECIMENTO QUINZENAL'), ('COMPARECIMENTO SEMANAL', 'COMPARECIMENTO SEMANAL'), ('COMPARECIMENTO TRIMESTRAL', 'COMPARECIMENTO TRIMESTRAL'), ('GRUPO REFLEXIVO', 'GRUPO REFLEXIVO'), ('PSC', 'PSC')], default='selecione', max_length=50, verbose_name='Medida de cumprimento'),
        ),
        migrations.AddField(
            model_name='informacoescomplementares',
            name='tip_penal',
            field=models.CharField(choices=[('', 'Selecione'), ('VIOLENCIA DOMESTICA', 'VIOLÊNCIA DOMÉSTICA'), ('TRANSITO', 'TRÂNSITO'), ('CRIME DE DROGAS', 'CRIME DE DROGAS'), ('OUTROS CRIMES', 'OUTROS CRIMES'), ('LESAO CORPORAL', 'LESÃO CORPORAL'), ('CRIME DE ARMA', 'CRIME DE ARMA'), ('ESTELIONATO', 'ESTELIONATO')], default='selecione', max_length=30, verbose_name='Tipificação penal'),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='escolaridade',
            field=models.CharField(choices=[('SELECIONE', 'Selecione'), ('NAO ESCOLARIZADO', 'Não escolarizado'), ('FUNDAMENTAL INCOMPLETO', 'Fundamental incompleto'), ('FUNDAMENTAL COMPLETO', 'Fundamental completo'), ('MEDIO INCOMPLETO', 'Médio Incompleto'), ('MEDIO COMPLETO', 'Médio Completo'), ('SUPERIOR INCOMPLETO', 'Superior Incompleto'), ('SUPERIOR COMPLETO', 'Superior Completo'), ('POS GRADUAÇÃO', 'Pós-Graduação'), ('MESTRADO', 'Mestrado'), ('DOUTORADO', 'Doutorado'), ('POS-DOUTORADO', 'Pós Doutorado'), ('NÃO DETERMINADO', 'Não determinado')], default='selecione', max_length=22),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='estado_civil',
            field=models.CharField(choices=[('', 'Selecione'), ('SOLTEIRO', 'Solteiro'), ('CASADO', 'Casado'), ('UNIAO ESTAVEL', 'União Estavel'), ('SEPARADO', 'Separado'), ('DIVORCIADO', 'Divorciado'), ('VIUVO', 'Viúvo')], default='selecione', max_length=20),
        ),
        migrations.AlterField(
            model_name='cidadao',
            name='nome_social',
            field=models.CharField(blank=True, default='Não informado', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='informacoescomplementares',
            name='escolaridade_familiar',
            field=models.CharField(choices=[('SELECIONE', 'Selecione'), ('NAO ESCOLARIZADO', 'Não escolarizado'), ('FUNDAMENTAL INCOMPLETO', 'Fundamental incompleto'), ('FUNDAMENTAL COMPLETO', 'Fundamental completo'), ('MEDIO INCOMPLETO', 'Médio Incompleto'), ('MEDIO COMPLETO', 'Médio Completo'), ('SUPERIOR INCOMPLETO', 'Superior Incompleto'), ('SUPERIOR COMPLETO', 'Superior Completo'), ('POS GRADUAÇÃO', 'Pós-Graduação'), ('MESTRADO', 'Mestrado'), ('DOUTORADO', 'Doutorado'), ('POS-DOUTORADO', 'Pós Doutorado'), ('NÃO DETERMINADO', 'Não determinado')], default='selecione', max_length=30, verbose_name='Grau de Escolaridade do familiar'),
        ),
    ]
