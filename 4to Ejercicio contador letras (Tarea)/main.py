# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-24 15:49:48
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-24 15:54:00
# Contador de letras


def main():
    names = ["Ana", "Carlos", "Luis", "Sofia", "Eva", "Alejandro"]
    names_4 = [name for name in names if len(name) > 4]
    print(f"Nombres con mas de 4 letras: {names_4}")


if __name__ == "__main__":
    main()
