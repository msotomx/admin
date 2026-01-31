from django import forms
from django.utils import formats
from datetime import date, datetime

class MXDateWidget(forms.TextInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        existing = attrs.get("class", "")
        attrs["class"] = (existing + " form-control form-control-sm mx-date").strip()
        attrs.setdefault("placeholder", "dd/mm/aaaa")
        attrs.setdefault("autocomplete", "off")
        attrs.setdefault("inputmode", "numeric")
        super().__init__(attrs=attrs)

    def format_value(self, value):
        if value in (None, ""):
            return ""

        # 1) Si ya es date/datetime
        if isinstance(value, datetime):
            value = value.date()
        if isinstance(value, date):
            return formats.date_format(value, "d/m/Y")

        # 2) Si viene como string ISO "YYYY-MM-DD"
        if isinstance(value, str):
            v = value.strip()
            try:
                dt = datetime.strptime(v, "%Y-%m-%d").date()
                return dt.strftime("%d/%m/%Y")
            except ValueError:
                # 3) Si ya viene dd/mm/aaaa o cualquier otra cosa, lo dejamos
                return v

        return super().format_value(value)
