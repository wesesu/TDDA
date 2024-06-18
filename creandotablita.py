import mysql.connector


class Conexion:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="oal",
            port="3306"
        )
        self.cursor = self.connection.cursor()
        if self.connection.is_connected():
            print("Conexión existosa a la base de datos!!1.")
            