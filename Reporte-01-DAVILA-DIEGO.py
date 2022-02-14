#!/usr/bin/env python
# coding: utf-8

# In[1]:


########################## LOGIN DE ACCESO #########################################
"""
LOGIN acceso reporte_Lifestore
usuario: admin
contra: lif3
"""
acceso_usuario = False
intentos = 0

#mensaje de bienvenida
mensaje_bienvenida = "Buenas tardes! Accede tus credenciales"
print(mensaje_bienvenida)
#Creación Bucle while para ingresar hasta 2 intentos o termina el programa
while not acceso_usuario:
  #ingresar credenciales
  usuario = input('Usuario: ')
  contra = input('Contra: ')
  intentos += 1
  #revisar si credenciales coinciden
  if usuario == 'admin' and contra == 'lif3':
    acceso_usuario = True
    print('Bienvenido', usuario)
  else:
    print('Tienes', 2 - intentos, 'intentos restantes')
    if usuario == 'admin':
      print('Te equivocaste en la contra')
    else:
      print('El usuario: ', usuario, 'no esta registrado')
  if intentos == 2:
    exit()
print("Otra vez estas en Lifestore")

"""
Empezamos con la gestion de datos del departamento de ventas
"""


# In[15]:


from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
#Dividir por meses las ventas que son validas, es decir, == 1 (extrayendo id_sale y date)
id_fecha = [[sale[0], sale[3]] for sale in lifestore_sales if sale[4] == 0]

#Para categorizar utilizamos un diccionario
categorizacion_meses = {}
#definir una variable que contenga id_venta y date
for par in id_fecha:
    # obtener id y mes desde date
    id = par[0]
    _, mes, _ = par[1].split('/')
    # Si el mes aun no existe como llave, la creamos mediante una lista
    if mes not in categorizacion_meses.keys():
        #creamos una lista dentro del diccionario
        categorizacion_meses[mes] = []
    categorizacion_meses[mes].append(id)

for key in categorizacion_meses.keys():
    print(key)
    print(categorizacion_meses[key])


# In[7]:


########################## TOTAL DE INGRESOS MENSUALES Y TICKET PROMEDIO MENSUAL #########################################
#sumar total de ingresos, numero de ventas y ticket promedio mensual
      
for key in categorizacion_meses.keys():
    lista_mes = categorizacion_meses[key]
    suma_venta = 0
    for id_venta in lista_mes:
        indice = id_venta - 1
        info_venta = lifestore_sales[indice]
        id_product = info_venta[1]
        precio = lifestore_products[id_product-1][2]
        suma_venta += precio        
           
    print(f'mes: {key}, total de ingresos mensual: {suma_venta}, ticket promedio mensual: {suma_venta / len(lista_mes)}')


# In[42]:


#Dividir las ventas por año que son validas, es decir, == 1 (extrayendo id_sale y date)
id_fecha = [[sale[0], sale[3]] for sale in lifestore_sales if sale[4] == 0]

#Para categorizar utilizamos un diccionario
categorizacion_anual = {}
#definir una variable que contenga id_venta y date
for par in id_fecha:
    # obtener id y año desde date
    id = par[0]
    _, _, anual = par[1].split('/')
    # Si el año aun no existe como llave, la creamos mediante una lista
    if anual not in categorizacion_anual.keys():
        #creamos una lista dentro del diccionario
        categorizacion_anual[anual] = []
    categorizacion_anual[anual].append(id)

for key in categorizacion_anual.keys():
    print(key)
    print(categorizacion_anual[key])


# In[45]:


########################## INGRESOS Y VENTAS ANUALES #########################################
#sumar numero de ventas y ticket promedio por mes 
for key in categorizacion_anual.keys():
    lista_anual = categorizacion_anual[key]
    suma_venta = 0
    for id_venta in lista_anual:
        indice = id_venta - 1
        info_venta = lifestore_sales[indice]
        id_product = info_venta[1]
        precio = lifestore_products[id_product-1][2]
        ventas = lifestore_products[id_product-1][0]
        suma_venta += precio
    print(f'Año: {key}, ingresos totales: {suma_venta}, ventas anuales: {len(lista_anual)}')


# In[85]:


########################## MESES CON MAS VENTAS AL AÑO #########################################
#sumar numero de ventas y ticket promedio por mes 
for key in categorizacion_meses.keys():
    lista_mes = categorizacion_meses[key]
    suma_venta = 0
    for id_venta in lista_mes:
        indice = id_venta - 1
        info_venta = lifestore_sales[indice]
        id_product = info_venta[1]
        precio = lifestore_products[id_product-1][2]
        ventas = lifestore_products[id_product-1][0]
        suma_venta += precio
    print(f'mes: {key}, ventas: {len(lista_mes)}, ticket promedio mensual: {suma_venta / len(lista_mes)}')


# In[80]:


########################## 5 PRODUCTOS CON LAS MEJORES RESEÑAS #########################################
#Obtener el id_product y score desde lifestore_sales
prod_reviews = {}
for sale in lifestore_sales:
    prod_id = sale[1]
    review = sale[2]
    if prod_id not in prod_reviews.keys():
        prod_reviews[prod_id] = []
    prod_reviews[prod_id].append(review)
id_rev_prom = {}
for id, reviews in prod_reviews.items():
    rev_prom = sum(reviews) / len(reviews)
    rev_prom = int(rev_prom*100)/100
    id_rev_prom[id] = [rev_prom, len(reviews)]
#Ordenarmos el diccionario conviertiendo en lista
dicc_en_list = []
for id, lista in id_rev_prom.items():
    rev_prom = lista[0]
    cant = lista[1]
    sub = [id, rev_prom, cant]
    dicc_en_list.append(sub)
#realizamos dos filtros, primero ordenando ventas en orden descendente y después el promedio del score
dicc_en_list = sorted(dicc_en_list, key=lambda lista:lista[2], reverse=True)
dicc_en_list = sorted(dicc_en_list, key=lambda lista:lista[1], reverse=True)
#for sublista in dicc_en_list:
print('Los 5 productos con mayores ventas y mayor score promedio durante el 2020 son:\n')
for sublista in dicc_en_list[:5]:
    id, rev, num = sublista
    indice_lsp = id - 1
    prod = lifestore_products[indice_lsp]
    nombre = prod[1]
    nombre = nombre.split(' ')
    nombre = ' '.join(nombre[:4])
    print(f'El Producto: "{nombre}", tuvo un score promedio: {rev} y ventas anuales: {num}')


# In[79]:


########################## 5 PRODUCTOS CON LAS PEORES RESEÑAS CONSIDERANDO LOS PRODUCTOS CON DEVOLUCIÓN #########################################
#Dividir las ventas por año que son validas, es decir, == 1 (extrayendo id_sale y date)
id_review = [[sale[1], sale[2]] for sale in lifestore_sales if sale[4] == 1]
#Obtener el id_product y score desde lifestore_sales
prod_reviews = {}
for sale in id_review:
    prod_id = sale[0]
    review = sale[1]
    if prod_id not in prod_reviews.keys():
        prod_reviews[prod_id] = []
    prod_reviews[prod_id].append(review)
id_rev_prom = {}
for id, reviews in prod_reviews.items():
    rev_prom = sum(reviews) / len(reviews)
    rev_prom = int(rev_prom*100)/100
    id_rev_prom[id] = [rev_prom, len(reviews)]
#Ordenarmos el diccionario conviertiendo en lista
dicc_en_list = []
for id, lista in id_rev_prom.items():
    rev_prom = lista[0]
    cant = lista[1]
    sub = [id, rev_prom, cant]
    dicc_en_list.append(sub)
#realizamos dos filtros, primero ordenando ventas en orden descendente y después el promedio del score
dicc_en_list = sorted(dicc_en_list, key=lambda lista:lista[2], reverse=True)
dicc_en_list = sorted(dicc_en_list, key=lambda lista:lista[1], reverse=False)
#for sublista in dicc_en_list:
print('Los 5 productos con peor promedio de reseñas y mayores ventas durante el 2020 son:\n')
for sublista in dicc_en_list[:5]:
    id, rev, num = sublista
    indice_lsp = id - 1
    prod = lifestore_products[indice_lsp]
    nombre = prod[1]
    nombre = nombre.split(' ')
    nombre = ' '.join(nombre[:4])
    print(f'El Producto: "{nombre}", tuvo un score promedio: {rev} y ventas anuales: {num}')

