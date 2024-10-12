
with open("METRO_MADRID_2.txt", "r") as file:
    lineas = file.readlines()  

diccionario = {}  # Diccionario para almacenar las conexiones entre estaciones

# Procesa cada línea del archivo
for linea in lineas:
    if linea.startswith("LINEA"):
        nombre_linea = linea.strip()
        diccionario[nombre_linea] = {}  # Crea un nuevo diccionario para la LINEA de metro

    elif linea.startswith("ESTACIONES:"):
        estaciones = linea.split(":")[1].strip().split(",")
        nombre_estaciones = [estacion.strip() for estacion in estaciones]  #Para cada ESTACION

    elif linea.startswith("DISTANCIA:"):
        nombre_linea = linea.strip()
        distancia_espacio = linea.split(":")[1].strip().split(",")     #Para cada DISTANCIA ENTRE ESTACIONES
        for distancia in distancia_espacio:
            try:
                estaciones, distancia_valor = distancia.split("=")
                estacion1, estacion2 = estaciones.strip().split("-")
                distancia_valor = int(distancia_valor.strip())
                diccionario.setdefault(estacion1, {}).update({estacion2: distancia_valor})
                diccionario.setdefault(estacion2, {}).update({estacion1: distancia_valor})
            except ValueError:
                pass

estacion_inicial = ""
while estacion_inicial not in diccionario:
    estacion_inicial = input("Ingrese la estacion inicio: ").strip()
    if estacion_inicial not in diccionario:
        print("Estación no válida. Por favor, inténtelo de nuevo.")


estacion_destino = ""
while estacion_destino not in diccionario:
    estacion_destino = input("Ingrese la estación de destino: ").strip()  #Se introduce la estacion destino
    if estacion_destino not in diccionario:
        print("Estación no válida. Por favor, inténtelo de nuevo.")






#BELLMAN FORD



distancias = {nodo: float('inf') for nodo in diccionario}
distancias[estacion_inicial] = 0
ruta_mas_corta = {}

estaciones_desconocidas = set(diccionario)


while estaciones_desconocidas:
    estacion_actual = min(estaciones_desconocidas, key=lambda nodo: distancias[nodo])
    estaciones_desconocidas.remove(estacion_actual)

    for sig_estacion, dist_estacion in diccionario[estacion_actual].items():
        if dist_estacion + distancias[estacion_actual] < distancias[sig_estacion]:
            distancias[sig_estacion] = dist_estacion + distancias[estacion_actual]
            ruta_mas_corta[sig_estacion] = estacion_actual

#     Reconstruye el trayecto de  la linea mas corta
ruta_corta = []
distancia_corta = 0

while estacion_destino:
    ruta_corta.insert(0, estacion_destino)
    estacion_destino = ruta_mas_corta.get(estacion_destino)
    if estacion_destino:
        distancia_corta += diccionario[ruta_corta[0]][estacion_destino]

# Muestra la ruta más corta y la distancia total recorrida
if ruta_corta:
    print("La ruta más corta es:", ruta_corta)
    print("La distancia total es:", distancia_corta, "metros")
else:
    print("No se encontró una ruta válida.")
