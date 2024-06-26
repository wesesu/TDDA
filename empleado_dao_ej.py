from creandotablita import Conexion
from empleado import Empleado
from beautifultable import BeautifulTable
import mysql.connector

class EmpleadoDao:
    def __init__(self) -> None:
        self.__mysql = Conexion()

    @property
    def mysql(self):
        return self.__mysql
    
    def buscarEmpleado(self, rut_trabajador):
        valor = (rut_trabajador,)
        self.mysql.cursor.execute("""
        SELECT e.RUT, e.NOMBRE, e.GENERO_EMPLEADO, e.DIRECCION, e.TELEFONO, 
               dl.CARGO, dl.FECHA_INGRESO, dl.AREA, dl.DEPARTAMENTO, 
               ce.NOMBRE_CONTACTO, ce.RELACION, ce.TELEFONO_CONTACTO, 
               cf.NOMBRE_CARGA, cf.PARENTESCO, cf.GENERO_CARGA, cf.RUT_CARGA
        FROM empleados e
        LEFT JOIN datos_laborales dl ON e.ID_EMPLEADOS = dl.ID_EMPLEADOS AND dl.is_deleted = FALSE
        LEFT JOIN contacto_emergencia ce ON e.ID_EMPLEADOS = ce.ID_EMPLEADOS AND ce.is_deleted = FALSE
        LEFT JOIN carga_familiar cf ON e.ID_EMPLEADOS = cf.ID_EMPLEADOS AND cf.is_deleted = FALSE
        WHERE e.RUT = %s AND e.is_deleted = FALSE
        """, valor)
        resultado = self.mysql.cursor.fetchone()
        if resultado:
            resultado = [elem if elem is not None else '' for elem in resultado]
            return Empleado(*resultado)
        else:
            return None

    def insertarEmpleado(self, empleado):
        if self.buscarEmpleado(empleado.rut) is None:
            self.mysql.cursor.execute("START TRANSACTION")
            try:
                self.mysql.cursor.execute("INSERT INTO empleados (RUT, NOMBRE, GENERO_EMPLEADO, DIRECCION, TELEFONO) VALUES (%s, %s, %s, %s, %s)",
                                      (empleado.rut, empleado.nombre, empleado.sexo, empleado.direccion, empleado.telefono))
                
                empleado_id = self.mysql.cursor.lastrowid

                self.mysql.cursor.execute("INSERT INTO datos_laborales (CARGO, FECHA_INGRESO, AREA, DEPARTAMENTO, ID_EMPLEADOS) VALUES (%s, %s, %s, %s, %s)",
                                      (empleado.cargo, empleado.fecha_ingreso, empleado.area, empleado.departamento, empleado_id))

                self.mysql.cursor.execute("INSERT INTO contacto_emergencia (NOMBRE_CONTACTO, RELACION, TELEFONO_CONTACTO, ID_EMPLEADOS) VALUES (%s, %s, %s, %s)",
                                      (empleado.nombre_contacto, empleado.relacion, empleado.telefono_contacto, empleado_id))
                
                if empleado.nombre_carga and empleado.rut_carga:
                    self.mysql.cursor.execute("INSERT INTO carga_familiar (NOMBRE_CARGA, PARENTESCO, GENERO_CARGA, RUT_CARGA, ID_EMPLEADOS) VALUES (%s, %s, %s, %s, %s)",
                                          (empleado.nombre_carga, empleado.parentesco, empleado.genero_carga, empleado.rut_carga, empleado_id))
                
                self.mysql.connection.commit()
            except Exception as e:
                self.mysql.connection.rollback()
                raise e

    def eliminarEmpleado(self, rut_trabajador):
        empleado = self.buscarEmpleado(rut_trabajador)
        if empleado is not None:
            try:
                self.mysql.cursor.execute("START TRANSACTION")

                # Obtener el ID del empleado
                query = "SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s"
                self.mysql.cursor.execute(query, (rut_trabajador,))
                empleado_id = self.mysql.cursor.fetchone()[0]

                # Marcar como eliminado en las tablas dependientes
                self.mysql.cursor.execute("UPDATE contacto_emergencia SET is_deleted = TRUE WHERE ID_EMPLEADOS = %s", (empleado_id,))
                self.mysql.cursor.execute("UPDATE datos_laborales SET is_deleted = TRUE WHERE ID_EMPLEADOS = %s", (empleado_id,))
                self.mysql.cursor.execute("UPDATE carga_familiar SET is_deleted = TRUE WHERE ID_EMPLEADOS = %s", (empleado_id,))

                # Marcar como eliminado en la tabla empleados
                self.mysql.cursor.execute("UPDATE empleados SET is_deleted = TRUE WHERE RUT = %s", (rut_trabajador,))
                
                self.mysql.connection.commit()
                return 'Empleado eliminado con éxito'
            except Exception as e:
                self.mysql.connection.rollback()
                raise e
        else:
            return 'No se encontró al empleado'
    
    def actualizarEmpleado(self, empleado_actualizado):
        empleado_existente = self.buscarEmpleado(empleado_actualizado.rut)
        if empleado_existente is not None:
            self.mysql.cursor.execute("START TRANSACTION")
            try:
                query_empleados = "UPDATE empleados SET NOMBRE = %s, GENERO_EMPLEADO = %s, DIRECCION = %s, TELEFONO = %s WHERE RUT = %s"
                values_empleados = (
                    empleado_actualizado.nombre, empleado_actualizado.sexo,
                    empleado_actualizado.direccion, empleado_actualizado.telefono, empleado_existente.rut
                )
                self.mysql.cursor.execute(query_empleados, values_empleados)

                query_datos_laborales = "UPDATE datos_laborales SET CARGO = %s, FECHA_INGRESO = %s, AREA = %s, DEPARTAMENTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s) AND is_deleted = FALSE"
                values_datos_laborales = (
                    empleado_actualizado.cargo, empleado_actualizado.fecha_ingreso, empleado_actualizado.area,
                    empleado_actualizado.departamento, empleado_existente.rut
                )
                self.mysql.cursor.execute(query_datos_laborales, values_datos_laborales)

                query_contacto_emergencia = "UPDATE contacto_emergencia SET NOMBRE_CONTACTO = %s, RELACION = %s, TELEFONO_CONTACTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s) AND is_deleted = FALSE"
                values_contacto_emergencia = (
                    empleado_actualizado.nombre_contacto, empleado_actualizado.relacion, empleado_actualizado.telefono_contacto, empleado_existente.rut
                )
                self.mysql.cursor.execute(query_contacto_emergencia, values_contacto_emergencia)

                self.mysql.connection.commit()
                return 'Empleado actualizado correctamente'
            except Exception as e:
                self.mysql.connection.rollback()
                raise e
        else:
            return 'Empleado no encontrado'
    
    def obtenerEmpleados(self):
        try:
            self.mysql.cursor.execute("SELECT ID_EMPLEADOS, RUT, NOMBRE, GENERO_EMPLEADO, DIRECCION, TELEFONO FROM EMPLEADOS WHERE is_deleted = FALSE")
            empleados = self.mysql.cursor.fetchall()
            tabla = BeautifulTable()
            tabla.columns.header = ["ID Empleado", "RUT", "Nombre", "Género", "Dirección", "Teléfono"]
            for empleado in empleados:
                tabla.rows.append(empleado)
            print("Mostrando todos los empleados registrados:")
            return tabla
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def empleadosPorCargo(self, cargo):
        try:
            query = """
                SELECT e.RUT, e.NOMBRE, e.GENERO_EMPLEADO, e.DIRECCION, e.TELEFONO 
                FROM EMPLEADOS e
                JOIN DATOS_LABORALES dl ON e.ID_EMPLEADOS = dl.ID_EMPLEADOS AND dl.is_deleted = FALSE
                WHERE dl.CARGO = %s AND e.is_deleted = FALSE
            """
            self.mysql.cursor.execute(query, (cargo,))
            empleados = self.mysql.cursor.fetchall()
        
            if not empleados:
                print("No se encontraron empleados con el cargo especificado.")
                return
        
            tabla = BeautifulTable()
            tabla.columns.header = ["RUT", "Nombre", "Género", "Dirección", "Teléfono"]
            for empleado in empleados:
                tabla.rows.append(empleado)
            print(tabla)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def cantidadEmpleados(self):
        query = "SELECT COUNT(*) FROM empleados WHERE is_deleted = FALSE"
        self.mysql.cursor.execute(query)
        cantidad = self.mysql.cursor.fetchone()
        return cantidad
