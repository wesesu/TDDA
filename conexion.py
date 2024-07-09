import mysql.connector

class Conexion:
    def __init__(self):
        # Conexión inicial sin especificar la base de datos
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port="3306"
        )
        self.cursor = self.connection.cursor()
        
        # Crear la base de datos si no existe
        self.crear_base_datos("correo_yury")
        
        # Cerrar la conexión inicial
        self.cursor.close()
        self.connection.close()
        
        # Conectar a la base de datos específica
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="correo_yury",
            port="3306"
        )
        self.cursor = self.connection.cursor()
        if self.connection.is_connected():
            print("Conexión existosa a la base de datos!!!.")
    
    def crear_base_datos(self, nombre_bd):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd};")
            print(f"Base de datos '{nombre_bd}' creada o ya existe.")
        except mysql.connector.Error as err:
            print(f"Error al crear la base de datos: {err}")

# Ejemplo de uso
conexion = Conexion()


            