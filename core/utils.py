from core.models import Empresa, EmpresaDB   
from django.core.exceptions import PermissionDenied

import threading
from threading import local

def cargar_datos_iniciales(db_alias):
    from inv.models import UnidadMedida, ClaveMovimiento, Moneda, Almacen, Categoria, Proveedor
    from fac.models import FormaPago, MetodoPago, UsoCfdi, TipoComprobante, Exportacion
    from cxc.models import RegimenFiscal, TipoCliente
    from core.models import Empresa

    if not FormaPago.objects.using(db_alias).exists():
        FormaPago.objects.using(db_alias).bulk_create([
            FormaPago(forma_pago='01', nombre='Efectivo'),
            FormaPago(forma_pago='02', nombre='Cheque nominativo'),
            FormaPago(forma_pago='03', nombre='Transferencia electrónica de fondos'),
            FormaPago(forma_pago='04', nombre='Tarjeta de crédito'),
            FormaPago(forma_pago='05', nombre='Monedero electrónico'),
            FormaPago(forma_pago='06', nombre='Dinero electrónico'),
            FormaPago(forma_pago='08', nombre='Vales de despensa'), 
            FormaPago(forma_pago='12', nombre='Dación en pago'),
            FormaPago(forma_pago='13', nombre='Pago por subrogación'),
            FormaPago(forma_pago='14', nombre='Pago por consignación'),
            FormaPago(forma_pago='15', nombre='Condonación'),
            FormaPago(forma_pago='17', nombre='Compensación'),
            FormaPago(forma_pago='23', nombre='Novación'),
            FormaPago(forma_pago='24', nombre='Confusión'),
            FormaPago(forma_pago='25', nombre='Remisión de deuda'),
            FormaPago(forma_pago='26', nombre='Prescripción o caducidad'),
            FormaPago(forma_pago='27', nombre='Satisfacción del acreedor'),
            FormaPago(forma_pago='28', nombre='Tarjeta de débito'),
            FormaPago(forma_pago='29', nombre='Tarjeta de servicios'),
            FormaPago(forma_pago='30', nombre='Aplicación de anticipos'),
            FormaPago(forma_pago='31', nombre='Intemediario pagos'),
            FormaPago(forma_pago='99', nombre='Por definir'),
        ])

    if not MetodoPago.objects.using(db_alias).exists():
        MetodoPago.objects.using(db_alias).bulk_create([
            MetodoPago(metodo_pago='PUE', nombre='Pago en una sola exhibición'),
            MetodoPago(metodo_pago='PDD', nombre='Pago en parcialidades o diferido'),
        ])

    if not UsoCfdi.objects.using(db_alias).exists():
        UsoCfdi.objects.using(db_alias).bulk_create([
            UsoCfdi(uso_cfdi='G01', nombre='Adquisición de mercancías'),
            UsoCfdi(uso_cfdi='G02', nombre='Devoluciones, descuentos o bonificaciones.'),
            UsoCfdi(uso_cfdi='G03', nombre='Gastos en general'),
            UsoCfdi(uso_cfdi='D01', nombre='Honorarios médicos, dentales y gastos hospitalarios'),
            UsoCfdi(uso_cfdi='D02', nombre='Gastos médicos por incapacidad o discapacidad'),
            UsoCfdi(uso_cfdi='D03', nombre='Gastos funerales'),
            UsoCfdi(uso_cfdi='D04', nombre='Donativos'),
            UsoCfdi(uso_cfdi='D05', nombre='Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
            UsoCfdi(uso_cfdi='D06', nombre='Aportaciones voluntarias al SAR'),
            UsoCfdi(uso_cfdi='D07', nombre='Primas por seguros de gastos médicos'),
            UsoCfdi(uso_cfdi='D08', nombre='Gastos de transportación escolar obligatoria'),
            UsoCfdi(uso_cfdi='D09', nombre='Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones'),
            UsoCfdi(uso_cfdi='D10', nombre='Pagos por servicios educativos (colegiaturas)'),
            UsoCfdi(uso_cfdi='I01', nombre='Construcciones'),
            UsoCfdi(uso_cfdi='I02', nombre='Mobiliario y equipo de oficina por inversiones'),
            UsoCfdi(uso_cfdi='I03', nombre='Equipo de transporte'),
            UsoCfdi(uso_cfdi='I04', nombre='Equipo de computo y accesorios'),
            UsoCfdi(uso_cfdi='I05', nombre='Dados, troqueles, moldes, matrices y herramental'),
            UsoCfdi(uso_cfdi='I06', nombre='Comunicaciones telefónicas'),
            UsoCfdi(uso_cfdi='I07', nombre='Comunicaciones satelitales'),
            UsoCfdi(uso_cfdi='I08', nombre='Otra maquinaria y equipo'),
            UsoCfdi(uso_cfdi='S01', nombre='Sin efectos fiscales'),
            UsoCfdi(uso_cfdi='P01', nombre='Por definir'),
        ])

    if not RegimenFiscal.objects.using(db_alias).exists():
        RegimenFiscal.objects.using(db_alias).bulk_create([
            RegimenFiscal(regimen_fiscal='601', nombre='General de Ley Personas Morales'),
            RegimenFiscal(regimen_fiscal='603', nombre='Personas Morales con Fines no Lucrativos'),
            RegimenFiscal(regimen_fiscal='605', nombre='Sueldos y Salarios e Ingresos Asimilados a Salarios'),
            RegimenFiscal(regimen_fiscal='606', nombre='Arrendamiento'),
            RegimenFiscal(regimen_fiscal='607', nombre='Régimen de Enajenación o Adquisición de Bienes'),
            RegimenFiscal(regimen_fiscal='608', nombre='Demás ingresos'),
            RegimenFiscal(regimen_fiscal='610', nombre='Residentes en el Extranjero sin Establecimiento Permanente en México'),
            RegimenFiscal(regimen_fiscal='611', nombre='Ingresos por Dividendos (socios y accionistas)'),
            RegimenFiscal(regimen_fiscal='612', nombre='Personas Físicas con Actividades Empresariales y Profesionales'),
            RegimenFiscal(regimen_fiscal='614', nombre='Ingresos por intereses'),
            RegimenFiscal(regimen_fiscal='615', nombre='Régimen de los ingresos por obtención de premios'),
            RegimenFiscal(regimen_fiscal='616', nombre='Sin obligaciones fiscales'),
            RegimenFiscal(regimen_fiscal='620', nombre='Sociedades Cooperativas de Producción que optan por diferir sus ingresos'),
            RegimenFiscal(regimen_fiscal='621', nombre='Incorporación Fiscal'),
            RegimenFiscal(regimen_fiscal='622', nombre='Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
            RegimenFiscal(regimen_fiscal='623', nombre='Opcional para Grupos de Sociedades'),
            RegimenFiscal(regimen_fiscal='624', nombre='Coordinados'),
            RegimenFiscal(regimen_fiscal='625', nombre='Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas'),
            RegimenFiscal(regimen_fiscal='626', nombre='Régimen Simplificado de Confianza'),
        ])

    if not UnidadMedida.objects.using(db_alias).exists():
        UnidadMedida.objects.using(db_alias).bulk_create([
            UnidadMedida(unidad_medida='H87', descripcion='Pieza'),
            UnidadMedida(unidad_medida='E48', descripcion='Unidad de servicio'),
            UnidadMedida(unidad_medida='KGM', descripcion='Kilogramo'),
            UnidadMedida(unidad_medida='LTR', descripcion='Litro'),
            UnidadMedida(unidad_medida='MTR', descripcion='Metro'),            
        ])

    if not Moneda.objects.using(db_alias).exists():
        Moneda.objects.using(db_alias).bulk_create([
            Moneda(nombre='PESO MEXICANO', clave='MXN', simbolo='$', activa=True, paridad=1),
            Moneda(nombre='DOLAR AMERICANO', clave='USD', simbolo='USD', activa=True, paridad=20.1234),
        ])

    if not ClaveMovimiento.objects.using(db_alias).exists():
        ClaveMovimiento.objects.using(db_alias).bulk_create([
            ClaveMovimiento(clave_movimiento='CO', nombre='COMPRAS', tipo= 'E', es_remision=False, es_compra=True, es_servicio=False),
            ClaveMovimiento(clave_movimiento='R1', nombre='REMISIONES', tipo= 'S', es_remision=True, es_compra=False, es_servicio=False),
            ClaveMovimiento(clave_movimiento='SE', nombre='SERVICIO', tipo= 'S', es_remision=False, es_compra=False, es_servicio=True),
        ])

    if not TipoCliente.objects.using(db_alias).exists():
        TipoCliente.objects.using(db_alias).bulk_create([
            TipoCliente(tipo_cliente=1, nombre='CONTADO'),
        ])

    if not Exportacion.objects.using(db_alias).exists():
        Exportacion.objects.using(db_alias).bulk_create([
            Exportacion(exportacion='01', nombre='NO APLICA'),
        ])

    if not TipoComprobante.objects.using(db_alias).exists():
        TipoComprobante.objects.using(db_alias).bulk_create([
            TipoComprobante(tipo_comprobante='I', nombre='INGRESO'),
            TipoComprobante(tipo_comprobante='E', nombre='EGRESO'),
            TipoComprobante(tipo_comprobante='T', nombre='TRASLADO'),
        ])

    if not Almacen.objects.using(db_alias).exists():
        Almacen.objects.using(db_alias).bulk_create([
            Almacen(almacen=1, nombre='ALMACEN 01'),
        ])

    if not Categoria.objects.using(db_alias).exists():
        Categoria.objects.using(db_alias).bulk_create([
            Categoria(categoria=1, nombre='CATEGORIA 1'),
        ])
    if not Proveedor.objects.using(db_alias).exists():
        Proveedor.objects.using(db_alias).bulk_create([
            Proveedor(nombre='SIN PROVEEDOR', contacto="SIN PROVEEDOR`"),
        ])    