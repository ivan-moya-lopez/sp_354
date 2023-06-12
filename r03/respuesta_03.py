import random
import csv

# Leer la tabla de distancias desde un archivo CSV
def leer_tabla_distancias(nombre_archivo):
    tabla_distancias = []
    with open(nombre_archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            fila_distancias = [int(distancia) for distancia in fila]
            tabla_distancias.append(fila_distancias)
    return tabla_distancias


# Parámetros del algoritmo genético
tamano_poblacion = 10
num_generaciones = 50
num_mejores_recorridos = 15


ciudades = ['A', 'B', 'C', 'D', 'E']

tabla_distancias = leer_tabla_distancias('./r03/tabla_distancias.csv')

# Función para evaluar un recorrido
def evaluar_recorrido(individual):
    distancia_total = 0
    for i in range(len(individual) - 1):
        origen = ciudades.index(individual[i])
        destino = ciudades.index(individual[i + 1])
        distancia_total += tabla_distancias[origen][destino]
    return distancia_total


# Función para generar la población inicial
def generar_poblacion_inicial():
    poblacion = []
    for _ in range(tamano_poblacion):
        recorrido = random.sample(ciudades, len(ciudades))
        poblacion.append(recorrido)
    return poblacion


# Función para seleccionar los mejores recorridos de la población
def seleccionar_mejores_recorridos(poblacion):
    mejores_recorridos = sorted(poblacion, key=lambda x: evaluar_recorrido(x))[:num_mejores_recorridos]
    return mejores_recorridos


# Función para cruzar dos recorridos
def cruzar_recorridos(padre1, padre2):
    punto_cruce = random.randint(0, len(padre1) - 1)
    hijo = padre1[:punto_cruce]
    for ciudad in padre2:
        if ciudad not in hijo:
            hijo.append(ciudad)
    return hijo


# Función para cruzar la población
def cruzar_poblacion(mejores_recorridos):
    nueva_poblacion = mejores_recorridos.copy()
    while len(nueva_poblacion) < tamano_poblacion:
        padre1 = random.choice(mejores_recorridos)
        padre2 = random.choice(mejores_recorridos)
        hijo = cruzar_recorridos(padre1, padre2)
        nueva_poblacion.append(hijo)
    return nueva_poblacion


# Función principal para ejecutar el algoritmo genético
def main():
    random.seed(42)
    poblacion = generar_poblacion_inicial()
    mejores_recorridos = seleccionar_mejores_recorridos(poblacion)

    for i in range(num_generaciones):
        nueva_poblacion = cruzar_poblacion(mejores_recorridos)
        mejores_recorridos = seleccionar_mejores_recorridos(nueva_poblacion)
        poblacion = nueva_poblacion

    mejor_recorrido = min(mejores_recorridos, key=lambda x: evaluar_recorrido(x))
    distancia_optima = evaluar_recorrido(mejor_recorrido)

    # Mostrar el camino óptimo sin repeticiones
    camino_optimo = ' -> '.join(mejor_recorrido)
    print("Camino óptimo:", camino_optimo)
    print("Distancia óptima:", distancia_optima)


# Llamada a la función principal
main()
