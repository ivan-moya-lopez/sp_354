import random
import csv
from deap import base, creator, tools, algorithms


# Lectura de la tabla de distancias desde un archivo CSV
def leer_tabla_distancias(nombre_archivo):
    tabla_distancias = []
    with open(nombre_archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            fila_distancias = [int(distancia) for distancia in fila]
            tabla_distancias.append(fila_distancias)
    return tabla_distancias


ciudades = ['A', 'B', 'C', 'D', 'E']
tabla_distancias = leer_tabla_distancias('tabla_distancias.csv')

# Configuración de DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(ciudades)), len(ciudades))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", lambda ind: sum(tabla_distancias[i][j] for i, j in zip(ind, ind[1:])))
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    random.seed(42)

    pop_size = 100
    num_generaciones = 500

    pop = toolbox.population(n=pop_size)

    for gen in range(num_generaciones):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        fitnesses = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = (fit,)
        pop = toolbox.select(offspring + pop, k=pop_size)

    # Obtener el mejor recorrido
    mejor_recorrido = tools.selBest(pop, k=1)[0]
    distancia_optima = mejor_recorrido.fitness.values[0]

    # Mostrar el camino óptimo sin repeticiones
    camino_optimo = ' -> '.join([ciudades[i] for i in mejor_recorrido])
    print("Camino óptimo:", camino_optimo)
    print("Distancia óptima:", distancia_optima)


# Llamada a la función principal
if __name__ == "__main__":
    main()