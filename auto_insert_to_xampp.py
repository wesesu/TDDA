from mysql.connector import Error
from conexion import Conexion

class InsertarDatos:
    def __init__(self):
        self.conexion = Conexion()
        self.cursor = self.conexion.connection.cursor() if self.conexion.connection else None

    def ejecutar_sql(self, query):
        """Ejecutar una consulta SQL en la base de datos."""
        if self.cursor:
            try:
                self.cursor.execute(query)
                self.conexion.connection.commit()
                print("Consulta SQL ejecutada exitosamente")
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")

    def insertar_datos(self):
        """Insertar datos en todas las tablas."""
        consultas = [
            "DELETE FROM CARGA_FAMILIAR;",
            "DELETE FROM CONTACTO_EMERGENCIA;",
            "DELETE FROM DATOS_LABORALES;",
            "DELETE FROM EMPLEADOS;",
            """
            INSERT INTO EMPLEADOS (RUT, NOMBRE, GENERO_EMPLEADO, DIRECCION, TELEFONO) VALUES
            ('11.111.111-1', 'JUAN PEREZ', 'M', 'CALLE FALSA 123', '912345678'),
            ('22.222.222-2', 'MARIA GONZALEZ', 'F', 'AVENIDA SIEMPRE VIVA 456', '923456789'),
            ('33.333.333-3', 'PEDRO MARTINEZ', 'M', 'BOULEVARD DE LOS SUEÑOS ROTOS 789', '934567890'),
            ('44.444.444-4', 'LUCIA FERNANDEZ', 'F', 'CALLE DE LA AMARGURA 321', '945678901'),
            ('55.555.555-5', 'CARLOS SANCHEZ', 'M', 'PASAJE DE LA ESPERANZA 654', '956789012');
            """,
            """
            INSERT INTO DATOS_LABORALES (CARGO, FECHA_INGRESO, AREA, DEPARTAMENTO, ID_EMPLEADOS) VALUES
            ('DESARROLLADOR', '2020-01-15', 'TECNOLOGÍA', 'DESARROLLO', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '11.111.111-1')),
            ('ANALISTA', '2019-03-20', 'FINANZAS', 'CONTABILIDAD', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '22.222.222-2')),
            ('GERENTE', '2018-07-10', 'ADMINISTRACIÓN', 'DIRECCIÓN', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '33.333.333-3')),
            ('DISEÑADORA', '2021-05-25', 'MARKETING', 'PUBLICIDAD', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '44.444.444-4')),
            ('SOPORTE', '2017-11-30', 'TECNOLOGÍA', 'SOPORTE TÉCNICO', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '55.555.555-5'));
            """,
            """
            INSERT INTO CONTACTO_EMERGENCIA (NOMBRE_CONTACTO, RELACION, TELEFONO_CONTACTO, ID_EMPLEADOS) VALUES
            ('ANA PEREZ', 'ESPOSA', '987654321', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '11.111.111-1')),
            ('JOSE GONZALEZ', 'HERMANO', '976543210', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '22.222.222-2')),
            ('LAURA MARTINEZ', 'MADRE', '965432109', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '33.333.333-3')),
            ('PEDRO FERNANDEZ', 'PADRE', '954321098', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '44.444.444-4')),
            ('ELENA SANCHEZ', 'ESPOSA', '943210987', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '55.555.555-5'));
            """,
            """
            INSERT INTO CARGA_FAMILIAR (NOMBRE_CARGA, PARENTESCO, GENERO_CARGA, RUT_CARGA, ID_EMPLEADOS) VALUES
            ('LUIS PEREZ', 'HIJO', 'M', '11.111.111-2', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '11.111.111-1')),
            ('MARTA GONZALEZ', 'HIJA', 'F', '22.222.222-3', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '22.222.222-2')),
            ('CARLOS MARTINEZ', 'HIJO', 'M', '33.333.333-4', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '33.333.333-3')),
            ('JULIA FERNANDEZ', 'HIJA', 'F', '44.444.444-5', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '44.444.444-4')),
            ('PABLO SANCHEZ', 'HIJO', 'M', '55.555.555-6', (SELECT ID_EMPLEADOS FROM EMPLEADOS WHERE RUT = '55.555.555-5'));
            """
        ]

        for query in consultas:
            self.ejecutar_sql(query)

    def cerrar(self):
        """Cerrar la conexión a la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.conexion.connection:
            self.conexion.connection.close()

if __name__ == "__main__":
    insercion = InsertarDatos()
    insercion.insertar_datos()
    insercion.cerrar()
