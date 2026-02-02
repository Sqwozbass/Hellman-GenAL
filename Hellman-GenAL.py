import random
from random import randint
from time import time
import subprocess
import multiprocessing
from itertools import product
"""
Алгорим Меркля-Хелмана Версия 4/ Алгорим создания рандомного ключа и последовательности (createKey_random).
Генетический алгоритм одно, двухточечный кросс, мутация одного-двух бит по очереди.
Сброс с мутацией лучшей особи по проценту mutation_rate_check. 
Оставление лучшей особи или рандомной при сбросе. Распараллеливание ver new6.
Добавлен выбор использования генерации классической популяции или прогрессивной
Уходим от букв в пользу битовой последовательности. Добавлен "поломаный" алгоритм Меркла, доработана расшифровка."
"""

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

#Модули для Алгоритма Меркла-Хеллмана
def createSuperincreasingSequence(n):
    sequence = [1]
    for _ in range(n-1):
        sequence.append(sum(sequence) + randint(1, 100))
    return sequence

def convertToBinary(string):
    binary = []
    for word in string:
        temp = []
        for char in word:
            temp.append("".join(format(ord(b), '08b') for b in char))

        binary.append(temp)
    return binary

def convertToString(binaryString):
    string = []
    for word in binaryString:
        temp = ""
        for char in word:
            temp += (chr(int(char, 2)))
        string.append(temp)
    return string

def formatMessage(message, type):
    string = ""
    if type == "binary":
        for word in message:
            wordTemp = ""
            for char in word:
                wordTemp += str(char)
            string = "{} {}".format(string, wordTemp).strip()
    elif type == "string":
        for word in message:
            string = "{} {}".format(string, word).strip()
    return string

def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
def is_prime(n):
    """Проверяет, является ли число простым (перебор делителей)."""
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

def generate_prime(start):
    """Генерирует случайное простое число больше start."""
    while True:
        candidate = start + randint(1, 100)
        if is_prime(candidate):
            return candidate

def gcd(a, b):
    while b:
        a, b = b, a % b  # Алгоритм Евклида
    return a

def createKey(n):
    sequence = createSuperincreasingSequence(n)  # супервозрастающая последовательность
    publicKey = []
    randInt1 = generate_prime(sum(sequence))

    while True:
        randInt2 = randint(1, randInt1)  #r
        if gcd(randInt1, randInt2) == 1:
            break
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2


def createKey_2(n, special_index):

    sequence = createSuperincreasingSequence_2(n, special_index)  # супервозрастающая последовательность
    publicKey = []
    randInt1 = generate_prime(sum(sequence))

    while True:
        randInt2 = randint(1, randInt1)  #r
        if gcd(randInt1, randInt2) == 1:
            break
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2

def createSuperincreasingSequence_2(n, special_index):
    sequence = [1]
    count = 0

    for _ in range(n - 1):
        last_app = sequence[-1]

        if count == special_index-2:
            #print(f'count: {count}, special_index: {special_index}')
            candidate = -1
            while candidate in sequence:
                candidate -= 1
            sequence.append(candidate)

        else:
            sequence.append(sum(sequence) + randint(1, 100))
        count += 1

    return sequence

def encrypt(bit_sequence, publicKey):
    print("==============ШИФРОВАНИЕ==============")
    if len(bit_sequence) != len(publicKey):
        raise ValueError("Длина битовой последовательности должна совпадать с длиной открытого ключа.")

    result = 0
    for i, bit in enumerate(bit_sequence):
        print(f"bit[{i}]: {bit} * publicKey[{i}]: {publicKey[i]} = {int(bit) * publicKey[i]}")
        result += int(bit) * publicKey[i]

    return result

def decrypt(encrypted_sum, sequence, randInt1, randInt2):
    print("==============РАСШИФРОВКА==============")
    inverse = modInverse(randInt2, randInt1)
    print(f"Обратный ключ (modular inverse): {inverse}")

    moduled = (encrypted_sum * inverse) % randInt1
    print(f"Значение после обратного преобразования: {moduled}")

    decrypted_bits = []

    # Перебираем последовательность в обратном порядке
    for i in reversed(sequence):
        print(sequence, max(sequence))
        s = max(sequence)
        sequence.remove(s)
        if moduled >= s:
            decrypted_bits.append(1)
            moduled -= s
        else:
            decrypted_bits.append(0)

    # Последовательность восстановлена в обратном порядке
    decrypted_bits.reverse()

    return decrypted_bits


#Модули для модифицированной модели Голдберга
#Вычисление разницы
def fitness(solution, b, C):
    return abs(C - sum([solution[i] * b[i] for i in range(len(b))]))

#Мутация с процентом вероятности для одного бита
def mutate(solution, mutation_rate,Test, b=None, C=None):
    mutated = solution.copy()

    # Случайно решаем, будет ли мутация происходить
    if random.random() <= mutation_rate:
        if Test == 0:
        # Выбираем один случайный индекс для мутации
            mutation_index = random.randint(0, len(mutated) - 1)

            # Флип бита
            mutated[mutation_index] = 1 - mutated[mutation_index]
        else:
            mutation_index = random.randint(0, len(mutated) - 1)

            # Флип бита
            mutated[mutation_index] = 1 - mutated[mutation_index]
            mutation_index = random.randint(0, len(mutated) - 1)

            # Флип бита
            mutated[mutation_index] = 1 - mutated[mutation_index]

        # print(f"\nДо мутации: {solution} с fitness {fitness(solution, b, C)}")
        # print(f"После мутации: {mutated} с fitness {fitness(mutated, b, C)}")
        # print(f"Мутация произошла в индексе: {mutation_index}\n")

    return mutated

#Мутация с процентом вероятности для всех битов
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
    # print(f"Количество мутаций: {mutation_count}\n")
    return mutated

#Одноточечный кроссовер
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

#Двухточечный кроссовер
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

def genetic_algorithm(b, C, pop_size=1000, generations=100000, mutation_rate=1,mutation_rate_check=0.6, gen_check=500, crossover_func=None, flag_ver = None, gen_ver = None):
    #print(f"Идеальное с fitness {fitness(a, b, C)}")
    n = len(b)

    if gen_ver is None:
        # Шаг 1: начальная генерация
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
    else:
        # Шаг 1: начальная генерация
        population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
        # Шаг 2: сортировка по фитнесу (чем меньше — тем лучше)
        population = sorted(population, key=lambda x: fitness(x, b, C))

        # Шаг 3: отбор лучших 50%
        survivors = population[:pop_size // 2]

        # Шаг 4: генерация новых особей до заполнения популяции
        worst_fitness = fitness(survivors[-1], b, C)
        while len(survivors) < pop_size:
            candidate = random.choices([0, 1], k=n)
            candidate_fitness = fitness(candidate, b, C)
            if candidate_fitness < worst_fitness:
                survivors.append(candidate)
                # обновляем худший фитнес в текущей популяции
                survivors = sorted(survivors, key=lambda x: fitness(x, b, C))
                worst_fitness = fitness(survivors[-1], b, C)
        population = survivors

    # print("Изначальная популяция:")
    # for i in population:
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

        if gen % 3000 == 0:
            print(f"\nПоколение {gen}:")
            print("Популяция:")
            for individual in population[:8]:
                print(f"{individual} с fitness {fitness(individual, b, C)}")

        best = population[0]
        # print(f"\nПоколение {gen+1}: Лучшее решение {best} с fitness {fitness(best, b, C)}")
        if fitness(best, b, C) == 0:
            print(f"\nТочное решение найдено: {best}")
            return best, gen + 1
    best = min(population, key=lambda x: fitness(x, b, C))
    print(f"\nЛучшее приближенное решение: {best} с fitness {fitness(best, b, C)}")
    return best, generations

def convertToString2(binaryList):
    # Объединяем список битов в одну строку
    binaryString = "".join(map(str, binaryList))
    # Разбиваем строку на блоки по 8 бит (по 1 байту)
    bytes_list = [binaryString[i:i + 8] for i in range(0, len(binaryString), 8)]
    # Конвертируем каждый байт в символ
    string = "".join(chr(int(byte, 2)) for byte in bytes_list)
    return string

# Перемещаем функцию run_test в глобальную область видимости
def run_test(mutation_rate, mutation_rate_check, gen_check, crossover_method, publicKey, encrypted_result, flag_ver,gen_ver, output_file):
    start_time = time()
    print(
        f"\nТест: crossover={crossover_method.__name__}, mutation_rate={mutation_rate}, mutation_rate_check={mutation_rate_check}, gen_check={gen_check}")

    best_solution, generations = genetic_algorithm(
        publicKey, encrypted_result,
        mutation_rate=mutation_rate,
        mutation_rate_check=mutation_rate_check,
        gen_check=gen_check,
        crossover_func=crossover_method,
        flag_ver=flag_ver,
        gen_ver = gen_ver
    )

    end_time = time()
    execution_time = end_time - start_time
    fitness_value = fitness(best_solution, publicKey, encrypted_result)

    result = {
        "crossover_method": crossover_method.__name__,
        "mutation_rate": mutation_rate,
        "mutation_rate_check": mutation_rate_check,
        "gen_check": gen_check,
        "generations": generations,
        "time": execution_time,
        "fitness": fitness_value,
        "best_solution": best_solution
    }

    print(f"Результат: Поколения={generations}, Время={execution_time:.4f} сек, Fitness={fitness_value}")

    # Записываем в файл с использованием блокировки
    with open(output_file, "a") as f:
        f.write(str(result) + "\n")
        f.flush()  # Принудительно записываем в файл (чтобы не ждать закрытия)

    return result  # Возвращаем результат для дальнейшей обработки

def test_genetic_algorithm(test_cases, crossover_methods, output_file="ver8.2.1_test28b_1700.txt", num_runs=None):
    start_program_time = time()

    results = []
    flag_input = input("Для запуска турниного отбора с сохранением лучшей особи при перезапуске нажмите enter\n"
                       "Для запуска турниного отбора без сохранения лучшей особи при перезапуске введите любой символ: ")
    gen_input = input(
        "\nДля запуска работы с классической популяцией нажмите enter\n"
        "Для запуска работы с прогрессивной популяцией введите любой символ: ")

    flag_ver = None if flag_input.strip() == "" else flag_input
    gen_ver = None if gen_input.strip() == "" else gen_input

    # Создаём пул процессов для параллельного выполнения тестов
    with multiprocessing.Pool(processes=4) as pool:
        # Создаём список всех тестов, которые нужно запустить
        test_params = []
        for mutation_rate, mutation_rate_check, gen_check in test_cases:
            for crossover_method in crossover_methods:
                for _ in range(num_runs):
                    test_params.append((mutation_rate, mutation_rate_check, gen_check, crossover_method, publicKey, encrypted_result, flag_ver, gen_ver, output_file))

        # Запуск тестов в параллельных процессах
        results = pool.starmap(run_test, test_params)

    end_program_time = time()
    total_program_time = end_program_time - start_program_time

    print(f"\nРезультаты сохранены в {output_file}")
    print(f"Общее время работы программы: {total_program_time:.4f} сек")



if __name__ == "__main__":
    print("\nПрограмма запущена. Выберите желаемое действие ↓↓↓\n")
    while True:
        print("\nКодирование подмножества символов - 1\n"
              "Получение результата с помощью алгоритма Меркля-Хелмана - 2\n"
              "Получение результата с помощью модифицированной модели Голдберга - 3\n"
              "Запуск тестирования с различными начальными данными - 4\n"
              "Отображение тестовых данных - 5\n"
              "Завершение работы программы - 6\n")

        inputs = input("\nВведите номер выбранного действия: ")
        if inputs == "1":

            flag_ver_encrypt = input("Для запуска кодирования подмножества символов рандомным алгоритмом нажмите enter\n"
                               "Для запуска кодирования подмножества символов алгоритмом Меркла-Хелмана введите любой символ: ")
            flag_ver_encrypt = None if flag_ver_encrypt.strip() == "" else flag_ver_encrypt

            if flag_ver_encrypt is None:
                bit_input = input("Введите битовую последовательность через пробел (например: 0 1 1 0 ...): ")
                bit_sequence = list(map(int, bit_input.strip().split()))
                sequence, publicKey, randInt1, randInt2 = createKey_2(len(bit_sequence), 4)  # Не менее 3-го индекса
                print('\n\nCупервозрастающая последовательность:', sequence)
                print("q:", randInt1)
                print("r:", randInt2)
                print("Открытый ключ:", publicKey)
                # Шифруем
                encrypted_result = encrypt(bit_sequence, publicKey)
                print(f"\nЗашифрованная сумма: {encrypted_result}")

                check_encrypted_result_uniqueness(publicKey, encrypted_result)
            else:
                # Ввод битовой последовательности от пользователя
                bit_input = input("Введите битовую последовательность через пробел (например: 0 1 1 0 ...): ")
                bit_sequence = list(map(int, bit_input.strip().split()))
                # Проверка на корректность битов
                if any(bit not in (0, 1) for bit in bit_sequence):
                    raise ValueError("Допустимы только биты 0 и 1.")
                # Генерация ключей
                sequence, publicKey, randInt1, randInt2 = createKey(len(bit_sequence))
                print('Cупервозрастающая последовательность:', sequence)
                print("q:", randInt1)
                print("r:", randInt2)
                print("Открытый ключ:", publicKey)
                # Шифруем
                encrypted_result = encrypt(bit_sequence, publicKey)
                print(f"\nЗашифрованная сумма: {encrypted_result}")

                #check_encrypted_result_uniqueness(publicKey, encrypted_result)

        if inputs == "2":
            if 'encrypted_result' in locals() and 'sequence' in locals() and 'randInt1' in locals() and 'randInt2' in locals():
                print("\nПолучение результатов с помощью алгоритма Меркля-Хеллмана запущено..")
                decrypted = decrypt(encrypted_result, sequence, randInt1, randInt2)
                print("\nРасшифрованная битовая последовательность:", decrypted)
            else:
                print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1 для алгоритма Меркла-хеллмана.")

        if inputs == "3":
            #encrypted = int(input("Введите зашифрованное слово:"))  # 3889444981
            # publicKey = [148486, 8018244, 19600152, 35636640, 69788420, 139873812, 283162802, 63890371, 130453490, 262094868, 30663663, 66821308, 119981904, 250357828, 6447153, 4282118, 9752124, 23513370, 43314590, 94053480, 186325128, 374729060, 246874401, 491669998]
            # # a = [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]
            # a = 0 0 1 1 0 0 0 0 0 1 0 1 0 1 1 1 0 0 1 1 0 0 0 1 0 1 1 1
            # encrypted_result = 1247256687

            if 'encrypted_result' in locals() and 'publicKey' in locals():
                encrypted = int(encrypted_result)
                # print(encrypted)
                result = []
                p = []
                p.append(encrypted)
                result.append(p)
                decoded_messages = []
                gener = []

                flag_input = input("Для запуска турниного отбора с сохранением лучшей особи при перезапуске нажмите enter\n"
                                   "Для запуска турниного отбора без сохранения лучшей особи при перезапуске введите любой символ: ")
                funk_input = input(
                    "\nДля запуска модели с одноточечным кроссовером нажмите enter\n"
                    "Для запуска  модели с двухточечным кроссовером введите любой символ: ")
                gen_input = input(
                    "\nДля запуска работы с классической популяцией нажмите enter\n"
                    "Для запуска работы с прогрессивной популяцией введите любой символ: ")
                flag_ver = None if flag_input.strip() == "" else flag_input
                funk_ver = crossover_one if funk_input.strip() == "" else crossover_two
                gen_ver = None if gen_input.strip() == "" else gen_input
                # Используем ГА для расшифровки
                start = time()
                for word in result:
                    for char in word:
                        solution, gen = genetic_algorithm(publicKey, char, crossover_func = funk_ver, flag_ver = flag_ver,gen_ver=gen_ver)
                        print("Преобразованная сумма:", sum([solution[i] * publicKey[i] for i in range(len(publicKey))]))

                        stringMessage = convertToString2(solution)
                        print("\nРасшифрованное сообщение \"{}\"".format(formatMessage(stringMessage, "string")))
                        # Форматируем и добавляем расшифрованное сообщение в список
                        decoded_message = formatMessage(stringMessage, "string")
                        decoded_messages.append(decoded_message)
                        gener.append(gen)

                # Выводим все расшифрованные сообщения в конце
                end = time()
                result_time = end-start
                print("Время работы", str(result_time)[:7])
            else:
                print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1.")

        if inputs == "4":
            # publicKey = [306105, 26325030, 43160805, 96423075, 187642365, 358448955, 101888743, 217552211, 411534337, 215406027, 434791419, 221208226, 459558332, 295842662, 585257119, 535608246, 447636385, 284549073, 554099001, 488903365, 347798418, 72016729, 164236388, 309188161]
            # # # a = [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]
            # encrypted_result = 2834565234

            if 'encrypted_result' in locals() and 'publicKey' in locals():
                # Тестовые параметры
                mutation_test_cases = [
                    # (1, 0.4, 250),
                    # (1, 0.4, 500),
                    # (1, 0.4, 1000),
                    # (1, 0.6, 250),
                    (1, 0.6, 250),
                    # (1, 0.6, 1000),
                    # (1, 0.5, 250),
                    # (1, 0.5, 500),
                    # (1, 0.5, 1000)
                ]

                # mutation_test_cases = [
                #     # (1, 0.4, 250),
                #     # (1, 0.4, 500),
                #     # (1, 0.4, 1000),
                #     # (1, 0.6, 250),
                #     (1, 0.6, 100
                #     # (1, 0.5, 500),
                #     # (1, 0.5, 1000)
                # ]

                # Разные кроссоверы
                crossover_variants = [
                    crossover_one,
                    #crossover_two,
                    # crossover_three
                ]
                # Запуск тестов
                count_tests = int(input("Введите число тестирований для каждого набора данных:"))
                test_genetic_algorithm(mutation_test_cases, crossover_variants, num_runs=count_tests)
            else:
                print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1.")
        if inputs == "5":
            subprocess.run(["C:/Users/Soundhugs/AppData/Local/Programs/Python/Python312/python.exe", "Tab_Gr_result.py"])
        if inputs == "6":
            exit()