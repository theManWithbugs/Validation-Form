# Generated by Django 5.0.7 on 2024-08-20 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_historicocriminal_ja_esteve_preso_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cidadao',
            name='remuneracao',
            field=models.CharField(choices=[('Empregado', 'Empregado'), ('Desempregado', 'Desempregado'), ('Trabalhador Rural', 'Trabalhador Rural'), ('Autônomo', 'Autônomo'), ('Funcionario Publico', 'Funcionario Publico'), ('Aposentado', 'Aposentado')], default=1.0, max_length=20),
            preserve_default=False,
        ),
    ]
