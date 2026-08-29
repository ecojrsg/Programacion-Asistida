# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-24 15:23:34
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-24 15:28:00
# Calculador de tablas de multiplicar


def main():
    number = int(input("Ingresa un número: "))
    for i in range(1, 11):
        print(f"{number} x {i} = {number * i}")


if __name__ == "__main__":
    main()
