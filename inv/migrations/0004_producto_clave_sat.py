# Generated by Django 4.2 on 2025-05-20 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0003_alter_compra_flete'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='clave_sat',
            field=models.CharField(default='', max_length=8),
        ),
    ]
