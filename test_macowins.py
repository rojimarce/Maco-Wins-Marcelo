import pytest
from macowins import *

#TEST 1. REGISTRAR PRODUCTOS

remera_talle_s = Prenda(codigo=100, nombre="remera talle s", categoria="remera", precio= 4500)
remera_talle_m = Prenda(codigo=110, nombre="remera talle m", categoria="remera", precio= 4750)
remera_talle_l = Prenda(codigo=120, nombre="remera talle l", categoria="remera", precio= 5000)


def test_registrar_un_producto_en_lista_de_productos():
    sucursal_madero = Sucursal()
    sucursal_madero.registrar_producto(remera_talle_s)
    assert remera_talle_s in sucursal_madero.productos
    
def test_registrar_una_lista_vacia_en_lista_de_productos():
    reiniciar_lista_productos()
    espero = [[]]
    lista_vacia = []
    registrar_producto(lista_vacia)
    assert productos == espero

#TEST 2. RECARGAR STOCK
        
def test_recargar_stock_a_remera_talle_s(): 
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)  
    recargar_stock(100,50)
    assert hay_stock(100) 
    
    
def test_recargar_100_de_stock_a_remera_talle_s():
    reiniciar_lista_productos()
    remera_talle_s["stock"] = 0
    registrar_producto(remera_talle_s)  
    recargar_stock(100,100)
    assert productos == [{"codigo":100,"nombre":"remera talle s","categoria":"remera","precio": 4500,"stock":100}]
    
#TEST 3. HAY STOCK 

def test_hay_stock_con_0_de_stock_del_producto_remera_talle_s():
     reiniciar_lista_productos()
     registrar_producto(remera_talle_s)
     remera_talle_s["stock"] = 0
     assert hay_stock(100) == False
     
def test_hay_stock_con_1_de_stock_del_producto_remera_talle_s():
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    recargar_stock(100,1)
    assert hay_stock(100) == True 
    
#TEST 4. CALCULAR PRECIO FINAL    

def test_calcular_precio_final_de_pantalon_talle_38_con_vendedor_extranjero():
    assert calcular_precio_final(pantalon_talle_38,True) == 8000
    
def test_calcular_precio_final_de_pantalon_talle_38_con_vendedor_local():
    assert calcular_precio_final(pantalon_talle_38,False) == 9680
    
#TEST 5. CUANTAS CATEGORIAS UNICAS HAY

def test_cuantas_categorias_tengo_con_1_producto():
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    assert contar_categorias() == 1

def test_cuantas_categorias_tengo_con_2_productos_de_misma_categoria():
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    registrar_producto(remera_talle_m)
    assert contar_categorias() == 1
    
def test_cuantas_categorias_tengo_con_2_productos_de_distinta_categoria():
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    registrar_producto(pantalon_talle_38)
    assert contar_categorias() == 2
          
#TEST 6. REALIZAR COMPRA  
def test_realizar_compra_con_1_producto():    
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    recargar_stock(100,100)
    realizar_compra(100,50)
    assert len(ventas) == 1
    
def test_realizar_2_compras_con_1_producto():
    reiniciar_lista_productos()
    reiniciar_lista_ventas()
    registrar_producto(remera_talle_s)
    remera_talle_s["stock"]= 0
    recargar_stock(100,10)
    realizar_compra(100,1)
    realizar_compra(100,2)
    assert len(ventas) == 2 
    
def test_realizar_compra_sin_stock():
    reiniciar_lista_productos()
    registrar_producto(pantalon_talle_38)
    pantalon_talle_38["stock"] = 0
    with pytest.raises(ValueError) as auxiliar:
        realizar_compra(200,1)
    assert str(auxiliar.value) ==  "No hay suficiente stock para realizar la venta"
    
    
#TEST 7. ELIMINAR LOS PRODUCTOS SIN STOCK

def test_eliminar_pantalon_talle_38_sin_stock():
    lista_de_2_productos_con_stock()
    productos[1]["stock"]= 0
    descontinuar_productos()
    lista_nombres = [producto["nombre"] for producto in productos]
    assert not "pantalon talle 38" in lista_nombres

# ADICIONAL!!!! POR LAS DUDAS 

def test_probar_multiples_asserts():
    lista_de_2_productos_con_stock()
    
    lista_nombres_inicial = [producto["nombre"] for producto in productos]
    errores = []
    if "pantalon talle 38" not in lista_nombres_inicial:
        errores.append("no existe pantalon talle 38 en la lista inicial")
    productos[1]["stock"]= 0
    
    descontinuar_productos()
    
    lista_nombres_final= [producto["nombre"] for producto in productos]
    if "pantalon talle 38" in lista_nombres_final:
        errores.append("si existe pantalon talle 38 en lista final(no se borro)")
    assert not errores, "errores encontrados: {}".format("".join(errores)) 
    
#TEST 8. DEVOLVER EL VALOR DE LAS VENTAS DEL DIA

def test_ventas_del_dia_con_1_venta_de_pantalon_talle_38_y_una_remera_talle_s_da_12500():
    lista_de_2_productos_con_stock()
    realizar_compra(100,1)
    realizar_compra(200,1)
    assert valor_ventas_del_dia() ==  12500
    
#TEST 9. DEVOLVER LAS VENTAS DEL ANIO

def test_ventas_del_anio_me_devuelve_el_valor_total_con_2_ventas_del_mismo_anio():
    lista_de_2_productos_con_stock()
    realizar_compra(200,1)
    realizar_compra(100,1)
    assert ventas_del_anio() == 12500
    
def test_ventas_anio_me_devuele_valor_total_con_2_ventas_de_distinto_anio_remera_talle_s_valor_4500():
    lista_de_2_productos_con_stock()
    realizar_compra(100,1)
    ventas.append({"producto":"pelota","monto":500,"anio":2023})
    assert ventas_del_anio() == 4500
        
#TEST 10. DEVUELVE UNA LISTA CON LOS PRODUCTOS QUE MAS APARECIERON EN VENTAS
    
def test_remera_talle_s_aparece_3_veces_y_pantalon_talle_38_aparece_1_vez():
    lista_de_2_productos_con_stock()
    realizar_compra(100,1)
    realizar_compra(100,1)
    realizar_compra(100,1)
    realizar_compra(200,1)
    assert len(productos_mas_vendidos(2)) == 2

#TEST 11. ACTUALIZAR LOS PRECIOS POR CATEGORIA

def test_actualizar_todos_los_precios_de_una_categoria_remera():
    reiniciar_lista_productos()
    registrar_producto(remera_talle_s)
    remera_talle_s["stock"] = 0
    registrar_producto(remera_talle_m)
    remera_talle_m["stock"] = 0
    registrar_producto(remera_talle_l)
    remera_talle_l["stock"] = 0
    actualizar_precios_por_categoria("remera",50)
    assert productos[0]["precio"] == 6750 and productos[1]["precio"] == 7125 and productos[2]["precio"] == 7500