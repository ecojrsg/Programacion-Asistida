# Playwright MCP — interacción con el navegador

Fecha de investigación: **21 de octubre de 2026**.
Estado: **investigado; no se ejecutó este MCP durante esta práctica**.

## ¿Qué hace el MCP?

Permite que un agente navegue por páginas, inspeccione su estructura y opere
elementos como enlaces y campos. Utiliza Playwright y puede proporcionar
información estructurada de accesibilidad. Su uso es apropiado para demostrar
un recorrido web o explorar una interfaz.

Lo mantiene **Microsoft** en `microsoft/playwright-mcp`, con licencia Apache 2.0.
El paquete oficial es `@playwright/mcp`. No debe confundirse el servidor MCP
con Playwright Test ni con una skill que emplea su CLI.
[Repositorio y requisitos oficiales](https://github.com/microsoft/playwright-mcp).

## ¿Cómo se instala o conecta en OpenCode?

Cada integrante necesita OpenCode, Node.js 18 o superior, `npx` y un navegador
compatible disponible. El lanzamiento con `npx` puede descargar el paquete.

Para OpenCode **v2**, agregar esta entrada en `mcp.servers` del archivo del
proyecto, conservando las entradas existentes:

```json
{
  "type": "local",
  "command": ["npx", "-y", "@playwright/mcp@latest", "--isolated"]
}
```

Nombrar la entrada `playwright`. Alternativamente, en v2:

```sh
opencode mcp add playwright -- npx -y @playwright/mcp@latest --isolated
opencode mcp list
```

La forma de registrar procesos locales corresponde a
[OpenCode v2](https://opencode.ai/v2/docs/mcp-servers/); los argumentos del proceso
proceden del [servidor oficial](https://github.com/microsoft/playwright-mcp).
En OpenCode v1, colocar la entrada directamente en `mcp` y agregar
`"enabled": true`.

`--isolated` mantiene el perfil de la sesión en memoria. `@latest` facilita el
primer ensayo, pero puede cambiar: después de una prueba satisfactoria, registrar
y usar la misma versión concreta del paquete en todos los equipos.

Si falta el navegador, seguir la indicación de instalación del propio servidor.
No tomar la mera aparición del servidor en la lista como prueba de navegación.

## Prueba propuesta para clase

Prompt:

> Usa Playwright MCP para abrir https://example.com, obtener el encabezado
> principal y describir el enlace visible. No uses sesiones personales.

Resultado esperado para esa página: encabezado **Example Domain**. Confirmarlo
al ejecutar; aquí se presenta como criterio esperado, no como resultado medido.

Guardar como evidencia:

- Versión de OpenCode y del paquete utilizado.
- Estado de conexión del servidor.
- Llamada de navegación y lectura de la página.
- Respuesta observada y, si se obtiene, captura de pantalla sin datos privados.

Si el navegador no abre, revisar la salida del servidor, la instalación del
navegador y el acceso de red. Documentar el error real antes de repetir.

## ¿Quién lo creó?

**Microsoft**, según la organización propietaria del
[repositorio oficial](https://github.com/microsoft/playwright-mcp). Para la
exposición, mostrar también el nombre exacto del paquete y su licencia.

## ¿Hay evidencia de que sea seguro?

Hay código público y una política de reporte de vulnerabilidades mediante el
Microsoft Security Response Center.
[Política de seguridad](https://github.com/microsoft/playwright-mcp/blob/main/SECURITY.md).

El propio proyecto advierte que el MCP no constituye una frontera de seguridad.
El aislamiento del perfil evita reutilizar el estado habitual del navegador,
pero no convierte en confiable una página maliciosa ni sus instrucciones.
[Advertencias y opciones oficiales](https://github.com/microsoft/playwright-mcp#security).

**Evaluación para la práctica:** usar una página pública de prueba, sin cuentas
personales, y revisar las acciones que el agente propone. Conceder navegación
no equivale a autorizar compras, publicaciones o el envío de formularios.
La política de reporte es evidencia de un proceso de atención de fallos;
no demuestra que el software esté libre de ellos.

## Guion para una presentación de seis diapositivas

| Diapositiva | Contenido | Evidencia que preparar |
| --- | --- | --- |
| 1. Necesidad | El agente debe interactuar con una web | Recorrido elegido |
| 2. Función y autor | Playwright MCP, de Microsoft | Repositorio y paquete |
| 3. Instalación | Proceso local iniciado por OpenCode | Configuración y versiones |
| 4. Demostración | Abrir y leer Example Domain | Llamadas y resultado reales |
| 5. Seguridad | Perfil separado y límites | Política de seguridad |
| 6. Experiencia | Qué funcionó y qué hubo que ajustar | Completar después del ensayo |

**Mensaje de cierre propuesto:** permite demostrar una interacción web concreta;
la calidad de la presentación depende de mostrar la ejecución y sus límites.
