

import mysql.connector
from mysql.connector import Error
from decouple import config
import json
class producto:
    def __init__(self,id_productos,nombre,marca,precio,stock,garantia):
        self.__id_productos = id_productos
        self.__nombre = nombre.upper() 
        self.__marca = marca.upper()
        self.__precio = self.validar_precio(precio)
        self.__stock = stock 
        self.__garantia = garantia

    @property
    def id_productos(self):
        return self.__id_productos
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def marca(self):
        return self.__marca

    @property
    def precio(self):
        return self.__precio
    
    @property
    def stock(self):
        return self.__stock
    
    @property
    def garantia(self):
        return self.__garantia
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser numérico positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")
    
   
    def to_dict(self):
        return{
            'id_productos': self.__id_productos,
            'nombre': self.__nombre,
            'marca':self.__marca,
            'precio': self.__precio,
            'stock' : self.__stock,
            'garantia':self.__garantia
        }

    def __str__(self):
        return f'{self.__id_productos},{self.__nombre},{self.__marca},{self.__precio}'
      

class productoTelevisor(producto):
    def __init__ (self,id_productos,nombre,marca,pantalla_pulgadas,precio,stock,garantia):
        super().__init__(id_productos,nombre,marca,precio,stock,garantia)
        self.__pantalla_pulgadas = pantalla_pulgadas

    @property
    def pantalla_pulgadas(self):
        return self.__pantalla_pulgadas

    def to_dict(self):
        data = super().to_dict()
        data ["pantalla_pulgadas"]= self.__pantalla_pulgadas
        return data
        

    def __str__(self): 
       return f'{super( ).__str__()} - pantalla_pulgadas {self.__pantalla_pulgadas}'

      
class productoHeladera(producto):
    def __init__ (self,id_productos,nombre,marca,capacidad_litros,precio,stock,garantia):
        super().__init__(id_productos,nombre,marca,precio,stock,garantia)
        self.__capacidad_litros = capacidad_litros

    @property
    def capacidad_litors(self):
        return self.__capacidad_litros   

    def to_dict(self):
        data = super().to_dict()
        data ["capacidad_litros"]= self.__capacidad_litros
        return data
        

    def __str__(self):
       return f'{super().__str__()} - capacidad_litros {self.__capacidad_litros}' 

class GestionProductos:
    
    def __init__(self):

        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):

        try:
            connection = mysql.connector.connect(  
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
                  )
            if connection.is_connected():
                return connection
                
        except Error as e:
            print (f'error al conectar a la base de datos:{e}')   
            return None


    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor :
                 
                    cursor.execute('SELECT id_productos FROM producto WHERE id_productos = %s ',(producto.id_productos,))
                    if cursor.fetchone():
                        print(f'Error: ya exixte producto ')
                        return
                    query = '''
                        INSERT INTO producto (id_productos, nombre, marca, precio, stock, garantia)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                    values = (producto.id_productos, producto.nombre, producto.marca, producto.precio, producto.stock, producto.garantia)
                    cursor.execute(query, values)

                    if isinstance(producto, productoTelevisor):
                        cursor.execute( ''' INSERT INTO productotelevisor (id_productos, pantalla_pulgadas)
                        VALUES (%s, %s)
                        ''', (producto.id_productos, producto.pantalla_pulgadas))
                    elif isinstance(producto, productoHeladera):
                        cursor.execute( ''' INSERT INTO productoheladera (id_productos, capacidad_litros)
                        VALUES (%s, %s)
                        ''', (producto.id_productos, producto.capacidad_litors))

                    connection.commit()    
                    print(f"El producto {producto.nombre} se agrego correctamente.")
    
        except Exception as error:
            print(f'Error al agregar el producto: {error}')


    def actualizar_precio(self, id_productos, nuevo_precio):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE id_productos = %s',(id_productos,))
                    if not cursor.fetchone():
                        print(f' No se encontro el producto con id_productos: {id_productos}')
                        return
                    cursor.execute('UPDATE producto SET precio = %s WHERE id_productos = %s', (nuevo_precio, id_productos))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Precio del producto con id_productos: {id_productos} actualizado ')
                    else:
                        print(f'no se encontró el producto')

        except Exception as e:
            print(f'Error al actualizar el precio: {e}')
        finally:
            if connection.is_connected():
             connection.close()

    def actualizar_stock(self, id_productos, nuevo_stock):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE id_productos = %s',(id_productos,))
                    if not cursor.fetchone():
                        print(f' No se encontro el producto con id_productos: {id_productos}')
                        return
                    cursor.execute('UPDATE producto SET stock = %s WHERE id_productos = %s', (nuevo_stock, id_productos))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Stock del producto con id_producto: {id_productos} actualizado ')
                    else:
                        print(f'no se encontró el producto')

        except Exception as e:
            print(f'Error al actualizar el stock: {e}')
        finally:
            if connection.is_connected():
             connection.close()
      
    def eliminar_producto(self, id_productos):
        try:
           connection = self.connect()
           if connection:
                with connection.cursor() as cursor:
                   
                    cursor.execute('SELECT * FROM producto WHERE id_productos = %s', (id_productos,))
                    if not cursor.fetchone():
                        print(f'No se encontro producto con id_productos: {id_productos}')
                        return 
                    cursor.execute('DELETE FROM productotelevisor WHERE id_productos = %s', (id_productos,))
                    cursor.execute('DELETE FROM productoheladera WHERE id_productos = %s', (id_productos,))
                    cursor.execute('DELETE FROM producto WHERE id_productos = %s', (id_productos,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'El producto Id:{id_productos} se elimino correctamente')
                    else:
                         print(f'No se encontró Id:{id_productos}')
        except Exception as e:
            print(f'Error al eliminar producto: {e}')    

   

    def mostrar_todos_los_productos_heladera(self,capacidad_litros):
        try:
           connection = self.connect()
           if connection:
                with connection.cursor() as cursor:
                        query = '''select  producto.id_productos, nombre, marca, capacidad_litros, precio, stock, garantia from producto  
                                inner join productoheladera on producto.id_productos = productoheladera.id_productos where capacidad_litros = %s '''
                        cursor.execute(query,(capacidad_litros,))
                        resultados = cursor.fetchall()

                print(f"{'id_propducto':<10} - {'nombre':<10} -  {'marca':<10} - { 'capacidad_litros':<10} - {'precio':<10} - {'stock':<10} - {'garantia':<10}")

                for fila in resultados:
                 print(f"{fila[0]:<14} {fila[1]:<13} {fila[2]:<13} { fila[3]:<18} {fila[4]:<11} {fila[5]:<11} {fila[6]:<10}")

        except Exception as e:
            print(f'Error al mostrar los producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def mostrar_todos_los_productos_televisor(self,pantalla_pulgadas):
        try:
           connection = self.connect()
           if connection:
                with connection.cursor() as cursor:
                        query = '''select  producto.id_productos, nombre, marca, pantalla_pulgadas, precio, stock, garantia from producto  
                                inner join productotelevisor on producto.id_productos = productotelevisor.id_productos where pantalla_pulgadas = %s '''
                        cursor.execute(query,(pantalla_pulgadas,))
                        resultados = cursor.fetchall()
                print(f"{'id_propducto':<10} - {'nombre':<10} - {'marca':<10} - { 'pantalla_pulgadas':<10} - {'precio':<10} - {'stock':<10} - {'garantia':<10}")

                for fila in resultados:
             
                 print(f"{fila[0]:<14} {fila[1]:<13} {fila[2]:<13} { fila[3]:<18} {fila[4]:<11} {fila[5]:<11} {fila[5]:<10}")

        except Exception as e:
            print(f'Error al mostrar los productos: {e}')
        finally:
            if connection.is_connected():
                connection.close()

















