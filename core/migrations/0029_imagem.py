# Generated by Django 5.0.7 on 2024-08-29 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_cidadao_renda_individual_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagens/')),
                ('descricao', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]