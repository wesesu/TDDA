from mysql.connector import connect, Error

def crear_usuario_root():
    try:
        conexion = connect(
            host="localhost",
            user="root",
            password="",  # Cambia la contraseña según tu configuración
            database="correo_yury",
            port="3306"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Crear el empleado root solo si no existe
            consulta_empleado = """
            INSERT INTO EMPLEADOS (RUT, NOMBRE, GENERO_EMPLEADO, DIRECCION, TELEFONO)
            SELECT '00.000.000-0', 'ROOT', 'M', '666', '666'
            WHERE NOT EXISTS (
                SELECT 1 FROM EMPLEADOS WHERE RUT = '00.000.000-0'
            );
            """

            cursor.execute(consulta_empleado)

            # Crear el usuario root solo si no existe
            consulta_usuario = """
            INSERT INTO USUARIOS (RUT, NOMBRE_USUARIO, CONTRASENA, ROL)
            SELECT '00.000.000-0', 'root', '666666', 'ADMIN'
            WHERE NOT EXISTS (
                SELECT 1 FROM USUARIOS WHERE RUT = '00.000.000-0'
            );
            """

            cursor.execute(consulta_usuario)

            conexion.commit()
            print("Empleado y usuario root creados o ya existentes")

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    crear_usuario_root()

