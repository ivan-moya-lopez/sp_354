import numpy as np
import random
import pandas as pd

# Tabla de distancias
tabla_distancias = np.array([[0, 7, 9, 8, 20],
                             [7, 0, 10, 4, 11],
                             [9, 10, 0, 15, 5],
                             [8, 4, 15, 0, 17],
                             [20, 11, 5, 17, 0]])

ciudades = ['A', 'B', 'C', 'D', 'E']

# Parámetros del algoritmo genético
tamano_poblacion = 10
num_generaciones = 50
num_mejores_recorridos = 15

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

    for _ in range(num_generaciones):
        nueva_poblacion = cruzar_poblacion(mejores_recorridos)
        mejores_recorridos = seleccionar_mejores_recorridos(nueva_poblacion)
        poblacion = nueva_poblacion

    mejor_recorrido = min(mejores_recorridos, key=lambda x: evaluar_recorrido(x))
    distancia_optima = evaluar_recorrido(mejor_recorrido)

    # Mostrar el camino óptimo sin repeticiones
    camino_optimo = ' -> '.join(mejor_recorrido)
    print("Camino óptimo:", camino_optimo)
    print("Distancia óptima:", distancia_optima)

    # Guardar los 15 mejores recorridos en un archivo CSV
    df = pd.DataFrame(mejores_recorridos, columns=ciudades)
    df.to_csv('mejores_recorridos.csv', index=False)

# Llamada a la función principal
main()
