# Plan del MVP: Castillo Matemático

## Objetivo
Crear un juego educativo simple en Streamlit donde un aventurero recorre un castillo, derrota enemigos resolviendo operaciones y obtiene oro.

## Reglas implementadas
- El jugador inicia con `n` puntos de vida.
- Cada habitación contiene un enemigo.
- Una respuesta correcta derrota al enemigo y permite avanzar.
- Una respuesta incorrecta resta `x` puntos.
- Si se agota el tiempo, el enemigo resta `z` puntos y aparece una nueva operación.
- El juego termina al completar todas las habitaciones o al llegar a cero de vida.
- La dificultad aumenta por habitación.

## Configuración editable
- `config/settings.json`: `n`, `x`, `z`, oro inicial y número de habitaciones.
- `config/exercises.json`: niveles, operaciones, rangos y tiempos.
- Los archivos se leen al iniciar/reiniciar la aplicación; los cambios se aplican sin tocar el código.

## Ejecución
```bash
uv sync
uv run streamlit run app.py
```

## Futuras mejoras
Combate visual, tipos de tesoro, habitaciones vacías, persistencia de puntuaciones y más operaciones.
