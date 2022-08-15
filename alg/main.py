from random import randint, uniform, choice
import random
from os import environ

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from pandas import read_csv
from sys import argv
from data import read_file
from NN import neuron
from warnings import simplefilter

simplefilter("ignore")

file = argv[-1]
X_train, y_train, dataset = read_file(file)
model = neuron(X_train, y_train)

crops_data = read_csv("data/crops_codes.csv", ";")
effects_data = read_csv("data/effects.csv", ";")
crops_siv = read_csv("data/crops.csv", ";")
years_data = read_csv("data/years.csv", ";")

effects = dict()
for index, row in effects_data.iterrows():
    effects[row['культура']] = [row['1'], row['2'], row['3'], row['4']]

crops = dict()
for index, row in crops_data.iterrows():
    crops[row['код']] = row['культура']

years = dict()
for index, row in years_data.iterrows():
    years[row['культура']] = row['рік']

dataset_readable = []
for i in range(10):
    dataset_readable.append([])
    for j in range(len(dataset[i])):
        dataset_readable[-1].append(crops[dataset[i][j]])


def fitness_function(chromosomes):
    row = [0] * 12
    for i in chromosomes:
        row[i - 1] = row[i - 1] + 1

    y = model.predict([row])
    data_readable = [crops[i] for i in chromosomes]
    all_coef = []
    for i in range(len(data_readable)):
        coef = crops_siv[crops_siv["культура"] == data_readable[i]][crops_siv["попередник"] == dataset_readable[0][i]]
        coef = coef["доцільність"].to_numpy()[0]
        coef = effects[data_readable[i]][coef - 1]
        for j in range(years[data_readable[i]]):
            if dataset_readable[j][i] == data_readable[i]:
                coef = 0.3
        all_coef.append(coef)
    mean_coef = sum(all_coef) / len(all_coef)
    return y[0][0] * mean_coef


def create_element(minimum, maximum):
    return [random.randint(minimum, maximum) for _ in range(0, 10)]


def create_start_population(minimum, maximum, size):
    return [create_element(minimum, maximum) for i in range(size)]


def calculate_fitness(population, fitness):
    return [fitness(population[i]) for i in range(len(population))]


def change_population(old_population):
    result = []
    for i in range(len(old_population) // 2):
        result.append(old_population[i])
        result.append(old_population[i])

    return result


def binary_encode(element):
    return '{0:04b}'.format(element)


def binary_decode(binary):
    return int(binary, 2)


def flip(c):
    return '1' if (c == '0') else '0'


def population_binary_encode(population):
    return [binary_encode(population[i][0]) + binary_encode(population[i][1]) + binary_encode(
        population[i][2]) + binary_encode(population[i][3]) + binary_encode(population[i][4]) + binary_encode(
        population[i][5]) + binary_encode(population[i][6]) + binary_encode(population[i][7]) + binary_encode(
        population[i][8]) + binary_encode(population[i][9]) for i in range(len(population))]


def population_binary_decode(bin_population):
    return [[binary_decode(bin_population[i][:len(bin_population[i]) // 2]),
             binary_decode(bin_population[i][len(bin_population[i]) // 2:])] for i in range(len(bin_population))]


def fix_value(x):
    if x > 12:
        x = 12
    elif x < 1:
        x = 1
    return x


def crossover_parents(length):
    set1 = set(range(0, length))
    set2 = set(range(0, length))
    parent1 = []
    parent2 = []
    for i in range(length):
        choice1 = choice(tuple(set1))
        choice2 = choice(tuple(set2))

        while choice2 == choice1 and len(set1) != 1:
            choice2 = choice(tuple(set2))

        parent1.append(choice1)
        parent2.append(choice2)
        set1.remove(parent1[i])
        set2.remove(parent2[i])

    return parent1, parent2


def pair_crossover(first, second, fitness):
    index = randint(2, len(first) - 3)
    i = 0
    c1, c2 = first[:index] + second[index:], second[:index] + first[index:]
    x1 = []
    x2 = []
    while i < 40:
        x11 = binary_decode(c1[i:i + 4])
        x22 = binary_decode(c2[i:i + 4])
        x11 = fix_value(x11)
        x22 = fix_value(x22)
        x1.append(x11)
        x2.append(x22)
        i = i + 4
    if fitness(x1) > fitness(x2):
        return c1
    else:
        return c2


def crossover(parents, population, fitness):
    result = []
    parent1, parent2 = parents
    for i in range(len(parent1)):
        result.append(pair_crossover(population[parent1[i]], population[parent2[i]], fitness))

    return result


def mutation(population, p_m):
    result = []
    for i in range(len(population)):
        element = population[i]
        if uniform(0, 1) < p_m:
            index = randint(0, len(element) - 1)
            element = element[:index] + flip(element[index]) + element[index + 1:]

            new_element = []
            is_changed = 0
            i = 0
            while i < 40:
                new_element.append(element[i:i + 4])
                i = i + 4

            for i, el in enumerate(new_element):
                if el == '1111' or el == '1110' or el == '1101':
                    new_element[i] = '1100'
                    is_changed = 1
                elif el == '0000':
                    new_element[i] = '0001'
                    is_changed = 1

            if is_changed == 1:
                new_element_str = ''
                for el in new_element:
                    new_element_str += el
                element = new_element_str

        result.append(element)

    return result


def return_population(population):
    i = 0
    x1 = []
    while i < 40:
        x11 = binary_decode(population[i:i + 4])
        x11 = fix_value(x11)
        x1.append(x11)
        i = i + 4
    return x1


def create_population(population, num):
    return [return_population(population[i]) for i in range(num)]


def sort_tuple(p_tuple):
    p_tuple = sorted(p_tuple, key=lambda item: item[1], reverse=True)
    return p_tuple


def optimization(p_count, min_value, max_value, fitness, p_m, size):
    population = create_start_population(min_value, max_value, p_count)

    for i in range(5):
        fitness_value = calculate_fitness(population, fitness)
        population_tuple = [(population[i], fitness_value[i]) for i in range(len(population))]
        population_tuple = sort_tuple(population_tuple)
        for idx, item in enumerate(population_tuple):
            element, fitness_v = item
            population[idx] = element
            fitness_value[idx] = fitness_v
        population = population_binary_encode(population)
        parents = crossover_parents(len(population))
        population = crossover(parents, population, fitness)
        population = mutation(population, p_m)
        population = create_population(population, size)
        fitness_value = calculate_fitness(population, fitness)
    fitness_value.reverse()
    res = population[-1]
    res.append(int(fitness_value[len(fitness_value) - 1]))
    return res


def calculate_result():
    p_count = 50
    min_value = 1
    max_value = 12
    p_m = 0.1
    size = 10

    res = optimization(p_count, min_value, max_value, fitness_function, p_m, size)

    for i in range(len(res) - 1):
        res[i] = crops[res[i]]

    s = ""
    for i in res:
        s += str(i) + ","
    print()
    return s[:-1]


print(calculate_result())
