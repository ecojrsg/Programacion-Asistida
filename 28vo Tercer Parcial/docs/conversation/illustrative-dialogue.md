# Diálogo ilustrativo para repasar la entrega

**Simulación didáctica.** Este diálogo de ejemplo resume solicitudes,
decisiones y comprobaciones del ejercicio.

**Estudiante (ejemplo):** Necesito el juego del ejercicio 5 en Python y
Streamlit. Primero presenta el diseño y un diagrama Mermaid; no escribas
código todavía. Solo quiero jugar una ronda y ver el marcador.

**Asistente (ejemplo):** La pantalla tendrá un selector con piedra, papel
y tijera, un botón para jugar, las dos jugadas, el resultado y tres
contadores. La lógica estará en `game.py` y la interfaz en `app.py`.
La computadora usará una elección aleatoria y el marcador vivirá en la sesión.

**Estudiante (ejemplo):** El contrato es `determine_winner(player_move,
computer_move)`. Debe devolver `player`, `computer` o `tie` y lanzar
`ValueError` si una jugada no es válida. Antes de implementar, prepara las
pruebas con las reglas del juego, sin deducir resultados de una implementación.

**Asistente (ejemplo):** Las pruebas cubrirán las nueve combinaciones
posibles y jugadas inválidas en ambos argumentos. El contrato inicial
levantará `NotImplementedError` para observar un fallo real.

**Estudiante (ejemplo):** Conserva el código de las pruebas y la salida
de la fase roja. Después implementa la función más sencilla, sin cambiar
las pruebas, sus valores esperados ni agregar `skip` o `xfail`.

**Asistente (ejemplo):** La implementación valida ambas jugadas, resuelve
el empate y comprueba las tres parejas ganadoras. Los archivos de evidencia
permiten comparar la ejecución roja y verde y el hash de las pruebas.

**Estudiante (ejemplo):** Revisa la claridad del código y agrega la interfaz.
Cambiar el selector no debe contar otra ronda. Guarda el último resultado
y aumenta solo el contador que corresponde al pulsar el botón.

**Asistente (ejemplo):** Se usarán los controles nativos y
`st.session_state`. Las pruebas de interfaz comprobarán victoria, derrota,
empate, acumulación del marcador y aislamiento entre sesiones.

**Estudiante (ejemplo):** Documenta lo que realmente se probó. Necesito el
diagrama, la conversación, las capturas de funciones y de TDD, y el enlace
al código para el PDF. No agregues funciones ajenas al examen.

**Asistente (ejemplo):** La entrega incluirá esos materiales, instrucciones
para ejecutar y las limitaciones comprobadas. El documento final quedará
pendiente de revisión antes de su commit.
