# 26. Tarea de skills de OpenCode

## Descripción del proyecto

Creé la skill **readme-academico** para redactar o actualizar el README de un
proyecto a partir de sus archivos reales. Incluye los seis apartados de la
tarea de la diapositiva 66: descripción, estructura, requerimientos, instalación,
ejecución y troubleshooting.

También incorporé las convenciones de este repositorio para numerar ejercicios,
distinguir el README general del de cada proyecto y preparar los PDF cuando se
soliciten. La skill documenta el proyecto seleccionado sin cambiar su código.

## Estructura de las carpetas

```text
26vo Skills OpenCode/
├── README.md
└── .opencode/
    └── skills/
        └── readme-academico/
            ├── SKILL.md
            └── references/
                ├── readme-template.md
                └── repository-conventions.md
```

- [SKILL.md](.opencode/skills/readme-academico/SKILL.md): flujo de trabajo y límites.
- [Plantilla](.opencode/skills/readme-academico/references/readme-template.md): los seis apartados obligatorios.
- [Convenciones](.opencode/skills/readme-academico/references/repository-conventions.md): numeración, registro general y PDF.

## Preparación de dependencias y requerimientos

Necesito OpenCode para cargar la skill; la documentación consultada corresponde
a v2. Los archivos son Markdown y no requieren instalar paquetes de Python ni
Node.js para utilizarlos como referencia. Debo disponer de permiso para leer el
proyecto que vaya a documentar y escribir su README.

La creación de PDF es un flujo opcional: requiere una herramienta de exportación
disponible y revisión visual. Este ejercicio entrega una skill y su documentación;
no necesita un servidor MCP ni un generador de PDF para cargarla.

## Modo de instalación

La skill ya está colocada a nivel de este ejercicio en
`.opencode/skills/readme-academico/SKILL.md`. Para que OpenCode pueda descubrirla,
abro una terminal desde esta carpeta:

```sh
cd "/Users/eco/Dev/Programacion-Asistida/26vo Skills OpenCode"
opencode
```

Inicio una sesión nueva si tenía OpenCode abierto antes de crear los archivos.
No instalé la skill globalmente ni cambié la configuración de otros ejercicios.
OpenCode busca skills desde su directorio de trabajo hacia la raíz del proyecto;
abrir únicamente la raíz del repositorio no garantiza descubrir esta carpeta hija.
[Referencia oficial de skills](https://opencode.ai/v2/docs/skills/).

## Modo de ejecución

En OpenCode v2 puedo solicitarla con este prompt:

> @readme-academico Revisa los archivos de este ejercicio y actualiza únicamente
> su README.md con los seis apartados de la tarea. Usa las convenciones del
> repositorio, comprueba las rutas y conserva las limitaciones de las pruebas.

Para otro proyecto, indico su ruta exacta y los archivos de salida autorizados.
Si quiero un PDF, lo pido expresamente; la skill aplica entonces el nombre
`Ejercicio_NN_Tema.pdf`, el formato de referencia y la carpeta `PDFs ejercicios`.

**Ejemplo aplicado:** este README usa los seis apartados y describe los archivos
creados para la tarea. La comprobación local revisa estructura y enlaces; no
equivale a una carga confirmada desde la interfaz de OpenCode.

## Troubleshooting

| Síntoma | Qué reviso |
| --- | --- |
| OpenCode no encuentra la skill | Abro el ejercicio 26 y verifico la ruta, el nombre exacto `SKILL.md` y los permisos de skills. |
| Carga una skill distinta | Compruebo si existe otra con el mismo identificador y qué origen tiene prioridad. |
| Un enlace del README no abre | Lo resuelvo desde la carpeta del propio README y reviso espacios, mayúsculas y el archivo de destino. |
| El número del ejercicio se repite | Comparo las carpetas reales; el índice general puede estar incompleto. |
| Un comando falla por rutas | Reviso el directorio de trabajo antes de instalar paquetes o cambiar el código. |
| El PDF contiene texto cortado | Renderizo las páginas y ajusto el contenido antes de volver a exportar. |

Las soluciones de carga son indicaciones para probar en OpenCode; no afirmo
haberlas ejecutado en una sesión de esa aplicación durante esta entrega.

### Fuentes

- Consigna: `5. AI-assisted coding workflows in practice (3).pdf`, diapositiva 66.
- [Skills en OpenCode v2](https://opencode.ai/v2/docs/skills/).
- Convenciones observadas en el README raíz, las carpetas existentes y los PDF de los ejercicios 22, 23 y 24.

### PDF de entrega

[Consultar la explicación en PDF](../PDFs%20ejercicios/Ejercicio_26_Skills_OpenCode.pdf).
