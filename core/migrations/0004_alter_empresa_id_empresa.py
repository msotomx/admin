# Generated by Django 4.2 on 2025-04-21 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_empresa_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='id_empresa',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
