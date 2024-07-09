from empleado_dao import EmpleadoDao
from empleado import Empleado
from os import system
from user_dao import UserDao
from user import User
import mysql.connector
from beautifultable import BeautifulTable
from validations import validar_rut, validar_nombre_usuario, validar_contrasena
import time

system('cls')
user_dao = UserDao()
empleado_dao = EmpleadoDao()

def login_menu():
    while True:
        print("1. Login como Administrador")
        print("2. Login como Empleado")
        print("3. Crear cuenta")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1" or opcion == "2":
            while True:
                rut = input("Ingrese su RUT (o '1' para volver al menú principal): ")
                if rut == '1':
                    break
                valido, mensaje = validar_rut(rut)
                if not valido:
                    print(f"Error: {mensaje}")
                else:
                    break
            if rut == '1':
                continue  # Vuelve al menú principal

            password = input("Ingrese su contraseña (o '1' para volver al menú principal): ")
            if password == '1':
                continue  # Vuelve al menú principal

            try:
                rol = user_dao.login(rut, password)
                if rol:
                    # Verificar si el usuario no está marcado como eliminado
                    if not user_dao.usuario_eliminado(rut):
                        if opcion == "1" and rol == "ADMIN":
                            print("Login exitoso como Administrador!")
                            menu_administrador()
                            break  # Salimos del bucle principal de login
                        elif opcion == "2" and rol == "EMPLEADO":
                            print("Login exitoso como Empleado!")
                            menu_empleado(rut)
                            break  # Salimos del bucle principal de login
                        else:
                            print("RUT o contraseña incorrectos o no tiene los permisos adecuados.")
                    else:
                        print("Este usuario ha sido marcado como eliminado y no puede iniciar sesión.")
                else:
                    print("RUT o contraseña incorrectos.")
            except ValueError as e:
                print(f"Error: {e}")
        elif opcion == "3":
            crear_cuenta()
        elif opcion == "4":
            print("Saliendo...")
            return None
        else:
            print("Opción no válida.")

def crear_cuenta():
    while True:
        rut = input("Ingrese su RUT (o '1' para volver al menú principal): ")
        if rut == '1':
            break
        valido, mensaje = validar_rut(rut)
        if not valido:
            print(f"Error: {mensaje}")
            continue

        nombre_usuario = input("Ingrese un nombre de usuario (o '1' para volver al menú principal): ")
        if nombre_usuario == '1':
            break
        valido, mensaje = validar_nombre_usuario(nombre_usuario)
        if not valido:
            print(f"Error: {mensaje}")
            continue

        password = input("Ingrese una contraseña (o '1' para volver al menú principal): ")
        if password == '1':
            break
        valido, mensaje = validar_contrasena(password)
        if not valido:
            print(f"Error: {mensaje}")
            continue

        nuevo_usuario = User(rut, nombre_usuario, password)
        try:
            user_dao.crearCuenta(nuevo_usuario)
            print("Cuenta creada exitosamente!")
        except Exception as e:
            print(f"Error al crear la cuenta: {e}")
        break

def menu_empleado(rut):
    while True:
        print("\nMenú Empleado")
        print("1. Actualizar mis datos")
        print("2. Agregar carga familiar")
        print("3. Cambiar mi contraseña")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            actualizar_mis_datos(rut)
        elif opcion == "2":
            agregar_carga_familiar(rut)
        elif opcion == "3":
            cambiar_mi_contrasena(rut)
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

def actualizar_mis_datos(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        while True:
            print("\n1: Actualizar datos personales")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                empleado_dao.actualizarPropio(rut)
                break
            elif sub_opcion == '2':
                break
            else:
                print("Opción no válida. Intente de nuevo.")
    else:
        print("Empleado no encontrado.")

def agregar_carga_familiar(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        nombre_carga = input("Ingrese el nombre de la carga familiar: ").upper()
        parentesco = input("Ingrese el parentesco con la carga familiar: ").upper()
        genero_carga = input("Ingrese el género de la carga familiar (M/F): ").upper()
        rut_carga = input("Ingrese el RUT de la carga familiar: ")

        carga_familiar = {
            'nombre_carga': nombre_carga,
            'parentesco': parentesco,
            'genero_carga': genero_carga,
            'rut_carga': rut_carga
        }

        empleado.cargas_familiares.append(carga_familiar)

        try:
            empleado_dao.insertarCargaFamiliar(empleado.rut, nombre_carga, parentesco, genero_carga, rut_carga)
            print("Carga familiar agregada correctamente.")
        except Exception as e:
            print(f"Error al agregar carga familiar: {e}")
    else:
        print("Empleado no encontrado.")

def cambiar_mi_contrasena(rut):
    nueva_contrasena = input("Ingrese su nueva contraseña: ")
    valido, mensaje = validar_contrasena(nueva_contrasena)
    if not valido:
        print(f"Error: {mensaje}")
        return
    resultado = user_dao.cambiar_contrasena(rut, nueva_contrasena)
    print(resultado)
    time.sleep(3)

def menu_administrador():
    while True:
        system('cls')
        print("Opción 1: Ingresar un Empleado")
        print("Opción 2: Eliminar un Empleado")
        print("Opción 3: Actualizar un Empleado")
        print("Opción 4: Mostrar todos los Empleados")
        print("Opción 5: Buscar Empleados por Cargo")
        print("Opción 6: Mostrar cantidad de Empleados")
        print("Opción 7: Cambiar el rol de un Empleado")
        print("Opción 8: Buscar empleados filtrados")
        print("Opción 9: Cambiar contraseña de un Empleado")
        print("Opción 10: Salir")

        opcion = input("Seleccione una opción entre 1 y 10: ")

        if opcion == '1':
            ingresar_empleado()
        elif opcion == '2':
            eliminar_empleado()
        elif opcion == '3':
            actualizar_empleado()
        elif opcion == "4":
            mostrar_todos_empleados()
        elif opcion == '5':
            buscar_empleados_por_cargo()
        elif opcion == '6':
            mostrar_cantidad_empleados()
        elif opcion == "7":
            cambiar_rol_empleado()
        elif opcion == '8':
            buscar_empleados_filtrados()
        elif opcion == '9':
            cambiar_contrasena_empleado()
        elif opcion == '10':
            login_menu()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def ingresar_empleado():
    while True:
        print("\n1: Ingresar un nuevo empleado")
        print("2: Volver al menú principal")
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '2':
            break
            
        rut_trabajador = input("Ingrese el RUT del empleado: ")
        empleado_existe = empleado_dao.buscarEmpleado(rut_trabajador)

        if empleado_existe is None:
            nombre_trabajador = input("Ingrese el nombre completo del empleado: ").upper()
            genero_trabajador = input("Ingrese el género del empleado (M/F): ").upper()
            direccion = input("Ingrese la dirección del trabajador: ").upper()
            telefono = input("Ingrese el teléfono del trabajador: ")
            cargo = input("Ingrese el cargo del trabajador: ").upper()
            fecha_ingreso = input("Ingrese la fecha de ingreso del trabajador (YYYY-MM-DD): ")
            area = input("Ingrese el área del trabajador: ").upper()
            departamento = input("Ingrese el departamento del trabajador: ").upper()
            nombre_contacto = input("Ingrese el nombre del contacto de emergencia: ").upper()
            relacion = input("Ingrese la relación con el contacto de emergencia: ").upper()
            telefono_contacto = input("Ingrese el teléfono del contacto de emergencia: ")
            nuevo_empleado = Empleado(rut_trabajador, nombre_trabajador, genero_trabajador, direccion, telefono, cargo, fecha_ingreso, area, departamento, nombre_contacto, relacion, telefono_contacto)
            empleado_dao.insertarEmpleado(nuevo_empleado)
            print("Empleado ingresado correctamente")
        else:
            print("El empleado ya existe")

        system('cls')
        break

def eliminar_empleado():
    while True:
        print("\n1: Eliminar un empleado")
        print("2: Volver al menú principal")
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '2':
            break

        rut_trabajador = input("Ingrese el RUT del empleado a eliminar: ")
        resultado_empleado = empleado_dao.eliminarEmpleado(rut_trabajador)
    
        if resultado_empleado.startswith('Empleado eliminado con éxito'):
            resultado_usuario = user_dao.eliminarUsuario(rut_trabajador)
            if resultado_usuario.startswith('Usuario eliminado con éxito'):
                print("Empleado y usuario asociado eliminados con éxito.")
            else:
                print("Error al eliminar el usuario asociado:", resultado_usuario)
        else:
            print("Error al eliminar el empleado:", resultado_empleado)
    
        system('cls')
        break

def mostrar_todos_empleados():
    while True:
        print("\n1: Mostrar todos los empleados")
        print("2: Volver al menú principal")
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '2':
            break

        empleados = empleado_dao.obtenerEmpleados()
        print(empleados)
        time.sleep(10)
        break

def buscar_empleados_por_cargo():
    while True:
        print("\n1: Buscar empleados por cargo")
        print("2: Volver al menú principal")
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '2':
            break
        system('cls')
        cargo = input("Ingrese el cargo a buscar: ")
        empleado_dao.empleadosPorCargo(cargo)
        
        
        system('cls')
        break

def mostrar_cantidad_empleados():
    while True:
        print("\n1: Mostrar cantidad de empleados")
        print("2: Volver al menú principal")
        sub_opcion = input("Seleccione una opción: ")
        if sub_opcion == '2':
            break

        cantidad = empleado_dao.cantidadEmpleados()
        print(f"La cantidad de empleados es: {cantidad[0]}")
        
        time.sleep(3)
        break

def cambiar_rol_empleado():
    rut = input("Ingrese el RUT del usuario: ")
    nuevo_rol = input("Ingrese el nuevo rol (ADMIN/EMPLEADO): ").upper()
    user_dao.cambiarRol(rut, nuevo_rol)

def buscar_empleados_filtrados():
    genero = input("Ingrese el género del trabajador (M/F): ").upper()
    cargo = input("Ingrese el cargo del trabajador: ").upper()
    area = input("Ingrese el área del trabajador: ").upper()
    departamento = input("Ingrese el departamento del trabajador: ").upper()

    empleados = empleado_dao.buscarEmpleadosFiltrados(genero, cargo, area, departamento)

    if empleados:
        table = BeautifulTable()
        table.columns.header = ["Nombre", "Dirección", "Género", "Teléfono", "Cargo", "Área", "Departamento"]
        
        for empleado in empleados:
            table.rows.append(empleado)
        
        print(table)
    else:
        print("No se encontraron empleados que cumplan con los criterios especificados.")
    
    input("Presione Enter para salir.")

def cambiar_contrasena_empleado():
    rut = input("Ingrese el RUT del empleado: ")
    nueva_contrasena = input("Ingrese la nueva contraseña: ")
    valido, mensaje = validar_contrasena(nueva_contrasena)
    if not valido:
        print(f"Error: {mensaje}")
        return
    resultado = user_dao.cambiar_contrasena(rut, nueva_contrasena)
    print(resultado)
    time.sleep(3)

def actualizar_empleado():
    while True:
        print("\nOpciones de actualización para un empleado:")
        print("1: Actualizar datos personales")
        print("2: Actualizar datos laborales")
        print("3: Actualizar datos de carga familiar")
        print("4: Actualizar datos del contacto de emergencia")
        print("5: Regresar al Menú Anterior")
        opcion = input("Seleccione una opción: ")

        if opcion in ['1', '2', '3', '4']:
            rut_trabajador = input("Ingrese el RUT del empleado a actualizar: ")
            if opcion == '1':
                actualizar_datos_personales(rut_trabajador)
            elif opcion == '2':
                actualizar_datos_laborales(rut_trabajador)
            elif opcion == '3':
                actualizar_datos_carga_familiar(rut_trabajador)
            elif opcion == '4':
                actualizar_datos_emergencia(rut_trabajador)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def actualizar_datos_personales(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        empleado_dao.actualizarDatosPropios(rut, empleado)
    else:
        print("Empleado no encontrado.")
        
#### agrega carga desde empleado

def agregar_carga_familiar(rut_empleado):
    print("Ingrese el nombre de la carga familiar:")
    nombre = input()
    print("Ingrese el parentesco con la carga familiar:")
    parentesco = input()
    print("Ingrese el género de la carga familiar (M/F):")
    genero = input().upper()
    print("Ingrese el RUT de la carga familiar:")
    rut_carga = input()

    empleado_dao = EmpleadoDao()
    try:
        empleado_dao.insertarCargaFamiliar(rut_empleado, nombre, parentesco, genero, rut_carga)
        print("Carga familiar agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar carga familiar: {e}")
        
###fin de agregar carga desde empleado

def actualizar_datos_laborales(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        empleado_dao.actualizarDatosLaborales(rut, empleado)
    else:
        print("Empleado no encontrado.")

def actualizar_datos_carga_familiar(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        empleado_dao.actualizarDatosCargaFamiliar(rut, empleado)
    else:
        print("Empleado no encontrado.")

def actualizar_datos_emergencia(rut):
    empleado = empleado_dao.buscarEmpleado(rut)
    if empleado is not None:
        empleado_dao.actualizarDatosEmergencia(rut, empleado)
    else:
        print("Empleado no encontrado.")

if __name__ == "__main__":
    login_menu()
