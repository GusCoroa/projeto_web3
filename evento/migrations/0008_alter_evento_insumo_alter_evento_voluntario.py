# Generated by Django 5.1.7 on 2025-05-23 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0007_remove_evento_post'),
        ('insumo', '0002_alter_insumo_options_alter_insumo_descricao_and_more'),
        ('voluntario', '0003_alter_voluntario_sexo_alter_voluntario_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='insumo',
            field=models.ManyToManyField(blank=True, related_name='eventos', to='insumo.insumo'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='voluntario',
            field=models.ManyToManyField(blank=True, related_name='eventos', to='voluntario.voluntario'),
        ),
    ]
