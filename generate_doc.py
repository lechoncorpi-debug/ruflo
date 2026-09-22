#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el reporte de la Actividad 3 (Gestión de Inventarios y S&OP) en DOCX."""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "actividad3-inventarios")
os.makedirs(OUT_DIR, exist_ok=True)
DOC_PATH = os.path.join(OUT_DIR, "Actividad3_Gestion_de_Inventarios_SOP.docx")

NAVY = RGBColor(0x1F, 0x38, 0x64)
ACCENT = RGBColor(0xC0, 0x00, 0x00)
GRAY = RGBColor(0x59, 0x59, 0x59)
HDR_FILL = "1F3864"
ALT_FILL = "F2F5FA"

doc = Document()

# ---------- base styles ----------
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for sname, size, color in (("Heading 1", 16, NAVY), ("Heading 2", 13, NAVY), ("Heading 3", 12, NAVY)):
    st = doc.styles[sname]
    st.font.name = "Calibri"
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = color

# page margins
for sec in doc.sections:
    sec.top_margin = Inches(0.9)
    sec.bottom_margin = Inches(0.9)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)


def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def cell_text(cell, text, bold=False, color=None, size=10.5, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color


def p(text="", bold=False, italic=False, size=11, color=None, align=None, space_after=6):
    par = doc.add_paragraph()
    if align is not None:
        par.alignment = align
    par.paragraph_format.space_after = Pt(space_after)
    r = par.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    if color is not None:
        r.font.color.rgb = color
    return par


def bullet(text, bold_prefix=None, level=0):
    par = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    par.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r = par.add_run(bold_prefix)
        r.bold = True
    par.add_run(text)
    return par


def add_table(headers, rows, widths=None, font_size=10, header_fill=HDR_FILL, alt=True):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = t.rows[0].cells[j]
        cell_text(c, h, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=font_size,
                  align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_bg(c, header_fill)
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        for j, val in enumerate(row):
            cell_text(cells[j], str(val), size=font_size)
            if alt and i % 2 == 1:
                set_cell_bg(cells[j], ALT_FILL)
    if widths:
        for j, w in enumerate(widths):
            for r in t.rows:
                r.cells[j].width = Inches(w)
    return t


def page_break():
    doc.add_page_break()


def caption(text):
    par = p(text, italic=True, size=9.5, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    return par


def add_figure(path, width_in, caption_text):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(path, width=Inches(width_in))
    caption(caption_text)


# ============================================================
# PORTADA
# ============================================================
for _ in range(4):
    doc.add_paragraph()
p("Actividad 3", bold=True, size=26, color=ACCENT, align=WD_ALIGN_PARAGRAPH.CENTER)
p("¿Para qué sirven los inventarios en las empresas?", bold=True, size=20, color=NAVY,
  align=WD_ALIGN_PARAGRAPH.CENTER)
p("Gestión de inventarios, metodologías y proceso S&OP", italic=True, size=13, color=GRAY,
  align=WD_ALIGN_PARAGRAPH.CENTER)
p("Caso: Distribuidora de productos electrónicos “XYZ” (Latinoamérica)", italic=True, size=11,
  color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
p("Equipo", bold=True, size=14, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
team = [
    ("Adrián Corpi Villaseñor", "AL03044078"),
    ("Erick Díaz", "AL03007876"),
    ("Patricio Ulises Morales", "AL07098185"),
]
for name, mat in team:
    p(f"{name}  —  {mat}", size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
p("Materia / Curso: Gestión de Inventarios y Cadena de Suministro", size=11,
  align=WD_ALIGN_PARAGRAPH.CENTER)
p("Fecha de entrega: Septiembre de 2026", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
page_break()

# ============================================================
# ÍNDICE
# ============================================================
doc.add_heading("Índice", level=1)
items = [
    "1. Contexto del caso: la empresa “XYZ”",
    "2. Clasificación de los tipos de inventario y costos asociados",
    "3. Metodología de gestión de inventarios recomendada (justificación)",
    "4. Priorización de productos: análisis ABC–XYZ y productos clave",
    "5. Pronóstico de demanda y planificación del requerimiento de inventario",
    "6. Cronograma de reuniones de S&OP: fases del proceso",
    "7. Conclusiones",
    "8. Referencias y fuentes de apoyo",
]
for it in items:
    doc.add_paragraph(it, style="List Number")
page_break()

# ============================================================
# 1. CONTEXTO
# ============================================================
doc.add_heading("1. Contexto del caso: la empresa “XYZ”", level=1)
p("“XYZ” es una empresa dedicada a la distribución de productos electrónicos en Latinoamérica. "
  "Su portafolio incluye smartphones, laptops, televisores, tabletas, audio, wearables y "
  "accesorios que se abastecen principalmente de proveedores asiáticos, con tiempos de entrega "
  "(lead time) de entre 3 y 9 semanas en su mayoría.")
p("Recientemente la empresa ha presentado problemas significativos de gestión de inventario que "
  "se traducen en tres síntomas principales:")
bullet("elevados costos de almacenamiento (exceso de stock y capital inmovilizado);", bold_prefix="• ")
bullet("rupturas de stock o stock outs (venta perdida y fallas de servicio al cliente);", bold_prefix="• ")
bullet("sobreinventario de productos de baja rotación y obsolescencia tecnológica.", bold_prefix="• ")
p("Ante ello, la dirección ha decidido implementar un proyecto de mejora para optimizar la "
  "gestión de inventarios mediante metodologías avanzadas (ABC–XYZ, EOQ, punto de reorden, "
  "pronóstico de demanda, MRP y Kanban) dentro de un proceso formal de S&OP (Sales & Operations "
  "Planning). Este documento desarrolla, con datos de referencia, las cuatro entregas "
  "solicitadas.")

# ============================================================
# 2. TIPOS DE INVENTARIO Y COSTOS
# ============================================================
doc.add_heading("2. Clasificación de los tipos de inventario y sus costos", level=1)
p("Para una distribuidora de electrónicos, el inventario no es un solo bloque: conviene "
  "clasificarlo según su función dentro de la cadena de suministro, porque cada tipo obedece a "
  "una lógica distinta y se asocia a costos distintos.", space_after=4)

doc.add_heading("2.1 Tipos de inventario", level=2)
tipos_headers = ["Tipo de inventario", "Descripción", "Ejemplo en XYZ", "Costo dominante"]
tipos_rows = [
    ("Ciclo (Cycle stock)", "Stock que cubre la demanda normal entre un pedido y otro.",
     "Cajas de smartphones que cubren la venta mientras llega el siguiente lote del proveedor.",
     "Costo de mantenimiento y de ordenar."),
    ("De seguridad (Safety stock)", "Colchón que protege contra variabilidad de demanda y de suministro.",
     "Unidades extras de laptops durante temporada escolar alta.",
     "Costo de mantenimiento (capital) + costo de faltante evitado."),
    ("En tránsito / tubería (Pipeline)", "Mercancía pagada y en movimiento proveedor → almacén/tienda.",
     "Contenedores de TVs OLED navegando desde Asia (45–60 días).",
     "Costo de capital inmovilizado + seguro y flete."),
    ("De anticipación / estacional", "Se acumula antes de picos conocidos de demanda.",
     "Acopio de audífonos y wearables para el Buen Fin / Black Friday.",
     "Costo de mantenimiento; riesgo de no vender todo."),
    ("Producto terminado", "Artículos listos para su venta/distribución.",
     "Inventario en centros de distribución regionales (México, Colombia, Perú…).",
     "Costo de mantenimiento y de oportunidad."),
    ("MRO (mantenimiento, reparación, operación)", "Materiales auxiliares no vendibles para operar.",
     "Empaque, cintas, repuestos de montacargas, etiquetas.",
     "Costo de ordenar y de mantenimiento menores."),
    ("Especulativo", "Compra anticipada esperando alzas de precio o tipo de cambio.",
     "Compra adelantada de memorias/chips ante escasez.",
     "Costo de mantenimiento + riesgo financiero."),
]
add_table(tipos_headers, tipos_rows, widths=[1.5, 2.3, 2.3, 1.9])
caption("Tabla 1. Tipos de inventario aplicables a una distribuidora de productos electrónicos.")

doc.add_heading("2.2 Costos asociados a los inventarios", level=2)
p("Los costos que explican la crisis de XYZ pueden agruparse en cinco categorías:", space_after=4)
cost_headers = ["Costo", "Fórmula / Descripción", "Impacto en XYZ"]
cost_rows = [
    ("De adquisición / compra", "Costo unitario C más flete, aranceles y seguro. Costo anual = C × D.",
     "Es la base del valor de inventario; en electrónicos puede ser 60–80 % del precio de venta."),
    ("De ordenar / preparación", "S = costo administrativo + transporte por pedido. Nº pedidos = D/Q.",
     "Pedidos frecuentes y chicos (pull) elevan el gasto administrativo y de flete."),
    ("De mantenimiento / almacenaje", "H = i × C (i = tasa anual, típicamente 18–30 %): capital, espacio, seguro, mermas, obsolescencia.",
     "Causa directa del problema de “altos costos de almacenamiento”."),
    ("Por faltantes (stock out)", "Margen perdido + urgencias de reabasto + penalización + pérdida de imagen.",
     "Cuanto más crítico el SKU (clase A), más caro es el faltante."),
    ("Por sobreinventario / obsolescencia", "Valor de ítems sin salida, remates a precio bajo y espacio ocupado.",
     "El ciclo corto de la electrónica hace que el exceso se deprecie muy rápido."),
]
add_table(cost_headers, cost_rows, widths=[1.7, 3.4, 2.9])
caption("Tabla 2. Costos del inventario y su relación con la problemática de XYZ.")

p("El equilibrio se logra minimizando la suma de los costos de ordenar y de mantener, "
  "protegiéndose al mismo tiempo contra el costo de faltante. En la sección 5 se calculan el "
  "lote económico (EOQ), el stock de seguridad y el punto de reorden para los dos productos "
  "clave.", space_after=4)

# ============================================================
# 3. METODOLOGÍA
# ============================================================
doc.add_heading("3. Metodología de gestión de inventarios recomendada", level=1)

doc.add_heading("3.1 Comparación de metodologías", level=2)
met_headers = ["Metodología", "Lógica", "Fortalezas", "Riesgos / límites"]
met_rows = [
    ("Push (empujar)", "Producir/comprar según pronóstico y empujar al canal (MRP).",
     "Escala, economías de lote, ideal para lanzamientos y promociones.",
     "Si el pronóstico falla, genera sobreinventario y obsolescencia."),
    ("Pull (jalar)", "Reabastecer solo según consumo real del cliente.",
     "Bajo inventario, responde a la demanda real.",
     "Requiere lead times cortos y demanda predecible a nivel operativo."),
    ("Por demanda (forecast-driven)", "Todo se planea a partir del pronóstico de demanda.",
     "Visibilidad y planeación agregada (base del S&OP).",
     "La calidad depende del pronóstico; rigidez ante cambios súbitos."),
    ("Kanban / JIT", "Señal de reabasto por tarjetas o contenedores cuando el nivel baja.",
     "Visual, autocontrolado, mínimo desperdicio, flujo continuo.",
     "Sensible a variabilidad y a fallas de suministro; no admite lead times largos."),
]
add_table(met_headers, met_rows, widths=[1.2, 2.1, 2.1, 2.2])
caption("Tabla 3. Comparación de metodologías de gestión de inventarios.")

doc.add_heading("3.2 Metodología seleccionada y justificación", level=2)
p("Para una distribuidora de electrónicos con lead times largos (3–9 semanas) y alta "
  "variabilidad, no existe una sola metodología correcta. Recomendamos un enfoque híbrido "
  "gobernado por S&OP:", space_after=4)
bullet("para la base del portafolio y los reaprovisionamientos recurrentes, un sistema "
       "Pull con Kanban (tarjetas/bins y reabastecimiento por consumo real), que reduce el "
       "sobreinventario y alinea el stock con la rotación real;", bold_prefix="• ")
bullet("para lanzamientos, promociones (Buen Fin, Black Friday) y productos de temporada, "
       "planeación Push apoyada en MRP y en el pronóstico de demanda, porque la demanda "
       "“empujada” por marketing no puede jalar sola;", bold_prefix="• ")
bullet("para los artículos críticos (clase A), control continuo con punto de reorden (ROP) y "
       "stock de seguridad calculado estadísticamente;", bold_prefix="• ")
bullet("todo sincronizado mensualmente por el proceso S&OP, que concilia la demanda (ventas y "
       "marketing) con el suministro (compras, logística y finanzas).", bold_prefix="• ")
p("Justificación: el Kanban puro exige lead times cortos y demanda estable, lo cual no aplica a "
  "importaciones desde Asia con 45+ días de tránsito; el Push puro volvería a inflar el "
  "almacén y a multiplicar la obsolescencia (el origen del problema de XYZ). El híbrido "
  "Pull+Kanban en la rotación diaria y Push/MRP en las excepciones, con la disciplina del "
  "S&OP como “semáforo” mensual, maximiza el nivel de servicio con el mínimo capital "
  "inmovilizado.", space_after=4)

# ============================================================
# 4. ABC-XYZ Y PRODUCTOS CLAVE
# ============================================================
doc.add_heading("4. Priorización de productos: análisis ABC–XYZ", level=1)
p("Se clasificó un portafolio de referencia de 10 SKU según su valor anual de consumo "
  "(costo unitario × demanda anual) y la variabilidad de su demanda (coeficiente de variación, "
  "CV). El cruce ABC–XYZ permite definir la política de control de cada grupo.", space_after=4)

add_figure(os.path.join(OUT_DIR, "fig_pareto.png"), 6.4,
           "Figura 1. Análisis ABC (Pareto) del valor anual de consumo del portafolio de XYZ.")

abc_headers = ["Producto / categoría", "Costo unit.", "Demanda anual", "Valor anual (USD)",
               "Participación", "Acumulado", "ABC", "Variab.", "ABC–XYZ"]
abc_rows = [
    ("Flagship 5G Smartphone", "$450", "25,040", "$11,268,000", "48.2 %", "48.2 %", "A", "Baja (0.11)", "AX"),
    ("Ultra-Slim Business Laptop 14”", "$750", "6,020", "$4,515,000", "19.3 %", "67.5 %", "A", "Media (0.17)", "AY"),
    ("Smart OLED TV 55” 4K", "$550", "4,200", "$2,310,000", "9.9 %", "77.4 %", "B", "Media (0.22)", "BY"),
    ("Tablet 10” gama media", "$220", "7,500", "$1,650,000", "7.1 %", "84.5 %", "B", "Media (0.19)", "BY"),
    ("Audífonos con cancelación de ruido", "$120", "9,000", "$1,080,000", "4.6 %", "89.1 %", "B", "Media (0.15)", "BY"),
    ("Smartwatch / banda fitness", "$85", "11,000", "$935,000", "4.0 %", "93.1 %", "C", "Media (0.25)", "CY"),
    ("Cámara de seguridad inteligente", "$60", "8,500", "$510,000", "2.2 %", "95.3 %", "C", "Alta (0.28)", "CZ"),
    ("Cargadores rápidos GaN", "$18", "28,000", "$504,000", "2.2 %", "97.4 %", "C", "Baja (0.09)", "CX"),
    ("Bocinas Bluetooth portátiles", "$45", "7,200", "$324,000", "1.4 %", "98.8 %", "C", "Alta (0.32)", "CZ"),
    ("Kits de cables HDMI / USB-C", "$8", "35,000", "$280,000", "1.2 %", "100.0 %", "C", "Baja (0.07)", "CX"),
]
add_table(abc_headers, abc_rows, widths=[2.3, 0.6, 0.8, 1.0, 0.7, 0.7, 0.5, 0.9, 0.7], font_size=9)
caption("Tabla 4. Portafolio clasificado por ABC (valor) y XYZ (variabilidad). Valor total ≈ $23.4 M.")

doc.add_heading("4.1 Política de control por grupo", level=2)
bullet("Clase A (≈68 % del valor con ≈20 % de los SKU): control estricto, conteo cíclico "
       "frecuente, pronóstico y stock de seguridad calculados por SKU, revisión continua y "
       "altos niveles de servicio (97–98 %).", bold_prefix="• ")
bullet("Clase B (≈21 % del valor): revisión periódica quincenal/mensual y nivel de servicio "
       "medio-alto (95 %).", bold_prefix="• ")
bullet("Clase C (≈11 % del valor, muchos SKU): control simple con sistema periódico (min–max) "
       "o Kanban de tarjetas y nivel de servicio algo menor (90–95 %), liberando tiempo del "
       "equipo.", bold_prefix="• ")
bullet("El eje XYZ refina la política: los AX (alto valor, demanda estable) se pueden manejar "
       "con Kanban/mínimo-máximo y planeación justo a tiempo; los AZ o CZ (erráticos) "
       "requieren más stock de seguridad o revisión más frecuente.", bold_prefix="• ")

doc.add_heading("4.2 Los dos productos principales y su valor en la cadena", level=2)
p("Los dos productos que, por su impacto conjunto en costo, volumen y tiempo de "
  "reabastecimiento, deben priorizarse son:", space_after=4)
bullet("Flagship 5G Smartphone (AX, $11.27 M/año — 48 % del valor del portafolio). Justificación: "
       "es el mayor generador de margen e ingresos; su ciclo de vida es corto (≈12 meses), por "
       "lo que un error de pronóstico o un exceso de inventario se transforma muy rápido en "
       "obsolescencia y remates. Su demanda es relativamente estable (CV ≈ 0.11), lo que "
       "permite un control ajustado con stock de seguridad bajo.", bold_prefix="1) ")
bullet("Ultra-Slim Business Laptop 14” (AY, $4.51 M/año — 19 % del valor). Justificación: "
       "segundo generador de valor con el mayor costo unitario ($750) y compradores B2B/de "
       "empresa muy sensibles al stock-out; un faltante aquí no solo pierde la venta, puede "
       "perder el contrato o contrato marco completo. Su demanda es moderadamente variable e "
       "influida por el ciclo escolar y el cierre fiscal corporativo.", bold_prefix="2) ")
p("En conjunto representan ≈68 % del valor anual de consumo, por lo que concentran la "
  "mayoría de las decisiones de pronóstico, stock de seguridad y reabastecimiento (los "
  "cálculos de la sección 5 se desarrollan sobre estos dos SKU).", space_after=4)

# ============================================================
# 5. PRONÓSTICO Y PLANIFICACIÓN
# ============================================================
doc.add_heading("5. Pronóstico de demanda y planificación del requerimiento", level=1)

doc.add_heading("5.1 Método de pronóstico", level=2)
p("Se utilizó regresión lineal de tendencia sobre 12 meses de historia (mínimos cuadrados) y, "
  "como referencia de validación, media móvil de 3 meses y suavizamiento exponencial (α = 0.3). "
  "Se eligió la línea de tendencia por su menor error de pronóstico (MAPE) y porque captura el "
  "crecimiento sostenido del mercado. La demanda proyectada se expresa como:", space_after=4)
p("Demanda_estimada (mes t) = a + b × t", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_figure(os.path.join(OUT_DIR, "fig_forecast.png"), 6.4,
           "Figura 2. Histórico (12 meses) y pronóstico (6 meses) de los dos productos clave.")

fore_headers = ["Producto", "Ecuación de tendencia", "Demanda media", "σ (desv.)", "MAPE",
                "MAD"]
fore_rows = [
    ("Flagship 5G Smartphone", "D = 1,690.3 + 61.0 × mes", "2,087/mes", "239", "3.4 %", "74 un."),
    ("Business Laptop 14”", "D = 352.1 + 23.0 × mes", "502/mes", "88", "4.6 %", "24 un."),
]
add_table(fore_headers, fore_rows, widths=[1.9, 1.9, 1.0, 0.8, 0.7, 0.7], font_size=9.5)
caption("Tabla 5. Parámetros del modelo de pronóstico y su precisión (MAPE < 5 % → muy bueno).")

doc.add_heading("5.2 Parámetros de planificación (EOQ, stock de seguridad, ROP)", level=2)
p("Supuestos de referencia: costo de ordenar S = $1,500/orden; tasa anual de mantenimiento "
  "i = 25 % del costo unitario; nivel de servicio objetivo 95 % (z = 1.645) para clase A; "
  "lead time L = 1.5 meses (≈45 días). Fórmulas aplicadas:", space_after=4)
bullet("Lote económico: EOQ = √(2DS/H), con D = demanda anual y H = costo de mantener por "
       "unidad por año.", bold_prefix="• ")
bullet("Stock de seguridad: SS = z × √L × σ_mensual.", bold_prefix="• ")
bullet("Punto de reorden: ROP = (d_promedio × L) + SS.", bold_prefix="• ")
doc.add_paragraph()
plan_headers = ["Concepto", "Fórmula", "Smartphone 5G", "Laptop 14”"]
plan_rows = [
    ("Demanda anual (D)", "Σ demanda mensual", "25,040 u. (≈2,087/mes)", "6,020 u. (≈502/mes)"),
    ("Costo de mantener (H)", "i × C", "0.25 × $450 = $112.50/año", "0.25 × $750 = $187.50/año"),
    ("Lote económico (EOQ)", "√(2DS/H)", "≈ 817 → lote práctico 1,000 u.", "≈ 310 → lote práctico 350 u."),
    ("Nº de pedidos al año", "D / lote", "25,040/1,000 ≈ 25 (≈ cada 2 semanas)", "6,020/350 ≈ 17 (≈ cada 3 semanas)"),
    ("Stock de seguridad (SS)", "z × √L × σ", "1.645 × √1.5 × 239 ≈ 481 u.", "1.645 × √1.5 × 88 ≈ 178 u."),
    ("Punto de reorden (ROP)", "d̄ × L + SS", "3,130 + 481 ≈ 3,611 u.", "753 + 178 ≈ 931 u."),
]
add_table(plan_headers, plan_rows, widths=[2.1, 1.7, 2.0, 2.0], font_size=9.5)
caption("Tabla 6. Parámetros de control de inventario para los dos productos clave. La "
        "desviación durante el lead time es σ_L = √L × σ_mensual.")

doc.add_heading("5.3 Planificación del requerimiento de inventario (MRP)", level=2)
p("Con el pronóstico de los próximos 6 meses (meses 13 a 18), se calculó el requerimiento neto "
  "y las liberaciones de pedido con MRP (lead time de 2 meses y lotes fijos iguales al EOQ "
  "redondeado: 1,000 y 350 unidades; stock de seguridad 481 y 178 unidades).", space_after=4)

doc.add_heading("Smartphone 5G (lote 1,000 u., SS 481 u.)", level=3)
mrp_headers = ["Concepto", "M1", "M2", "M3", "M4", "M5", "M6"]
mrp1_rows = [
    ("Requerimiento bruto (demanda)", "2,483", "2,544", "2,605", "2,666", "2,727", "2,788"),
    ("Recepciones programadas", "2,000", "—", "—", "—", "—", "—"),
    ("Disponible proyectado (PAB)", "2,317", "773", "1,168", "502", "775", "987"),
    ("Requerimiento neto", "0", "708", "2,313", "1,979", "2,706", "2,494"),
    ("Recepción planificada de pedido", "—", "1,000", "3,000", "2,000", "3,000", "3,000"),
    ("Liberación planificada (LT = 2 meses)", "3,000", "2,000", "3,000", "3,000", "—", "—"),
]
add_table(mrp_headers, mrp1_rows, widths=[2.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8], font_size=9)
caption("Tabla 7. Plan MRP del smartphone (unidades). Liberaciones a 2 meses anticipadas: "
        "M1=3,000 · M2=2,000 · M3=3,000 · M4=3,000 · M5=M6=— (totales estimados ya incluidos).")

doc.add_heading("Business Laptop 14” (lote 350 u., SS 178 u.)", level=3)
mrp2_rows = [
    ("Requerimiento bruto (demanda)", "651", "674", "697", "720", "743", "766"),
    ("Recepciones programadas", "600", "—", "—", "—", "—", "—"),
    ("Disponible proyectado (PAB)", "799", "475", "478", "458", "415", "349"),
    ("Requerimiento neto", "0", "53", "400", "420", "463", "529"),
    ("Recepción planificada de pedido", "—", "350", "700", "700", "700", "700"),
    ("Liberación planificada (LT = 2 meses)", "700", "700", "700", "700", "—", "—"),
]
add_table(mrp_headers, mrp2_rows, widths=[2.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8], font_size=9)
caption("Tabla 8. Plan MRP de la laptop (unidades). Liberaciones a 2 meses anticipadas: "
        "M1=M2=M3=M4=700 · M5=M6=—.")

p("Interpretación: el stock inicial más las recepciones en tránsito cubren el primer mes; a "
  "partir de ahí se liberan pedidos con dos meses de anticipación para cubrir la demanda sin "
  "caer por debajo del stock de seguridad. El lote es un múltiplo del EOQ redondeado (1,000 y "
  "350 unidades), por lo que, en promedio, el smartphone se pide unas 25 veces al año y la "
  "laptop unas 17. Esto traduce el pronóstico en un plan de compras concreto y en compromisos "
  "de capacidad con los proveedores.", space_after=4)

# ============================================================
# 6. S&OP
# ============================================================
doc.add_heading("6. Cronograma de reuniones de S&OP: fases del proceso", level=1)

doc.add_heading("6.1 Las cinco fases del proceso S&OP", level=2)
p("El proceso S&OP es un ciclo mensual de planeación táctica que integra ventas, operaciones, "
  "compras, finanzas y dirección. Sus cinco fases son:", space_after=4)
sop_headers = ["Fase", "Objetivo", "Entradas", "Salidas", "Dueño", "Duración"]
sop_rows = [
    ("1. Revisión de datos (Data review)", "Actualizar cifras reales: ventas, inventario, pedidos, backorders, lead times y errores de pronóstico.",
     "Ventas reales del mes, niveles de stock, cumplimiento de proveedores.",
     "Base de datos única y confiable (single source of truth).",
     "Planeador de demanda / Analista de datos", "Días 1–3 del ciclo"),
    ("2. Pronóstico de demanda (Demand planning)", "Generar el pronóstico consensuado por SKU/familia (estadístico + aportes de ventas y marketing).",
     "Históricos, pipeline comercial, promociones, tendencias de mercado.",
     "Pronóstico de demanda base + escenarios alto/bajo por familia.",
     "Gerente de demanda / Ventas y Marketing", "Día 4–7 del ciclo"),
    ("3. Revisión de suministro (Supply review)", "Validar capacidad, proveedores, niveles de inventario y restricciones para cumplir el pronóstico.",
     "Pronóstico aprobado en fase 2, capacidad de almacenes, planes de compra.",
     "Plan de suministro, inventarios proyectados, brechas de capacidad.",
     "Gerente de operaciones / Compras y Logística", "Día 8–10 del ciclo"),
    ("4. Reconciliación / Pre-S&OP", "Confrontar demanda vs. suministro, resolver desbalances y preparar escenarios con impacto financiero.",
     "Planes de demanda y suministro, costos, márgenes, restricciones.",
     "Escenarios conciliados y recomendaciones para la dirección.",
     "Líder de S&OP / Finanzas", "Día 11–12 del ciclo"),
    ("5. Reunión ejecutiva S&OP", "Revisar escenarios, tomar decisiones, aprobar el plan único y asignar responsables.",
     "Escenarios de la fase 4, KPIs, riesgos.",
     "Plan operativo aprobado (ventas + operaciones + inventario + financiero) y acciones.",
     "Dirección general", "Día 13–15 del ciclo"),
]
add_table(sop_headers, sop_rows, widths=[1.7, 1.9, 1.5, 1.6, 1.2, 0.9], font_size=8.5)
caption("Tabla 9. Fases del proceso mensual de S&OP (adaptado de APICS/ASCM).")

doc.add_heading("6.2 Cadencia mensual (cronograma tipo)", level=2)
p("Cada ciclo mensual sigue una secuencia semanal fija para que el ritmo sea predecible:", space_after=4)
week_headers = ["Semana del mes", "Actividad", "Participantes", "Resultado"]
week_rows = [
    ("Semana 1 (días 1–5)", "Fase 1: cierre y revisión de datos; Fase 2: arranque del pronóstico.", "Analistas, planeador de demanda.", "Base de datos validada."),
    ("Semana 2 (días 6–12)", "Fase 2 (cierre): consenso de demanda; Fase 3: revisión de suministro.", "Ventas, marketing, compras, logística.", "Pronóstico y plan de suministro preliminares."),
    ("Semana 3 (días 13–20)", "Fase 4: reconciliación y escenarios financieros (Pre-S&OP).", "Líder S&OP, finanzas, operaciones.", "Escenarios conciliados con impacto $."),
    ("Semana 4 (días 21–30)", "Fase 5: reunión ejecutiva; aprobación y comunicación del plan.", "Dirección y gerentes de área.", "Plan único aprobado + acciones."),
]
add_table(week_headers, week_rows, widths=[1.4, 3.0, 2.0, 1.9], font_size=9.5)
caption("Tabla 10. Cadencia estándar de un ciclo mensual de S&OP.")

doc.add_heading("6.3 Cronograma anual de reuniones ejecutivas", level=2)
p("La reunión ejecutiva (fase 5) se celebra el último jueves de cada mes (excepto cuando "
  "coincide con días festivos, en cuyo caso se recorre al jueves anterior); el resto de fases "
  "se repite cada mes con el calendario de la Tabla 10. Cada trimestre, la fase ejecutiva "
  "incluye además una revisión de portafolio (ABC) y de parámetros de inventario (EOQ, SS, "
  "ROP).", space_after=4)
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
    ("Ciclo 12 — Septiembre 2027", "Balance anual y arranque del ciclo planning del año siguiente."),
]
add_table(["Ciclo / Mes", "Enfoque principal de la reunión ejecutiva"], cal_rows,
          widths=[2.0, 5.6], font_size=9.5)
caption("Tabla 11. Cronograma anual de reuniones ejecutivas de S&OP (12 ciclos mensuales).")

doc.add_heading("6.4 KPIs que se monitorean en cada ciclo", level=2)
kpi_rows = [
    ("Nivel de servicio / Fill rate", "≥ 95 % (clase A) · 90–95 % (B, C)", "Ventas atendidas / ventas solicitadas."),
    ("Exactitud del pronóstico (1-MAPE)", "≥ 80 %", "Calidad del plan de demanda."),
    ("Días de inventario (DSI) o rotación", "8–10 vueltas/año", "Costo de ventas / inventario promedio."),
    ("Costo de faltantes y de exceso", "Tendencia a la baja", "Margen perdido + remates y obsolescencia."),
    ("% de inventario clase A sin rotación", "< 2 %", "Exceso sobre stock de seguridad."),
    ("Cumplimiento del plan S&OP", "≥ 90 % de adherencia", "Producción/compras vs. plan aprobado."),
]
add_table(["Indicador", "Meta", "Fórmula / medida"], kpi_rows, widths=[2.1, 1.7, 3.8], font_size=9.5)
caption("Tabla 12. Cuadro de mando del proceso S&OP.")

# ============================================================
# 7. CONCLUSIONES
# ============================================================
doc.add_heading("7. Conclusiones", level=1)
for txt in [
    "El inventario no es un solo problema ni un solo costo: clasificarlo por tipo (ciclo, seguridad, tránsito, anticipación, MRO) y por costo (ordenar, mantener, faltante, exceso/obsolescencia) permite atacar cada causa raíz de la crisis de XYZ.",
    "No hay una metodología única ganadora: la combinación de Pull+Kanban para la rotación diaria y Push/MRP para promociones y lanzamientos, sincronizada por el S&OP, es la que mejor equilibra servicio y capital en una distribuidora con lead times largos.",
    "El ABC–XYZ concentra la atención donde está el dinero: dos SKU (smartphone y laptop) explican ≈68 % del valor; diferenciar su política de control es la palanca de mayor impacto.",
    "El pronóstico por tendencia (MAPE < 5 %) y las herramientas EOQ/ROP/SS/MRP convierten la demanda esperada en un plan de compra concreto y medible, eliminando tanto los stock outs como el sobreinventario.",
    "El S&OP es el “ritmo” que sostiene la mejora: con sus cinco fases mensuales (datos, demanda, suministro, reconciliación y decisión ejecutiva) asegura que todas las áreas se muevan con un solo plan aprobado.",
]:
    bullet(txt)
p("Con este proyecto, XYZ puede reducir sus costos de almacenamiento, eliminar prácticamente "
  "los faltantes en productos críticos y liberar capital hoy inmovilizado en stock sin "
  "rotación.", space_after=4)

# ============================================================
# 8. REFERENCIAS
# ============================================================
doc.add_heading("8. Referencias y fuentes de apoyo", level=1)
refs = [
    "Heizer, J., Render, B., & Munson, C. (2020). Operations Management: Sustainability and Supply Chain Management (13.ª ed.). Pearson. (Capítulos de administración de inventarios, EOQ, MRP y S&OP).",
    "Chopra, S., & Meindl, P. (2019). Supply Chain Management: Strategy, Planning, and Operation (7.ª ed.). Pearson.",
    "Vollmann, T. E., Berry, W. L., Whybark, D. C., & Jacobs, F. R. (2011). Manufacturing Planning and Control for Supply Chain Management (6.ª ed.). McGraw-Hill. (Proceso S&OP y MRP).",
    "ASCM / APICS (2023). APICS Dictionary — Definiciones de Sales & Operations Planning, EOQ, ROP y seguridad de inventario. Association for Supply Chain Management.",
    "Silver, E. A., Pyke, D. F., & Thomas, D. J. (2017). Inventory and Production Management in Supply Chains (4.ª ed.). CRC Press. (Clasificación ABC y control de inventarios).",
    "Institute of Business Forecasting & Planning (IBF). (s. f.). Guías de pronóstico de demanda y diseño de procesos S&OP. Recuperado de ibf.org.",
]
for r in refs:
    par = doc.add_paragraph(style="List Number")
    par.add_run(r)
doc.add_paragraph()
p("Nota metodológica: las series de demanda históricas y la composición del portafolio son "
  "datos de referencia construidos para el ejercicio (la empresa “XYZ” es ficticia); todos los "
  "cálculos son verificables con las fórmulas estándar citadas en las referencias.",
  italic=True, size=9.5, color=GRAY)

# ---------- metadata & save ----------
cp = doc.core_properties
cp.title = "Actividad 3 — ¿Para qué sirven los inventarios en las empresas? (S&OP)"
cp.author = "Adrián Corpi Villaseñor; Erick Díaz; Patricio Ulises Morales"
cp.subject = "Gestión de inventarios y proceso S&OP"
cp.keywords = "inventarios; S&OP; ABC-XYZ; EOQ; MRP; Kanban"
doc.save(DOC_PATH)
print("Saved:", DOC_PATH)
