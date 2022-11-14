# Productos definidos


pantalon_talle_38 = {"codigo":200,"nombre":"pantalon talle 38","categoria":"pantalon","precio":8000,"stock":0}
pantalon_talle_40 = {"codigo":210,"nombre":"pantalon talle 40","categoria":"pantalon","precio":9000,"stock":0}
pantalon_talle_42 = {"codigo":220,"nombre":"pantalon talle 42","categoria":"pantalon","precio":10000,"stock":0}
    

import time
from collections import Counter
from traceback import print_list

class Sucursal:
    def __init__(self):
        self.productos = set()
        self.ventas = []
        self.gasto_por_dia = 15000

    def ver_productos(self):
        if not len(self.productos) == 0:
           for producto in self.productos:
            print("codigo:"+str(producto.codigo)+" nombre:"+producto.nombre+" precio:"+str(producto.precio)+" stock:"+str(producto.stock)+" categoria/s:"+producto.ver_categorias())
        else:
            raise ValueError ("No hay productos registrados")    
               
    def registrar_producto(self,nuevo_producto):
        largo_inicial = len(self.productos)
        self.productos.add(nuevo_producto)
        if len(self.productos) == largo_inicial:
            raise ValueError ("El producto ya se encuentra registrado")

    def recargar_stock(self,codigo_producto,cantidad_a_agregar):
        codigo_valido = False
        for producto in self.productos:
            if codigo_producto == producto.codigo: # TODO delegar para evitar este for + if en todos lados
               codigo_valido = True
               producto.stock += cantidad_a_agregar
        if not codigo_valido:
            raise ValueError ("El codigo no corresponde a un producto registrado")        

    def hay_stock(self,codigo_producto):
        for producto in self.productos:
            if codigo_producto == producto.codigo:
               return producto.stock > 0
        return False

    def calcular_precio_final(self,producto,es_extranjero):
        
        valor_final = 0
        valor_final = producto.precio_final(producto.precio)
        
        if es_extranjero and valor_final > 70:
           return valor_final
        else:
           valor_final = valor_final+(21*valor_final)/100
           return valor_final   

    def contar_categorias(self):
        lista_total_categorias = []
        for producto in self.productos:
            for categoria in producto.categoria:
                if not categoria in lista_total_categorias:
                   lista_total_categorias.append(categoria)
        return len(lista_total_categorias) 

    def realizar_compra(self,codigo_producto,cantidad_a_comprar,es_extranjero):
        codigo_valido = False
        for producto in self.productos:
            if codigo_producto == producto.codigo:
               codigo_valido = True
               if self.hay_stock(codigo_producto) and  producto.stock > cantidad_a_comprar:
                  producto.stock -= cantidad_a_comprar
                  monto_total = producto.calcular_precio_final(producto,es_extranjero)*cantidad_a_comprar
                  self.ventas.append({"producto":producto.nombre,"cantidad_vendida":cantidad_a_comprar,"monto":monto_total,"fecha":time.strftime("%d/%m"),"anio":time.strftime("%Y")})
               else:
                  raise ValueError ("No hay suficiente stock para realizar la venta")      
        if not codigo_valido:
           raise ValueError ("El codigo no corresponde a un producto registrado")

    def descontinuar_productos(self):
        for producto in self.productos:
            if producto.stock <= 0:
               self.productos.remove(producto)

    def valor_ventas_del_dia(self):
        valor_total = 0
        for venta in self.ventas:
            if time.strftime("%d/%m") == venta["fecha"]:
               valor_total += venta["monto"]
        return valor_total

    def ventas_del_anio(self):
        ventas_anio = 0
        for venta in self.ventas:
            if time.strftime("%Y") == venta["anio"]:
               ventas_anio += venta["monto"]
        return ventas_anio

    def productos_mas_vendidos(self,cantidad_de_productos):
        productos_vendidos = []
        mas_vendidos = []
        for venta in self.ventas:
            productos_vendidos.append(venta["producto"])
        
            mas_vendidos = Counter(productos_vendidos)
            print ("",mas_vendidos.most_common(cantidad_de_productos))

    def actualizar_precios_por_categoria(self,categoria,porcentaje):
        for producto in self.productos:
            for categoria in producto.categoria:
                if categoria.lower() == categoria:
                   producto.precio += (producto.precio*porcentaje)/100

    def gastos_del_dia(self):
        return self.gasto_por_dia

    def ganancia_diaria(self):
        return self.valor_ventas_del_dia() - self.gastos_del_dia()                                                            


class SucursalVirtual:
    def __init__(self):
        self.productos = set()
        self.ventas = []
        self.gasto_por_dia = 15000
        self.gasto_variable = 1

    def ver_productos(self):
        if not len(self.productos) == 0:
           for producto in self.productos:
            print("codigo:"+str(producto.codigo)+" nombre:"+producto.nombre+" precio:"+str(producto.precio)+" stock:"+str(producto.stock)+" categoria/s:"+producto.ver_categorias())
        else:
            raise ValueError ("No hay productos registrados")    
               
    def registrar_producto(self,nuevo_producto):
        largo_inicial = len(self.productos)
        self.productos.add(nuevo_producto)
        if len(self.productos) == largo_inicial:
            raise ValueError ("El producto ya se encuentra registrado")

    def recargar_stock(self,codigo_producto,cantidad_a_agregar):
        codigo_valido = False
        for producto in self.productos:
            if codigo_producto == producto.codigo:
               codigo_valido = True
               producto.stock += cantidad_a_agregar
        if not codigo_valido:
            raise ValueError ("El codigo no corresponde a un producto registrado")        

    def hay_stock(self,codigo_producto):
        for producto in self.productos:
            if codigo_producto == producto.codigo:
               return producto.stock > 0
        return False

    def calcular_precio_final(self,producto,es_extranjero):
        
        valor_final = 0
        valor_final = producto.precio_final(producto.precio)
        
        if es_extranjero and valor_final > 70:
           return valor_final
        else:
           valor_final = valor_final+(21*valor_final)/100
           return valor_final   

    def contar_categorias(self): # TODO usar un set 
        lista_total_categorias = []
        for producto in self.productos:
            for categoria in producto.categoria:
                if not categoria in lista_total_categorias:
                   lista_total_categorias.append(categoria)
        return len(lista_total_categorias) 

    def realizar_compra(self,codigo_producto,cantidad_a_comprar,es_extranjero):
        codigo_valido = False
        for producto in self.productos: # TODO evitar estructuras de control anidadas
            if codigo_producto == producto.codigo:
               codigo_valido = True
               if self.hay_stock(codigo_producto) and  producto.stock > cantidad_a_comprar:
                  producto.stock -= cantidad_a_comprar
                  monto_total = producto.calcular_precio_final(producto,es_extranjero)*cantidad_a_comprar
                  self.ventas.append({"producto":producto.nombre,"cantidad_vendida":cantidad_a_comprar,"monto":monto_total,"fecha":time.strftime("%d/%m"),"anio":time.strftime("%Y")})
               else:
                  raise ValueError ("No hay suficiente stock para realizar la venta")      
        if not codigo_valido:
           raise ValueError ("El codigo no corresponde a un producto registrado")

    def descontinuar_productos(self):
        for producto in self.productos:
            if producto.stock <= 0:
               self.productos.remove(producto)

    def valor_ventas_del_dia(self):
        valor_total = 0
        for venta in self.ventas:
            if time.strftime("%d/%m") == venta["fecha"]:
               valor_total += venta["monto"]
        return valor_total

    def ventas_del_anio(self):
        ventas_anio = 0
        for venta in self.ventas:
            if time.strftime("%Y") == venta["anio"]:
               ventas_anio += venta["monto"]
        return ventas_anio

    def productos_mas_vendidos(self,cantidad_de_productos):
        productos_vendidos = []
        mas_vendidos = []
        for venta in self.ventas:
            productos_vendidos.append(venta["producto"])
        
            mas_vendidos = Counter(productos_vendidos)
            print ("",mas_vendidos.most_common(cantidad_de_productos))

    def actualizar_precios_por_categoria(self,categoria,porcentaje):
        for producto in self.productos:
            for categoria in producto.categoria: # TODO encapsular y delegar
                if categoria.lower() == categoria:
                   producto.precio += (producto.precio*porcentaje)/100

    def gastos_del_dia(self):
        if len(self.ventas) > 100:
            return len(self.ventas)*self.gasto_variable

    def modificar_gasto_variable(self,nuevo_valor):
        self.gasto_variable = nuevo_valor

    def ganancia_diaria(self):
        return self.valor_ventas_del_dia() - self.gastos_del_dia()   



class Prenda:
    def __init__(self,codigo,nombre,precio,categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = 0
        self.categoria = [categoria]
        self.estado = Nueva()

    def ver_categorias(self):
        categorias = ",".join(self.categoria)
        return categorias
           
    def agregar_categoria(self,nueva_categoria):
        self.categoria.append(nueva_categoria)
    
    def cambiar_estado(self,nuevo_estado):
        self.estado = nuevo_estado

    def precio_final(self,precio):
        return self.estado.precio_final(precio)

    def es_de_categoria(self,categoria):
        return categoria in self.categoria    


class Nueva:
    def precio_final(self,precio):
        return precio

class Promocion:
    def __init__(self,valor):
        self.valor_promo = valor
        
    def precio_final(self,precio):
        return precio - self.valor_promo

class Liquidacion:
    def precio_final(self,precio):
        return precio/2


        


#ADICIONAL REINICIAR LISTA DE PRODUCTOS
def reiniciar_lista_productos(self):
    self.productos.clear()

#ADICIONAL REINICIAR LISTA DE VENTAS
def reiniciar_lista_ventas(self):
    self.ventas.clear()

#ADICIONAL CARGAR 2 PRODUCTOS A LA LISTA CON STOCK
def lista_de_2_productos_con_stock(self):
    self.reiniciar_lista_productos()
    self.reiniciar_lista_ventas()
    self.registrar_producto(remera_talle_s)
    remera_talle_s.stock = 0
    self.registrar_producto(pantalon_talle_38)
    pantalon_talle_38.stock = 0
    self.recargar_stock(100,100)
    self.recargar_stock(200,100)    

