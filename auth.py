from creandotablita import Conexion
import hashlib

def login():
    conexion = Conexion()
    cursor = conexion.cursor

    rut = input("Ingrese su RUT: ")
    contrasena = input("Ingrese su contraseña: ")

    try:
        cursor.execute("SELECT NOMBRE_USUARIO, CONTRASENA FROM USUARIOS WHERE RUT = %s", (rut,))
        usuario = cursor.fetchone()

        if usuario:
            hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
            if usuario[1] == hashed_password:
                print(f"Bienvenido, {usuario[0]}!")  # Imprime el nombre de usuario
                return True
            else:
                print("Credenciales incorrectas.")
                return False
        else:
            print("Credenciales incorrectas.")
            return False
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return False

