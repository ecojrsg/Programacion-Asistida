# -*- coding: utf-8 -*-
# @Author: Jonathan Serna
# @Date:   2026-11-12 10:36:06
# @Last Modified by:   Jonathan Serna
# @Last Modified time: 2026-11-12 10:46:56

"""Build the academic report from the preserved test evidence."""

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PROJECT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT.parent / (
    "PDFs ejercicios/Ejercicio_29_Pruebas_estacionamiento.pdf"
)
WIDTH = letter[0] - 84
STYLES = getSampleStyleSheet()


def configure_styles():
    """Match the typography and margins of the preceding exercise PDF."""
    font_dir = Path("C:/Windows/Fonts")
    for name, filename in (
        ("Arial", "arial.ttf"), ("Arial-Bold", "arialbd.ttf")
    ):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")
    for name in ("BodyText", "Heading1", "Heading2"):
        STYLES[name].fontName = "Arial"
    STYLES["BodyText"].fontSize = 10
    STYLES["BodyText"].leading = 14
    STYLES["BodyText"].spaceAfter = 9
    for name, size in (("Heading1", 18), ("Heading2", 12)):
        STYLES[name].fontName = "Arial-Bold"
        STYLES[name].fontSize = size
        STYLES[name].leading = size + 4
        STYLES[name].spaceAfter = 12
    STYLES["Code"].fontName = "Courier"
    STYLES["Code"].fontSize = 8.2
    STYLES["Code"].leading = 11
    STYLES["Code"].textColor = colors.black
    STYLES.add(ParagraphStyle(
        "Cell", parent=STYLES["BodyText"], fontSize=9, leading=12,
        spaceAfter=0,
    ))
    STYLES.add(ParagraphStyle(
        "Caption", parent=STYLES["BodyText"], fontSize=9, leading=12,
        textColor=colors.HexColor("#475569"),
    ))
    for name, size in (
        ("CoverTitle", 28), ("CoverSubtitle", 23), ("CoverName", 13)
    ):
        STYLES.add(ParagraphStyle(
            name, fontName="Arial", fontSize=size, leading=size + 8,
            alignment=TA_CENTER, spaceAfter=18,
        ))


def add_text(story, text, style="BodyText"):
    """Append a paragraph in the selected report style."""
    story.append(Paragraph(text, STYLES[style]))


def add_page(story, title):
    """Start a numbered section on a new page."""
    story.extend([PageBreak(), Paragraph(title, STYLES["Heading1"])])


def add_table(story, rows, widths):
    """Add a compact table with a repeated header and wrapped cells."""
    cells = [
        [Paragraph(escape(str(cell)), STYLES["Cell"]) for cell in row]
        for row in rows
    ]
    table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#94a3b8")),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([table, Spacer(1, 12)])


def draw_footer(canvas, document):
    """Draw the running exercise title and page number."""
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    if document.page > 1:
        canvas.drawString(42, 23, "Ejercicio 29 - Pruebas y cobertura")
    canvas.drawRightString(letter[0] - 42, 23, str(document.page))
    canvas.restoreState()


def build_report():
    """Assemble the specification, tests, results, and observations."""
    summary = json.loads(
        (PROJECT / "evidence/summary.json").read_text(encoding="utf-8-sig")
    )
    initial = summary["stages"]["initial"]
    full = summary["stages"]["full"]
    story = [Spacer(1, 105)]
    add_text(story, "29. Pruebas unitarias", "CoverTitle")
    add_text(story, "Estacionamiento y cobertura", "CoverSubtitle")
    story.append(Spacer(1, 60))
    add_text(story, "Jonathan Serna", "CoverName")
    add_text(story, "Ingeniería en Software", "CoverName")
    add_text(story, "Programación Asistida por Inteligencia Artificial",
             "CoverName")
    add_text(story, "12 de noviembre de 2026", "CoverName")

    add_page(story, "1. Objetivo y especificación")
    add_text(story, "Mi objetivo fue comprobar la función "
             "<b>calculate_toll</b> con pruebas basadas en su especificación. "
             "Primero preparé tres pruebas unitarias, después solicité a una "
             "IA las pruebas adicionales y finalmente medí la cobertura. "
             "Conservé intacto el archivo <b>parking_lot.py</b> recibido.")
    add_text(story, "Contrato proporcionado", "Heading2")
    story.append(Preformatted(
        'calculate_toll(minutes: int, type: str = "auto",\n'
        '               weekend: bool = False)', STYLES["Code"]
    ))
    add_table(story, [
        ["Regla", "Resultado esperado"],
        ["Minutos negativos", "Lanzar ValueError."],
        ["Primeros 15 minutos", "Estancia gratuita hasta el minuto 15."],
        ["Hora completa o fracción", "Redondear hacia arriba las horas."],
        ["Tarifas por hora", "Auto: $20. Moto: $10."],
        ["Otro tipo de vehículo", "Lanzar ValueError."],
        ["Fin de semana", "Aumentar la tarifa un 50 %."],
        ["Máximo por estancia", "$150, también con recargo."],
    ], [190, WIDTH - 190])
    add_text(story, "Ejemplos: <b>calculate_toll(90) = 40</b>; "
             '<b>calculate_toll(16, "moto") = 10</b>; '
             '<b>calculate_toll(120, "auto", True) = 60</b>.')

    add_page(story, "2. Tres pruebas unitarias iniciales")
    add_text(story, "Elegí una validación, el límite de gratuidad y un "
             "ejemplo de cobro. Cada prueba tiene una expectativa obtenida "
             "de la especificación. Las guardé en <b>test_initial.py</b>.")
    source = (PROJECT / "test_initial.py").read_text(encoding="utf-8")
    story.append(Preformatted(source[source.index("import unittest"):],
                              STYLES["Code"]))
    story.append(Spacer(1, 15))
    add_table(story, [
        ["Caso", "Esperado", "Resultado"],
        ["-1 minuto", "ValueError", "Aprobado"],
        ["15 minutos", "$0", "Aprobado"],
        ["90 minutos de auto", "$40", "Aprobado"],
    ], [260, 130, WIDTH - 390])
    add_text(story, f"Resultado real: <b>{initial['tests']} pruebas "
             f"aprobadas</b>, código de salida 0. La cobertura inicial fue "
             f"de <b>{initial['covered_lines']}/{initial['total_lines']} "
             "líneas (68.42 %)</b>; trace muestra 68 % al usar enteros.")
    add_text(story, "La salida completa está en "
             "<b>evidence/initial/tests.txt</b>. También recibí asistencia "
             "de IA al preparar estas tres pruebas; las distingo de la "
             "ampliación posterior solicitada a otro agente.", "Caption")

    add_page(story, "3. Generación de las demás pruebas con IA")
    add_text(story, "Después de ejecutar las tres pruebas, envié la "
             "especificación y sus expectativas a un agente separado. "
             "No le compartí la implementación. Así pude comparar el "
             "programa con el contrato sin pedir a la IA que imitara "
             "el comportamiento del código existente.")
    add_text(story, "Solicitud enviada (extractos literales)", "Heading2")
    request = (PROJECT / "docs/ai-request.md").read_text(encoding="utf-8")
    excerpts = [
        "Actúa como generador de pruebas adicionales, independiente de la "
        "implementación. Solo devuelve el código y una matriz breve; "
        "NO escribas archivos ni leas parking_lot.py ni otros ejercicios.",
        "Genera pruebas adicionales en una sola clase "
        "GeneratedTollTests(unittest.TestCase), importando calculate_toll "
        "desde parking_lot. Usa un método por caso, expectativas explícitas "
        "y breves docstrings.",
        "No pruebes contratos no especificados (float, None, mensajes "
        "exactos o tipo exacto del retorno). No adaptes expectativas a "
        "ningún código. Evita redundancias innecesarias.",
    ]
    for excerpt in excerpts:
        assert excerpt in request
        add_text(story, escape(excerpt))
    add_text(story, "El mensaje completo, incluida la especificación "
             "reproducida, está en <b>docs/ai-request.md</b>. La respuesta "
             "se incorporó en <b>test_generated.py</b>, con 31 métodos "
             "adicionales y sin cambiar sus expectativas.")
    add_table(story, [
        ["Grupo adicional", "Casos cubiertos"],
        ["Duración y redondeo", "0, 14, 16, 60, 61, 120 y 121 minutos."],
        ["Moto y fin de semana", "Tarifas de $10/$20 y recargo del 50 %."],
        ["Fronteras del máximo", "Antes, al alcanzar y al superar $150 "
         "cuando la tarifa permite esos importes."],
        ["Estancias largas", "Un día en auto y una semana en moto; "
         "el máximo es por estancia."],
        ["Tipos inválidos", "pension a 0, 15 y 60 minutos; truck a 60."],
    ], [170, WIDTH - 170])
    add_text(story, "La especificación fue el criterio de aceptación. "
             "Mantuve los fallos visibles; no los marqué como esperados "
             "ni ajusté las pruebas para que el código aprobara.")

    add_page(story, "4. Resultados y discrepancias")
    add_table(story, [
        ["Batería", "Total", "Pasan", "Fallan", "Errores"],
        ["Inicial", initial["tests"], initial["passed"], 0, 0],
        ["Adicional de IA", 31, full["passed"] - 3, full["failures"], 0],
        ["Completa", full["tests"], full["passed"], full["failures"], 0],
    ], [180, 87, 87, 87, WIDTH - 441])
    add_text(story, "La batería completa terminó con código de salida "
             "<b>1</b>: hubo diez fallos de aserción y ningún error de "
             "ejecución. Las tarifas ordinarias, el redondeo, la gratuidad "
             "para vehículos válidos y el recargo sí aprobaron los casos "
             "incluidos. Estos son todos los casos que fallaron:")
    add_table(story, [
        ["Entrada (minutos, tipo, fin de semana)", "Esperado", "Obtenido"],
        ['(421, "auto", False)', "$150", "$160"],
        ['(481, "auto", False)', "$150", "$180"],
        ['(901, "moto", False)', "$150", "$160"],
        ['(301, "auto", True)', "$150", "$180"],
        ['(601, "moto", True)', "$150", "$165"],
        ['(1440, "auto", False)', "$150", "$200"],
        ['(10080, "moto", False)', "$150", "$200"],
        ['(0, "pension", False)', "ValueError", "$0"],
        ['(15, "pension", False)', "ValueError", "$0"],
        ['(60, "pension", False)', "ValueError", "$0"],
    ], [300, 114, WIDTH - 414])
    add_text(story, "Los siete fallos de importe muestran que "
             "<b>min(total, 200)</b> usa un máximo de $200. Los tres fallos "
             "de validación muestran dos rutas: la gratuidad devuelve cero "
             "antes de validar el tipo, y la rama <b>pension</b> lo admite "
             "en estancias de pago. El contrato solo acepta auto y moto.")
    add_text(story, "Conservé estos defectos para respetar la consigna. "
             "Las trazas y los nombres de las diez pruebas están en "
             "<b>evidence/full/tests.txt</b>.")

    add_page(story, "5. Prueba de cobertura")
    add_text(story, "Medí únicamente la cobertura de líneas de "
             "<b>parking_lot.py</b> con trace. El porcentaje indica cuántas "
             "de sus líneas ejecutables se ejecutaron al menos una vez; "
             "incluye la carga del módulo. No medí cobertura de ramas.")
    add_table(story, [
        ["Batería", "Ejecutadas / total", "Sin ejecutar", "Cobertura"],
        ["Tres pruebas iniciales", "13 / 19", "6", "68.42 %"],
        ["Batería completa", "19 / 19", "0", "100 %"],
    ], [180, 140, 105, WIDTH - 425])
    add_text(story, "Listado final real de trace", "Heading2")
    coverage = (PROJECT / "evidence/full/parking_lot.cover").read_text(
        encoding="utf-8"
    )
    story.append(Preformatted(coverage, STYLES["Code"]))
    story.append(Spacer(1, 10))
    add_text(story, "Los números a la izquierda son conteos de ejecución. "
             "El archivo inicial marca con <b>&gt;&gt;&gt;&gt;&gt;&gt;</b> "
             "las seis líneas que faltaban. En el listado final no queda "
             "ninguna de esas marcas. La rama incorrecta de pension "
             "también se ejecutó al comprobar que debía rechazarse.",
             "Caption")
    add_text(story, "La salida completa está en "
             "<b>evidence/full/coverage-run.txt</b>. El 100 % corresponde "
             "al módulo evaluado; no se usa el porcentaje de los archivos "
             "de pruebas para justificar su calidad.", "Caption")

    add_page(story, "6. Observaciones y reproducción")
    add_text(story, "Párrafo de observaciones", "Heading2")
    add_text(story, "Al ejecutar las pruebas observé que las tres iniciales "
             "aprobaron, pero solo cubrieron 13 de las 19 líneas reportadas "
             "por trace, equivalentes al 68.42 %. Después de ampliar los "
             "casos con IA alcancé el 100 % de cobertura de líneas; aun "
             "así, 10 de las 34 pruebas fallaron. Esto me permitió distinguir "
             "entre ejecutar todo el código y cumplir la especificación. "
             "Los fallos se concentraron en el máximo por estancia, que "
             "el programa limita a $200 en lugar de $150, y en la "
             "aceptación de pension, incluido el periodo gratuito donde "
             "se devuelve cero antes de validar el vehículo. Los límites "
             "de minutos y del tope ayudaron a detectar diferencias que "
             "los ejemplos habituales no mostraban. Conservé "
             "parking_lot.py sin cambios para documentar el resultado "
             "real. Como estudiante de Ingeniería en Software, concluyo "
             "que necesito revisar tanto la cobertura como las aserciones "
             "y sus resultados; además, esta medición no demuestra "
             "cobertura de ramas ni prueba entradas fuera del contrato.")
    add_text(story, "Cómo reproducir", "Heading2")
    add_text(story, "Desde la carpeta <b>29vo Pruebas estacionamiento</b>, "
             "con Python 3.12, puedo ejecutar:")
    story.append(Preformatted(
        "python -B -m unittest -v test_initial\n"
        "python -B -m unittest -v test_initial test_generated\n\n"
        "python -B -m trace --count --missing --summary \\\n"
        "  --coverdir evidence/reproduced --module unittest \\\n"
        "  -v test_initial test_generated", STYLES["Code"]
    ))
    add_text(story, "Las barras inversas anteriores indican continuación "
             "visual; en PowerShell uno las líneas en un único comando. "
             "El README incluye comandos de una sola línea y un filtro "
             "para omitir la biblioteca estándar en el informe. Ejecuto "
             "unittest también por separado porque trace captura "
             "SystemExit y su código de salida no refleja esos fallos.")
    add_text(story, '<a href="https://docs.python.org/3.12/library/'
             'unittest.html" color="#155e75">Python 3.12: unittest</a>; '
             '<a href="https://docs.python.org/3.12/library/trace.html" '
             'color="#155e75">Python 3.12: trace</a>.', "Caption")
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=42, rightMargin=42,
        topMargin=40, bottomMargin=40,
        title="29. Pruebas unitarias y cobertura",
        author="Jonathan Serna", subject="Pruebas del estacionamiento",
    )
    document.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(OUTPUT)


if __name__ == "__main__":
    configure_styles()
    build_report()
