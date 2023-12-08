from django import template

register = template.Library()
@register.filter
def get_nombre(dictionary, key):
    # Verifica si la clave existe en el diccionario y si el valor es un diccionario
    if key in dictionary and isinstance(dictionary[key], dict):
        return dictionary[key].get('nombre', '')  # Devuelve '' si 'nombre' no existe en el diccionario anidado
    else:
        return ''
    
@register.filter
def get_valor_esp(dictionary, key):
    # Verifica si la clave existe en el diccionario y si el valor es un diccionario
    if key in dictionary and isinstance(dictionary[key], dict):
        return dictionary[key].get('valor_esperado', '')  # Devuelve '' si 'valor_esperado' no existe en el diccionario anidado
    else:
        return ''
    
@register.filter
def get_unidad(dictionary, key):
    # Verifica si la clave existe en el diccionario y si el valor es un diccionario
    if key in dictionary and isinstance(dictionary[key], dict):
        return dictionary[key].get('unidad', '')  # Devuelve '' si 'unidad' no existe en el diccionario anidado
    else:
        return ''
    
@register.filter
def get_valor_obt(dictionary, key):
    # Verifica si la clave existe en el diccionario y si el valor es un diccionario
    if key in dictionary and isinstance(dictionary[key], dict):
        return dictionary[key].get('valor_obtenido', '')  # Devuelve '' si 'valor_esperado' no existe en el diccionario anidado
    else:
        return ''

@register.filter
def get_rango(dictionary, key):
    # Verifica si la clave existe en el diccionario y si el valor es un diccionario
    if key in dictionary and isinstance(dictionary[key], dict):
        return dictionary[key].get('rango', '')  # Devuelve '' si 'rango' no existe en el diccionario anidado
    else:
        return ''