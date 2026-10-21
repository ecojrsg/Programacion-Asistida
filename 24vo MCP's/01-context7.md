# Context7 MCP — documentación para el agente

Fecha de investigación y prueba: **21 de octubre de 2026**.

## ¿Qué hace el MCP?

Context7 busca documentación y ejemplos de bibliotecas para que el agente
consulte una fuente concreta antes de responder. Su flujo consiste en resolver
el identificador de una biblioteca y después consultar sus documentos. El
proyecto pertenece a **Upstash**. [Repositorio oficial](https://github.com/upstash/context7).

En este ejercicio se eligió Context7 para investigar cómo conectar servidores
MCP a OpenCode. La consulta produjo material que ayudó a redactar estos Markdown.

## ¿Cómo se instala o conecta en OpenCode?

Se detectó **OpenCode v2.0.23** en este equipo. El archivo `opencode.json` de
esta carpeta deja preparado el servidor remoto; no contiene contraseñas.
La configuración para v2 es:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp"
      }
    }
  }
}
```

Desde esta carpeta:

```sh
opencode --version
opencode mcp list
opencode
```

En v2 también se puede agregar con
`opencode mcp add context7 --url https://mcp.context7.com/mcp`. No hace falta
repetirlo si ya se usa el archivo incluido. Si aparece una solicitud de
autenticación, abrir `/mcps`, seleccionar Context7 y completar el inicio de
sesión. [Configuración MCP de OpenCode v2](https://opencode.ai/v2/docs/mcp-servers/).

**Compatibilidad:** en v1 las entradas van directamente en `mcp` y se usa
`enabled`; v2 utiliza `mcp.servers` y `disabled` para desactivar una entrada.
No mezclar ambas estructuras. [Documentación v1](https://opencode.ai/docs/mcp-servers/).

El proveedor también ofrece un asistente de instalación y un plugin. Aquí se
eligió la conexión MCP manual para mantener el ejercicio local y explícito.
[Integración de Context7 con OpenCode](https://context7.com/docs/clients/opencode).

## Prueba real realizada

Se utilizó el conector Context7 disponible en esta conversación:

1. Herramienta `resolve-library-id`, biblioteca `OpenCode`.
2. Se seleccionó `/anomalyco/opencode`, correspondiente al proyecto actual.
3. Herramienta `query-docs`, con esta consulta:

   > How do I configure a remote MCP server such as Context7 in opencode.json
   > and verify its connection with opencode mcp list?

**Resultado observado:** devolvió ejemplos de configuración, el comando para
listar conexiones y enlaces a archivos de documentación del repositorio de
OpenCode. La respuesta incluía ejemplos de distintas generaciones; se contrastó
con la documentación oficial de v2 antes de preparar la configuración local.

Esto demuestra una consulta funcional mediante Context7 y su utilidad para
elaborar la entrega. El estado de la conexión desde la CLI de OpenCode se
registra por separado en [la evidencia](04-evidencia-context7.md).

### Prueba para repetir en clase

En OpenCode, pedir:

> Usa Context7 para consultar cómo configurar un servidor MCP remoto en
> OpenCode v2. Indica la biblioteca consultada, las herramientas utilizadas
> y las fuentes. No cambies archivos.

**Criterio de éxito:** se observa una llamada real al MCP y la respuesta incluye
fuentes pertinentes. Una respuesta del modelo sin llamada no cuenta como prueba.

## ¿Quién lo creó?

**Upstash**, organización responsable del repositorio `upstash/context7`.
La licencia publicada es MIT. La autoría se respalda en el
[repositorio oficial](https://github.com/upstash/context7), no en el nombre de
un paquete de terceros.

## ¿Hay evidencia de que sea seguro?

El proveedor publica sus prácticas de seguridad: consultas enviadas al servicio,
protección y rotación de claves e infraestructura operada por Upstash con
cumplimiento SOC 2. Son declaraciones documentadas del proveedor; esta práctica
no realizó una auditoría ni verificó certificaciones de forma independiente.
[Seguridad de Context7](https://context7.com/docs/security/overview).

**Evaluación para esta práctica:** usar consultas sobre documentación pública,
sin secretos ni código privado. La solicitud sale del equipo hacia un servicio
remoto y el contenido recuperado debe revisarse. El código abierto y las
políticas públicas aportan evidencia de transparencia, pero no garantizan
ausencia de vulnerabilidades.

## Guion para una presentación de seis diapositivas

| Diapositiva | Contenido | Apoyo para explicar |
| --- | --- | --- |
| 1. Problema | El agente puede necesitar documentación actual | Plantear una duda técnica concreta |
| 2. Solución y autor | Context7, de Upstash | Mostrar el repositorio |
| 3. Conexión | Servidor remoto y configuración v2 | Mostrar el JSON sin credenciales |
| 4. Demostración | Resolver biblioteca y consultar documentos | Mostrar la evidencia real |
| 5. Seguridad | Evidencias, envío de consultas y límites | Diferenciar transparencia de garantía |
| 6. Experiencia | La versión del cliente importa | Explicar el contraste entre v1 y v2 |

**Conclusión para exponer:** Context7 ayudó a fundamentar la documentación; la
revisión humana permitió elegir el formato compatible con la versión instalada.
