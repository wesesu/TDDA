from user import User
import mysql.connector
from conexion import Conexion
from validations import validar_rut


class UserDao:
    def __init__(self):
        self.__mysql = Conexion()

    @property
    def mysql(self):
        return self.__mysql

    def login(self, rut, password):
        query = "SELECT ROL FROM usuarios WHERE RUT = %s AND CONTRASENA = %s"
        values = (rut, password)
        self.mysql.cursor.execute(query, values)
        result = self.mysql.cursor.fetchone()
        if result:
            return result[0]  # Return the role
        else:
            return None

    def crearCuenta(self, user):
        query = "INSERT INTO usuarios (RUT, NOMBRE_USUARIO, CONTRASENA, ROL) VALUES (%s, %s, %s, 'EMPLEADO')"
        values = (user.rut, user.nombre_usuario, user.contrasena)
        self.mysql.cursor.execute(query, values)
        self.mysql.connection.commit()

    def cambiarRol(self, rut, nuevo_rol):
        query = "UPDATE usuarios SET ROL = %s WHERE RUT = %s"
        values = (nuevo_rol, rut)
        self.mysql.cursor.execute(query, values)
        self.mysql.connection.commit()

    # Método para cambiar la contraseña de un usuario

    def cambiar_contrasena(self, rut, nueva_contrasena):
        try:
            self.mysql.cursor.execute("UPDATE usuarios SET CONTRASENA = %s WHERE RUT = %s", (nueva_contrasena, rut))
            self.mysql.connection.commit()
            return "Contraseña actualizada correctamente."
        except mysql.connector.Error as err:
            self.mysql.connection.rollback()
            return f"Error: {err}"

    def eliminarUsuario(self, rut):
        try:
            query = "UPDATE usuarios SET is_deleted = TRUE WHERE RUT = %s"
            values = (rut,)
            self.mysql.cursor.execute(query, values)
            self.mysql.connection.commit()
            return "Usuario eliminado correctamente."
        except mysql.connector.Error as err:
            return f"Error al eliminar usuario: {err}"
        
    def usuario_eliminado(self, rut):
        try:
            query = "SELECT is_deleted FROM usuarios WHERE RUT = %s"
            values = (rut,)
            self.mysql.cursor.execute(query, values)
            result = self.mysql.cursor.fetchone()
            if result and result[0]:
                return True  # Usuario marcado como eliminado
            else:
                return False  # Usuario no está marcado como eliminado o no existe
        except mysql.connector.Error as err:
            print(f"Error al verificar usuario eliminado: {err}")
            return False
