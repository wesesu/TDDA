from conexion import Conexion
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
        

    def buscarEmpleadosFiltrados(self, genero, cargo, area, departamento):
        query = """
            SELECT e.NOMBRE, e.DIRECCION, e.GENERO_EMPLEADO, e.TELEFONO, d.CARGO, d.AREA, d.DEPARTAMENTO
            FROM EMPLEADOS e
            JOIN DATOS_LABORALES d ON e.ID_EMPLEADOS = d.ID_EMPLEADOS
            WHERE e.GENERO_EMPLEADO = %s AND d.CARGO = %s AND d.AREA = %s AND d.DEPARTAMENTO = %s AND e.is_deleted = FALSE AND d.is_deleted = FALSE
        """
        values = (genero, cargo, area, departamento)
        self.mysql.cursor.execute(query, values)
        result = self.mysql.cursor.fetchall()
        return result



    def actualizarDatosPropios(self, rut_logueado):
        empleado_existente = self.buscarEmpleado(rut_logueado)
        if empleado_existente is not None:
            while True:
                print("\nSeleccione el aspecto que desea actualizar:")
                print("1: Nombre")
                print("2: Género")
                print("3: Dirección")
                print("4: Teléfono")
                print("5: Finalizar Actualización")

                opcion = input("Seleccione una opción: ")

                if opcion == '1':
                    nuevo_valor = input(f"Ingrese el nuevo nombre (actual: {empleado_existente.nombre}): ").upper()
                    query = "UPDATE empleados SET NOMBRE = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_logueado)
                elif opcion == '2':
                    nuevo_valor = input(f"Ingrese el nuevo género (M/F) (actual: {empleado_existente.sexo}): ").upper()
                    query = "UPDATE empleados SET GENERO_EMPLEADO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_logueado)
                elif opcion == '3':
                    nuevo_valor = input(f"Ingrese la nueva dirección (actual: {empleado_existente.direccion}): ").upper()
                    query = "UPDATE empleados SET DIRECCION = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_logueado)
                elif opcion == '4':
                    nuevo_valor = input(f"Ingrese el nuevo teléfono (actual: {empleado_existente.telefono}): ").upper()
                    query = "UPDATE empleados SET TELEFONO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_logueado)
                elif opcion == '5':
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

# Ejemplo de uso:
# empleado_dao.actualizarDatosPropios('11.111.111-1')

    def actualizarPropio(self, rut_trabajador):
        empleado_existente = self.buscarEmpleado(rut_trabajador)
        if empleado_existente is not None:
            while True:
                print("\nSeleccione el aspecto que desea actualizar:")
                print("1: Nombre")
                print("2: Género")
                print("3: Dirección")
                print("4: Teléfono")
                print("5: Finalizar Actualización")

                opcion = input("Seleccione una opción: ")

                if opcion == '1':
                    nuevo_valor = input(f"Ingrese el nuevo nombre (actual: {empleado_existente.nombre}): ").upper()
                    query = "UPDATE empleados SET NOMBRE = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '2':
                    nuevo_valor = input(f"Ingrese el nuevo género (M/F) (actual: {empleado_existente.sexo}): ").upper()
                    query = "UPDATE empleados SET GENERO_EMPLEADO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '3':
                    nuevo_valor = input(f"Ingrese la nueva dirección (actual: {empleado_existente.direccion}): ").upper()
                    query = "UPDATE empleados SET DIRECCION = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '4':
                    nuevo_valor = input(f"Ingrese el nuevo teléfono (actual: {empleado_existente.telefono}): ").upper()
                    query = "UPDATE empleados SET TELEFONO = %s WHERE RUT = %s"
                    values = (nuevo_valor, rut_trabajador)
                elif opcion == '5':
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


                    
    def actualizarDatosLaborales(self, rut_trabajador, empleado_existente):
        while True:
            print("1: Cargo")
            print("2: Fecha de Ingreso")
            print("3: Área")
            print("4: Departamento")
            print("5: Regresar al Menú Anterior")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                nuevo_valor = input(f"Ingrese el nuevo cargo (actual: {empleado_existente.cargo}): ").upper()
                query = "UPDATE datos_laborales SET CARGO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '2':
                nuevo_valor = input(f"Ingrese la nueva fecha de ingreso (YYYY-MM-DD) (actual: {empleado_existente.fecha_ingreso}): ").upper()
                query = "UPDATE datos_laborales SET FECHA_INGRESO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '3':
                nuevo_valor = input(f"Ingrese la nueva área (actual: {empleado_existente.area}): ").upper()
                query = "UPDATE datos_laborales SET AREA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '4':
                nuevo_valor = input(f"Ingrese el nuevo departamento (actual: {empleado_existente.departamento}): ").upper()
                query = "UPDATE datos_laborales SET DEPARTAMENTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '5':
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
    
    def actualizarDatosEmergencia(self, rut_trabajador, empleado_existente):
        while True:
            print("\nSeleccione el aspecto de emergencia que desea actualizar:")
            print("1: Nombre de Contacto")
            print("2: Relación")
            print("3: Teléfono de Contacto")
            print("4: Regresar al Menú Anterior")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                nuevo_valor = input(f"Ingrese el nuevo nombre de contacto (actual: {empleado_existente.nombre_contacto}): ").upper()
                query = "UPDATE contacto_emergencia SET NOMBRE_CONTACTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '2':
                nuevo_valor = input(f"Ingrese la nueva relación (actual: {empleado_existente.relacion}): ").upper()
                query = "UPDATE contacto_emergencia SET RELACION = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '3':
                nuevo_valor = input(f"Ingrese el nuevo teléfono de contacto (actual: {empleado_existente.telefono_contacto}): ")
                query = "UPDATE contacto_emergencia SET TELEFONO_CONTACTO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '4':
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

    def actualizarDatosCargaFamiliar(self, rut_trabajador, empleado_existente):
        while True:
            print("\nSeleccione el aspecto de carga familiar que desea actualizar:")
            print("1: Nombre de Carga")
            print("2: Parentesco")
            print("3: Género de Carga")
            print("4: RUT de Carga")
            print("5: Regresar al Menú Anterior")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                nuevo_valor = input(f"Ingrese el nuevo nombre de carga (actual: {empleado_existente.nombre_carga}): ").upper()
                query = "UPDATE carga_familiar SET NOMBRE_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '2':
                nuevo_valor = input(f"Ingrese el nuevo parentesco (actual: {empleado_existente.parentesco}): ").upper()
                query = "UPDATE carga_familiar SET PARENTESCO = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '3':
                nuevo_valor = input(f"Ingrese el nuevo género de carga (actual: {empleado_existente.genero_carga}): ").upper()
                query = "UPDATE carga_familiar SET GENERO_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '4':
                nuevo_valor = input(f"Ingrese el nuevo RUT de carga (actual: {empleado_existente.rut_carga}): ").upper()
                query = "UPDATE carga_familiar SET RUT_CARGA = %s WHERE ID_EMPLEADOS = (SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s)"
                values = (nuevo_valor, rut_trabajador)
            elif opcion == '5':
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

    # Resto de tu código de la clase EmpleadoDao...

    def insertarCargaFamiliar(self, rut_empleado, nombre, parentesco, genero, rut_carga):
        try:
            self.mysql.cursor.execute("START TRANSACTION")

            # Obtener el ID del empleado
            query = "SELECT ID_EMPLEADOS FROM empleados WHERE RUT = %s"
            self.mysql.cursor.execute(query, (rut_empleado,))
            empleado_id = self.mysql.cursor.fetchone()[0]

            # Insertar carga familiar
            self.mysql.cursor.execute("INSERT INTO carga_familiar (NOMBRE_CARGA, PARENTESCO, GENERO_CARGA, RUT_CARGA, ID_EMPLEADOS) VALUES (%s, %s, %s, %s, %s)",
                                      (nombre, parentesco, genero, rut_carga, empleado_id))

            self.mysql.connection.commit()
            print("Carga familiar agregada exitosamente.")
        except Exception as e:
            self.mysql.connection.rollback()
            raise e
