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
    
    def actualizarEmpleado(self, rut_trabajador):
        empleado_existente = self.buscarEmpleado(rut_trabajador)
        if empleado_existente is not None:
            while True:
                print("\nSeleccione el aspecto que desea actualizar:")
                print("1: Nombre")
                print("2: Género")
                print("3: Dirección")
                print("4: Teléfono")
                print("5: Cargo")
                print("6: Fecha de Ingreso")
                print("7: Área")
                print("8: Departamento")
                print("9: Nombre de Contacto de Emergencia")
                print("10: Relación con Contacto de Emergencia")
                print("11: Teléfono del Contacto de Emergencia")
                print("12: Carga Familiar (Nombre)")
                print("13: Carga Familiar (Parentesco)")
                print("14: Carga Familiar (Género)")
                print("15: Carga Familiar (RUT)")
                print("16: Finalizar Actualización")

                opcion = input("Seleccione una opción: ")

                if opcion == '1':
                    nuevo_valor = input(f"Ingrese el nuevo nombre (actual: {empleado_existente.nombre}): ")
                    query = "UPDATE empleados SET NOMBRE = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '2':
                    nuevo_valor = input(f"Ingrese el nuevo género (M/F) (actual: {empleado_existente.sexo}): ")
                    query = "UPDATE empleados SET GENERO_EMPLEADO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '3':
                    nuevo_valor = input(f"Ingrese la nueva dirección (actual: {empleado_existente.direccion}): ")
                    query = "UPDATE empleados SET DIRECCION = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '4':
                    nuevo_valor = input(f"Ingrese el nuevo teléfono (actual: {empleado_existente.telefono}): ")
                    query = "UPDATE empleados SET TELEFONO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '5':
                    nuevo_valor = input(f"Ingrese el nuevo cargo (actual: {empleado_existente.cargo}): ")
                    query = "UPDATE datos_laborales SET CARGO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '6':
                    nuevo_valor = input(f"Ingrese la nueva fecha de ingreso (YYYY-MM-DD) (actual: {empleado_existente.fecha_ingreso}): ")
                    query = "UPDATE datos_laborales SET FECHA_INGRESO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '7':
                    nuevo_valor = input(f"Ingrese la nueva área (actual: {empleado_existente.area}): ")
                    query = "UPDATE datos_laborales SET AREA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '8':
                    nuevo_valor = input(f"Ingrese el nuevo departamento (actual: {empleado_existente.departamento}): ")
                    query = "UPDATE datos_laborales SET DEPARTAMENTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '9':
                    nuevo_valor = input(f"Ingrese el nuevo nombre del contacto de emergencia (actual: {empleado_existente.nombre_contacto}): ")
                    query = "UPDATE contacto_emergencia SET NOMBRE_CONTACTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '10':
                    nuevo_valor = input(f"Ingrese la nueva relación con el contacto de emergencia (actual: {empleado_existente.relacion}): ")
                    query = "UPDATE contacto_emergencia SET RELACION = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '11':
                    nuevo_valor = input(f"Ingrese el nuevo teléfono del contacto de emergencia (actual: {empleado_existente.telefono_contacto}): ")
                    query = "UPDATE contacto_emergencia SET TELEFONO_CONTACTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '12':
                    nuevo_valor = input(f"Ingrese el nuevo nombre de la carga familiar (actual: {empleado_existente.nombre_carga}): ")
                    query = "UPDATE carga_familiar SET NOMBRE_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '13':
                    nuevo_valor = input(f"Ingrese el nuevo parentesco de la carga familiar (actual: {empleado_existente.parentesco}): ")
                    query = "UPDATE carga_familiar SET PARENTESCO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '14':
                    nuevo_valor = input(f"Ingrese el nuevo género de la carga familiar (actual: {empleado_existente.genero_carga}): ")
                    query = "UPDATE carga_familiar SET GENERO_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '15':
                    nuevo_valor = input(f"Ingrese el nuevo RUT de la carga familiar (actual: {empleado_existente.rut_carga}): ")
                    query = "UPDATE carga_familiar SET RUT_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '16':
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
                    continue
            
                try:
                    self.mysql.cursor.execute("START TRANSACTION")
                    self.mysql.cursor.execute(query, values)
                    self.mysql.connection.commit()
                    print("Actualización exitosa.")
                except Exception as e:
                    self.mysql.connection.rollback()
                    print(f"Error al actualizar: {e}")

        else:
            print("Empleado no encontrado")
    
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
