import mysql.connector
from empleado_dao import EmpleadoDao
from empleado import Empleado
from os import system

empleado_dao = EmpleadoDao()

def opciones():
    print("Opción 1: Ingresar un Empleado")
    print("Opción 2: Eliminar un Empleado")
    print("Opción 3: Actualizar un Empleado")
    print("Opción 4: Mostrar todos los Empleados")
    print("Opción 5: Buscar Empleados por Cargo")
    print("Opción 6: Mostrar cantidad de Empleados")
    print("Opción 7: Salir")

def autenticar_usuario(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="oal",
            port="3306"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def login():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    if autenticar_usuario(username, password):
        print("Login exitoso")
        return True
    else:
        print("Credenciales incorrectas")
        return False

if __name__ == "__main__":
    if login():
        while True:
            opciones()
            opcion = input("Seleccione una opción entre 1 y 7: ")

            if opcion == '1':
                rut_trabajador = input("Ingrese el RUT del empleado: ")
                empleado_existe = empleado_dao.buscarEmpleado(rut_trabajador)

                if empleado_existe is None:
                    nombre_trabajador = input("Ingrese el nombre completo del empleado: ")
                    genero_trabajador = input("Ingrese el género del empleado (M/F): ")
                    direccion = input("Ingrese la dirección del trabajador: ")
                    telefono = input("Ingrese el teléfono del trabajador: ")
                    cargo = input("Ingrese el cargo del trabajador: ")
                    fecha_ingreso = input("Ingrese la fecha de ingreso del trabajador (YYYY-MM-DD): ")
                    area = input("Ingrese el área del trabajador: ")
                    departamento = input("Ingrese el departamento del trabajador: ")
                    nombre_contacto = input("Ingrese el nombre del contacto de emergencia: ")
                    relacion = input("Ingrese la relación con el contacto de emergencia: ")
                    telefono_contacto = input("Ingrese el teléfono del contacto de emergencia: ")
                    agregar_carga = input("¿Desea agregar una carga familiar? (S/N): ").lower()
                    if agregar_carga == 's':
                        nombre_carga = input("Ingrese el nombre de la carga familiar: ")
                        parentesco = input("Ingrese el parentesco con la carga familiar: ")
                        genero_carga = input("Ingrese el género de la carga familiar: ")
                        rut_carga = input("Ingrese el RUT de la carga familiar: ")
                    else:
                        nombre_carga = ''
                        parentesco = ''
                        genero_carga = ''
                        rut_carga = ''

                    nuevo_empleado = Empleado(rut_trabajador, nombre_trabajador, genero_trabajador, direccion, telefono, cargo, fecha_ingreso, area, departamento, nombre_contacto, relacion, telefono_contacto, nombre_carga, parentesco, genero_carga, rut_carga)
                    empleado_dao.insertarEmpleado(nuevo_empleado)
                    print("Empleado ingresado correctamente")
                else:
                    print("El empleado ya existe")
            
            elif opcion == '2':
                rut_trabajador = input("Ingrese el RUT del empleado a eliminar: ")
                resultado = empleado_dao.eliminarEmpleado(rut_trabajador)
                print(resultado)
                
            elif opcion == '3':
                rut_trabajador = input("Ingrese el RUT del empleado a actualizar: ")
                empleado_existe = empleado_dao.buscarEmpleado(rut_trabajador)

                if empleado_existe is not None:
                    nombre_trabajador = input(f"Ingrese el nombre completo del empleado ({empleado_existe.nombre}): ") or empleado_existe.nombre
                    genero_trabajador = input(f"Ingrese el género del empleado (M/F) ({empleado_existe.sexo}): ") or empleado_existe.sexo
                    direccion = input(f"Ingrese la dirección del trabajador ({empleado_existe.direccion}): ") or empleado_existe.direccion
                    telefono = input(f"Ingrese el teléfono del trabajador ({empleado_existe.telefono}): ") or empleado_existe.telefono
                    cargo = input(f"Ingrese el cargo del trabajador ({empleado_existe.cargo}): ") or empleado_existe.cargo
                    fecha_ingreso = input(f"Ingrese la fecha de ingreso del trabajador (YYYY-MM-DD) ({empleado_existe.fecha_ingreso}): ") or empleado_existe.fecha_ingreso
                    area = input(f"Ingrese el área del trabajador ({empleado_existe.area}): ") or empleado_existe.area
                    departamento = input(f"Ingrese el departamento del trabajador ({empleado_existe.departamento}): ") or empleado_existe.departamento
                    nombre_contacto = input(f"Ingrese el nombre del contacto de emergencia ({empleado_existe.nombre_contacto}): ") or empleado_existe.nombre_contacto
                    relacion = input(f"Ingrese la relación con el contacto de emergencia ({empleado_existe.relacion}): ") or empleado_existe.relacion
                    telefono_contacto = input(f"Ingrese el teléfono del contacto de emergencia ({empleado_existe.telefono_contacto}): ") or empleado_existe.telefono_contacto
                    nombre_carga = input(f"Ingrese el nombre de la carga familiar ({empleado_existe.nombre_carga}): ") or empleado_existe.nombre_carga
                    parentesco = input(f"Ingrese el parentesco con la carga familiar ({empleado_existe.parentesco}): ") or empleado_existe.parentesco
                    genero_carga = input(f"Ingrese el género de la carga familiar ({empleado_existe.genero_carga}): ") or empleado_existe.genero_carga
                    rut_carga = input(f"Ingrese el RUT de la carga familiar ({empleado_existe.rut_carga}): ") or empleado_existe.rut_carga

                    empleado_actualizado = Empleado(rut_trabajador, nombre_trabajador, genero_trabajador, direccion, telefono, cargo, fecha_ingreso, area, departamento, nombre_contacto, relacion, telefono_contacto, nombre_carga, parentesco, genero_carga, rut_carga)
                    resultado = empleado_dao.actualizarEmpleado(empleado_actualizado)
                    print(resultado)
                else:
                    print("El Empleado no existe")

            elif opcion == "4":
                empleado_dao.obtenerEmpleados()
                while True:
                    volver = input("Ingrese el número 1 para volver al menú principal: ")
                    if volver == "1":
                        break
            
            elif opcion == '5':
                cargo = input("Ingrese el cargo a buscar: ")
                empleado_dao.empleadosPorCargo(cargo)

            elif opcion == '6':
                cantidad = empleado_dao.cantidadEmpleados()
                print(f"La cantidad de empleados es: {cantidad[0]}")

            elif opcion == '7':
                break

            else:
                print("Opción no válida. Intente de nuevo.")
    else:
        print("No se pudo iniciar sesión.")
