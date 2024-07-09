from conexion import Conexion
from mysql.connector import Error
from root import crear_usuario_root  # Importar la función para crear el usuario root

class CreadorTablas:
    def __init__(self):
        self.conexion = Conexion()
        self.cursor = self.conexion.connection.cursor() if self.conexion.connection else None

    def __enter__(self):
        """Support with-statement for resource management."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Support with-statement for resource management."""
        self.cerrar()

    def cerrar(self):
        """Cerrar la conexión y el cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conexion.connection:
            self.conexion.connection.close()
            print("Conexión cerrada")

    def ejecutar_sql(self, query):
        """Ejecutar una consulta SQL en la base de datos."""
        if self.cursor:
            try:
                self.cursor.execute(query)
                self.conexion.connection.commit()
                print("Consulta SQL ejecutada exitosamente")
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")

    def crear_tablas(self):
        """Crear todas las tablas necesarias."""
        tablas = [
            """
            CREATE TABLE IF NOT EXISTS EMPLEADOS(
                ID_EMPLEADOS INT AUTO_INCREMENT NOT NULL,
                RUT VARCHAR(14) NOT NULL,
                NOMBRE VARCHAR(20) NOT NULL,
                GENERO_EMPLEADO CHAR(1) NOT NULL,
                DIRECCION VARCHAR(50),
                TELEFONO VARCHAR(12),
                CONSTRAINT PK_EMPLEADOS_ID PRIMARY KEY(ID_EMPLEADOS),
                CONSTRAINT UQ_EMPLEADOS_RUT UNIQUE(RUT),
                CONSTRAINT CHK_GENERO_EMPLEADO CHECK (GENERO_EMPLEADO IN ('M', 'F'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS DATOS_LABORALES(
                ID_DATOS_LABORALES INT AUTO_INCREMENT NOT NULL,
                CARGO VARCHAR(20),
                FECHA_INGRESO DATE,
                AREA VARCHAR(20),
                DEPARTAMENTO VARCHAR(20),
                ID_EMPLEADOS INT,
                CONSTRAINT PK_DATOS_LABORALES_ID PRIMARY KEY(ID_DATOS_LABORALES),
                CONSTRAINT FK_DATOS_LABORALES_ID_EMPLEADOS FOREIGN KEY (ID_EMPLEADOS) REFERENCES EMPLEADOS(ID_EMPLEADOS)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS CONTACTO_EMERGENCIA(
                ID_CONTACTO_EMERGENCIA INT AUTO_INCREMENT NOT NULL,
                NOMBRE_CONTACTO VARCHAR(30),
                RELACION VARCHAR(15),
                TELEFONO_CONTACTO VARCHAR(10),
                ID_EMPLEADOS INT,
                CONSTRAINT PK_CONTACTO_EMERGENCIA_ID PRIMARY KEY(ID_CONTACTO_EMERGENCIA),
                CONSTRAINT FK_CONTACTO_EMERGENCIA_ID_EMPLEADOS FOREIGN KEY (ID_EMPLEADOS) REFERENCES EMPLEADOS(ID_EMPLEADOS)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS CARGA_FAMILIAR(
                ID_CARGA_FAMILIAR INT AUTO_INCREMENT NOT NULL,
                NOMBRE_CARGA VARCHAR(30),
                PARENTESCO VARCHAR(15),
                GENERO_CARGA CHAR(1),
                RUT_CARGA VARCHAR(14),
                ID_EMPLEADOS INT,
                CONSTRAINT PK_CARGA_FAMILIAR_ID PRIMARY KEY(ID_CARGA_FAMILIAR),
                CONSTRAINT FK_CARGA_FAMILIAR_ID_EMPLEADOS FOREIGN KEY (ID_EMPLEADOS) REFERENCES EMPLEADOS(ID_EMPLEADOS),
                CONSTRAINT UQ_RUT_CARGA UNIQUE(RUT_CARGA)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS USUARIOS(
                ID_USUARIO INT AUTO_INCREMENT NOT NULL,
                RUT VARCHAR(14) NOT NULL,
                NOMBRE_USUARIO VARCHAR(15) NOT NULL,
                CONTRASENA VARCHAR(15) NOT NULL,
                CONSTRAINT PK_USUARIOS_ID PRIMARY KEY(ID_USUARIO),
                CONSTRAINT UQ_USUARIOS_RUT UNIQUE(RUT),
                CONSTRAINT FK_USUARIOS_RUT FOREIGN KEY (RUT) REFERENCES EMPLEADOS(RUT)
            );
            """,
            """
            ALTER TABLE EMPLEADOS ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
            """,
            """
            ALTER TABLE DATOS_LABORALES ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
            """,
            """
            ALTER TABLE CONTACTO_EMERGENCIA ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
            """,
            """
            ALTER TABLE CARGA_FAMILIAR ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
            """,
            """
            ALTER TABLE USUARIOS ADD COLUMN ROL ENUM('ADMIN', 'EMPLEADO') NOT NULL DEFAULT 'EMPLEADO';
            """,
            """
           ALTER TABLE usuarios ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE;
            """
        ]

        for query in tablas:
            self.ejecutar_sql(query)


if __name__ == "__main__":
    with CreadorTablas() as creador:
        creador.crear_tablas()
        crear_usuario_root()  # Crear el usuario root automáticamente después de crear las tablas
