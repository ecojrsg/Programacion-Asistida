# Docker MCP Toolkit y Gateway — gestión de servidores

Fecha de investigación: **21 de octubre de 2026**.
Estado: **investigado; no se conectó el Gateway durante esta práctica**.

## ¿Qué hace el MCP?

En este documento, “MCP de Docker” se interpreta como **Docker MCP Toolkit y
MCP Gateway**, productos de Docker. Si el servidor que ya usa el equipo tiene
otro nombre o repositorio, habrá que ajustar esta ficha a ese servidor concreto.

El Toolkit permite organizar servidores y conectarlos con clientes de IA.
El Gateway expone las herramientas de esos servidores mediante una conexión.
Las capacidades disponibles dependen del catálogo y del perfil habilitado;
el Gateway no implica por sí mismo una herramienta para administrar todos los
contenedores del equipo.
[Descripción oficial del Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/).

## ¿Cómo se instala o conecta en OpenCode?

Preparación por integrante:

1. Instalar y abrir Docker Desktop; habilitar MCP Toolkit si la versión lo requiere.
2. Crear un perfil y agregar solo el servidor elegido para la demostración.
3. Completar la configuración de ese servidor si solicita credenciales.
4. Conectar OpenCode desde la sección de clientes o registrar el Gateway manualmente.

La guía actual describe Docker Desktop 4.62 o posterior; versiones anteriores
pueden mostrar otra interfaz.
[Inicio del Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/).

En OpenCode **v2**, añadir una entrada llamada `MCP_DOCKER` dentro de
`mcp.servers`, sin eliminar las otras entradas:

```json
{
  "type": "local",
  "command": ["docker", "mcp", "gateway", "run"]
}
```

Para un perfil específico, agregar `"--profile", "ID_DEL_PERFIL"` al final
de `command`, sustituyendo el identificador por el real. También puede
registrarse el proceso en v2:

```sh
opencode mcp add MCP_DOCKER -- docker mcp gateway run
opencode mcp list
```

La sintaxis del cliente procede de
[OpenCode v2](https://opencode.ai/v2/docs/mcp-servers/); los argumentos del Gateway,
de la [referencia de Docker](https://docs.docker.com/reference/cli/docker/mcp/gateway/run/).
En v1, colocar la entrada directamente en `mcp` y agregar `"enabled": true`.

## Prueba propuesta para clase

Elegir un servidor de documentación pública del catálogo, por ejemplo Context7
si está disponible, y habilitarlo en el perfil. Pedir al agente:

> Usa las herramientas de Context7 expuestas por MCP_DOCKER para buscar la
> documentación de OpenCode sobre servidores MCP. Muestra la herramienta
> invocada y la fuente del resultado.

**Criterio de éxito:** conexión del Gateway y una llamada real a una herramienta
del servidor habilitado. Para probar esa ruta, evitar que el agente use a la
vez la conexión directa a Context7 del archivo incluido en este ejercicio.

Registrar perfil, servidor, versión de Docker Desktop y resultado. Un Gateway
conectado sin una llamada funcional no completa por sí solo la prueba.

## ¿Quién lo creó?

El Toolkit y el Gateway son de **Docker**. Los servidores que se agregan pueden
pertenecer a otros autores. Por ejemplo, ejecutar Context7 mediante Docker no
cambia su autoría: Context7 sigue siendo de Upstash.
[Gateway oficial](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/).

## ¿Hay evidencia de que sea seguro?

Docker documenta procedencia de compilaciones y SBOM firmados para imágenes de
su catálogo, además de verificación de firmas mediante el Gateway. Un SBOM es
un inventario de componentes, no una prueba de que estén libres de fallos.
[Preguntas de seguridad del Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/faqs/).

El proyecto también describe sus fronteras de seguridad y qué accesos dependen
de permisos concedidos por el usuario. Un servidor puede abusar de secretos o
directorios que se le hayan otorgado; contenerizarlo no elimina ese riesgo.
[Modelo de seguridad del Gateway](https://github.com/docker/mcp-gateway/blob/main/docs/security.md).

**Evaluación para esta práctica:** habilitar solo las herramientas necesarias,
evitar montajes amplios de carpetas y no incluir secretos en la entrega.
Hay controles técnicos documentados; no se auditó la instalación de este equipo.

## Guion para una presentación de seis diapositivas

| Diapositiva | Contenido | Apoyo para explicar |
| --- | --- | --- |
| 1. Problema | Administrar varias conexiones MCP | Esquema cliente → Gateway → servidor |
| 2. Producto y autor | Toolkit y Gateway, de Docker | Distinguir autores de los servidores |
| 3. Instalación | Desktop, perfil y conexión local | Mostrar perfil sin secretos |
| 4. Demostración | Una consulta mediante el Gateway | Mostrar la ruta real de la llamada |
| 5. Seguridad | Firmas, procedencia y permisos | Explicar qué demuestran y qué no |
| 6. Experiencia | Organización y costo de configuración | Completar tras la prueba |

**Mensaje de cierre propuesto:** Docker organiza el acceso a servidores MCP;
la función final y sus riesgos dependen de los servidores y permisos habilitados.
