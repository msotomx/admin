# Generated by Django 4.2 on 2025-05-16 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0002_compra_detallecompra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='flete',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
