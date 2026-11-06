# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-06 01:40:52
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-06 02:22:09

"""Build the exercise report from preserved source and real evidence."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

PROJECT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT.parent / "PDFs ejercicios/Ejercicio_28_Tercer_Parcial.pdf"
CODE_URL = (
    "https://github.com/ecojrsg/Programacion-Asistida/"
    "tree/main/28vo%20Tercer%20Parcial"
)
WIDTH = letter[0] - 84
FONT_DIR = Path("C:/Windows/Fonts")


def add_image(story, relative_path, caption, max_height=560):
    """Fit an original evidence image without altering its contents."""
    picture = Image(str(PROJECT / relative_path))
    scale = min(WIDTH / picture.imageWidth, max_height / picture.imageHeight)
    picture.drawWidth = picture.imageWidth * scale
    picture.drawHeight = picture.imageHeight * scale
    picture.hAlign = "CENTER"
    story.extend([
        picture, Spacer(1, 7), Paragraph(caption, STYLES["Caption"])
    ])


def add_page(story, title):
    """Start a numbered report section on a new page."""
    story.extend([PageBreak(), Paragraph(title, STYLES["Heading1"])])


def add_text(story, text, style="BodyText"):
    """Append report text using the selected paragraph style."""
    story.append(Paragraph(text, STYLES[style]))


def draw_footer(canvas, document):
    """Draw a restrained running title and page number."""
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    if document.page > 1:
        canvas.drawString(42, 23, "Tercer parcial - Ejercicio 5")
    canvas.drawRightString(letter[0] - 42, 23, str(document.page))
    canvas.restoreState()


def build_report():
    """Create the PDF with evidence and an illustrative dialogue."""
    story = [Spacer(1, 105)]
    add_text(story, "Tercer examen parcial", "CoverTitle")
    add_text(story, "5. Piedra, papel o tijera", "CoverSubtitle")
    story.append(Spacer(1, 60))
    add_text(story, "Jonathan Serna", "CoverName")
    add_text(story, "Programación Asistida por Inteligencia Artificial",
             "CoverName")
    add_text(story, "6 de noviembre de 2026", "CoverName")

    add_page(story, "1. Objetivo, diseño y ejecución")
    add_text(story, "Implementar el ejercicio 5: el jugador elige piedra, "
             "papel o tijera; la computadora elige al azar y se resuelve "
             "una ronda. La interfaz usa Streamlit y muestra las victorias "
             "del jugador, las de la computadora y los empates.")
    add_text(story, "Se eligieron dos módulos: <b>game.py</b> "
             "para las reglas y <b>app.py</b> para la pantalla y el estado.")
    add_text(story, "Contrato y reglas", "Heading2")
    add_text(story, "<b>determine_winner(player_move: str, "
             "computer_move: str) -&gt; str</b>. Acepta exactamente "
             "<b>piedra</b>, <b>papel</b> o <b>tijera</b>. Devuelve "
             "<b>player</b>, <b>computer</b> o <b>tie</b>. Si cualquiera "
             "de las jugadas es inválida, lanza <b>ValueError</b>.")
    add_text(story, "Piedra vence a tijera, papel vence a piedra y tijera "
             "vence a papel. Dos jugadas iguales empatan. La elección "
             "aleatoria y el aumento del marcador ocurren una vez por "
             "clic en <b>Jugar ronda</b>.")
    add_text(story, "Instalación y uso", "Heading2")
    add_text(story, "Requisitos: Python 3.14 y uv. Dentro de "
             "<b>28vo Tercer Parcial</b>, ejecutar:")
    story.append(Preformatted(
        "uv sync --locked\nuv run streamlit run app.py\n"
        "uv run python -m pytest -v", STYLES["Code"]
    ))
    add_text(story, "Abrir la dirección local indicada por Streamlit. "
             "Seleccionar una jugada y pulsar el botón. El marcador "
             "pertenece a la sesión; recargar o cerrar la página puede "
             "reiniciarlo. No se añadió base de datos ni funciones extras.")
    add_text(story, f'<b>Código funcional:</b> <a href="{CODE_URL}" '
             'color="#155e75">abrir proyecto en GitHub</a>.')

    add_page(story, "2. Diagrama de flujo en Mermaid")
    add_image(story, "docs/flowchart.png", "Diagrama renderizado desde "
              "docs/flowchart.mmd. La selección por sí sola no juega una "
              "ronda; el botón actualiza un único contador.", 605)

    add_page(story, "3. Interfaz y resultado de una ronda")
    add_image(story, "docs/evidence/ui-controls.png", "Selección de "
              "piedra, papel o tijera y botón para jugar.", 190)
    story.append(Spacer(1, 14))
    add_image(story, "docs/evidence/ui-player-detail.png", "Victoria "
              "del jugador: piedra contra tijera. Se muestran ambas "
              "jugadas, el resultado y los tres contadores.", 335)

    add_page(story, "4. Derrota, empate y marcador")
    add_image(story, "docs/evidence/ui-computer-detail.png", "La "
              "computadora gana: papel contra piedra del jugador.", 265)
    story.append(Spacer(1, 12))
    add_image(story, "docs/evidence/ui-tie-detail.png", "Empate: ambas "
              "jugadas son piedra. Las capturas proceden de rondas "
              "reales; no se forzó la elección aleatoria.", 265)

    add_page(story, "5. Pruebas escritas antes de implementar")
    add_text(story, "Las expectativas salen de las reglas: nueve pares "
             "válidos y diez entradas inválidas. La función inicial solo "
             "lanzaba NotImplementedError. Las mismas pruebas se "
             "ejecutaron en rojo y en verde, sin cambiar sus expectativas.")
    add_image(story, "docs/evidence/tdd-tests-detail.png", "Código "
              "completo de tests/test_game.py usado en las dos fases.", 535)

    add_page(story, "6. TDD: fase roja")
    add_text(story, "Comando: <b>python -m pytest tests/test_game.py "
             "-v --tb=short --color=no</b>. Resultado real: <b>19 failed</b>, "
             "por NotImplementedError; código de salida 1.")
    add_image(story, "docs/evidence/tdd-red-output.png", "Vista de la "
              "salida real guardada. Se muestra el resumen y el primer "
              "fallo; tdd-red.txt conserva la salida completa.", 545)

    add_page(story, "7. TDD: fase verde y verificación final")
    add_text(story, "Se implementaron la validación, el empate y las tres "
             "parejas ganadoras. El mismo comando produjo <b>19 passed</b>, "
             "con código de salida 0. No se modificó tests/test_game.py.")
    add_image(story, "docs/evidence/tdd-green-output.png", "Salida "
              "real de la fase verde. Las capturas comparativas completas "
              "con código y salida están en docs/evidence/tdd-red.png "
              "y tdd-green.png.", 405)
    add_text(story, "Comprobación final: <b>22 pruebas aprobadas</b>. "
             "AppTest verificó los tres resultados, dos clics sucesivos, "
             "la selección sin sumar puntos y sesiones independientes. "
             "También se revisaron sintaxis, docstrings y estilo básico.")
    checksum = (PROJECT / "docs/evidence/test-hash-red.txt").read_text()
    add_text(story, "SHA-256 del archivo de pruebas, idéntico antes "
             f"y después de implementar: <font size='8'>{checksum.strip()}"
             "</font>.")
    add_text(story, "Las imágenes de TDD muestran el archivo y la salida "
             "guardada de ejecuciones reales. Son vistas de esa evidencia, "
             "no fotografías de una terminal nativa. Los archivos de "
             "texto permiten revisar todos los fallos y resultados.")

    add_page(story, "8. Diálogo ilustrativo")
    dialogue = (PROJECT / "docs/conversation/illustrative-dialogue.md")
    paragraphs = dialogue.read_text(encoding="utf-8").split("\n\n")
    for paragraph in paragraphs[1:]:
        if paragraph.startswith("## "):
            add_text(story, escape(paragraph[3:]), "Heading2")
            continue
        text = paragraph.strip().replace("**", "").replace("`", "")
        text = text.replace("\n", " ")
        text = escape(text)
        text = text.replace("Estudiante:", "<b>Estudiante:</b>", 1)
        text = text.replace("Asistente:", "<b>Asistente:</b>", 1)
        add_text(story, text, "Dialogue")

    add_page(story, "9. Referencias")
    add_text(story, "Tercer examen parcial - Programación asistida por IA "
             "(editable), ejercicio 5, página 5. Dr. Miguel Jara Maldonado.")
    add_text(story, "Módulo 6. Verificación, pruebas y depuración: "
             "pruebas basadas en especificación y ciclo rojo-verde-refactor. "
             "Se consultaron especialmente las páginas 14, 16 y 28-43.")
    add_text(story, "Los PDF de ejercicios anteriores del repositorio "
             "se usaron como referencia de portada, apartados y evidencia.")
    add_text(story, '<a href="https://docs.streamlit.io/develop/concepts/'
             'architecture/session-state" color="#155e75">Streamlit: '
             'Session State</a>; <a href="https://docs.streamlit.io/develop/'
             'concepts/app-testing/cheat-sheet" color="#155e75">AppTest</a>; '
             '<a href="https://mermaid.js.org/config/usage.html" '
             'color="#155e75">Mermaid: renderizado</a>.')
    add_text(story, f'<b>Código del proyecto en GitHub:</b><br/>'
             f'<a href="{CODE_URL}" color="#155e75">{CODE_URL}</a>')

    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=42, rightMargin=42,
        topMargin=40, bottomMargin=40, title="Tercer parcial - Ejercicio 5",
        author="Jonathan Serna", subject="Juego y evidencia de TDD",
    )
    document.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(OUTPUT)


pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")
STYLES = getSampleStyleSheet()
for style_name in ("BodyText", "Heading1", "Heading2", "Heading3"):
    STYLES[style_name].fontName = "Arial"
STYLES["BodyText"].fontSize = 10
STYLES["BodyText"].leading = 14
STYLES["BodyText"].spaceAfter = 9
STYLES["Code"].fontSize = 10
STYLES["Code"].leading = 14
STYLES["Code"].textColor = colors.black
for style_name, size in (("Heading1", 18), ("Heading2", 12), ("Heading3", 11)):
    STYLES[style_name].fontName = "Arial-Bold"
    STYLES[style_name].fontSize = size
    STYLES[style_name].leading = size + 4
    STYLES[style_name].spaceAfter = 12
STYLES.add(ParagraphStyle(
    "Caption", parent=STYLES["BodyText"], fontSize=9, leading=12,
    textColor=colors.HexColor("#475569"), spaceAfter=10,
))
STYLES.add(ParagraphStyle(
    "Dialogue", parent=STYLES["BodyText"], fontSize=9.5, leading=13,
))
for name, size in (
    ("CoverTitle", 28), ("CoverSubtitle", 23), ("CoverName", 13)
):
    STYLES.add(ParagraphStyle(
        name, fontName="Arial", fontSize=size, leading=size + 8,
        alignment=TA_CENTER, spaceAfter=18,
    ))

if __name__ == "__main__":
    build_report()
