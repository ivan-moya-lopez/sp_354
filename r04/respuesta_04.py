import random
from deap import base, creator, tools,algorithms

# Tabla de distancias
tabla_distancias = [[0, 7, 9, 8, 20],
                    [7, 0, 10, 4, 11],
                    [9, 10, 0, 15, 5],
                    [8, 4, 15, 0, 17],
                    [20, 11, 5, 17, 0]]

ciudades = ['A', 'B', 'C', 'D', 'E']

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

    pop_size = 10
    num_generaciones = 5
    num_mejores_recorridos = 15

    pop = toolbox.population(n=pop_size)

    mejores_recorridos = []
    for gen in range(num_generaciones):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        fitnesses = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = (fit,)
        pop = toolbox.select(offspring + pop, k=pop_size)

        mejores_recorridos = tools.selBest(pop, k=num_mejores_recorridos)
        print("Generación:", gen + 1)
        print("Mejor recorrido:", mejores_recorridos[0])
        print("Distancia óptima:", mejores_recorridos[0].fitness.values[0])
        print("-----")

    # Guardar los 15 mejores recorridos en un archivo CSV
    with open('mejores_recorridos.csv', 'w') as f:
        f.write('Camino,Distancia\n')
        for recorrido in mejores_recorridos:
            distancia = recorrido.fitness.values[0]
            camino = ' , '.join([ciudades[i] for i in recorrido])
            f.write(f'{camino},{distancia}\n')


# Llamada a la función principal
if __name__ == "__main__":
    main()
