import os
import platform

from desafio_1 import (
    productoHeladera,
    productoTelevisor,
    GestionProductos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') 

        
def mostrar_menu():
    print("========== Menú ==========")
    print('1. Agregar Producto')
    print('2. Actualizar productos')
    print('3. Eliminar Producto')
    print('4. Mostrar Productos Heladera/Televisor segun litros/pulgadas')
    print('5. salir')
    print('======================================================')

def agregar_producto(gestion):
    try:
        id_productos = (input('Ingrese id de el Producto: '))
        nombre = input('Ingrese nombre del Producto: ')
        marca = input('Ingrese marca del Producto: ')
        precio =float(input('Ingrese el precio del Producto: '))
        stock = int(input('Ingrese stock del Producto: '))
        garantia = int(input('Ingrese garantia del Producto: '))
        
        if nombre == 'televisor':
            pantalla_pulgadas = int(input('Ingrese pulgadas de la pantalla: '))
            producto = productoTelevisor(id_productos, nombre, marca,pantalla_pulgadas,precio, stock, garantia)
        elif nombre == 'heladera':
            capacidad_litros = int(input('Ingresar capacida en litors del producto: '))
            producto = productoHeladera(id_productos, nombre, marca,capacidad_litros,precio, stock, garantia)
        else:

            print('Nombre del producto invalido')
            input('Presione enter para continuar...')
            return

        gestion.crear_producto(producto)
        input('Presione enter para continuar...')


    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')    
    input('Presione enter para continuar...')

def actualizar_producto(gestion):
    id_productos = input('Ingrese el id del producto : ')
    atributo = input ('Ingrese atributo que desea actualizar(precio/stock): ')
    if atributo == 'precio':
       precio = float(input('Ingrese Nuevo Precio del Producto: '))
       gestion.actualizar_precio(id_productos, precio)
    elif atributo == 'stock':
       stock = int(input('Ingrese nuevo stock del Producto:'))
       gestion.actualizar_stock(id_productos, stock)
    else :
        print ('opcion no valida') 
        input('Presione enter para continuar...')
        return 
        
    input('Presione enter para continuar...')

def eliminar_producto(gestion):
    id_productos = input('Ingrese el Id del Producto que desea eliminar: ')
    gestion.eliminar_producto(id_productos)
    input('Presione enter para continuar...')    

def mostrar_todos_los_productos(gestion):
    try:
        nombre = input('Ingrese nombre del Producto: ')
        if nombre =='heladera':
           capacidad_litros =  input('Ingresar capacida en litors del producto: ')
           print('=============== Lista de Productos Heladeras ==============')
           gestion.mostrar_todos_los_productos_heladera(capacidad_litros)
           print('=====================================================================')
        elif nombre == 'televisor':
           pantalla_pulgadas = input('Ingrese pulgadas de la pantalla: ')
           print('=============== Lista de Producto Televisor ==============')
           gestion.mostrar_todos_los_productos_televisor(pantalla_pulgadas)
           print('=====================================================================')
    except Exception as e:
        print(f'Error al mostrar productos {e}')
    input('Presione enter para continuar...')
   


if __name__ == "__main__":

    gestion = GestionProductos()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1':
            agregar_producto(gestion)
        
        elif opcion == '2':
            actualizar_producto(gestion)

        elif opcion == '3':
            eliminar_producto(gestion)

        elif opcion == '4':
            mostrar_todos_los_productos(gestion)

        elif opcion == '5':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-6)')     
        
