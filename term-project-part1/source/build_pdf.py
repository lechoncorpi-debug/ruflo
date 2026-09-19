"""Build a PDF version of the Term Project Part 1 from the .docx (no LibreOffice needed).

Pipeline: python-docx file -> mammoth (semantic HTML) -> light post-processing/CSS ->
PyMuPDF Story (layout engine) -> PDF, then page numbers + metadata are added.

Usage:  python3 build_pdf.py            (reads Nubank_Case_Story_Part1.docx, writes Nubank_Case_Story_Part1.pdf)
"""
import os
import re
import sys

import mammoth
import pymupdf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(HERE, "Nubank_Case_Story_Part1.docx")
PDF = os.path.join(HERE, "Nubank_Case_Story_Part1.pdf")
FONT_DIR = "/tmp/pdf_fonts"

PURPLE = "#6A0DAD"
GREY = "#595959"

# ---------------------------------------------------------------- fonts ----
def prepare_fonts():
    """Extract the FiraGO family shipped with the pymupdf-fonts package to a folder for @font-face."""
    os.makedirs(FONT_DIR, exist_ok=True)
    fd = pymupdf.fitz_fontdescriptors
    wanted = {"figo": "FiraGO-R.ttf", "figbo": "FiraGO-B.ttf", "figit": "FiraGO-I.ttf", "figbi": "FiraGO-BI.ttf"}
    for key, fn in wanted.items():
        path = os.path.join(FONT_DIR, fn)
        if not os.path.exists(path):
            data = fd[key]["loader"]()
            with open(path, "wb") as f:
                f.write(bytes(data))
    return FONT_DIR


# ------------------------------------------------------------ html prep ----
def docx_to_html(path):
    with open(path, "rb") as f:
        result = mammoth.convert_to_html(f)
    return result.value


def decorate(html):
    """Add classes so the CSS can style the title block, captions, source notes and references."""
    # --- title block: the first six paragraphs
    paras = re.findall(r"<p>.*?</p>", html, flags=re.S)
    classes = ["t-course", "t-project", "t-title", "t-subtitle", "t-case", "t-student"]
    for p, cls in zip(paras[:6], classes):
        html = html.replace(p, p.replace("<p>", f'<p class="{cls}">', 1), 1)
    # --- table captions and source notes
    html = html.replace("<p><strong>Table ", '<p class="cap"><strong>Table ')
    html = html.replace("<p><em>Sources:</em>", '<p class="src"><em>Sources:</em>')
    # --- references (everything after the References heading)
    m = re.search(r"<h1>(?:<strong>)?References(?:</strong>)?</h1>", html)
    if m:
        head, tail = html[: m.end()], html[m.end():]
        tail = tail.replace("<p>", '<p class="ref">')
        html = head + tail
    # --- give each table an id (column widths differ per table)
    n = 0

    def _tbl(_m):
        nonlocal n
        n += 1
        return f'<table id="t{n}">'

    html = re.sub(r"<table>", _tbl, html)
    # column width hints (Story honours <col width> reasonably well)
    colgroups = {
        1: '<colgroup><col width="12%"><col width="50%"><col width="38%"></colgroup>',
        2: '<colgroup><col width="29%"><col width="71%"></colgroup>',
        3: '<colgroup><col width="30%"><col width="35%"><col width="35%"></colgroup>',
    }
    for i, cg in colgroups.items():
        html = html.replace(f'<table id="t{i}">', f'<table id="t{i}">{cg}', 1)
    return html


CSS = f"""
@font-face {{ font-family: fira; src: url(FiraGO-R.ttf); }}
@font-face {{ font-family: fira; src: url(FiraGO-B.ttf); font-weight: bold; }}
@font-face {{ font-family: fira; src: url(FiraGO-I.ttf); font-style: italic; }}
@font-face {{ font-family: fira; src: url(FiraGO-BI.ttf); font-weight: bold; font-style: italic; }}

body {{ font-family: fira; font-size: 10.2pt; line-height: 1.32; color: #1f1f1f; }}
p    {{ margin: 0 0 6pt 0; text-align: justify; }}

h1 {{ font-family: fira; font-size: 12.8pt; font-weight: bold; color: {PURPLE};
      margin: 13pt 0 5pt 0; text-align: left; page-break-after: avoid; }}
h2 {{ font-family: fira; font-size: 11pt; font-weight: bold; color: #1f1f1f;
      margin: 8pt 0 3pt 0; text-align: left; page-break-after: avoid; }}

p.t-course   {{ text-align: center; font-size: 10pt; color: {GREY}; margin: 0 0 2pt 0; }}
p.t-project  {{ text-align: center; font-size: 10pt; color: {GREY}; margin: 0 0 10pt 0; }}
p.t-title    {{ text-align: center; font-size: 19pt; color: {PURPLE}; margin: 0 0 3pt 0; line-height: 1.2; }}
p.t-subtitle {{ text-align: center; font-size: 12.5pt; color: #1f1f1f; margin: 0 0 8pt 0; }}
p.t-case     {{ text-align: center; font-size: 9.5pt; color: {GREY}; margin: 0 0 6pt 0; }}
p.t-student  {{ text-align: center; font-size: 10pt; color: #1f1f1f; margin: 0 0 4pt 0; }}

p.cap {{ text-align: left; font-size: 9.6pt; margin: 6pt 0 3pt 0; page-break-after: avoid; }}
p.src {{ text-align: left; font-size: 8.4pt; color: {GREY}; margin: 2pt 0 8pt 0; }}
p.ref {{ text-align: left; font-size: 9.2pt; margin: 0 0 4pt 0; padding-left: 0.4in; text-indent: -0.4in; line-height: 1.25; }}

table {{ border-collapse: collapse; width: 100%; margin: 2pt 0 4pt 0; font-size: 8.7pt; line-height: 1.22; }}
th {{ color: {PURPLE}; font-weight: bold; text-align: left;
      border: 0.6pt solid #9a9a9a; padding: 3pt 4pt; vertical-align: top; }}
td {{ border: 0.6pt solid #9a9a9a; padding: 3pt 4pt; vertical-align: top; }}
td p, th p {{ margin: 0; text-align: left; }}
"""


# --------------------------------------------------------------- render ----
def render(html, out_pdf, font_dir):
    arch = pymupdf.Archive(font_dir)
    story = pymupdf.Story(html=html, user_css=CSS, archive=arch)
    mediabox = pymupdf.paper_rect("letter")
    where = mediabox + (72, 72, -72, -72)  # 1-inch margins
    writer = pymupdf.DocumentWriter(out_pdf)
    more = True
    pages = 0
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
        pages += 1
    writer.close()
    return pages


HEADER_KEYS = ["Nubank / case events", "Why it matters for the decision", "Role in the case"]
HEADER_FILL = (0.929, 0.894, 0.961)  # #EDE4F5


def shade_header_rows(doc):
    """Paint the light-purple background of each table header row *underneath* the page content.

    (Story's own cell background-color is buggy: it re-emits thin bands on every following page,
    so the CSS leaves headers unshaded and we add the shading here.)"""
    for page in doc:
        hlines, vx = [], []
        for dr in page.get_drawings():
            r = dr["rect"]
            fill = dr.get("fill")
            if not fill or abs(fill[0] - 0.6) > 0.05:
                continue  # only the grey table borders
            if r.height <= 1.5 and r.width > 20:
                hlines.append(r.y0)
            elif r.width <= 1.5 and r.height > 5:
                vx.extend([r.x0, r.x1])
        if not hlines or not vx:
            continue
        for key in HEADER_KEYS:
            for hit in page.search_for(key):
                above = [y for y in hlines if hit.y0 - 14 <= y <= hit.y0]
                below = [y for y in hlines if hit.y1 <= y <= hit.y1 + 14]
                if not above or not below:
                    continue
                row = pymupdf.Rect(min(vx), max(above), max(vx), min(below))
                page.draw_rect(row, color=None, fill=HEADER_FILL, width=0, overlay=False)


def finish(out_pdf, font_dir):
    """Add header shading, 'Page X of N' footers and document metadata."""
    doc = pymupdf.open(out_pdf)
    shade_header_rows(doc)
    n = doc.page_count
    fontfile = os.path.join(font_dir, "FiraGO-R.ttf")
    for i, page in enumerate(doc, start=1):
        page.insert_font(fontname="FiraGO", fontfile=fontfile)
        text = f"Page {i} of {n}"
        tw = pymupdf.Font(fontfile=fontfile).text_length(text, fontsize=8.5)
        x = (page.rect.width - tw) / 2
        y = page.rect.height - 40
        page.insert_text((x, y), text, fontname="FiraGO", fontfile=fontfile, fontsize=8.5, color=(0.35, 0.35, 0.35))
    doc.set_metadata({
        "title": "The Purple Card Goes North: Nubank and the Decision to Take Digital Banking from Brazil to Mexico",
        "subject": "Doing Business in the Americas - Term Project Part 1",
        "author": "Adrián Corpi Villaseñor",
        "creator": "build_pdf.py (PyMuPDF Story)",
    })
    try:
        doc.subset_fonts()  # embed only the glyphs actually used (much smaller file)
    except Exception:
        pass
    tmp = out_pdf + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, out_pdf)
    return n


def main():
    if not os.path.exists(DOCX):
        sys.exit(f"missing {DOCX} - run build_docx.py first")
    font_dir = prepare_fonts()
    html = decorate(docx_to_html(DOCX))
    render(html, PDF, font_dir)
    n = finish(PDF, font_dir)
    print(f"saved {os.path.basename(PDF)} ({n} pages)")


if __name__ == "__main__":
    main()
