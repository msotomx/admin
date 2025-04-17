# Generated by Django 4.2 on 2025-04-17 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('almacen', models.CharField(default='01', max_length=2)),
                ('nombre', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=3)),
                ('subcategoria', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ClaveMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave_movimiento', models.CharField(default='01', max_length=2)),
                ('nombre', models.CharField(max_length=30, null=True)),
                ('tipo', models.CharField(default='E', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=6)),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=13)),
                ('telefono', models.CharField(max_length=12)),
                ('direccion', models.TextField(null=True)),
                ('codigo_postal', models.CharField(default='00000', max_length=5)),
                ('ciudad', models.CharField(max_length=100, null=True)),
                ('direccion_entrega', models.TextField(null=True)),
                ('codigo_postal_entrega', models.CharField(default='00000', max_length=5)),
                ('ciudad_entrega', models.CharField(max_length=100, null=True)),
                ('telefono1', models.CharField(max_length=13, null=True)),
                ('telefono2', models.CharField(max_length=13, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('plazo_credito', models.SmallIntegerField(default=0)),
                ('limite_credito', models.BigIntegerField(default=0)),
                ('cuenta_cnt', models.CharField(max_length=24, null=True)),
                ('retencion_iva', models.BooleanField(default='False')),
                ('retencion_isr', models.BooleanField(default='False')),
                ('ieps', models.BooleanField(default='False')),
                ('campo_libre_str', models.CharField(max_length=50, null=True)),
                ('campo_libre_real', models.FloatField(default=0, max_length=15)),
                ('comentarios', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(default='', max_length=12)),
                ('subcategoria', models.CharField(max_length=3)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(null=True)),
                ('precio1', models.DecimalField(decimal_places=2, max_digits=9)),
                ('precio2', models.DecimalField(decimal_places=2, max_digits=9)),
                ('precio3', models.DecimalField(decimal_places=2, max_digits=9)),
                ('precio4', models.DecimalField(decimal_places=2, max_digits=9)),
                ('precio5', models.DecimalField(decimal_places=2, max_digits=9)),
                ('precio6', models.DecimalField(decimal_places=2, max_digits=9)),
                ('maximo', models.IntegerField(default=0)),
                ('minimo', models.IntegerField(default=0)),
                ('reorden', models.IntegerField(default=0)),
                ('fecha_registro', models.DateField()),
                ('imagen', models.ImageField(blank=True, upload_to='productos')),
                ('descuento_venta', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('costo_reposicion', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('iva', models.DecimalField(decimal_places=4, max_digits=10)),
                ('campo_libre_str', models.CharField(max_length=50, null=True)),
                ('campo_libre_real', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField(null=True)),
                ('contacto', models.CharField(max_length=100)),
                ('telefono1', models.CharField(max_length=13)),
                ('telefono2', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('plazo_credito', models.SmallIntegerField(default=0)),
                ('comentarios', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(default='01', max_length=2)),
                ('nombre', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidad_medida', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Traspaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=8)),
                ('fecha_traspaso', models.DateField()),
                ('alm1', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='traspasos_salida', to='web.almacen')),
                ('alm2', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='traspasos_entrada', to='web.almacen')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaldoInicial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Existencia', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fecha', models.DateField()),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.almacen')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Remision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_remision', models.CharField(max_length=6)),
                ('numero_factura', models.CharField(max_length=20, null=True)),
                ('fecha_remision', models.DateField()),
                ('monto_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estado', models.CharField(choices=[('C', 'Cotizacion'), ('P', 'Pedido'), ('R', 'Remisionado'), ('F', 'Facturado')], default='R', max_length=1)),
                ('clave_remision', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.clavemovimiento')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.proveedor'),
        ),
        migrations.AddField(
            model_name='producto',
            name='unidad_de_medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.unidadmedida'),
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=8)),
                ('move_s', models.CharField(max_length=1)),
                ('fecha_movimiento', models.DateField()),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.almacen')),
                ('clave_movimiento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.clavemovimiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_empresa', models.CharField(max_length=8)),
                ('directorio', models.CharField(max_length=8)),
                ('fecha_inicio', models.DateField()),
                ('almacen_actual', models.CharField(default='01', max_length=2)),
                ('almacen_facturacion', models.CharField(default='01', max_length=2)),
                ('decimales_unidades', models.SmallIntegerField(default='2')),
                ('decimales_importe', models.SmallIntegerField(default='2')),
                ('cuenta_iva', models.CharField(max_length=24, null=True)),
                ('clave_compras', models.CharField(default='CO', max_length=2)),
                ('clave_traspasos', models.CharField(default='TR', max_length=2)),
                ('clave_remision', models.CharField(default='RE', max_length=2)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=9)),
                ('retencion_iva', models.DecimalField(decimal_places=5, max_digits=9)),
                ('retencion_isr', models.DecimalField(decimal_places=5, max_digits=9)),
                ('ieps', models.DecimalField(decimal_places=5, max_digits=9)),
                ('ip', models.CharField(max_length=24, null=True)),
                ('empresa', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleTraspaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.producto')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.traspaso')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('numero_remision', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.remision')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.cliente')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.movimiento')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipoCliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.tipocliente'),
        ),
    ]
