# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-08-24 16:13:12
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-08-24 16:27:13
# Días de la semana

def main():
    week_dyas = (
        "Lunes", 
        "Martes", 
        "Miércoles", 
        "Jueves", 
        "Viernes", 
        "Sábado", 
        "Domingo",
        );

    print(f"El tercer día de la semana es: {week_dyas[2]}");
    print(f"Saturday esta en la lista: {'Saturday' in week_dyas}");

    for day in week_dyas:
       print(f"Día {week_dyas.index(day) + 1}: {day}");


if __name__ == "__main__":
    main()
