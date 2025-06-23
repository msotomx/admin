    function safeSetValue(input, value, label) {
        if (!input) {
            console.error(`❌ Campo no encontrado: ${label}`);
            return;
        }
        try {
            input.value = value ?? '';
        } catch (err) {
            console.error(`❌ Error al asignar valor a ${label}:`, err);
        }
    }

llamada a la funcion:
                safeSetValue(row.querySelector("input[name$='-tasa_iva']"), det.tasa_iva, 'tasa_iva');
                safeSetValue(row.querySelector("input[name$='-tasa_ieps']"), det.tasa_ieps, 'tasa_ieps');
                safeSetValue(row.querySelector("input[name$='-tasa_retencion_iva']"), det.tasa_retencion_iva, 'tasa_retencion_iva');
                safeSetValue(row.querySelector("input[name$='-tasa_retencion_isr']"), det.tasa_retencion_isr, 'tasa_retencion_isr');
                safeSetValue(row.querySelector("input[name$='-descripcion']"), det.nombre_producto, 'descripcion');
                safeSetValue(row.querySelector("input[name$='-clave_unidad']"), det.clave_unidad, 'clave_unidad');
                safeSetValue(row.querySelector("input[name$='-importe']"), det.subtotal, 'importe');
                safeSetValue(row.querySelector("select[name$='-producto']"), det.producto_id, 'producto');

