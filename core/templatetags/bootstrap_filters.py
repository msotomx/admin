from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Filtro para agregar una clase CSS a un campo del formulario
    """
    return field.as_widget(attrs={"class": css_class})
