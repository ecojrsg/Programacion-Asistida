# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-24 15:41:27
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-24 15:54:02
# Listas


def main():
    numbers = [12, 45, 7, 23, 56, 8, 34]

    print(f"La suma de los números es: {sum(numbers)}")
    print(f"El promedio de los números es: {sum(numbers) / len(numbers)}")
    print(f"Maximo: {max(numbers)}")
    print(f"Minimo: {min(numbers)}")
    print(f"Cantidad de numeros mayores que 13: {len([n for n in numbers if n > 13])}")



if __name__ == "__main__":
    main()
