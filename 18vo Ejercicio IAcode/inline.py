# @Author: Jonathan Serna
# @Date:   2026-09-28 15:58:32
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-09-28 16:08:09


def main():
    ## Genera una interfaz de terminal simple para escoer entre las funciones y ejecutarlas
    print("Bienvenido al menú de funciones")
    print("1. Verificar si una palabra es palíndroma")
    print("2. Contar vocales en una palabra")
    print("3. Verificar si un número es primo")
    print("4. Invertir una palabra")
    print("5. Salir")

    while True:
        choice = input("Ingrese el número de la opción que desea ejecutar: ")

        if choice == "1":
            word = input("Ingrese una palabra: ")
            if is_palindrome(word):
                print(f"{word} es un palíndromo.")
            else:
                print(f"{word} no es un palíndromo.")
        elif choice == "2":
            word = input("Ingrese una palabra: ")
            vowel_count = count_vowels(word)
            print(f"{word} tiene {vowel_count} vocales.")
        elif choice == "3":
            number = int(input("Ingrese un número: "))
            if is_prime(number):
                print(f"{number} es un número primo.")
            else:
                print(f"{number} no es un número primo.")
        elif choice == "4":
            word = input("Ingrese una palabra: ")
            inverted_word = ivenrt_word(word)
            print(f"La palabra invertida es: {inverted_word}")
        elif choice == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def is_palindrome(s):
    return s == s[::-1]

def count_vowels(s):
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def ivenrt_word(s):
    return s[::-1]

if __name__ == "__main__":
    main()
