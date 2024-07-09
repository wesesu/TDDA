# validations.py
import re

def validar_rut(rut):
    if not re.match(r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$", rut):
        return False, "Formato de RUT inválido."
    return True, ""

def validar_nombre_usuario(nombre_usuario):
    if len(nombre_usuario) < 4 or len(nombre_usuario) > 15:
        return False, "El nombre de usuario debe tener entre 4 y 15 caracteres."
    return True, ""

def validar_contrasena(contrasena):
    if len(contrasena) < 6 or len (contrasena) > 15:
        return False, "La contraseña debe tener entre 6 y 15 caracteres."
    return True, ""
