# Generated by Django 4.2 on 2025-06-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fac', '0008_alter_detallefactura_tasa_ieps_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='estatus',
            field=models.CharField(choices=[('BORRADOR', 'Borrador'), ('VIGENTE', 'Vigente'), ('CANCELADA', 'Cancelado'), ('ERROR', 'Error')], max_length=10),
        ),
    ]
