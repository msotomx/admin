from django import template
from django.forms import widgets

register = template.Library()

@register.filter(name='add_bootstrap_class')
def add_bootstrap_class(field):
    css_class = 'form-control form-control-sm'
    if isinstance(field.field.widget, widgets.Select):
        css_class = 'form-select form-select-sm'
    elif isinstance(field.field.widget, widgets.Textarea):
        css_class = 'form-control form-control-sm'
    elif isinstance(field.field.widget, widgets.ClearableFileInput):
        css_class = 'form-control form-control-sm'
    elif isinstance(field.field.widget, widgets.CheckboxInput):
        css_class = 'form-check-input'
    
    return field.as_widget(attrs={"class": css_class})

