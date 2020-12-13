from sys import stdin, argv, maxsize
from math import sin, log10, sqrt
from random import sample, uniform, gauss, randint
import matplotlib.pyplot as plt


def genetic_algorithm(f_id, population_size, k, mutation_probability, f_evaluation_max, binary=False, explicit=[-maxsize, maxsize], p=0, eps=1e-6, print_step=False):
    f = f_id
    #Calculate the number of bits for binary format
    n = int(log10(abs(1 + (explicit[1] - explicit[0]) * pow(10, p))) / log10(2)) + 1

    #Create a population of size population_size
    x = get_population_bin(f.get_dimension(), population_size, n) if binary else get_population_float(f.get_dimension(), population_size, explicit)
    #Evaluate F(X) for each individual
    f_eval = [f.calc(bin_to_float(xi, n, explicit[0], explicit[1])) if binary else f.calc(xi) for xi in x] 
    #Define the worst and best individual
    f_worst = max(f_eval)
    f_best = min(f_eval)
    #Calculate fitness value for each individual
    fitness = [get_fitness(f_eval_i, explicit, f_worst, f_best) for f_eval_i in f_eval]

    new_best_change = True
    best_individual_index = fitness.index(max(fitness))

    #Main loop
    #Stop if the number of iterations exceedes f_evaluation_max or the destination function is smaller than eps
    while f.get_count() < f_evaluation_max and f_eval[fitness.index(max(fitness))] > eps:
        
        if print_step and new_best_change:
            print("F_evalutions: %6d | The best individual: %-140s | F(x): %10f" % (f.get_count(), str(x[best_individual_index]), f_eval[best_individual_index]))

        #Tournament elimination using k individuals
        tournament_selection_indexes = tournament_selection(population_size, k)
        individual_index = remove_individual(fitness, tournament_selection_indexes)
        tournament_selection_indexes.remove(individual_index)
        cross_x = tournament_selection_indexes
        for cross in cross_x:
            if fitness[cross] > fitness[cross_x[0]]:
                cross_x[1] = cross_x[0]
                cross_x[0] = cross
            elif fitness[cross] > fitness[cross_x[1]]:
                cross_x[1] = cross

        #Do a crossover and a mutation using two individuals from the tournament selection
        if binary:
            new_individual = mutation_bin(crossover_bin(x[cross_x[0]], x[cross_x[1]]), mutation_probability, n)
        else:
            new_individual = mutation_float(crossover_float(x[cross_x[0]], x[cross_x[1]]), mutation_probability, explicit)

        #Place the new individual into the population and calculate F(x) and fitness
        x[individual_index] = new_individual
        f_eval[individual_index] = f.calc(bin_to_float(new_individual, n, explicit[0], explicit[1]) if binary else new_individual)
        fitness[individual_index] = get_fitness(f_eval[individual_index], explicit, f_worst, f_best)

        if fitness[individual_index] > fitness[best_individual_index]:
            new_best_change = True
            best_individual_index = individual_index
        else:
            new_best_change = False
    
    return x[best_individual_index], f_eval[best_individual_index]

def get_population_float(dimension, population_size, explicit):
    return [[uniform(explicit[0], explicit[1]) for d in range(dimension)] for p in range(population_size)]

def get_population_bin(dimension, population_size, n):
    return [[[randint(0,1) for b in range(n)] for d in range(dimension)] for p in range(population_size)]

def bin_to_float(x, n, dg, gg):
    t = [int(''.join(map(str,xi)), 2) / (2 ** n - 1) for xi in x]
    return [dg + ti * (gg - dg) for ti in t]

def get_fitness(f_eval, explicit, f_worst, f_best):
    delta_f = f_best - f_worst
    return explicit[0] + (explicit[1] - explicit[0]) * (f_eval - f_worst) / delta_f

def tournament_selection(population_size, k):
    return sample(range(population_size), k)

def remove_individual(fitness, tournament_selection_indexes):
    remove_index = tournament_selection_indexes[0]
    for i in tournament_selection_indexes:
        if fitness[i] < fitness[remove_index]:
            remove_index = i
    return remove_index

def crossover_bin(x1, x2):
    rand_chromosome = [[randint(0,1) for i in range(len(xi1))] for xi1 in x1]
    return [[a & b | r & (a ^ b) for a, b, r in zip(xi1, xi2, rci)] for xi1, xi2, rci in zip(x1, x2, rand_chromosome)]

def crossover_float(x1, x2):
    a = uniform(0,1)
    return [a * xi1 + (1 - a) * xi2 for xi1, xi2 in zip(x1, x2)]

def mutation_bin(x, probability, n):
    x_mut = []
    for j in range(len(x)):
        mutation_indexes = sample(range(n), int(n * probability))
        x_mut.append([x[j][i] ^ 1 if i in mutation_indexes else x[j][i] for i in range(n)])
    return x_mut

def mutation_float(x, probability, explicit):
    x_mut = []
    for j in range(len(x)):
        if uniform(0,1) > probability:
            x_mut_tmp = gauss(x[j], abs(explicit[1] - explicit[0]) / 4)
            x_mut_tmp = explicit[0] if x_mut_tmp < explicit[0] else x_mut_tmp
            x_mut_tmp = explicit[1] if x_mut_tmp > explicit[1] else x_mut_tmp
            x_mut.append(x_mut_tmp)
        else:
            x_mut.append(x[j])

    return x_mut

class Function:
    identity = 0
    count = 0 
    dimension = 1

    def __init__(self, identity, dimension):
        self.identity = identity
        self.count = 0
        self.dimension = dimension

    def raise_count(self):
        self.count += 1

    def get_id(self):
        return self.identity

    def get_count(self):
        return self.count

    def reduce_count(self, substract):
        self.count -= substract

    def get_dimension(self):
        return self.dimension

    def f1(self, x):
        return 100 * (x[1] - x[0] * x[0]) ** 2 + (1 - x[0]) ** 2

    def f3(self, x):
        total_sum = 0
        for xi, i in enumerate(x, start=1):
            total_sum += (xi - i) ** 2

        return total_sum

    def f6(self, x):
        quadratic_sum = sum([xi * xi for xi in x])
        numerator = sin(sqrt(quadratic_sum)) ** 2 - 0.5
        denominator = (1 + 0.001 * quadratic_sum) ** 2

        return 0.5 + numerator / denominator

    def f7(self, x):
        quadratic_sum = sum([xi * xi for xi in x])
        return pow(quadratic_sum, 0.25) * (1 + sin(50 * pow(quadratic_sum, 0.1)) ** 2)

    def calc(self, x):
        self.raise_count()
        if self.identity == 1:
            return self.f1(x)
        elif self.identity == 3:
            return self.f3(x)
        elif self.identity == 6:
            return self.f6(x)
        elif self.identity == 7:
            return self.f7(x)

def first():
    f_id = [Function(1, 2), Function(3, 5), Function(6, 2), Function(7, 2)]
    explicit = [-50, 150]
    
    for i in range(4):
        data = [[],[]]
        for binary in [False, True]:
            print("%s representation" % ("Binary" if binary else "Float")) 
            for j in range(20):
                x_min, f = genetic_algorithm(f_id[i], 100, 3, 0.1, 10000, binary=binary, explicit=explicit, p=3, print_step=False)
                if binary:
                    data[1].append(f)
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (f_id[i].get_id(), str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), f, f_id[i].get_count()))
                else:
                    data[0].append(f)
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (f_id[i].get_id(), str(x_min), f, f_id[i].get_count()))

                f_id[i].reduce_count(f_id[i].get_count())
                #zad = stdin.readline().strip()
        fig1, ax1 = plt.subplots()
        plt.suptitle("Function %d" % (f_id[i].get_id()))
        x_names = ["Float", "Binary"]
        plt.boxplot(data, labels=x_names)
        plt.ylabel("F(X)")
        plt.xlabel("Data representation")
        #plt.savefig("task1_function%d.png" % (f_id[i].get_id()))
        plt.show() 

def second():
    f_id = [6, 7]
    dimension = [1, 3, 6, 10]
    explicit = [-50, 150]
    for fi in f_id:
        data = [[], [], [], []]
        i = 0
        for d in dimension:
            
            for binary in [False, True]:
                print("%s representation" % ("Binary" if binary else "Float")) 
                for j in range(10):
                    f = Function(fi,d)
                    x_min, fx = genetic_algorithm(f, 100, 3, 0.1, 10000, binary=binary, explicit=explicit, p=3, print_step=False)
                    data[i].append(fx)
                    if binary:
                        print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                            % (fi, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                    else:
                        print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                            % (fi, str(x_min), fx, f.get_count()))
                    #zad = stdin.readline().strip()
            i += 1

        fig1, ax1 = plt.subplots()
        ax1.set_title("Function %d" % (fi))
        ax1.boxplot(data, labels=dimension)
        plt.ylabel("F(X)")
        plt.xlabel("Dimensions")
        #plt.savefig("task2_function%d.png" % (fi))
        plt.show() 


def third():
    f_id = [6, 7]
    dimension = [3, 6]
    explicit = [-50, 150]
    for fi in f_id:
        i = 0
        for d in dimension:
            data = [[], []]
            for binary in [False, True]:
                print("%s representation" % ("Binary" if binary else "Float")) 
                for j in range(5):
                    f = Function(fi,d)
                    x_min, fx = genetic_algorithm(f, 100, 3, 0.1, 100000, binary=binary, explicit=explicit, p=4, print_step=False)
                    if binary:
                        data[1].append(fx)
                        print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                            % (fi, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                    else:
                        data[0].append(fx)
                        print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                            % (fi, str(x_min), fx, f.get_count()))
                    #zad = stdin.readline().strip()

            fig1, ax1 = plt.subplots()
            x_names = ["Float", "Binary"]
            ax1.set_title("Function %d, Dimension %d" % (fi, d))
            plt.boxplot(data, labels=x_names)
            plt.xlabel("Data representation")
            plt.ylabel("F(X)")
            #plt.savefig("task3_function%d_dimension%d.png" % (fi, d))
            plt.show() 

def fourth():
    f = Function(6,4)
    populations = [30, 50, 100, 200]
    mutations = [0.1, 0.3, 0.6, 0.9]
    max_iterations = [100, 1000, 10000, 100000]
    explicit = [-50, 150]

    data = [[],[]]
    for max_iteration in max_iterations:
        print("Max iterations: %d" % (max_iteration))
        for j in range(10):
            for binary in [False, True]:
                x_min, fx = genetic_algorithm(f, 100, 3, 0.1, max_iteration, binary=binary, explicit=explicit, p=4, print_step=False)
                if binary:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                else:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(x_min), fx, f.get_count()))
                data[0].append(max_iteration)
                data[1].append(fx)
                f.reduce_count(f.get_count())

    max_index = 0
    for i in range(len(data[0])):
        if data[1][i] < data[1][max_index]:
            max_index = i

    iterations = data[0][max_index]
    print("Best max iterations %d" % (iterations))

    data = [[],[]]
    for population in populations:
        print("Population: %d" % (population))
        for j in range(10):
            for binary in [False, True]:
                x_min, fx = genetic_algorithm(f, population, 3, 0.1, iterations, binary=binary, explicit=explicit, p=4, print_step=False)
                if binary:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                else:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(x_min), fx, f.get_count()))
                data[0].append(population)
                data[1].append(fx)
                f.reduce_count(f.get_count())

    max_index = 0
    for i in range(len(data[0])):
        if data[1][i] < data[1][max_index]:
            max_index = i

    population = data[0][max_index]
    print("Best population size: %d" % (population))
    data = [[],[], [], []]

    i = 0
    for mutation in mutations:
        print("Mutation probability: %f" % (mutation))
        for j in range(10):
            for binary in [False, True]:
                x_min, fx = genetic_algorithm(f, population, 3, mutation, iterations, binary=binary, explicit=explicit, p=4, print_step=False)
                if binary:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                else:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(x_min), fx, f.get_count()))
                data[i].append(fx)
                f.reduce_count(f.get_count())
        i += 1


    fig1, ax1 = plt.subplots()
    ax1.set_title("Function 6, population %d, iterations %d" % (population, iterations))
    plt.ylabel("F(X)")
    plt.xlabel("Mutation probability")
    plt.boxplot(data, labels=mutations)
    plt.savefig("task4.png")
    #plt.show() 



def fifth():
    f = Function(6, 4)
    tournament_pool = [3, 6, 9, 15, 20, 30]
    explicit = [-50, 150]
    data = [[], [], [], [], [], []]
    i = 0
    for pool in tournament_pool:
        print("Pool size: %d" % (pool))
        for binary in [False, True]:
            print("%s representation" % ("Binary" if binary else "Float")) 
            for j in range(10):
                x_min, fx = genetic_algorithm(f, 100, pool, 0.1, 100000, binary=binary, explicit=explicit, p=4, print_step=False)
                data[i].append(fx)
                if binary:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(bin_to_float(x_min, len(x_min[0]), explicit[0], explicit[1])), fx, f.get_count()))
                else:
                    print("Function: %d | Xmin: %-130s | F(X)=%10.6f | f_count = %4d"  
                        % (6, str(x_min), fx, f.get_count()))
                f.reduce_count(f.get_count())
        i += 1

    fig1, ax1 = plt.subplots()
    ax1.set_title("Function %d" % (6))
    plt.ylabel("F(X)")
    plt.xlabel("Tournament pool size")
    plt.boxplot(data, labels=tournament_pool)
    plt.savefig("task5.png")
    #plt.show() 


#while True:
#    print("Choose between assignment 1-5 or 0 for exit.")
#    zad = stdin.readline().strip()
zad = argv[1].strip()

if zad == '1':
    first()
elif zad == '2':
    second()
elif zad == '3':
    third()
elif zad == '4':
    fourth()
elif zad == '5':
    fifth()
else:
    exit(0)
