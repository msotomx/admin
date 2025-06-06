from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Filtro para agregar una clase CSS a un campo del formulario
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='add_bootstrap_class')
def add_bootstrap_class(field):
    existing_classes = field.field.widget.attrs.get('class', '')
    if field.name in ['flete', 'paridad', 'cantidad', 'subtotal']:
        return field.as_widget(attrs={
            'class': f'{existing_classes} form-control form-control-sm text-end'
        })
    return field.as_widget(attrs={
        'class': f'{existing_classes} form-control form-control-sm'
    })

@register.filter(name='format_number')
def format_number(value):
    try:
        return "{:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return value
