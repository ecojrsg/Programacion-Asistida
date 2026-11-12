# Especificación

&nbsp;

Minutos negativos → ValueError

Los primeros 15 minutos son gratis.

Después se cobra por hora completa o fracción, i.e. una hora y un minuto se cobran como dos horas.

Tarifa por hora: auto \$20, moto \$10

Cualquier otro tipo de vehículo → ValueError

En fin de semana la tarifa aumenta 50 %

Tope máximo de \$150 por estancia

&nbsp;

# Contrato de la función

calculate\_toll(minutes:int, type:string="auto", weekend:bool=False)

&nbsp;

## Ejemplos

calculate\_toll(90) → 40

calculate\_toll(16, "moto") → 10

calculate\_toll(120, "auto", True) → 60

&nbsp;