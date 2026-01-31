# Crea un mixin para forms: aplica formatos + widget

from .widgets import MXDateWidget

MX_DATE_INPUT_FORMATS = ["%d/%m/%Y"]

class MXDateFormMixin:
    """
    Aplica a campos de fecha:
    - Widget MXDateWidget
    - input_formats dd/mm/aaaa
    """
    mx_date_fields = ()  # e.g. ("fecha_compra", "fecha_vencimiento")

    def apply_mx_date_fields(self):
        for name in getattr(self, "mx_date_fields", ()):
            if name in self.fields:
                self.fields[name].widget = MXDateWidget()
                self.fields[name].input_formats = MX_DATE_INPUT_FORMATS
