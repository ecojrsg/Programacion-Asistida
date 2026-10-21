# Evidencia de la práctica con Context7

Fecha: **21 de octubre de 2026**, zona de referencia America/Mexico_City.

## Entorno y alcance

- Se encontró el ejecutable de OpenCode y se obtuvo **`opencode v2.0.23`**.
- Se encontró el ejecutable de Docker; esto no demuestra que Desktop o el
  Gateway estén activos.
- Se utilizó el conector Context7 disponible en esta conversación.
- Solo se añadieron archivos de entrega en la carpeta del ejercicio 24.
- No se instalaron paquetes ni se cambió la configuración global de OpenCode.

## Consulta MCP completada

### Llamada 1: resolver biblioteca

Herramienta del conector: `resolve-library-id`.

```json
{
  "libraryName": "OpenCode",
  "query": "Configure remote Context7 MCP and local Playwright MCP servers in opencode.json and list connected MCP servers"
}
```

Resultado: se recibieron candidatos, entre ellos **`/anomalyco/opencode`**.
Se eligió ese identificador porque corresponde al proyecto actual de OpenCode.

### Llamada 2: consultar documentación

Herramienta del conector: `query-docs`.

```json
{
  "libraryId": "/anomalyco/opencode",
  "query": "How do I configure a remote MCP server such as Context7 in opencode.json and verify its connection with opencode mcp list?"
}
```

Resultado observado: respuesta no vacía con fragmentos sobre configuración de
Context7, registro de servidores y listado de conexiones. Incluyó referencias
a documentación en `github.com/anomalyco/opencode`.

**Hallazgo:** aparecieron ejemplos con `mcp.context7` y referencias al formato
`mcp.servers`. Se verificó la diferencia entre versiones con la
[documentación oficial v2](https://opencode.ai/v2/docs/mcp-servers/).
El archivo entregado usa la estructura de v2.

Este registro resume llamadas reales realizadas durante la elaboración; no es
una captura ni una exportación íntegra del transporte MCP.

## Intento de conexión desde OpenCode

Se creó `opencode.json` local con Context7 remoto y se ejecutó
`opencode mcp list`. Para mantener los archivos auxiliares dentro del ejercicio,
se asignaron temporalmente `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`
y `XDG_STATE_HOME` a subdirectorios de `.opencode-check`.

La CLI no llegó a confirmar el estado del MCP. El error informó que el servicio
gestionado no podía iniciar en `127.0.0.1:49374` porque el puerto estaba ocupado.
No se comprobó de forma independiente si había otro proceso escuchando o si
la restricción del entorno causó ese diagnóstico.

Un intento con `--standalone` tampoco resolvió el problema: esta versión no
aceptó esa opción para `mcp list`. No se alteraron puertos ni se detuvieron
servicios de otras sesiones. Se eliminaron los archivos auxiliares creados para
el ensayo; la configuración del proyecto permanece lista para usar.

## Qué demuestra esta evidencia

| Comprobación | Estado |
| --- | --- |
| OpenCode instalado y versión identificada | Confirmado: v2.0.23 |
| Consulta funcional con Context7 | Confirmada mediante el conector de esta conversación |
| Configuración local preparada para OpenCode v2 | Confirmada; JSON revisado |
| Conexión Context7 desde la CLI local de OpenCode | Pendiente; falló el inicio del servicio local |
| Prueba de Playwright MCP | No realizada; protocolo en su documento |
| Prueba de Docker MCP Gateway | No realizada; protocolo en su documento |
| Instalación y prueba por todos los integrantes | Pendiente de evidencia individual |

## Cómo completar la evidencia en clase

1. Abrir una terminal normal dentro de esta carpeta y ejecutar `opencode mcp list`.
2. Si inicia, verificar el estado de Context7; completar la autenticación si la pide.
3. Pedir la consulta indicada en `01-context7.md` y observar la llamada a la herramienta.
4. Guardar aquí el resultado o una captura sin credenciales y actualizar el estado.
5. Si persiste el conflicto de servicio, revisarlo con el propietario de la sesión;
   no cerrar procesos ajenos para forzar la demostración.

**Conclusión factual para la exposición actual:** se probó Context7 desde el
conector y se preparó su configuración para OpenCode; falta demostrar la llamada
desde OpenCode en la sesión de cada integrante.
