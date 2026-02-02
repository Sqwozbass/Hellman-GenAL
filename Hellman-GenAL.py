from random import randint
"""
Алгорим Меркля-Хелмана Версия 4
"""
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
    randInt2 = randint(1, randInt1)  #r
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

if __name__ == "__main__":
    message = input("Введите текст:").split()
    n = len(message[0])*8
    sequence, publicKey, randInt1, randInt2 = createKey(n)
    print('Cупервозрастающая последовательность:',sequence)

    print("q:", randInt1)
    print("r:", randInt2)
    print("Открытый ключ:", publicKey)

    binaryMessage = convertToBinary(message)

    encrypted = encrypt(binaryMessage, publicKey)
    encrypted_result = (sum(encrypted[0]))

    print("\nЗашифрованное сообщение \"{}\"\n".format(encrypted_result))
    decrypted = decrypt(encrypted, sequence, randInt1, randInt2)
    print("\n\nБуквы в двоичном представлении",decrypted)

    stringMessage = convertToString(decrypted)

    print("Расшифрованное сообщение \"{}\"".format(formatMessage(stringMessage, "string")))




