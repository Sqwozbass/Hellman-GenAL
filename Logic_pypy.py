import sys
import random
from random import randint
from time import time
from itertools import product
import json
import multiprocessing
from multiprocessing import Pool, Manager

#функция для проверки единственности решения
def check_encrypted_result_uniqueness(publicKey, encrypted_result):
    matches = []
    for bits in product([0, 1], repeat=len(publicKey)):
        result = sum(p * b for p, b in zip(publicKey, bits))
        if result == encrypted_result:
            matches.append(bits)
    if len(matches) == 0:
        print(f"❌ encrypted_result = {encrypted_result} не может быть получен с этим открытым ключом.")
    elif len(matches) == 1:
        print(f"✅ Однозначное соответствие для encrypted_result = {encrypted_result}.")
        print("Бинарное сообщение:", matches[0])
    else:
        print(f"❗ Коллизия! {len(matches)} бинарных векторов дают encrypted_result = {encrypted_result}:")
        for m in matches:
            print("   ", m)
    return matches

#функиця для формирования уловий задачи о ранце модифицированным алгоритмом Меркла-Хеллмана
def createKey_mod(n, special_index):
    sequence = createSuperincreasingSequence_mod(n, special_index)
    publicKey = []
    randInt1 = generate_prime(sum(sequence)) #q
    while True:
        randInt2 = randint(1, randInt1)  #r
        if gcd(randInt1, randInt2) == 1:
            break
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2

#функиця для формирования модифицированной супервозрастающей последовательности
def createSuperincreasingSequence_mod(n, special_index):
    sequence = [1]
    count = 0
    for _ in range(n - 1):
        if count == special_index-2:

            candidate = -1 # Другие варианты в 9.1_autorun
            while candidate in sequence:
                candidate -= 1
            sequence.append(candidate)
        else:
            sequence.append(sum(sequence) + randint(1, 100))
        count += 1
    return sequence

#функиця для формирования уловий задачи о ранце алгоритмом Меркла-Хеллмана
def createKey(n):
    sequence = createSuperincreasingSequence(n)
    publicKey = []
    randInt1 = generate_prime(sum(sequence))

    while True:
        randInt2 = randint(1, randInt1)
        if gcd(randInt1, randInt2) == 1:
            break
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2

#функиця для формирования модифицированной супервозрастающей последовательности
def createSuperincreasingSequence(n):
    sequence = [1]
    for _ in range(n-1):
        sequence.append(sum(sequence) + randint(1, 100))
    return sequence

#функция для создания зашифрованного сообщения задачи о ранце
def encrypt(bit_sequence, publicKey):
    print("==============ШИФРОВАНИЕ==============")
    if len(bit_sequence) != len(publicKey):
        raise ValueError("Длина битовой последовательности должна совпадать с длиной открытого ключа.")
    result = 0
    for i, bit in enumerate(bit_sequence):
        print(f"bit[{i}]: {bit} * publicKey[{i}]: {publicKey[i]} = {int(bit) * publicKey[i]}")
        result += int(bit) * publicKey[i]
    return result

#функция для решения задачи о ранце алгоритмом Меркла-Хеллмана
def decrypt(encrypted_sum, sequence, randInt1, randInt2):
    print("==============РАСШИФРОВКА==============")
    inverse = modInverse(randInt2, randInt1)
    print(f"Обратный ключ (modular inverse): {inverse}")
    moduled = (encrypted_sum * inverse) % randInt1
    print(f"Значение после обратного преобразования: {moduled}")
    decrypted_bits = []
    # Перебираем последовательность в обратном порядке
    for i in reversed(sequence):
        s = max(sequence)
        sequence.remove(s)
        if moduled >= s:
            decrypted_bits.append(1)
            moduled -= s
        else:
            decrypted_bits.append(0)
    decrypted_bits.reverse()
    return decrypted_bits

#функция для высчитывания числа мультипликативно обратного r
def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x

#функция для генерации случайного простого числа больше start.
def generate_prime(start):
    while True:
        candidate = start + randint(1, 100)
        if is_prime(candidate):
            return candidate

#функция для проверки, является ли число простым (перебор делителей).
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

#функция реализующая алгоритм Евклида для поиска взаимно простого числа r с q
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#функция реализующая одноточечный кроссовер
def crossover_one(parent1, parent2, b, C):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    # print(f"Родители:")
    # print(f"{parent1} (Родитель 1) с fitness {fitness(parent1, b, C)}")
    # print(f"{parent2} (Родитель 2) с fitness {fitness(parent2, b, C)}")
    # print(f"Точка кроссовера: {point}")
    # print(f"Дети до мутации:")
    # print(f"{child1} (Ребёнок 1) с fitness {fitness(child1, b, C)}")
    # print(f"{child2} (Ребёнок 2) с fitness {fitness(child2, b, C)}")
    return child1, child2

#функция реализующая Двухточечный кроссовер
def crossover_two(parent1, parent2, b, C):
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)

    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    # print(f"Родители:")
    # print(f"{parent1} (Родитель 1) с fitness {fitness(parent1, b, C)}")
    # print(f"{parent2} (Родитель 2) с fitness {fitness(parent2, b, C)}")
    # print(f"Точки кроссовера: {point1}, {point2}")
    # print(f"Дети до мутации:")
    # print(f"{child1} (Ребёнок 1) с fitness {fitness(child1, b, C)}")
    # print(f"{child2} (Ребёнок 2) с fitness {fitness(child2, b, C)}")
    return child1, child2

#функция реализующая вычисление приближения
def fitness(solution, b, C):
    return abs(C - sum([solution[i] * b[i] for i in range(len(b))]))

#функция реализующая мутациюя с процентом вероятности
def mutate(solution, mutation_rate,Test, b=None, C=None):
    mutated = solution.copy()
    if random.random() <= mutation_rate:
        if Test == 0:
            # Выбираем один случайный индекс для мутации
            mutation_index = random.randint(0, len(mutated) - 1)
            # Флип бита
            mutated[mutation_index] = 1 - mutated[mutation_index]
        else:
            mutation_index = random.randint(0, len(mutated) - 1)
            mutated[mutation_index] = 1 - mutated[mutation_index]
            mutation_index = random.randint(0, len(mutated) - 1)
            mutated[mutation_index] = 1 - mutated[mutation_index]
        # print(f"\nДо мутации: {solution} с fitness {fitness(solution, b, C)}")
        # print(f"После мутации: {mutated} с fitness {fitness(mutated, b, C)}")
        # print(f"Мутация произошла в индексе: {mutation_index}\n")
    return mutated

#функция реализующая мутацию с процентом вероятности при эвристике 1
def mutate_check(solution, mutation_rate, b=None, C=None):
    mutated = solution.copy()
    mutation_count = 0  # Счётчик мутаций
    # print(f"\nДо мутации: {mutated} с fitness {fitness(mutated, b, C)}")
    mutation_indexes = list(range(len(mutated)))
    random.shuffle(mutation_indexes)
    mutated[mutation_indexes[0]] = 1 - mutated[mutation_indexes[0]]  # Гарантируем хотя бы одну мутацию
    mutation_count += 1
    for i in mutation_indexes[1:]:
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]  # Флип бита
            mutation_count += 1  # Увеличиваем счётчик мутаций
    # print(f"После мутации: {mutated} с fitness {fitness(mutated, b, C)}")
    return mutated

#функция реализующая модифицированную модель Голдберга
def genetic_algorithm(b, C, pop_size, generations, mutation_rate,mutation_rate_check, gen_check, crossover_func=None, flag_ver = None, gen_ver = None):
    n = len(b)
    if gen_ver == "Классическая":
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
    else:
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
        population = sorted(population, key=lambda x: fitness(x, b, C))
        survivors = population[:pop_size // 4]
        worst_fitness = fitness(survivors[-1], b, C)
        while len(survivors) < pop_size:
            candidate = random.choices([0, 1], k=n)
            candidate_fitness = fitness(candidate, b, C)
            if candidate_fitness < worst_fitness:
                survivors.append(candidate)
                survivors = sorted(survivors, key=lambda x: fitness(x, b, C))
                worst_fitness = fitness(survivors[-1], b, C)
        population = survivors

    # print("Начальная популяция:")
    # for i in population:
    #
    #     print(f"{i} с fitness {fitness(i, b, C)}")

    for gen in range(generations):
        new_population = []
        TEST = (gen + 1) % 2
        if flag_ver is None:
            # Лучшая особь и её мутации
            if (gen + 1) % gen_check == 0:
                best = min(population, key=lambda x: fitness(x, b, C))
                new_population.append(best)
                for _ in range(pop_size - 1):
                    mutated = mutate_check(best, mutation_rate_check,b,C)
                    new_population.append(mutated)
                    #print(f"\nПосле {gen+1} поколений: Лучшее решение {best} с fitness {fitness(best, b, C)}")
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i+1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)

                    child1 = mutate(child1, mutation_rate,TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]
        elif flag_ver == "∞":
            for i in range(len(population)):
                parent1 = population[i]
                parent2 = random.choice(population[:i] + population[i+1:])
                child1, child2 = crossover_func(parent1, parent2, b, C)

                child1 = mutate(child1, mutation_rate,TEST, b, C)
                child2 = mutate(child2, mutation_rate, TEST, b, C)
                best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]
        else:
            # Вместо выбора лучшей особи создаем новую случайную популяцию
            if (gen + 1) % gen_check == 0:
                new_population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
                #print(f"\nПосле {gen + 1} поколений: Сгенерирована новая случайная популяция")
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i + 1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)
                    child1 = mutate(child1, mutation_rate, TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]

        # if gen != 0 and gen % 100 == 0:
        #     print(f"\nПоколение {gen}:")
        #     print("Популяция:")
        #     for individual in population[:8]:
        #         print(f"{individual} с fitness {fitness(individual, b, C)}")

        best = population[0]
        # print(f"\nПоколение {gen+1}: Лучшее решение {best} с fitness {fitness(best, b, C)}")
        if fitness(best, b, C) == 0:
            print(f"\nТочное решение найдено: {best}")
            return best, gen + 1
    best = min(population, key=lambda x: fitness(x, b, C))
    print(f"\nЛучшее приближенное решение: {best} с fitness {fitness(best, b, C)}")
    return best, generations

#функция реализующая процесс тестирования модели Голдберга
def run_test(pop_size, generations,mutation_rate, mutation_rate_check, gen_check, crossover_method, publicKey, encrypted_result, flag_ver,gen_ver, save_file, multi):
    start_time = time()
    print(
        f"\nТест: crossover={crossover_method.__name__}, mutation_rate={mutation_rate}, mutation_rate_check={mutation_rate_check}, gen_check={gen_check}")

    if multi != "":
        best_solution, generations = genetic_algorithm(
            publicKey, encrypted_result,
            pop_size, generations,
            mutation_rate=mutation_rate,
            mutation_rate_check=mutation_rate_check,
            gen_check=gen_check,
            crossover_func=crossover_method,
            flag_ver=flag_ver,
            gen_ver=gen_ver
        )
    else:
        best_solution, generations = algoritm_parallel(
            publicKey, int(encrypted_result),
            int(pop_size), float(mutation_rate),
            mutation_rate_check,
            gen_check,
            crossover_method, flag_ver, gen_ver,
            generations, num_processes=4
        )

    if flag_ver == "∞":
        gen_check = "-"
    end_time = time()
    execution_time = end_time - start_time
    fitness_value = fitness(best_solution, publicKey, encrypted_result)
    result = {
        "crossover_method": crossover_method.__name__,
        "mutation_rate": mutation_rate,
        "mutation_rate_check": mutation_rate_check,
        "gen_check": gen_check,
        "gen_version": gen_ver,
        "generations": generations,
        "time": execution_time,
        "fitness": fitness_value,
        "best_solution": best_solution
    }
    print(f"Результат: Поколения={generations}, Время={execution_time:.4f} сек, Fitness={fitness_value}")
    if save_file is None:
        pass
    else:
        filename = save_file + ".txt"
        with open(filename, "a") as f:
            f.write(str(result) + "\n")
            f.flush()  # Принудительно записываем в файл
    return result

#функция реализующая распараллеленное или однопоточное тестировнаие модели
def test_genetic_algorithm(pop_size, generations,publicKey, encrypted_result, flag_ver, gen_ver, test_cases, crossover_methods, save_file,multi, num_runs=None):
    try:
        start_program_time = time()
        results = []
        test_params = []
        for mutation_rate, mutation_rate_check, gen_check in test_cases:
            if flag_ver is not None:
                mutation_rate_check = "-"
            for crossover_method in crossover_methods:
                for _ in range(num_runs):
                    test_params.append((
                        pop_size, generations, mutation_rate,
                        mutation_rate_check, gen_check,
                        crossover_method, publicKey, encrypted_result,
                        flag_ver, gen_ver, save_file
                    ))

        if multi != "":
            # --- Последовательный запуск
            for params in test_params:
                result = run_test(*params,multi)
                results.append(result)
        else:
            # --- Параллельный запуск
            for params in test_params:
                result = run_test(*params,multi)
                results.append(result)

        end_program_time = time()
        total_program_time = end_program_time - start_program_time
        if save_file is None:
            pass
        else:
            print(f"\nРезультаты сохранены в {save_file}.txt")
        print(f"Общее время работы программы: {total_program_time:.4f} сек")
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return

#функция реализующая запуск распараллеленной модифицированной модели Голдберга
def algoritm_parallel(b, C, pop_size, mutation_rate, mutation_rate_check,
                      gen_check, crossover_func, flag_ver,gen_ver, generations, num_processes=4):

    n = len(b)
    if gen_ver == "Классическая":
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
    else:
        # Прогрессивная генерация
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
        population = sorted(population, key=lambda x: fitness(x, b, C))
        survivors = population[:pop_size // 4]
        worst_fitness = fitness(survivors[-1], b, C)
        while len(survivors) < pop_size:
            candidate = random.choices([0, 1], k=n)
            candidate_fitness = fitness(candidate, b, C)
            if candidate_fitness < worst_fitness:
                survivors.append(candidate)
                survivors = sorted(survivors, key=lambda x: fitness(x, b, C))
                worst_fitness = fitness(survivors[-1], b, C)
        population = survivors

    k, m = divmod(pop_size, num_processes)
    population_chunks = [
        population[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
        for i in range(num_processes)
    ]

    manager = Manager()
    stop_flag = manager.Event()
    result_holder = manager.list()

    args_list = [
        (chunk, b, C, generations, mutation_rate, mutation_rate_check, gen_check,
         crossover_func, flag_ver, stop_flag, result_holder)
        for chunk in population_chunks
    ]

    with Pool(processes=num_processes) as pool:
        tasks = [pool.apply_async(run_genetic_subprocess, args=args) for args in args_list]

        # Ждём завершения хотя бы одного процесса с решением
        for task in tasks:
            task.wait()  # блокируем пока один не завершится
            if stop_flag.is_set():
                break

        # Завершаем пул, даже если кто-то ещё работает
        pool.terminate()
        pool.join()

    if result_holder:
        best, gen = result_holder[0]
        print(f"\nТочное решение найдено в одном из процессов: {best}")
        return best, gen
    else:
        print("\nТочное решение не найдено.")
        try:
            bests = [task.get() for task in tasks if task.ready()]
            if bests:
                best = min(bests, key=lambda x: fitness(x[0], b, C))
                print(f"\nЛучшее приближенное решение: {best[0]} с fitness {fitness(best[0], b, C)}")
                return best
        except:
            pass
        return None, None

#функция реализующая распараллеленную версию модифицированной модели Голдберга
def run_genetic_subprocess(population_chunk, b, C, generations, mutation_rate, mutation_rate_check, gen_check,
                           crossover_func, flag_ver, stop_flag, result_holder):
    pop_size = len(population_chunk)
    n = len(b)
    population = population_chunk.copy()

    for gen in range(generations):
        if gen + 1 % gen_check == 0 and stop_flag.is_set():
            return None
        new_population = []
        TEST = (gen + 1) % 2
        if flag_ver is None:
            if (gen + 1) % gen_check == 0:
                best = min(population, key=lambda x: fitness(x, b, C))
                new_population.append(best)
                for _ in range(pop_size - 1):
                    mutated = mutate_check(best, mutation_rate_check, b, C)
                    new_population.append(mutated)
                    # print(f"\nПосле {gen+1} поколений: Лучшее решение {best} с fitness {fitness(best, b, C)}")
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i + 1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)

                    child1 = mutate(child1, mutation_rate, TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]
        elif flag_ver == "∞":
            for i in range(len(population)):
                parent1 = population[i]
                parent2 = random.choice(population[:i] + population[i + 1:])
                child1, child2 = crossover_func(parent1, parent2, b, C)

                child1 = mutate(child1, mutation_rate, TEST, b, C)
                child2 = mutate(child2, mutation_rate, TEST, b, C)
                best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]
        else:
            if (gen + 1) % gen_check == 0:
                new_population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
                # print(f"\nПосле {gen + 1} поколений: Сгенерирована новая случайная популяция")
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i + 1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)
                    child1 = mutate(child1, mutation_rate, TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    new_population.append(best)
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]

        # if gen % 3000 == 0:
        #     print(f"\nПоколение {gen}:")
        #     print("Популяция:")
        #     for individual in population[:8]:
        #         print(f"{individual} с fitness {fitness(individual, b, C)}")

        best = population[0]
        if fitness(best, b, C) == 0:
            stop_flag.set()
            result_holder.append((best, gen + 1))
            return best, gen + 1

    best = min(population, key=lambda x: fitness(x, b, C))
    return best, generations

#функция реализующая создание условий задачи (по кнопке)
def encrypt_qui(flag_ver_encrypt, bit_input):
    flag_ver_encrypt = None if flag_ver_encrypt.strip() == "" else flag_ver_encrypt
    if flag_ver_encrypt is None:
        bit_sequence = list(map(int, bit_input.strip().split()))
        sequence, publicKey, randInt1, randInt2 = createKey_mod(len(bit_sequence), 4)  # Не менее 3-го индекса
        print('Создание условий NP-полной задачи о ранце')
        print('\nCупервозрастающая последовательность:', sequence)
        print("q:", randInt1)
        print("r:", randInt2)
        print("Открытый ключ:", publicKey)
        encrypted_result = encrypt(bit_sequence, publicKey)
        print(f"\nЗашифрованная сумма: {encrypted_result}")
        check_encrypted_result_uniqueness(publicKey, encrypted_result)
    else:
        bit_sequence = list(map(int, bit_input.strip().split()))
        sequence, publicKey, randInt1, randInt2 = createKey(len(bit_sequence))
        print('Создание условий обычной задачи о ранце')
        print('\nCупервозрастающая последовательность:', sequence)
        print("q:", randInt1)
        print("r:", randInt2)
        print("Открытый ключ:", publicKey)
        encrypted_result = encrypt(bit_sequence, publicKey)
        print(f"\nЗашифрованная сумма: {encrypted_result}")
        #check_encrypted_result_uniqueness(publicKey, encrypted_result)

    # Сохранение результатов в json
    data = {
        "bit_input": bit_input,
        "encrypted_result": encrypted_result,
        "publicKey": publicKey,
        "sequence": sequence,
        "randInt1": randInt1,
        "randInt2": randInt2
    }
    with open("temp_data.json", "w") as f:
        json.dump(data, f)

#функция реализующая решение задачи о ранце алгоритмом Меркла-Хеллмана (по кнопке)
def decrypt_qui():
    with open("temp_data.json", "r") as f:
        data = json.load(f)
    encrypted_result = data["encrypted_result"]
    sequence = data["sequence"]
    randInt1 = data["randInt1"]
    randInt2 = data["randInt2"]
    if 'encrypted_result' in locals() and 'sequence' in locals() and 'randInt1' in locals() and 'randInt2' in locals():
        print("\nПолучение результатов с помощью алгоритма Меркля-Хеллмана запущено..")
        decrypted = decrypt(encrypted_result, sequence, randInt1, randInt2)
        print("\nРасшифрованная битовая последовательность:", decrypted)
    else:
        print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1 для алгоритма Меркла-хеллмана.")

#функция реализующая решение задачи о ранце модифицированной моделью Голдберга
def decrypt_al_qui(flag_input,funk_input,gen_input, pop_size, generations, mutation_rate, mutation_rate_check, gen_check,multi):
    with open("temp_data.json", "r") as f:
        data = json.load(f)
    encrypted_result = data["encrypted_result"]
    publicKey = data["publicKey"]

    if 'encrypted_result' in locals() and 'publicKey' in locals():
        encrypted = int(encrypted_result)
        result = []
        p = []
        p.append(encrypted)
        result.append(p)

        flag_ver = None if flag_input.strip() == "" else \
            "∞" if flag_input.strip() == "∞" else flag_input
        funk_ver = crossover_one if funk_input.strip() == "" else crossover_two
        gen_ver = "Классическая" if gen_input.strip() == "" else gen_input
        # Используем ГА для расшифровки
        if multi != "":
            print("Запуск решения задачи модифицированной моделью Голдберга\n")
            start = time()
            for word in result:
                for char in word:
                    solution, gen = genetic_algorithm(publicKey, char, int(pop_size), int(generations), float(mutation_rate),float(mutation_rate_check), int(gen_check), crossover_func=funk_ver, flag_ver=flag_ver,
                                                      gen_ver=gen_ver)
                    print("Преобразованная сумма:", sum([solution[i] * publicKey[i] for i in range(len(publicKey))]))
        else:
            print("Запуск решения задачи модифицированной моделью Голдберга с применением распараллеливания\n")
            start = time()
            solution, gen = algoritm_parallel(
                publicKey,
                int(encrypted_result),
                int(pop_size),
                float(mutation_rate),
                float(mutation_rate_check),
                int(gen_check),
                crossover_func=funk_ver,
                flag_ver=flag_ver,
                gen_ver=gen_ver,
                generations=int(generations),
                num_processes=4,
            )
            print("Преобразованная сумма:", sum([solution[i] * publicKey[i] for i in range(len(publicKey))]))

        end = time()
        result_time = end - start
        print(f"\nРезультат получен на {gen} поколении.")
        print("Время работы", str(result_time)[:7])
    else:
        print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные.")

#функция реализующая тестирование решения задачи о ранце алгоритмом Меркла-Хеллмана (по кнопке)
def decrypt_test_al_qui(flag_input,gen_input, count_tests, pop_size, generations, config_file_path, save_file, multi):
    with open("temp_data.json", "r") as f:
        data = json.load(f)
    encrypted_result = data["encrypted_result"]
    publicKey = data["publicKey"]
    if 'encrypted_result' in locals() and 'publicKey' in locals():
        try:
            with open(config_file_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            mutation_test_cases = config["mutation_test_cases"]
            crossover_variants_names = config["crossover_variants"]
            # Преобразуем имена функций в реальные объекты
            func_map = {
                "crossover_one": crossover_one,
                "crossover_two": crossover_two,
            }
            crossover_variants = [func_map[name] for name in crossover_variants_names if name in func_map]
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return

        flag_ver = None if flag_input.strip() == "" else \
            "∞" if flag_input.strip() == "∞"else flag_input
        gen_ver = "Классическая" if gen_input.strip() == "" else "Прогрессивная"
        save_file = None if save_file == "" else save_file
        # Запуск тестов
        test_genetic_algorithm(int(pop_size), int(generations), publicKey, encrypted_result, flag_ver, gen_ver, mutation_test_cases, crossover_variants,save_file, multi,num_runs=int(count_tests))
    else:
        print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1.")

if __name__ == "__main__":
    command = sys.argv[1]  # имя функции
    args = sys.argv[2:]    # аргументы
    if command == "encrypt_qui":
        encrypt_qui(*args)
    elif command == "decrypt_qui":
        decrypt_qui()
    elif command == "decrypt_al_qui":
        decrypt_al_qui(*args)
    elif command == "decrypt_test_al_qui":
        decrypt_test_al_qui(*args)
    else:
        print("Неизвестная команда")