#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el PDF de la Actividad 3 (Gestión de Inventarios y S&OP) con ReportLab."""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "actividad3-inventarios")
PDF_PATH = os.path.join(OUT_DIR, "Actividad3_Gestion_de_Inventarios_SOP.pdf")

NAVY = colors.HexColor("#1F3864")
ACCENT = colors.HexColor("#C00000")
GRAY = colors.HexColor("#595959")
HDR = colors.HexColor("#1F3864")
ALT = colors.HexColor("#F2F5FA")
LIGHT = colors.HexColor("#D9E2F3")

styles = getSampleStyleSheet()

S_TITLE = ParagraphStyle("TitleC", parent=styles["Title"], fontName="Helvetica-Bold",
                         fontSize=26, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=6)
S_SUB = ParagraphStyle("SubC", parent=styles["Normal"], fontName="Helvetica-Bold",
                       fontSize=19, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)
S_SUB2 = ParagraphStyle("Sub2", parent=styles["Normal"], fontName="Helvetica-Oblique",
                        fontSize=13, textColor=GRAY, alignment=TA_CENTER, spaceAfter=4)
S_H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                      fontSize=15, textColor=NAVY, spaceBefore=14, spaceAfter=6)
S_H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                      fontSize=12.5, textColor=NAVY, spaceBefore=10, spaceAfter=4)
S_H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                      fontSize=11.5, textColor=NAVY, spaceBefore=8, spaceAfter=3)
S_BODY = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica",
                        fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
S_BULLET = ParagraphStyle("Bullet", parent=S_BODY, leftIndent=16, bulletIndent=4,
                          spaceAfter=3, alignment=TA_LEFT)
S_CAP = ParagraphStyle("Cap", parent=styles["Normal"], fontName="Helvetica-Oblique",
                       fontSize=8.5, textColor=GRAY, alignment=TA_CENTER, spaceBefore=3,
                       spaceAfter=10)
S_REF = ParagraphStyle("Ref", parent=S_BODY, alignment=TA_LEFT, leftIndent=18,
                       firstLineIndent=-18, spaceAfter=4)
S_COVER_NAME = ParagraphStyle("CN", parent=S_BODY, fontName="Helvetica",
                              fontSize=12, alignment=TA_CENTER, spaceAfter=2)
S_COVER_META = ParagraphStyle("CM", parent=S_BODY, fontName="Helvetica",
                              fontSize=10.5, alignment=TA_CENTER, spaceAfter=3)


def h1(t):
    return Paragraph(t, S_H1)


def h2(t):
    return Paragraph(t, S_H2)


def h3(t):
    return Paragraph(t, S_H3)


def body(t):
    return Paragraph(t, S_BODY)


def bullet(t, bold_prefix=None):
    if bold_prefix:
        return Paragraph(f"<b>{bold_prefix}</b> {t}", S_BULLET, bulletText="•")
    return Paragraph(t, S_BULLET, bulletText="•")


def caption(t):
    return Paragraph(t, S_CAP)


def story_table(headers, rows, widths, fs=8.5, header_fs=8.5):
    data = [[Paragraph(f"<b>{h}</b>", ParagraphStyle(
        "h", fontName="Helvetica-Bold", fontSize=header_fs, leading=header_fs + 2,
        textColor=colors.white, alignment=TA_CENTER)) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), ParagraphStyle(
            "c", fontName="Helvetica", fontSize=fs, leading=fs + 2.5,
            alignment=TA_CENTER if _is_num(str(c)) else TA_LEFT)) if not _is_para(c)
            else c for c in r])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HDR),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0B7C3")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ALT))
    t.setStyle(TableStyle(style))
    return t


def _is_num(s):
    try:
        float(str(s).replace(",", "").replace("%", "").replace("$", ""))
        return True
    except Exception:
        return False


def _is_para(c):
    return isinstance(c, Paragraph)


def fig(path, w, cap):
    im = Image(path, width=w * inch, height=w * inch * 0.56)
    im.hAlign = "CENTER"
    return [im, caption(cap)]


story = []

# ================= PORTADA =================
story += [Spacer(1, 1.4 * inch)]
story.append(Paragraph("Actividad 3", S_TITLE))
story.append(Paragraph("¿Para qué sirven los inventarios en las empresas?", S_SUB))
story.append(Paragraph("Gestión de inventarios, metodologías y proceso S&amp;OP", S_SUB2))
story.append(Paragraph("Caso: Distribuidora de productos electrónicos “XYZ” (Latinoamérica)", S_SUB2))
story.append(Spacer(1, 0.5 * inch))
story.append(Paragraph("Equipo", ParagraphStyle("eq", parent=S_SUB, fontSize=14)))
team = [
    ("Adrián Corpi Villaseñor", "AL03044078"),
    ("Erick Díaz", "AL03007876"),
    ("Patricio Ulises Morales", "AL07098185"),
]
for name, mat in team:
    story.append(Paragraph(f"{name} — {mat}", S_COVER_NAME))
story.append(Spacer(1, 0.4 * inch))
story.append(Paragraph("Materia / Curso: Gestión de Inventarios y Cadena de Suministro", S_COVER_META))
story.append(Paragraph("Fecha de entrega: Septiembre de 2026", S_COVER_META))
story.append(PageBreak())

# ================= ÍNDICE =================
story.append(h1("Índice"))
for it in [
    "1. Contexto del caso: la empresa “XYZ”",
    "2. Clasificación de los tipos de inventario y costos asociados",
    "3. Metodología de gestión de inventarios recomendada (justificación)",
    "4. Priorización de productos: análisis ABC–XYZ y productos clave",
    "5. Pronóstico de demanda y planificación del requerimiento de inventario",
    "6. Cronograma de reuniones de S&OP: fases del proceso",
    "7. Conclusiones",
    "8. Referencias y fuentes de apoyo",
]:
    story.append(Paragraph(it, ParagraphStyle("idx", parent=S_BODY, leftIndent=18,
                                              spaceAfter=4, alignment=TA_LEFT)))
story.append(PageBreak())

# ================= 1. CONTEXTO =================
story.append(h1("1. Contexto del caso: la empresa “XYZ”"))
story.append(body(
    "“XYZ” es una empresa dedicada a la distribución de productos electrónicos en Latinoamérica. "
    "Su portafolio incluye smartphones, laptops, televisores, tabletas, audio, wearables y "
    "accesorios que se abastecen principalmente de proveedores asiáticos, con tiempos de entrega "
    "(lead time) de entre 3 y 9 semanas en su mayoría."))
story.append(body(
    "Recientemente la empresa ha presentado problemas significativos de gestión de inventario que "
    "se traducen en tres síntomas principales:"))
story.append(bullet("elevados costos de almacenamiento (exceso de stock y capital inmovilizado)."))
story.append(bullet("rupturas de stock o stock outs (venta perdida y fallas de servicio al cliente)."))
story.append(bullet("sobreinventario de productos de baja rotación y obsolescencia tecnológica."))
story.append(body(
    "Ante ello, la dirección ha decidido implementar un proyecto de mejora para optimizar la "
    "gestión de inventarios mediante metodologías avanzadas (ABC–XYZ, EOQ, punto de reorden, "
    "pronóstico de demanda, MRP y Kanban) dentro de un proceso formal de S&OP (Sales &amp; "
    "Operations Planning). Este documento desarrolla, con datos de referencia, las cuatro "
    "entregas solicitadas."))

# ================= 2. TIPOS Y COSTOS =================
story.append(h1("2. Clasificación de los tipos de inventario y sus costos"))
story.append(body(
    "Para una distribuidora de electrónicos, el inventario no es un solo bloque: conviene "
    "clasificarlo según su función dentro de la cadena de suministro, porque cada tipo obedece a "
    "una lógica distinta y se asocia a costos distintos."))
story.append(h2("2.1 Tipos de inventario"))
story.append(story_table(
    ["Tipo de inventario", "Descripción", "Ejemplo en XYZ", "Costo dominante"],
    [
        ("Ciclo (cycle stock)", "Stock que cubre la demanda normal entre un pedido y otro.",
         "Cajas de smartphones que cubren la venta mientras llega el siguiente lote.",
         "Mantenimiento y de ordenar."),
        ("De seguridad", "Colchón contra variabilidad de demanda y de suministro.",
         "Unidades extra de laptops en temporada escolar alta.",
         "Mantenimiento (capital) + faltante evitado."),
        ("En tránsito (pipeline)", "Mercancía pagada y en movimiento proveedor → almacén.",
         "Contenedores de TVs OLED navegando desde Asia (45–60 días).",
         "Capital inmovilizado + seguro y flete."),
        ("De anticipación / estacional", "Se acumula antes de picos conocidos de demanda.",
         "Acopio de audífonos y wearables para Buen Fin / Black Friday.",
         "Mantenimiento; riesgo de no vender todo."),
        ("Producto terminado", "Artículos listos para venta/distribución.",
         "Inventario en centros de distribución regionales (México, Colombia, Perú…).",
         "Mantenimiento y de oportunidad."),
        ("MRO", "Materiales auxiliares no vendibles para operar.",
         "Empaque, cintas, repuestos de montacargas, etiquetas.",
         "De ordenar y mantenimiento menores."),
        ("Especulativo", "Compra anticipada esperando alzas de precio o tipo de cambio.",
         "Compra adelantada de memorias/chips ante escasez.",
         "Mantenimiento + riesgo financiero."),
    ],
    [1.15 * inch, 2.15 * inch, 2.15 * inch, 1.55 * inch], fs=8))
story.append(caption("Tabla 1. Tipos de inventario aplicables a una distribuidora de productos electrónicos."))

story.append(h2("2.2 Costos asociados a los inventarios"))
story.append(body("Los costos que explican la crisis de XYZ pueden agruparse en cinco categorías:"))
story.append(story_table(
    ["Costo", "Fórmula / descripción", "Impacto en XYZ"],
    [
        ("De adquisición / compra",
         "Costo unitario C más flete, aranceles y seguro. Costo anual = C × D.",
         "Es la base del valor de inventario; en electrónicos puede ser 60–80 % del precio de venta."),
        ("De ordenar / preparación",
         "S = costo administrativo + transporte por pedido. Nº pedidos = D/Q.",
         "Pedidos frecuentes y chicos (pull) elevan el gasto administrativo y de flete."),
        ("De mantenimiento / almacenaje",
         "H = i × C (i = tasa anual, típicamente 18–30 %): capital, espacio, seguro, mermas, obsolescencia.",
         "Causa directa del problema de “altos costos de almacenamiento”."),
        ("Por faltantes (stock out)",
         "Margen perdido + urgencias de reabasto + penalización + pérdida de imagen.",
         "Cuanto más crítico el SKU (clase A), más caro es el faltante."),
        ("Por sobreinventario / obsolescencia",
         "Valor de ítems sin salida, remates a precio bajo y espacio ocupado.",
         "El ciclo corto de la electrónica hace que el exceso se deprecie muy rápido."),
    ],
    [1.4 * inch, 2.8 * inch, 2.8 * inch], fs=8))
story.append(caption("Tabla 2. Costos del inventario y su relación con la problemática de XYZ."))
story.append(body(
    "El equilibrio se logra minimizando la suma de los costos de ordenar y de mantener, "
    "protegiéndose al mismo tiempo contra el costo de faltante. En la sección 5 se calculan el "
    "lote económico (EOQ), el stock de seguridad y el punto de reorden para los dos productos "
    "clave."))

# ================= 3. METODOLOGÍA =================
story.append(h1("3. Metodología de gestión de inventarios recomendada"))
story.append(h2("3.1 Comparación de metodologías"))
story.append(story_table(
    ["Metodología", "Lógica", "Fortalezas", "Riesgos / límites"],
    [
        ("Push (empujar)", "Producir/comprar según pronóstico y empujar al canal (MRP).",
         "Escala, economías de lote, ideal para lanzamientos y promociones.",
         "Si el pronóstico falla, genera sobreinventario y obsolescencia."),
        ("Pull (jalar)", "Reabastecer solo según consumo real del cliente.",
         "Bajo inventario, responde a la demanda real.",
         "Requiere lead times cortos y demanda predecible."),
        ("Por demanda", "Todo se planea a partir del pronóstico de demanda.",
         "Visibilidad y planeación agregada (base del S&OP).",
         "La calidad depende del pronóstico; rigidez ante cambios súbitos."),
        ("Kanban / JIT", "Señal de reabasto por tarjetas o contenedores al bajar el nivel.",
         "Visual, autocontrolado, mínimo desperdicio, flujo continuo.",
         "Sensible a variabilidad; no admite lead times largos."),
    ],
    [0.85 * inch, 1.85 * inch, 1.8 * inch, 1.75 * inch], fs=7.8))
story.append(caption("Tabla 3. Comparación de metodologías de gestión de inventarios."))

story.append(h2("3.2 Metodología seleccionada y justificación"))
story.append(body(
    "Para una distribuidora de electrónicos con lead times largos (3–9 semanas) y alta "
    "variabilidad, no existe una sola metodología correcta. Recomendamos un enfoque híbrido "
    "gobernado por S&OP:"))
story.append(bullet("para la base del portafolio y los reaprovisionamientos recurrentes, un "
                    "sistema Pull con Kanban (tarjetas/bins y reabastecimiento por consumo real), "
                    "que reduce el sobreinventario y alinea el stock con la rotación real."))
story.append(bullet("para lanzamientos, promociones (Buen Fin, Black Friday) y productos de "
                    "temporada, planeación Push apoyada en MRP y en el pronóstico de demanda, "
                    "porque la demanda “empujada” por marketing no puede jalar sola."))
story.append(bullet("para los artículos críticos (clase A), control continuo con punto de "
                    "reorden (ROP) y stock de seguridad calculado estadísticamente."))
story.append(bullet("todo sincronizado mensualmente por el proceso S&OP, que concilia la "
                    "demanda (ventas y marketing) con el suministro (compras, logística y "
                    "finanzas)."))
story.append(body(
    "Justificación: el Kanban puro exige lead times cortos y demanda estable, lo cual no aplica a "
    "importaciones desde Asia con 45+ días de tránsito; el Push puro volvería a inflar el almacén "
    "y a multiplicar la obsolescencia (el origen del problema de XYZ). El híbrido Pull+Kanban en "
    "la rotación diaria y Push/MRP en las excepciones, con la disciplina del S&OP como “semáforo” "
    "mensual, maximiza el nivel de servicio con el mínimo capital inmovilizado."))

# ================= 4. ABC-XYZ =================
story.append(h1("4. Priorización de productos: análisis ABC–XYZ"))
story.append(body(
    "Se clasificó un portafolio de referencia de 10 SKU según su valor anual de consumo "
    "(costo unitario × demanda anual) y la variabilidad de la demanda (coeficiente de variación, "
    "CV). El cruce ABC–XYZ permite definir la política de control de cada grupo."))
story += fig(os.path.join(OUT_DIR, "fig_pareto.png"), 6.6,
             "Figura 1. Análisis ABC (Pareto) del valor anual de consumo del portafolio de XYZ.")
story.append(story_table(
    ["Producto / categoría", "Costo unit.", "Demanda anual", "Valor anual", "Part.", "Acum.",
     "ABC", "Variab.", "ABC–XYZ"],
    [
        ("Flagship 5G Smartphone", "$450", "25,040", "$11,268,000", "48.2 %", "48.2 %", "A", "Baja (0.11)", "AX"),
        ("Business Laptop 14”", "$750", "6,020", "$4,515,000", "19.3 %", "67.5 %", "A", "Media (0.17)", "AY"),
        ("Smart OLED TV 55” 4K", "$550", "4,200", "$2,310,000", "9.9 %", "77.4 %", "B", "Media (0.22)", "BY"),
        ("Tablet 10” gama media", "$220", "7,500", "$1,650,000", "7.1 %", "84.5 %", "B", "Media (0.19)", "BY"),
        ("Audífonos cancelación", "$120", "9,000", "$1,080,000", "4.6 %", "89.1 %", "B", "Media (0.15)", "BY"),
        ("Smartwatch / banda", "$85", "11,000", "$935,000", "4.0 %", "93.1 %", "C", "Media (0.25)", "CY"),
        ("Cámara de seguridad", "$60", "8,500", "$510,000", "2.2 %", "95.3 %", "C", "Alta (0.28)", "CZ"),
        ("Cargadores rápidos GaN", "$18", "28,000", "$504,000", "2.2 %", "97.4 %", "C", "Baja (0.09)", "CX"),
        ("Bocinas Bluetooth", "$45", "7,200", "$324,000", "1.4 %", "98.8 %", "C", "Alta (0.32)", "CZ"),
        ("Kits de cables HDMI/USB-C", "$8", "35,000", "$280,000", "1.2 %", "100.0 %", "C", "Baja (0.07)", "CX"),
    ],
    [1.55 * inch, 0.62 * inch, 0.72 * inch, 0.95 * inch, 0.5 * inch, 0.5 * inch, 0.4 * inch,
     0.68 * inch, 0.6 * inch], fs=7.2))
story.append(caption("Tabla 4. Portafolio clasificado por ABC (valor) y XYZ (variabilidad). "
                     "Valor total ≈ $23.4 M."))

story.append(h2("4.1 Política de control por grupo"))
story.append(bullet("Clase A (≈68 % del valor con ≈20 % de los SKU): control estricto, conteo "
                    "cíclico frecuente, pronóstico y stock de seguridad por SKU, revisión "
                    "continua y nivel de servicio 97–98 %."))
story.append(bullet("Clase B (≈21 % del valor): revisión periódica quincenal/mensual y nivel "
                    "de servicio medio-alto (95 %)."))
story.append(bullet("Clase C (≈11 % del valor, muchos SKU): control simple con sistema "
                    "periódico (min–max) o Kanban de tarjetas y nivel de servicio 90–95 %, "
                    "liberando tiempo del equipo."))
story.append(bullet("El eje XYZ refina la política: los AX (alto valor, demanda estable) se "
                    "manejan con Kanban/mínimo-máximo y justo a tiempo; los AZ o CZ (erráticos) "
                    "requieren más stock de seguridad o revisión más frecuente."))

story.append(h2("4.2 Los dos productos principales y su valor en la cadena"))
story.append(body("Los dos productos que, por su impacto conjunto en costo, volumen y tiempo de "
                  "reabastecimiento, deben priorizarse son:"))
story.append(Paragraph("<b>1) Flagship 5G Smartphone (AX, $11.27 M/año — 48 % del valor del "
                       "portafolio).</b> Justificación: es el mayor generador de margen e "
                       "ingresos; su ciclo de vida es corto (≈12 meses), por lo que un error de "
                       "pronóstico o un exceso de inventario se transforma muy rápido en "
                       "obsolescencia y remates. Su demanda es relativamente estable (CV ≈ 0.11), "
                       "lo que permite un control ajustado con stock de seguridad bajo.", S_BULLET,
                       bulletText="•"))
story.append(Paragraph("<b>2) Ultra-Slim Business Laptop 14” (AY, $4.51 M/año — 19 % del valor)."
                       "</b> Justificación: segundo generador de valor con el mayor costo "
                       "unitario ($750) y compradores B2B/empresa muy sensibles al stock-out; un "
                       "faltante aquí no solo pierde la venta, puede perder el contrato completo. "
                       "Su demanda es moderadamente variable e influida por el ciclo escolar y el "
                       "cierre fiscal corporativo.", S_BULLET, bulletText="•"))
story.append(body(
    "En conjunto representan ≈68 % del valor anual de consumo, por lo que concentran la mayoría "
    "de las decisiones de pronóstico, stock de seguridad y reabastecimiento (los cálculos de la "
    "sección 5 se desarrollan sobre estos dos SKU)."))

# ================= 5. PRONÓSTICO =================
story.append(h1("5. Pronóstico de demanda y planificación del requerimiento"))
story.append(h2("5.1 Método de pronóstico"))
story.append(body(
    "Se utilizó regresión lineal de tendencia sobre 12 meses de historia (mínimos cuadrados) y, "
    "como validación, media móvil de 3 meses y suavizamiento exponencial (α = 0.3). Se eligió la "
    "línea de tendencia por su menor error (MAPE) y porque captura el crecimiento sostenido del "
    "mercado. La demanda estimada se expresa como:"))
story.append(Paragraph("Demanda_estimada (mes t) = a + b × t", ParagraphStyle(
    "eq2", parent=S_BODY, fontName="Helvetica-Oblique", alignment=TA_CENTER)))
story += fig(os.path.join(OUT_DIR, "fig_forecast.png"), 6.6,
             "Figura 2. Histórico (12 meses) y pronóstico (6 meses) de los dos productos clave.")
story.append(Paragraph("<b>Nota de la Figura 2.</b> Smartphone: ecuación D = 1,690.3 + 61.0 × "
                       "mes; demanda media 2,087 u/mes; σ = 239; MAPE 3.4 %; MAD 74 un. Laptop: "
                       "D = 352.1 + 23.0 × mes; media 502 u/mes; σ = 88; MAPE 4.6 %; MAD 24 un. "
                       "Los MAPE < 5 % indican un pronóstico muy bueno.", ParagraphStyle(
                           "cap2", parent=S_CAP, alignment=TA_LEFT)))

story.append(h2("5.2 Parámetros de planificación (EOQ, stock de seguridad, ROP)"))
story.append(body(
    "Supuestos de referencia: costo de ordenar S = $1,500/orden; tasa anual de mantenimiento "
    "i = 25 % del costo unitario; nivel de servicio objetivo 95 % (z = 1.645) para clase A; "
    "lead time L = 1.5 meses (≈45 días). Fórmulas aplicadas:"))
story.append(bullet("Lote económico: EOQ = √(2DS/H), con D = demanda anual y H = costo de "
                    "mantener por unidad por año."))
story.append(bullet("Stock de seguridad: SS = z × √L × σ_mensual."))
story.append(bullet("Punto de reorden: ROP = (d_promedio × L) + SS."))
story.append(story_table(
    ["Concepto", "Fórmula", "Smartphone 5G", "Laptop 14”"],
    [
        ("Demanda anual (D)", "Σ demanda mensual", "25,040 u. (≈2,087/mes)", "6,020 u. (≈502/mes)"),
        ("Costo de mantener (H)", "i × C", "0.25 × $450 = $112.50/año", "0.25 × $750 = $187.50/año"),
        ("Lote económico (EOQ)", "√(2DS/H)", "≈ 817 → lote práctico 1,000 u.", "≈ 310 → lote práctico 350 u."),
        ("Nº de pedidos al año", "D / lote", "≈ 25 (≈ cada 2 semanas)", "≈ 17 (≈ cada 3 semanas)"),
        ("Stock de seguridad (SS)", "z × √L × σ", "1.645 × √1.5 × 239 ≈ 481 u.", "1.645 × √1.5 × 88 ≈ 178 u."),
        ("Punto de reorden (ROP)", "d̄ × L + SS", "3,130 + 481 ≈ 3,611 u.", "753 + 178 ≈ 931 u."),
    ],
    [1.75 * inch, 1.1 * inch, 2.1 * inch, 2.1 * inch], fs=8))
story.append(caption("Tabla 5. Parámetros de control de inventario para los dos productos "
                     "clave. La desviación durante el lead time es σ_L = √L × σ_mensual."))

story.append(h2("5.3 Planificación del requerimiento de inventario (MRP)"))
story.append(body(
    "Con el pronóstico de los próximos 6 meses (meses 13 a 18), se calculó el requerimiento neto "
    "y las liberaciones de pedido con MRP (lead time de 2 meses y lotes fijos iguales al EOQ "
    "redondeado: 1,000 y 350 unidades; stock de seguridad 481 y 178 unidades)."))
story.append(h3("Smartphone 5G (lote 1,000 u., SS 481 u.)"))
story.append(story_table(
    ["Concepto", "M1", "M2", "M3", "M4", "M5", "M6"],
    [
        ("Requerimiento bruto", "2,483", "2,544", "2,605", "2,666", "2,727", "2,788"),
        ("Recepciones programadas", "2,000", "—", "—", "—", "—", "—"),
        ("Disponible proyectado", "2,317", "773", "1,168", "502", "775", "987"),
        ("Requerimiento neto", "0", "708", "2,313", "1,979", "2,706", "2,494"),
        ("Recepción planificada", "—", "1,000", "3,000", "2,000", "3,000", "3,000"),
        ("Liberación planificada (LT = 2)", "3,000", "2,000", "3,000", "3,000", "—", "—"),
    ],
    [1.95 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch], fs=8))
story.append(caption("Tabla 6. Plan MRP del smartphone (unidades). Liberaciones a 2 meses de "
                     "anticipación: M1=3,000 · M2=2,000 · M3=3,000 · M4=3,000."))
story.append(h3("Business Laptop 14” (lote 350 u., SS 178 u.)"))
story.append(story_table(
    ["Concepto", "M1", "M2", "M3", "M4", "M5", "M6"],
    [
        ("Requerimiento bruto", "651", "674", "697", "720", "743", "766"),
        ("Recepciones programadas", "600", "—", "—", "—", "—", "—"),
        ("Disponible proyectado", "799", "475", "478", "458", "415", "349"),
        ("Requerimiento neto", "0", "53", "400", "420", "463", "529"),
        ("Recepción planificada", "—", "350", "700", "700", "700", "700"),
        ("Liberación planificada (LT = 2)", "700", "700", "700", "700", "—", "—"),
    ],
    [1.95 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch], fs=8))
story.append(caption("Tabla 7. Plan MRP de la laptop (unidades). Liberaciones a 2 meses de "
                     "anticipación: M1=M2=M3=M4=700."))
story.append(body(
    "Interpretación: el stock inicial más las recepciones en tránsito cubren el primer mes; a "
    "partir de ahí se liberan pedidos con dos meses de anticipación para cubrir la demanda sin "
    "caer por debajo del stock de seguridad. El lote es un múltiplo del EOQ redondeado (1,000 y "
    "350 unidades), por lo que, en promedio, el smartphone se pide unas 25 veces al año y la "
    "laptop unas 17. Esto traduce el pronóstico en un plan de compras concreto y en compromisos "
    "de capacidad con los proveedores."))

# ================= 6. S&OP =================
story.append(h1("6. Cronograma de reuniones de S&OP: fases del proceso"))
story.append(h2("6.1 Las cinco fases del proceso S&OP"))
story.append(body(
    "El proceso S&OP es un ciclo mensual de planeación táctica que integra ventas, operaciones, "
    "compras, finanzas y dirección. Sus cinco fases son:"))
story.append(story_table(
    ["Fase", "Objetivo", "Salidas", "Dueño"],
    [
        ("1. Revisión de datos", "Actualizar cifras reales: ventas, inventario, pedidos, "
         "cumplimiento y errores de pronóstico.",
         "Base de datos única y confiable (single source of truth).",
         "Planeador de demanda / Analista de datos (días 1–3)."),
        ("2. Pronóstico de demanda", "Generar el pronóstico consensuado por SKU/familia "
         "(estadístico + aportes de ventas y marketing).",
         "Pronóstico base + escenarios alto/bajo por familia.",
         "Gerente de demanda / Ventas y Marketing (días 4–7)."),
        ("3. Revisión de suministro", "Validar capacidad, proveedores, inventario y "
         "restricciones para cumplir el pronóstico.",
         "Plan de suministro, inventarios proyectados, brechas de capacidad.",
         "Gerente de operaciones / Compras y Logística (días 8–10)."),
        ("4. Reconciliación / Pre-S&OP", "Confrontar demanda vs. suministro y preparar "
         "escenarios con impacto financiero.",
         "Escenarios conciliados y recomendaciones para la dirección.",
         "Líder de S&OP / Finanzas (días 11–12)."),
        ("5. Reunión ejecutiva", "Revisar escenarios, decidir, aprobar el plan único y "
         "asignar responsables.",
         "Plan operativo aprobado (ventas + operaciones + inventario + financiero).",
         "Dirección general (días 13–15)."),
    ],
    [1.35 * inch, 2.35 * inch, 2.05 * inch, 1.3 * inch], fs=7.4))
story.append(caption("Tabla 8. Fases del proceso mensual de S&OP (adaptado de APICS/ASCM)."))

story.append(h2("6.2 Cadencia mensual (cronograma tipo)"))
story.append(story_table(
    ["Semana del mes", "Actividad", "Resultado"],
    [
        ("Semana 1 (días 1–5)", "Fase 1: cierre y revisión de datos; arranque del pronóstico.",
         "Base de datos validada."),
        ("Semana 2 (días 6–12)", "Fase 2 (cierre): consenso de demanda; Fase 3: revisión de suministro.",
         "Pronóstico y plan de suministro preliminares."),
        ("Semana 3 (días 13–20)", "Fase 4: reconciliación y escenarios financieros (Pre-S&OP).",
         "Escenarios conciliados con impacto $."),
        ("Semana 4 (días 21–30)", "Fase 5: reunión ejecutiva; aprobación y comunicación del plan.",
         "Plan único aprobado + acciones."),
    ],
    [1.5 * inch, 3.3 * inch, 2.2 * inch], fs=8))
story.append(caption("Tabla 9. Cadencia estándar de un ciclo mensual de S&OP."))

story.append(h2("6.3 Cronograma anual de reuniones ejecutivas"))
story.append(body(
    "La reunión ejecutiva (fase 5) se celebra el último jueves de cada mes (excepto festivos, en "
    "cuyo caso se recorre al jueves anterior); el resto de fases se repite cada mes con el "
    "calendario de la Tabla 9. Cada trimestre, la fase ejecutiva incluye además una revisión de "
    "portafolio (ABC) y de parámetros de inventario (EOQ, SS, ROP)."))
cal_rows = [
    ("Ciclo 1 — Octubre 2026", "Cierre y ajuste del plan anual; parámetros de inventario A."),
    ("Ciclo 2 — Noviembre 2026", "Revisión post-pico promocional (Buen Fin); forecast dic–feb."),
    ("Ciclo 3 — Diciembre 2026", "Cierre de año; plan de inventario de fin de periodo."),
    ("Ciclo 4 — Enero 2027", "Revisión trimestral ABC–XYZ; ajuste de stock de seguridad."),
    ("Ciclo 5 — Febrero 2027", "Preparación de la temporada escolar (laptops y tabletas)."),
    ("Ciclo 6 — Marzo 2027", "Evaluación de lanzamientos y del ciclo de vida de SKU."),
    ("Ciclo 7 — Abril 2027", "Revisión trimestral ABC–XYZ y de plazos de proveedores."),
    ("Ciclo 8 — Mayo 2027", "Planeación de demanda de mitad de año (Día de las Madres)."),
    ("Ciclo 9 — Junio 2027", "Cierre fiscal H1; reconciliación de presupuesto vs. real."),
    ("Ciclo 10 — Julio 2027", "Revisión trimestral ABC–XYZ; renovación de portafolio."),
    ("Ciclo 11 — Agosto 2027", "Preparación de temporada alta Q4 (Black Friday, fiestas)."),
    ("Ciclo 12 — Septiembre 2027", "Balance anual y arranque del planning del año siguiente."),
]
story.append(story_table(["Ciclo / Mes", "Enfoque principal de la reunión ejecutiva"],
                         cal_rows, [1.6 * inch, 5.4 * inch], fs=8))
story.append(caption("Tabla 10. Cronograma anual de reuniones ejecutivas de S&OP "
                     "(12 ciclos mensuales)."))

story.append(h2("6.4 KPIs que se monitorean en cada ciclo"))
story.append(story_table(
    ["Indicador", "Meta", "Fórmula / medida"],
    [
        ("Nivel de servicio / Fill rate", "≥ 95 % (clase A) · 90–95 % (B, C)",
         "Ventas atendidas / ventas solicitadas."),
        ("Exactitud del pronóstico (1-MAPE)", "≥ 80 %", "Calidad del plan de demanda."),
        ("Días de inventario (DSI) o rotación", "8–10 vueltas/año",
         "Costo de ventas / inventario promedio."),
        ("Costo de faltantes y de exceso", "Tendencia a la baja",
         "Margen perdido + remates y obsolescencia."),
        ("% de inventario clase A sin rotación", "< 2 %", "Exceso sobre stock de seguridad."),
        ("Cumplimiento del plan S&OP", "≥ 90 % de adherencia",
         "Compras vs. plan aprobado."),
    ],
    [2.2 * inch, 1.7 * inch, 3.1 * inch], fs=8))
story.append(caption("Tabla 11. Cuadro de mando del proceso S&OP."))

# ================= 7. CONCLUSIONES =================
story.append(h1("7. Conclusiones"))
for txt in [
    "El inventario no es un solo problema ni un solo costo: clasificarlo por tipo (ciclo, "
    "seguridad, tránsito, anticipación, MRO) y por costo (ordenar, mantener, faltante, "
    "exceso/obsolescencia) permite atacar cada causa raíz de la crisis de XYZ.",
    "No hay una metodología única ganadora: la combinación de Pull+Kanban para la rotación "
    "diaria y Push/MRP para promociones y lanzamientos, sincronizada por el S&OP, es la que "
    "mejor equilibra servicio y capital en una distribuidora con lead times largos.",
    "El ABC–XYZ concentra la atención donde está el dinero: dos SKU (smartphone y laptop) "
    "explican ≈68 % del valor; diferenciar su política de control es la palanca de mayor "
    "impacto.",
    "El pronóstico por tendencia (MAPE < 5 %) y las herramientas EOQ/ROP/SS/MRP convierten la "
    "demanda esperada en un plan de compra concreto y medible, eliminando tanto los stock outs "
    "como el sobreinventario.",
    "El S&OP es el “ritmo” que sostiene la mejora: con sus cinco fases mensuales asegura que "
    "todas las áreas se muevan con un solo plan aprobado.",
]:
    story.append(bullet(txt))
story.append(body(
    "Con este proyecto, XYZ puede reducir sus costos de almacenamiento, eliminar prácticamente "
    "los faltantes en productos críticos y liberar capital hoy inmovilizado en stock sin "
    "rotación."))

# ================= 8. REFERENCIAS =================
story.append(h1("8. Referencias y fuentes de apoyo"))
refs = [
    "Heizer, J., Render, B., & Munson, C. (2020). Operations Management: Sustainability and "
    "Supply Chain Management (13.ª ed.). Pearson.",
    "Chopra, S., & Meindl, P. (2019). Supply Chain Management: Strategy, Planning, and "
    "Operation (7.ª ed.). Pearson.",
    "Vollmann, T. E., Berry, W. L., Whybark, D. C., & Jacobs, F. R. (2011). Manufacturing "
    "Planning and Control for Supply Chain Management (6.ª ed.). McGraw-Hill.",
    "ASCM / APICS (2023). APICS Dictionary — Definiciones de Sales & Operations Planning, EOQ, "
    "ROP y stock de seguridad. Association for Supply Chain Management.",
    "Silver, E. A., Pyke, D. F., & Thomas, D. J. (2017). Inventory and Production Management "
    "in Supply Chains (4.ª ed.). CRC Press.",
    "Institute of Business Forecasting & Planning (IBF). (s. f.). Guías de pronóstico de "
    "demanda y diseño de procesos S&OP. Recuperado de ibf.org.",
]
story.append(Paragraph("1. " + refs[0], S_REF))
for i, r in enumerate(refs[1:], start=2):
    story.append(Paragraph(f"{i}. {r}", S_REF))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Nota metodológica: las series de demanda históricas y la composición del portafolio son "
    "datos de referencia construidos para el ejercicio (la empresa “XYZ” es ficticia); todos "
    "los cálculos son verificables con las fórmulas estándar citadas en las referencias.",
    ParagraphStyle("note", parent=S_BODY, fontSize=8.5, textColor=GRAY, alignment=TA_LEFT)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(letter[0] / 2, 0.45 * inch,
                             "Actividad 3 — Gestión de Inventarios y S&OP — XYZ")
    canvas.drawRightString(letter[0] - 0.9 * inch, 0.45 * inch, f"Página {doc.page}")
    canvas.restoreState()


doc_t = SimpleDocTemplate(PDF_PATH, pagesize=letter,
                          leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                          topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                          title="Actividad 3 — ¿Para qué sirven los inventarios en las empresas?",
                          author="Adrián Corpi Villaseñor; Erick Díaz; Patricio Ulises Morales",
                          subject="Gestión de inventarios y proceso S&OP")
doc_t.build(story, onFirstPage=footer, onLaterPages=footer)
print("Saved:", PDF_PATH)
print("Size (KB):", round(os.path.getsize(PDF_PATH) / 1024, 1))
