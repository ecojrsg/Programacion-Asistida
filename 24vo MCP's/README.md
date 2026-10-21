# Ejercicio 24 — MCP general en OpenCode

Investigación preparada el **21 de octubre de 2026**.

La entrega cubre los tres MCP o soluciones mencionados: Context7, Playwright y
Docker MCP Toolkit/Gateway. OpenCode admite otros servidores; esta carpeta no
pretende ser un catálogo exhaustivo.

## Documentos para estudiar y exponer

| Documento | Contenido | Estado práctico |
| --- | --- | --- |
| [Context7](01-context7.md) | Documentación técnica para el agente | Consulta real mediante el conector |
| [Playwright MCP](02-playwright.md) | Navegación e interacción web | Guía y prueba propuestas |
| [Docker MCP](03-docker.md) | Gestión y exposición de servidores | Guía y prueba propuestas |
| [Evidencia](04-evidencia-context7.md) | Consultas, resultado y límites del ensayo | Distingue conector y CLI de OpenCode |

Cada ficha responde las cuatro preguntas del ejercicio: qué hace, cómo
conectarlo, quién lo creó y qué evidencia de seguridad existe. También incluye
un guion de seis diapositivas para una presentación posterior.

## MCP elegido para la práctica

**Context7.** Se utilizó para investigar la integración MCP de OpenCode y elaborar
la documentación. Se detectó OpenCode **v2.0.23** y se dejó preparado
`opencode.json` dentro de esta carpeta con una conexión remota a Context7.

La consulta mediante el conector fue satisfactoria. El intento desde la CLI
de OpenCode falló al iniciar su servicio local, por lo que no se presenta
como una conexión confirmada. El detalle y la forma de repetirlo están en
[la evidencia](04-evidencia-context7.md).

## Relación con la consigna

- La organización del grupo en **cuatro equipos** debe hacerse en clase.
- Cada integrante debe conectar y probar el MCP elegido en su propio entorno.
- La exposición debe mostrar la experiencia real; los resultados esperados de
  las guías no deben presentarse como pruebas ejecutadas.

La parte documental está preparada. Para acreditar toda la parte práctica,
faltan la conexión funcional desde OpenCode y las evidencias individuales.

## Registro del equipo para completar

Agregar una fila por integrante, sin incluir claves ni tokens:

| Integrante | Versión de OpenCode | MCP elegido | Conexión confirmada | Prueba y evidencia |
| --- | --- | --- | --- | --- |
| Por registrar | Por registrar | Context7 sugerido | Pendiente | Pendiente |

## Preparación de la presentación

Usar el guion del MCP que finalmente exponga el equipo. Para Context7:

1. Presentar la necesidad de consultar documentación.
2. Explicar el flujo OpenCode → MCP → Context7 → documentación.
3. Mostrar configuración, versión y autoría de Upstash.
4. Ejecutar la consulta y mostrar evidencia de una llamada real.
5. Explicar las prácticas de seguridad y sus límites.
6. Contar el hallazgo sobre versiones y la experiencia de cada integrante.

Reservar aproximadamente un minuto por diapositiva, más la demostración.
La indicación de **20 minutos** en la consigna se conserva como tiempo de la
actividad; no se asume que sea la duración obligatoria de la exposición.

Antes de presentar, completar nombres y pruebas, revisar que las capturas no
contengan secretos y comprobar que los enlaces a las fuentes abran correctamente.
Todavía no se ha generado un archivo de diapositivas.
