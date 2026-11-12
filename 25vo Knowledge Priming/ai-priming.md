# Knowledge Priming: Mi Castillo Matemático

## 1. Arquitectura
- `app.py` contiene la interfaz de Streamlit; `game.py`, las reglas.
- La partida se guarda como diccionario en `st.session_state.game`.
- `Exercise` representa los ejercicios y `ExerciseGenerator` los genera según la configuración JSON.
- El jugador empieza con 100 de vida y 0 de oro, y recorre 9 habitaciones.
- Un acierto entrega `room * 10` monedas y permite avanzar; un error resta 5 de vida y agotar el tiempo resta 10.
- Se gana al completar las habitaciones y se pierde con vida menor o igual a cero.

## 2. Stack y versiones
- Proyecto en versión `0.1.0`, con Python `>=3.11`; `.venv/pyvenv.cfg` registra Python 3.14.
- Dependencias gestionadas con uv: Streamlit `1.64.0` y streamlit-autorefresh `1.0.1`, fijadas en `uv.lock`.
- Biblioteca estándar: `json`, `random`, `time`, `dataclasses` y `pathlib`.

## 3. Fuentes de referencia
- Consultar primero `app.py`, `game.py` y `config/`; los comportamientos comprobados están en `tests/test_game.py`.
- Revisar `pyproject.toml` y `uv.lock` para las dependencias, y `docs/PLAN.md` para las reglas y comandos.
- `docs/CLASS_DIAGRAM.md` documenta las relaciones. `GameState` y `GameRules` describen diccionarios, no clases implementadas.

## 4. Estructura del proyecto
- Carpeta principal: `19vo Ejercicio videojuego/`.
- `config/settings.json`: vida inicial, daño y número de habitaciones.
- `config/exercises.json`: dificultades, operaciones y tiempos.
- `tests/test_game.py`: comprobaciones de reglas e interfaz; `docs/`: plan, diagramas e historial.
- Ejecutar desde la carpeta principal: las rutas JSON son relativas al directorio de trabajo.

## 5. Convenciones de nombres
- Funciones y variables en `snake_case`; clases en `PascalCase`.
- Identificadores, comentarios y docstrings en inglés; mensajes de interfaz en español.
- Funciones pequeñas, con una responsabilidad y nombres descriptivos. Conservar claves existentes como `n`, `x` y `z`.

## 6. Ejemplo de código
```python
def load_json(path: str | Path) -> dict:
    """Read UTF-8 JSON, relative to the current working directory."""
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)
```

## 7. Antipatrones y mantenimiento
- No incluir llamadas de Streamlit en `game.py` ni guardar partidas en variables globales compartidas.
- No duplicar valores de configuración ni fijar dificultades en el código; los niveles deben estar ordenados y cubrir todas las habitaciones.
- No generar divisiones con resto ni restas negativas; no bloquear el temporizador con `sleep`.
- No añadir clases, dependencias o funciones sin necesidad. Niebla, mascota y Wordle pertenecen a otras ramas.
- Revisar esta base cuando cambie el juego o dentro de seis meses.
- No se contrastaron los archivos del repositorio; las versiones y rutas registradas pueden estar desactualizadas.
