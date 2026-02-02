from random import randint

"""
Алгорим Меркля-Хелмана Версия 2
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
    randInt2 = randInt1 - randint(0, randInt1)  #r
    for i in range(n):
        publicKey.append((sequence[i] * randInt2) % randInt1)
    return sequence, publicKey, randInt1, randInt2


def encrypt(message, publicKey):
    encrypted = []

    for word in message:
        wordTemp = []

        for char in word:
            result = 0

            for i, bit in enumerate(char):
                result += int(bit) * publicKey[i]

            wordTemp.append(result)

        encrypted.append(wordTemp)

    return encrypted


def decrypt(message, sequence, randInt1, randInt2):
    inverse = modInverse(randInt2, randInt1)

    decrypted = []

    for word in message:
        wordTemp = []

        for char in word:
            moduled = (char * inverse) % randInt1
            charTemp = ""

            for i in range(7, -1, -1):
                if moduled >= sequence[i]:
                    moduled -= sequence[i]
                    charTemp += '1'
                else:
                    charTemp += '0'

            wordTemp.append(charTemp[::-1])

        decrypted.append(wordTemp)

    return decrypted


if __name__ == "__main__":
    message = input("Введите текст:").split()
    n = len(message[0])*8
    sequence, publicKey, randInt1, randInt2 = createKey(n)
    print('Cупервозрастающая последовательность:',sequence)

    print("q:", randInt1)
    print("r:", randInt2)
    print("Публичный ключ:", publicKey)

    binaryMessage = convertToBinary(message)

    encrypted = encrypt(binaryMessage, publicKey)

    print("\nЗашифрованное сообщение \"{}\"\n".format(formatMessage(encrypted, "binary")))
    print(len(format(formatMessage(encrypted, "binary"))))

    decrypted = decrypt(encrypted, sequence, randInt1, randInt2)
    print("ff",decrypted)

    stringMessage = convertToString(decrypted)

    print("Расшифрованное сообщение \"{}\"".format(formatMessage(stringMessage, "string")))