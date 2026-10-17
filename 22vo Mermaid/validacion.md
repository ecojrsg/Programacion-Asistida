# Validación de la entrega

- Motor: Mermaid 12.2.0, biblioteca oficial distribuida por jsDelivr.
- Los seis archivos pasaron `mermaid.parse()` y `mermaid.render()` sin errores.
- Las seis capturas PNG se tomaron de páginas reales en Chromium con el motor Mermaid local. Durante el renderizado se bloquearon las solicitudes externas.
- Cada SVG se conserva también por separado para ampliarlo sin perder nitidez.
- No se ejecutó OpenCode. No se subieron los diagramas a mermaid.live.
- Las comprobaciones de escritorio de `fallos_y_cambios.md` revisan coherencia de reglas; no son pruebas de una aplicación ni de concurrencia real.

## Archivos comprobados

- `diagramas/antes/01_flujo.mmd`: sintaxis y renderizado correctos.
- `diagramas/antes/02_casos_uso.mmd`: sintaxis y renderizado correctos.
- `diagramas/antes/03_clases.mmd`: sintaxis y renderizado correctos.
- `diagramas/despues/01_flujo.mmd`: sintaxis y renderizado correctos.
- `diagramas/despues/02_casos_uso.mmd`: sintaxis y renderizado correctos.
- `diagramas/despues/03_clases.mmd`: sintaxis y renderizado correctos.

## Límite de la evidencia

La revisión automática de permisos rechazó enviar el contenido local a Mermaid Live. Las capturas demuestran el renderizado local, no una visita a ese editor con los diagramas. Este paso de la consigna queda pendiente si se exige evidencia del sitio exacto. La revisión «sin IA» también requiere que el alumno haga su propia revisión.

## Referencias técnicas

- [Flujo: documentación oficial](https://mermaid.js.org/syntax/flowchart.html).
- [Casos de uso nativos, Mermaid 12+](https://mermaid.js.org/syntax/usecase.html).
- [Clases: documentación oficial](https://mermaid.js.org/syntax/classDiagram.html).
- [Mermaid Live, para revisión manual si se autoriza](https://mermaid.live).

Consultadas el 16 de octubre de 2026.
