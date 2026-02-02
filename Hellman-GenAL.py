import random
from random import randint
from time import time

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

def createKey(n):
    sequence = createSuperincreasingSequence(n)  # супервозрастающая последовательность
    publicKey = []
    randInt1 = generate_prime(sum(sequence))
    randInt2 = randInt1 - randint(0, randInt1)  #r
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2

def encrypt(message, publicKey):
    encrypted = []
    print("==============ШИФРОВАНИЕ==============")
    for word in message:
        wordTemp = []
        offset = 0  # Смещение для publicKey

        for index, char in enumerate(word):
            print(f"\nОбрабатываем элемент {index}: {char}")
            result = 0

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

    return encrypted

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

def fitness(solution, b, C):
    return abs(C - sum([solution[i] * b[i] for i in range(len(b))]))

#Мутация с процентом вероятности для одного бита
def mutate(solution, mutation_rate, b=None, C=None):
    mutated = solution.copy()

    # Случайно решаем, будет ли мутация происходить
    if random.random() <= mutation_rate:
        # Выбираем один случайный индекс для мутации
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
def crossover(parent1, parent2, b, C):
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

# #Двухточечный кроссовер
# def crossover(parent1, parent2, b, C):
#     point1 = random.randint(1, len(parent1) - 2)
#     point2 = random.randint(point1 + 1, len(parent1) - 1)
#
#     child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
#     child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
#
#     # print(f"Родители:")
#     # print(f"{parent1} (Родитель 1) с fitness {fitness(parent1, b, C)}")
#     # print(f"{parent2} (Родитель 2) с fitness {fitness(parent2, b, C)}")
#     # print(f"Точки кроссовера: {point1}, {point2}")
#     # print(f"Дети до мутации:")
#     # print(f"{child1} (Ребёнок 1) с fitness {fitness(child1, b, C)}")
#     # print(f"{child2} (Ребёнок 2) с fitness {fitness(child2, b, C)}")
#
#     return child1, child2

def genetic_algorithm(b, C, pop_size=1000, generations=15000, mutation_rate=1,mutation_rate_check=0.4,gen_check=250):
    # print(f"Идеальное с fitness {fitness(a, b, C)}")
    n = len(b)
    population = [random.choices([0, 1], k=n) for _ in range(pop_size)]
    # print("Изначальная популяция:")
    # for i in population:
    #     print(i)
    for gen in range(generations):
        new_population = []
        if (gen + 1) % gen_check == 0:
            best = min(population, key=lambda x: fitness(x, b, C))
            new_population.append(best)
            for _ in range(pop_size - 1):
                mutated = mutate_check(best, mutation_rate_check,b,C)
                new_population.append(mutated)
            print(f"\nПосле {gen+1} поколений: Лучшее решение {best} с fitness {fitness(best, b, C)}")
        else:
            for i in range(len(population)):
                parent1 = population[i]
                parent2 = random.choice(population[:i] + population[i+1:])
                child1, child2 = crossover(parent1, parent2, b, C)
                child1 = mutate(child1, mutation_rate, b, C)
                child2 = mutate(child2, mutation_rate, b, C)
                best = min([parent1, child1, child2], key=lambda x: fitness(x, b, C))
                # print(f"Выбран лучший: {best} с fitness {fitness(best, b, C)}\n")
                new_population.append(best)
        population = sorted(new_population, key=lambda x: fitness(x, b, C))[:pop_size]

        if gen % 25 == 0:
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

if __name__ == "__main__":

    while True:
        print("\nЗакодировать слово - 1\nПолучение результата с помощью модели генетического алгоритма Голберга - 2\nЗавершить работу - 3")
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
            encrypted = encrypt(binaryMessage, publicKey)
            encrypted_result = (sum(encrypted[0]))
            print("\nЗашифрованное сообщение \"{}\"\n".format(encrypted_result))
            # decrypted = decrypt(encrypted, sequence, randInt1, randInt2)
            # print("\n\nБуквы в двоичном представлении", decrypted)
            # stringMessage = convertToString(decrypted)
            # print("Расшифрованное сообщение \"{}\"".format(formatMessage(stringMessage, "string")))

        if inputs == "2":
            # encrypted = int(input("Введите зашифрованное слово:"))  # 3889444981
            # publicKey = [99571071, 80295717, 14979770, 143409098, 149797700, 34036028, 29521348, 155419466, 157737383, 74587615, 29227522, 21005619, 130898123, 101204812, 135992394, 46077407, 34328752, 96524026, 63517441, 149504537, 152296127, 86174758, 134900091, 63168155]
            # a = [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0]
            encrypted = int(encrypted_result)
            result = []
            p = []
            p.append(encrypted)
            result.append(p)


            decoded_messages = []
            gener = []

            # Используем ГА для расшифровки
            start = time()
            for word in result:
                for char in word:
                    solution, gen = genetic_algorithm(publicKey, char)
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

        if inputs == "3":
            break