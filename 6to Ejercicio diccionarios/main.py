# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-24 16:36:50
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-24 16:41:36


def main():
    my_dict = {
        "borrador": 15,
        "cuaderno": 8,
        "regla": 12,
    }

    dict_keys = ", ".join(my_dict.keys())
    dict_values = ", ".join(map(str, my_dict.values()))

    print(f"Los productos son: {dict_keys}")
    print(f"Los precios son: {dict_values}")

    my_dict["lapiz"] = 50;
    my_dict["cuaderno"] = 20;

    print("El diccionario es:")
    for producto, precio in my_dict.items():
        print(f"{producto}: {precio}")

if __name__ == "__main__":
    main()
