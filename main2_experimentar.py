from empleado_dao_ej import EmpleadoDao
from empleado import Empleado
from os import system
system('cls')

empleado_dao = EmpleadoDao()

def opciones():
    print("Opción 1: Ingresar un Empleado")
    print("Opción 2: Eliminar un Empleado")
    print("Opción 3: Actualizar un Empleado")
    print("Opción 4: Mostrar todos los Empleados")
    print("Opción 5: Buscar Empleados por Cargo")
    print("Opción 6: Mostrar cantidad de Empleados")
    print("Opción 7: Salir")

def volver_menu():
    
    input("Presione Enter para volver al menú principal...")
while True:
    
    system('cls')
    
    opciones()
    opcion = input("Seleccione una opción entre 1 y 7: ")
    if opcion == '1':
        while True:
            print("\n1: Ingresar un nuevo empleado")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '2':
                break
                
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

            volver_menu()
            break

    elif opcion == '2':
        while True:
            print("\n1: Eliminar un empleado")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '2':
                break

            rut_trabajador = input("Ingrese el RUT del empleado a eliminar: ")
            resultado = empleado_dao.eliminarEmpleado(rut_trabajador)
            print(resultado)
            
            volver_menu()
            break

    elif opcion == '3':
        while True:
            print("\n1: Actualizar un empleado")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                rut_trabajador = input("Ingrese el RUT del empleado a actualizar: ")
                empleado_dao.actualizarEmpleado(rut_trabajador)
                volver_menu()
                break
            elif sub_opcion == '2':
                break
            else:
                print("Opción no válida. Intente de nuevo.")
 

    elif opcion == "4":
        while True:
            print("\n1: Mostrar todos los empleados")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '2':
                break
            system('cls')
            empleados = empleado_dao.obtenerEmpleados()
            print(empleados)
            volver_menu()
            break

    elif opcion == '5':
        while True:
            print("\n1: Buscar empleados por cargo")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '2':
                break
            system('cls')
            cargo = input("Ingrese el cargo a buscar: ")
            empleado_dao.empleadosPorCargo(cargo)
            
            
            
            
            volver_menu()
            break

    elif opcion == '6':
        while True:
            print("\n1: Mostrar cantidad de empleados")
            print("2: Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '2':
                break
            system('cls')
            cantidad = empleado_dao.cantidadEmpleados()
            print(f"La cantidad de empleados es: {cantidad[0]}")
            
            
            volver_menu()
            break

    elif opcion == '7':
        break

    else:
        print("Opción no válida. Intente de nuevo.")
