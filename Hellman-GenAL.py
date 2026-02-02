import random
from random import randint
from time import time
import subprocess
"""
Алгорим Меркля-Хелмана Версия 4
Генетический алгоритм одно,двухточечный кросс, мутация одного бита, сброс с мутацией лучшей особи и процентом. 
оставление лучшей особи или рандомной. Добавлено сравнение количества единиц с точным значением.
"ЭКСПЕРИМЕНТ С TEST мутацией - 1 или 2 бита по очереди, стагнация исправлена.
"""
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
        randInt2 = randint(1, randInt1//1000)  #r
        if gcd(randInt1, randInt2) == 1:
            break
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2


def encrypt(message, publicKey):
    encrypted = []
    ones_count_list = []  # Список для количества единиц в каждом слове
    total_ones = 0  # Общее количество единиц

    print("==============ШИФРОВАНИЕ==============")
    for word in message:
        wordTemp = []
        word_ones = 0  # Количество единиц в текущем слове
        offset = 0  # Смещение для publicKey

        for index, char in enumerate(word):
            print(f"\nОбрабатываем элемент {index}: {char}")
            result = 0
            char_ones = char.count("1")  # Подсчет единиц в char
            word_ones += char_ones  # Добавляем к количеству единиц в слове

            for i, bit in enumerate(char):
                key_index = offset + i  # Используем смещение для publicKey

                if key_index < len(publicKey):  # Проверяем, чтобы не выйти за границы
                    print(f"i: {i}, bit: {bit}, publicKey[{key_index}]: {publicKey[key_index]}")
                    result += int(bit) * publicKey[key_index]
                else:
                    print(f"Пропускаем i={i}, key_index={key_index} (выход за границы)")

            wordTemp.append(result)
            offset += len(char)  # Увеличиваем смещение для следующего символа

        encrypted.append(wordTemp)
        ones_count_list.append(word_ones)  # Сохраняем количество единиц для слова
        total_ones += word_ones  # Добавляем количество единиц из слова к общему счету

    return encrypted, total_ones

def decrypt(message, sequence, randInt1, randInt2):
    inverse = modInverse(randInt2, randInt1)  # Обратный ключ
    print("==============РАСШИФРОВКА==============")
    decrypted = []
    offset = 0  # Смещение для sequence
    n = 1

    for word in message:
        wordTemp = []

        for char in word:
            print("\nОбрабатываем символ:", char)
            moduled = (char * inverse) % randInt1  # Обратное преобразование
            charTemp = ""

            for i in range(8*n-1,offset,-1):
                key_index =  i  # Используем смещение для publicKey
                if key_index < len(sequence):  # Проверка, чтобы не выйти за границы
                    print(f"Индекс {i}, key_index {key_index}: {sequence[key_index]}")
                    if moduled >= sequence[key_index]:
                        moduled -= sequence[key_index]
                        charTemp += '1'
                    else:
                        charTemp += '0'

            wordTemp.append(charTemp[::-1])  # Переворачиваем строку
            offset += 8
            n += 1
        decrypted.append(wordTemp)
        offset += len(word)  # Увеличиваем `offset` для следующего слова
    return decrypted


#Модули для модифицированной модели Голдберга
#Вычисление разницы
def fitness(solution, b, C):
    return abs(C - sum([solution[i] * b[i] for i in range(len(b))]))

#Вычисление разницы в единицах
def unit_difference(solution, exact_ones):
    return abs(exact_ones - sum(solution))

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

def genetic_algorithm(b, C, ones, pop_size=5000, generations=100000, mutation_rate=1,mutation_rate_check=0.6, gen_check=500, crossover_func=None, flag_ver = None):
    #print(f"Идеальное с fitness {fitness(a, b, C)}")
    reset_counter = 0  # Счётчик поколений
    last_best_fitness = float('inf')  # Хранение лучшего fitness

    n = len(b)
    population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
    # print("Изначальная популяция:")
    # for i in population:
    #     print(i)
    for gen in range(generations):
        new_population = []
        TEST = (gen + 1) % 2
        if flag_ver is None:
            # Лучшая особь и её мутации
            if reset_counter >= gen_check-1:
                best = min(population, key=lambda x: fitness(x, b, C))
                new_population.append(best)
                for _ in range(pop_size - 1):
                    mutated = mutate_check(best, mutation_rate_check,b,C)
                    new_population.append(mutated)
                best_ones = sum(best)
                ones_diff = abs(best_ones - ones) if ones is not None else "N/A"
                # print(f"\nПосле {gen+1} поколений: Лучшее решение {best} с fitness {fitness(best, b, C)},ed:{ones_diff}")
                reset_counter = 0  # Сброс счетчика после обновления популяции
                #print("СБРОССССС")
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i+1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)

                    child1 = mutate(child1, mutation_rate,TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    # best_ones = sum(best)
                    # ones_diff = abs(best_ones - ones) if ones is not None else "N/A"
                    # print(f"Выбран лучший: {best} с fitness {fitness(best, b, C)},ed:{ones_diff}\n")
                    new_population.append(best)
                reset_counter += 1  # Увеличиваем счётчик
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]
        else:
            # Вместо выбора лучшей особи создаем новую случайную популяцию
            if reset_counter >= gen_check-1:
                new_population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
                print(f"\nПосле {gen + 1} поколений: Сгенерирована новая случайная популяция")
                reset_counter = 0  # Сброс счетчика после обновления популяции
            else:
                for i in range(len(population)):
                    parent1 = population[i]
                    parent2 = random.choice(population[:i] + population[i + 1:])
                    child1, child2 = crossover_func(parent1, parent2, b, C)
                    child1 = mutate(child1, mutation_rate, TEST, b, C)
                    child2 = mutate(child2, mutation_rate, TEST, b, C)
                    best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                    new_population.append(best)
                reset_counter += 1  # Увеличиваем счётчик
            population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]

        best = population[0]
        current_fitness = fitness(best, b, C)

        if current_fitness < last_best_fitness:
            #print("УЛУЧШИЛОСЬ")
            reset_counter = 0  # Если особь улучшилась, сбрасываем счетчик

        last_best_fitness = current_fitness

        if gen % 250 == 0:
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


def test_genetic_algorithm(test_cases, crossover_methods, output_file="ver6_2000.txt", num_runs=None):
    results = []
    flag_input = input("Для запуска турниного отбора с сохранением лучшей особи при перезапуске нажмите enter\n"
                       "Для запуска турниного отбора без сохранения лучшей особи при перезапуске введите любой символ: ")
    flag_ver = None if flag_input.strip() == "" else flag_input
    with open(output_file, "a") as f:  # Открываем файл заранее
        for mutation_rate, mutation_rate_check, gen_check in test_cases:
            for crossover_method in crossover_methods:
                for _ in range(num_runs):
                    print(
                        f"\nТест: crossover={crossover_method.__name__}, mutation_rate={mutation_rate}, mutation_rate_check={mutation_rate_check}, gen_check={gen_check}")

                    start_time = time()
                    best_solution, generations = genetic_algorithm(
                        publicKey, encrypted_result, ones,
                        mutation_rate=mutation_rate,
                        mutation_rate_check=mutation_rate_check,
                        gen_check=gen_check,
                        crossover_func=crossover_method,
                        flag_ver=flag_ver
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
                        "fitness": fitness_value
                    }

                    print(f"Результат: Поколения={generations}, Время={execution_time:.4f} сек, Fitness={fitness_value}")

                    # Записываем результат сразу после каждого теста
                    f.write(str(result) + "\n")
                    f.flush()  # Принудительно записываем в файл (чтобы не ждать закрытия)

    print(f"\nРезультаты сохранены в {output_file}")

if __name__ == "__main__":
    print("\nПрограмма запущена. Выберите желаемое действие ↓↓↓\n")
    while True:
        print("\nКодирование подмножества символов алгоритмом Меркла-Хелмана - 1\n"
              "Получение результата с помощью алгоритма Меркля-Хелмана - 2\n"
              "Получение результата с помощью модифицированной модели Голдберга - 3\n"
              "Запуск тестирования с различными начальными данными - 4\n"
              "Отображение тестовых данных - 5\n"
              "Завершение работы программы - 6\n")
        inputs = input("\nВведите номер выбранного действия: ")

        if inputs == "1":
            message = input("Введите текст:").split()
            n = len(message[0]) * 8
            sequence, publicKey, randInt1, randInt2 = createKey(n)
            print('Cупервозрастающая последовательность:', sequence)
            print("q:", randInt1)
            print("r:", randInt2)
            print("Открытый ключ:", publicKey)
            binaryMessage = convertToBinary(message)
            encrypted, ones = encrypt(binaryMessage, publicKey)
            encrypted_result = (sum(encrypted[0]))
            print("\nЗашифрованное сообщение \"{}\"\n".format(encrypted_result))

        if inputs == "2":
            if 'encrypted' in locals() and 'sequence' in locals() and 'randInt1' in locals() and 'randInt2' in locals():
                print("\nПолучение результатов с помощью алгоритма Меркля-Хеллмана запущено..")
                decrypted = decrypt(encrypted, sequence, randInt1, randInt2)
                print("\n\nБуквы в двоичном представлении:", decrypted)
                stringMessage = convertToString(decrypted)
                print("Расшифрованное сообщение \"{}\"".format(formatMessage(stringMessage, "string")))
            else:
                print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1.")

        if inputs == "3":
            # encrypted = int(input("Введите зашифрованное слово:"))  # 3889444981
            #publicKey = [56235750, 5342396250, 10459849500, 16308367500, 33460271250, 68270200500, 138452416500, 112185908777, 56559927081, 115313048412, 68887667351, 133332710452, 102902504431, 44066579389, 84702778028, 7779598083, 13253530416, 30499799082, 58525225164, 118006458078, 69663155183, 141407033116, 120513279259, 72933489295, 147104165090, 131963778957, 96003195941, 31505148909, 59804860068, 123265043886, 82373521049, 163734798598]
            # a = [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]
            #encrypted_result = 1194928103296
            #ones = 5
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

                flag_ver = None if flag_input.strip() == "" else flag_input
                funk_ver = crossover_one if funk_input.strip() == "" else crossover_two
                # Используем ГА для расшифровки
                start = time()
                for word in result:
                    for char in word:
                        solution, gen = genetic_algorithm(publicKey, char, ones, crossover_func = funk_ver, flag_ver = flag_ver)
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
            if 'encrypted_result' in locals() and 'publicKey' in locals():
                # Тестовые параметры
                mutation_test_cases = [
                    (1, 0.4, 250),
                    (1, 0.4, 500),
                    (1, 0.4, 1000),
                    (1, 0.6, 250),
                    (1, 0.6, 500),
                    (1, 0.6, 1000),
                    (1, 0.5, 250),
                    (1, 0.5, 500),
                    (1, 0.5, 1000)
                ]

                # Разные кроссоверы
                crossover_variants = [
                    crossover_one,
                    crossover_two,
                    # crossover_three
                ]
                # Запуск тестов
                count_tests = int(input("Введите число тестирований для каждого набора данных:"))
                test_genetic_algorithm(mutation_test_cases, crossover_variants, num_runs=count_tests)
            else:
                print("\nОШИБКА: отсутствуют необходимые данные. Попробуйте сгенерировать данные в пункте 1.")
        if inputs == "5":
            subprocess.run(["python", "Tab_Gr_result.py"])
        if inputs == "6":
            exit()