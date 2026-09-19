import os
# -*- coding: utf-8 -*-
"""
Builds the Word deliverable for Term Project Part 1 (Doing Business in the Americas):
"The Purple Card Goes North: Nubank and the Decision to Take Digital Banking from Brazil to Mexico"
Run:  python3 build_docx.py
"""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

PURPLE = RGBColor(0x6A, 0x0D, 0xAD)
DARK = RGBColor(0x1F, 0x1F, 0x1F)
GREY = RGBColor(0x59, 0x59, 0x59)
HEADER_FILL = "E9DDF5"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Nubank_Case_Story_Part1.docx")

# --------------------------------------------------------------------------- helpers

def set_cell_shading(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def set_cell_margins(cell, top=50, bottom=50, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for k, v in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = OxmlElement(f"w:{k}")
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def add_runs(paragraph, text, size=11, color=None, base_bold=False, base_italic=False):
    """Tiny inline markup: **bold**, *italic*."""
    tokens = re.split(r"(\*\*.+?\*\*|\*.+?\*)", text)
    for tok in tokens:
        if not tok:
            continue
        bold, italic = base_bold, base_italic
        if tok.startswith("**") and tok.endswith("**"):
            tok, bold = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*"):
            tok, italic = tok[1:-1], True
        run = paragraph.add_run(tok)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        run.font.name = "Calibri"
        if color is not None:
            run.font.color.rgb = color
    return paragraph


def para(doc, text, size=11, align="justify", space_after=6, color=None, bold=False, italic=False,
         line_spacing=1.15):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    pf.line_spacing = line_spacing
    p.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY, "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "right": WD_ALIGN_PARAGRAPH.RIGHT}.get(align, WD_ALIGN_PARAGRAPH.LEFT)
    add_runs(p, text, size=size, color=color, base_bold=bold, base_italic=italic)
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph(style="Heading 1" if level == 1 else "Heading 2")
    pf = p.paragraph_format
    pf.keep_with_next = True
    if level == 1:
        pf.space_before = Pt(12)
        pf.space_after = Pt(5)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13.5)
        run.font.color.rgb = PURPLE
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "6A0DAD")
        pbdr.append(bottom)
        pPr.append(pbdr)
    else:
        pf.space_before = Pt(7)
        pf.space_after = Pt(3)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = DARK
    run.font.name = "Calibri"
    return p


def table(doc, headers, rows, widths, font_size=9.5, header_size=10):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].width = widths[i]
        set_cell_shading(hdr[i], HEADER_FILL)
        set_cell_margins(hdr[i])
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        add_runs(p, h, size=header_size, base_bold=True, color=PURPLE)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)
    for r in rows:
        cells = t.add_row().cells
        for i, val in enumerate(r):
            cells[i].width = widths[i]
            set_cell_margins(cells[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            add_runs(p, val, size=font_size)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        cant.set(qn("w:val"), "true")
        trPr.append(cant)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Term Project Part 1 · Nubank: Democratizing Financial Services · Page ")
    run.font.size = Pt(8.5)
    run.font.color.rgb = GREY
    fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
    r2 = p.add_run(); r2.font.size = Pt(8.5); r2.font.color.rgb = GREY
    r2._r.append(fld_begin); r2._r.append(instr); r2._r.append(fld_end)


def reference(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Inches(0.5)
    pf.first_line_indent = Inches(-0.5)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.05
    add_runs(p, text, size=9.5)


# --------------------------------------------------------------------------- document

doc = Document()

def _tune_heading_styles(d):
    """Make built-in Heading 1/2 inherit the body font and colour so custom run formatting rules."""
    from docx.shared import Pt as _Pt
    for name, size in (("Heading 1", 13.5), ("Heading 2", 11.5)):
        st = d.styles[name]
        st.font.name = "Calibri"
        st.font.size = _Pt(size)
        st.font.bold = True
        st.font.color.rgb = PURPLE
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
        for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(attr), "Calibri")
        rfonts.attrib.pop(qn("w:asciiTheme"), None); rfonts.attrib.pop(qn("w:hAnsiTheme"), None)
        rfonts.attrib.pop(qn("w:eastAsiaTheme"), None); rfonts.attrib.pop(qn("w:cstheme"), None)
        st.paragraph_format.space_before = _Pt(12 if name == "Heading 1" else 7)
        st.paragraph_format.space_after = _Pt(5 if name == "Heading 1" else 3)
        st.paragraph_format.keep_with_next = True
_tune_heading_styles(doc)
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(1)
sec.top_margin = sec.bottom_margin = Inches(1)
add_page_number_footer(sec)

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

# ---- Title block
para(doc, "Universidad Tecmilenio · Doing Business in the Americas", size=10.5, align="center",
     color=GREY, space_after=2)
para(doc, "Term Project – Part 1: Analyzing a Business Case in the Americas", size=10.5,
     align="center", color=GREY, space_after=10)
para(doc, "The Purple Card Goes North", size=22, align="center", bold=True, color=PURPLE, space_after=2,
     line_spacing=1.0)
para(doc, "Nubank and the Decision to Take Digital Banking from Brazil to Mexico", size=14,
     align="center", color=DARK, space_after=10, line_spacing=1.0)
para(doc, "Case analyzed: Chu, M., Larangeira, C., & Levindo, P. (2020). *Nubank: Democratizing "
          "Financial Services* (HBS Case No. 321-068). Harvard Business School – Latin America Research Center.",
     size=10, align="center", color=GREY, space_after=2)
para(doc, "Student: ______________________    Student ID: ____________    Professor: ______________________    "
          "Date: September 2026", size=10, align="center", color=GREY, space_after=4)

# ---- 1. Case selection and location
heading(doc, "1. The case I chose and where the story takes place")
para(doc,
     "From the Harvard Business School *Latin America* page I selected **Nubank: Democratizing Financial "
     "Services**, a 33-page case by Michael Chu, Carla Larangeira and Pedro Levindo of HBS's Latin America Research "
     "Center (Chu et al., 2020; Harvard Business School, n.d.). It follows David Vélez, the Colombian founder and CEO of Nubank, when his company—“a "
     "wholly-digital solution created to disrupt Brazilian banking, with 6 million clients and a $4 billion valuation "
     "after five years”—must decide whether to expand to Mexico, which Vélez saw as “the gateway” to a Latin America "
     "that shared “the same banking pain points as Brazil” (Chu et al., 2020). I chose it because it links the two "
     "largest economies of Latin America, because its outcome is unfolding in my own country today (Nu México became "
     "a licensed bank in July 2026 with 16 million customers), and because it illustrates the central lesson of this "
     "course: the Americas share many pain points, but country differences still decide which strategies work.")
para(doc,
     "**Geographical location.** Nubank was born on May 6, 2013, in a small rented house in Brooklin, a neighborhood "
     "in the south of São Paulo—the largest city of South America and Brazil's financial capital, home to the B3 "
     "stock exchange and the headquarters of the largest private banks (Financial Times, 2025; Sequoia Capital, "
     "2021). Brazil is a Portuguese-speaking federal republic of about 212 million people and the largest economy in "
     "Latin America. The decision in the case points north, toward Mexico (North America, about 126 million people at "
     "the time), where Nubank opened an office in Mexico City in April–May 2019 under general manager Emilio González "
     "(Mexico News Daily, 2022). The story thus stretches across the two poles of Latin America—the South Atlantic "
     "giant and the Spanish-speaking neighbor of the United States—with Colombia, Vélez's homeland and Nubank's "
     "third market in 2020, in between.")

# ---- 2. Business environment
heading(doc, "2. The business environment: economic, political, regulatory and cultural context")
heading(doc, "2.1 Brazil's economy in the 2010s: a rich banking oligopoly in a poor decade", level=2)
para(doc,
     "The Brazil in which Nubank grew up was living its worst recession in modern history. Real GDP fell 3.5% in 2015 "
     "and 3.3% in 2016, inflation passed 10%, the central bank raised the Selic policy rate from 11% in mid-2014 to "
     "14.25% by July 2015, and unemployment climbed to around 13% in 2017 (IMF, 2019). Paradoxically, the banking "
     "system remained extremely profitable. Five institutions—Itaú Unibanco, Bradesco, Banco do Brasil, Caixa "
     "Econômica Federal and Santander Brasil—controlled roughly 80% of assets and more than 80% of credit, far above "
     "the ~50% concentration of the United States, and private banks earned returns on equity in the mid-to-high "
     "teens thanks to wide spreads and heavy fees (Seafarer Funds, 2022; U.S. Department of State, 2025). Credit "
     "cards were the most visible symptom: Brazilians paid annual fees on cards whose revolving interest rate was the "
     "most expensive credit in the country—still 431.6% per year in 2023, even after the central bank limited "
     "revolving balances to 30 days in 2017 (Reuters, 2023). Meanwhile, 45 million adults had no bank account—86% of "
     "them from the C, D and E income classes and 39% in the poorer Northeast—yet moved an estimated R$817 billion a "
     "year in cash (G1, 2019), and only about 60% of Brazil's 5,570 municipalities had a bank branch (Nubank, 2019). "
     "Two technological shifts turned this frustration into an opportunity: smartphones spread across all income "
     "classes, and cloud computing (Nubank ran on Amazon Web Services from day one) made it possible to run a bank "
     "without branches or mainframes. The macro cycle helped too: as the Selic fell to 6.5% in 2018 and 4.5% by the "
     "end of 2019, incumbents' interest income came under pressure while cheap global capital was hunting for growth "
     "in emerging markets.")

heading(doc, "2.2 Politics and regulation: from Lava Jato to a pro-competition central bank", level=2)
para(doc,
     "Politically, the decade was turbulent: mass protests in June 2013 (one month after Nubank was founded), the "
     "*Lava Jato* corruption investigation from 2014, the impeachment of President Dilma Rousseff in 2016, the "
     "unpopular Temer interlude and, in October 2018, the election of Jair Bolsonaro on a liberal economic agenda "
     "led by minister Paulo Guedes (IMF, 2019). For a start-up this meant currency volatility, a deep consumer-credit "
     "downturn and uncertainty about the rules of the game. The regulatory story, however, moved in Nubank's favor. "
     "Law 12,865 of 2013 created the *payment institution*, which let a non-bank issue a credit card under central "
     "bank supervision—the framework under which the purple card was launched in 2014. Because Nubank was "
     "foreign-controlled, it needed a presidential decree, signed by Temer in January 2018, before the Banco Central "
     "do Brasil (BCB) authorized Nu Financeira as a financial institution on November 23, 2018, ending its dependence "
     "on partner banks to fund credit and opening the door to personal loans and a debit card (Seu Dinheiro, 2018). "
     "In April 2018 the National Monetary Council created licenses for lending fintechs (Resolution 4,656), and the "
     "BCB's *Agenda BC+/BC#* explicitly promoted competition and inclusion, later delivering the instant-payment "
     "system Pix (November 2020) and Open Finance (2021), one of the fastest and most comprehensive implementations "
     "in the world (U.S. Department of State, 2025). The regulator, in short, was not an obstacle but an ally trying "
     "to break the oligopoly—a crucial difference when comparing Brazil with Mexico.")

heading(doc, "2.3 Culture: distrust of banks, love of credit and the power of word of mouth", level=2)
para(doc,
     "Brazilians had a deeply ambivalent relationship with banks. Vélez himself needed five months, security doors, "
     "a guard and stacks of documents to open an account when he moved to São Paulo in 2008 (Stanford Graduate School of Business, 2022). "
     "Banking meant queues, hidden tariffs and condescending service, yet the credit card was a symbol of belonging: "
     "purchases are habitually split into interest-free installments, and 51% of the unbanked borrowed a friend's or "
     "relative's card to shop (G1, 2019). Brazil is also one of the most intensive users of social media in the "
     "world, so a transparent, fee-free purple card managed from an app spread almost entirely by referral, earned "
     "the nickname *roxinho* and generated a waiting list of millions; the brand name—*nu*, “naked”—promised "
     "transparency in a market that had none. Finally, Brazil's size and regional inequality mattered: a digital bank "
     "could reach the Northeast and the interior where branches did not exist, which is why Nubank was present in "
     "100% of Brazilian municipalities within five years (Nubank, 2019).")

heading(doc, "2.4 The target market: Mexico in 2019", level=2)
para(doc,
     "Mexico looked like Brazil's pain points multiplied. Only 47% of Mexicans aged 18–70 had an account with a bank "
     "or financial institution in 2018, 68% had at least one formal financial product and just 31% had formal credit "
     "(INEGI, 2018; CONDUSEF, 2019). Cash dominated everyday life—even in 2024, 85% of adults still used cash as their "
     "main payment method for purchases under 500 pesos (INEGI, 2025)—and more than half of the workforce was "
     "informal (54.6% in December 2025 according to INEGI's ENOE), which makes traditional credit scoring difficult. "
     "The banking system was, like Brazil's, an oligopoly, but a mostly foreign-owned one—BBVA, Citibanamex, "
     "Santander, Banorte, HSBC and Scotiabank—with high annual fees. Politically, Andrés Manuel López Obrador had "
     "just taken office (December 2018) with a discourse critical of bank commissions, and Banco de México was "
     "preparing its own QR-payment system, CoDi (September 2019). Mexico had passed Latin America's first "
     "comprehensive Fintech Law in March 2018, but the ladder to becoming a bank was long: Nubank would have to start "
     "as a non-bank lender (SOFOM), buy a *Sociedad Financiera Popular* (Akala, September 2021) to take deposits, and "
     "only in April 2025 obtain CNBV approval to become a bank—the first SOFIPO ever allowed to do so (Fintech "
     "Futures, 2025; Mexico News Daily, 2022). Culturally, Mexico shares Latin America's distrust of banks, but with a "
     "stronger cash habit, a different credit-bureau infrastructure, remittance-dependent households and a consumer "
     "who had never seen a large digital bank succeed.")

# ---- 3. Historical context & timeline
heading(doc, "3. Historical context: global events that shaped the story")
para(doc,
     "Nubank is a child of the 2008 global financial crisis, which destroyed trust in incumbent banks, pushed "
     "interest rates in rich countries to zero and sent venture capital looking for growth in emerging markets—and "
     "which brought Vélez to Brazil in 2008 to open a private-equity office. The smartphone revolution and cloud "
     "computing made branchless banking possible, and Chinese platforms such as Tencent's WeChat Pay provided both a "
     "model and, in 2018, an investor. Ironically, Sequoia Capital had withdrawn from Latin America in 2012 for lack "
     "of technical talent, yet backed Vélez anyway—“there was no pitch. We invested 80% based on him,” recalled "
     "partner Doug Leone (Sequoia Capital, 2021). In 2019 SoftBank's US$5 billion Latin America fund flooded the "
     "region with capital; in 2020 the COVID-19 pandemic accelerated digital adoption by years, just as Nubank was "
     "launching in Mexico; and the 2022 global rate shock later forced fintechs to prove they could be profitable, "
     "which Nubank did in 2023. Table 1 summarizes the timeline that leads to, and follows, the decision.")
para(doc, "**Table 1.** Timeline of the case and its context (case decision point in bold)", size=10,
     align="left", space_after=3)
table(doc,
      ["Year", "Nubank / case events", "Brazil, Mexico and global context"],
      [
          ["2008–2012", "Vélez moves to Brazil (opening a bank account takes five months); as a Sequoia partner he "
                        "decides to build a digital bank after Sequoia leaves Latin America in 2012.",
           "Global financial crisis; smartphones reach the mass market; Brazil's commodity boom ends."],
          ["2013", "May 6: Nubank founded in São Paulo by Vélez, Cristina Junqueira (ex-Itaú) and Edward Wible; "
                   "US$2 million seed round led by Sequoia and Kaszek.",
           "June: mass protests across Brazil; Law 12,865 creates payment institutions."],
          ["2014", "Purple no-fee Mastercard launched (first transaction April 1); Series A of US$14.3 million.",
           "*Lava Jato* begins; Rousseff re-elected; recession starts."],
          ["2015–2016", "Viral waiting list; 1 million customers by 2016; Series B (Tiger Global), C (Founders "
                        "Fund) and D (DST Global).",
           "GDP falls 3.5% and 3.3%; Selic at 14.25%; Rousseff impeached (2016)."],
          ["2017", "NuConta digital account (October) and Nubank Rewards launched; engineering office opened in "
                   "Berlin to attract talent.",
           "BCB limits revolving credit to 30 days; unemployment peaks near 13%."],
          ["2018", "Presidential decree (Jan.) and BCB authorization (Nov.) for Nu Financeira; 5 million customers "
                   "(Sept.); Tencent invests US$180 million at a US$4 billion valuation (Oct.).",
           "Mexico enacts its Fintech Law (March); Resolution 4,656 licenses lending fintechs; Bolsonaro elected; "
           "AMLO takes office in Mexico (Dec.)."],
          ["**2019**", "**Case decision point:** ~6 million clients; personal loans launched; offices opened in "
                       "Mexico City (GM Emilio González) and Argentina; July: Series F of US$400 million led by TCV "
                       "at a US$10 billion valuation with 12 million customers; net loss of R$312 million.",
           "Selic falls to 4.5%; Instituto Locomotiva counts 45 million unbanked Brazilians; SoftBank's US$5 "
           "billion LatAm fund; Banxico launches CoDi."],
          ["2020", "March: no-fee credit card launched in Mexico; entry into Colombia; 20+ million customers; the "
                   "HBS case is published (August).",
           "COVID-19 pandemic accelerates digital banking; Pix launched in Brazil (November)."],
          ["2021–2023", "Nu México buys the SOFIPO Akala (Sept. 2021); Berkshire Hathaway invests; IPO on the NYSE "
                        "on December 9, 2021 (~US$41.5 billion); Cuenta Nu launched in Mexico with a 9% yield (May "
                        "2023); first profitable year (2023).",
           "Open Finance starts in Brazil; 2022 rate shock crushes fintech valuations; Brazil caps revolving card "
           "debt at 2x (2023)."],
          ["2024–2025", "100 million customers (May 2024) and 114 million by year-end; CNBV approves Nu México's "
                        "banking license (April 2025); 10+ million Mexican customers.",
           "ENIF 2024: Mexicans with a credit card up almost 50% since 2021; former BCB governor Roberto Campos "
           "Neto joins Nubank."],
          ["2026", "Nu México authorized to operate as a bank (July) with 16 million customers and a US$4.2 "
                   "billion investment plan to 2030; 2Q26 net income of US$1.1 billion; 139 million customers "
                   "(118 M Brazil, 16 M Mexico, 5 M Colombia).",
           "Conditional U.S. bank-charter approval (Jan.); Pix processes more transactions than cards in Brazil."],
      ],
      widths=[Inches(0.8), Inches(3.25), Inches(2.45)])
para(doc,
     "*Sources:* Chu et al. (2020); Sequoia Capital (2021); Estadão (2018); Seu Dinheiro (2018); Nubank (2019); "
     "Forex.com (2021); Nu International (2023, 2025); Reuters (2025); Finextra (2026); Mexico Business News (2026).",
     size=9, align="left", color=GREY, space_after=4)

# ---- 4. Business situation
heading(doc, "4. The business situation and the challenges Nubank faced")
para(doc,
     "At the decision point Nubank was the fastest-growing financial institution in Brazil and, in its own words, "
     "the largest digital bank in the world outside Asia. Its model rested on four pillars: (1) a no-fee, radically "
     "transparent product that incumbents could not copy without cannibalizing billions in fee income; (2) a cost "
     "structure a fraction of a branch bank's, built on proprietary cloud software, data-driven credit models and "
     "chat-based service by young “Xpeers” empowered to solve problems; (3) growth driven almost entirely by word of "
     "mouth, which kept acquisition costs near zero and Net Promoter Scores far above the industry; and (4) patient "
     "venture capital that financed years of losses—R$312 million in 2019 and R$230 million in 2020 (Forex.com, "
     "2021). In 2017–2019 it had begun to evolve from a single product into a platform: NuConta (8 million users by "
     "mid-2019), Rewards, personal loans (offered to more than 500,000 customers within months) and an account for "
     "small businesses (Nubank, 2019).")
para(doc,
     "Yet the situation was far from comfortable. First, the Brazilian disruption was unfinished: 6–12 million "
     "customers in a country of 210 million with 45 million unbanked meant the home market alone could absorb all of "
     "Nubank's capital and attention. Second, incumbents were finally reacting—Bradesco's *next*, Itaú's *iti*, "
     "Santander's *Superdigital*—while digital rivals such as Banco Inter, C6 Bank, Neon, PicPay and Mercado Pago "
     "multiplied, and the central bank's Pix and Open Finance agenda threatened to commoditize some of Nubank's "
     "advantages while opening new ones. Third, the economics were fragile: revenue depended on card interchange and "
     "interest in an economy recovering from recession, credit losses had to be managed with limited positive credit "
     "data, and every new product required a new license. Fourth, talent was scarce, which is why Nubank had opened "
     "an engineering office in Berlin. Against this backdrop, Vélez argued that Nubank's true market was not Brazil "
     "but the 650 million people of Latin America, and that Mexico—large, underbanked, concentrated and "
     "geographically the gateway to the region—was the place to prove that the model traveled.")

# ---- 5. Problem definition
heading(doc, "5. Definition of the central problem and the variables that affect it")
para(doc,
     "**Central problem.** In 2019, with roughly six million customers, a US$4 billion valuation, growing losses and "
     "incumbents beginning to respond at home, should Nubank commit scarce capital, engineering talent and "
     "management attention to replicate its digital-banking model in Mexico—a larger unbanked market with a "
     "different regulatory path, competitive set, credit infrastructure and consumer culture—or concentrate on "
     "deepening its still-incomplete disruption of Brazil? And if it goes, *how* should it enter: with which product, "
     "under which license, with what team and at what pace? It is a classic trade-off between depth and breadth in "
     "international expansion, complicated by the fact that Nubank's advantage was partly built on Brazil-specific "
     "conditions. Table 2 lists the variables that determine the answer and why each one matters.")
para(doc, "**Table 2.** Relevant variables of the central problem", size=10, align="left", space_after=3)
table(doc,
      ["Variable", "Why it matters for the decision"],
      [
          ["Size of the inclusion gap in each market",
           "Brazil still had 45 million unbanked; Mexico had 53% of adults without an account and 69% without formal "
           "credit. The larger gap in Mexico is the main argument to go; the unfinished gap in Brazil is the main "
           "argument to stay."],
          ["Regulatory pathway and regulator attitude",
           "In Brazil the BCB actively promoted competition and Nubank already held a financial-institution license; "
           "in Mexico it would have to climb from SOFOM to SOFIPO to bank (completed only in 2025–2026), limiting "
           "products, deposit funding and speed."],
          ["Competitive intensity, incumbent response and timing",
           "Brazilian incumbents were launching digital banks; in Mexico the foreign-owned oligopoly and local "
           "fintechs (Klar, Stori, albo, Mercado Pago) were scaling in 2019–2020. Entering early could lock in "
           "leadership (16 million customers by 2026); entering with an incomplete product could burn capital and "
           "reputation."],
          ["Capital availability and runway",
           "Expansion had to be financed with venture money while the Brazilian operation still lost hundreds of "
           "millions of reais; the US$400 million Series F of July 2019 was raised precisely to fund new products "
           "and internationalization."],
          ["Unit economics: acquisition cost, cost to serve, revenue mix",
           "Word-of-mouth growth and a low cost structure made the model viable in Brazil; whether Mexicans would "
           "refer friends at the same rate, and whether interchange and interest income would cover risk in a cash "
           "economy, was unknown."],
          ["Credit-risk data and infrastructure",
           "Models trained on Brazilian bureaus (Serasa, Boa Vista) do not transfer automatically to Mexico's Buró "
           "de Crédito and a 55%-informal labor market; mispriced risk could destroy the entry."],
          ["Portability of the technology platform",
           "A cloud-native, proprietary core lowers the marginal cost of a second market, but localization—Spanish, "
           "peso, tax, KYC, card processing—still consumes scarce engineering time."],
          ["Talent, organization and management focus",
           "With about 2,000 employees and a Berlin office created because of talent scarcity, every engineer sent to "
           "Mexico was one less improving the Brazilian product; opportunity cost is a real variable."],
          ["Macroeconomic and political risk",
           "Brazil's recovery was fragile and Mexico's new government was hostile to bank fees yet unpredictable; "
           "exchange-rate swings affect dollar-denominated funding and valuation."],
          ["Cultural fit and brand transferability",
           "Nubank's brand meant transparency and a “cool” purple card in Brazil; in Mexico the same product could be "
           "seen as a risky foreign start-up in a cash-loving market—later addressed with the *moradita* card and "
           "secured cards for people with no credit history."],
      ],
      widths=[Inches(1.9), Inches(4.6)])

# ---- 6. Stakeholders
heading(doc, "6. Stakeholders: who is involved, their roles and their connections")
para(doc,
     "The decision touched a dense web of individuals, companies and institutions in two countries. Table 3 "
     "identifies them; the paragraph that follows explains how they are connected.")
para(doc, "**Table 3.** Stakeholder map of the case", size=10, align="left", space_after=3)
table(doc,
      ["Stakeholder", "Role in the case", "Connection to the problem"],
      [
          ["David Vélez (founder & CEO)",
           "Colombian ex-Sequoia partner; framed Latin America, not Brazil, as the market.",
           "Owner of the decision; his regional ambition versus the team's capacity to execute."],
          ["Cristina Junqueira and Edward Wible (co-founders)",
           "Junqueira, ex-Itaú credit-card executive, led product and later Nubank Brazil; Wible, American "
           "engineer, built the technology.",
           "Junqueira embodies the Brazilian focus; Wible's platform determines whether the model can be exported "
           "cheaply."],
          ["Employees (~2,000 in 2019: Xpeers, engineers, Berlin office)",
           "Deliver the service culture and the software that are the real competitive advantage.",
           "Scarce talent must be split between Brazil and a new country; the culture must be transplanted."],
          ["Venture investors: Sequoia, Kaszek, Tiger Global, Founders Fund, DST Global, Tencent, TCV, QED, Ribbit "
           "(later Berkshire Hathaway)",
           "Financed years of losses; Tencent brought Chinese fintech know-how; TCV's US$400 million round funded "
           "internationalization.",
           "They expect regional scale to justify a US$10 billion valuation, but also discipline in burning capital."],
          ["Customers in Brazil (6–12 million, mostly young and urban) and the 45 million unbanked",
           "Source of revenue, referrals and brand; the unbanked are the mission.",
           "Any dilution of service quality at home risks the word-of-mouth engine that finances expansion."],
          ["Mexican consumers (53% without an account; later 16 million Nu customers, about half with no prior "
           "credit)",
           "Target market of the expansion.",
           "Their cash habits, informality and distrust dictate product design (no-fee card, secured card, "
           "high-yield account)."],
          ["Banco Central do Brasil and National Monetary Council",
           "Licensed Nubank as payment institution and financial institution; pushed pro-competition reforms "
           "(Pix, Open Finance).",
           "A supportive regulator at home versus an unknown one abroad; its former governor, Roberto Campos "
           "Neto, joined Nubank in 2025 as global head of public policy."],
          ["Mexican authorities: CNBV, Banco de México, SHCP, CONDUSEF",
           "Gatekeepers of SOFOM/SOFIPO/bank licenses and consumer protection under the 2018 Fintech Law.",
           "Determined the speed and scope of Nu México's products (deposits only from 2023, bank status in 2026)."],
          ["Incumbent banks: Itaú, Bradesco, Banco do Brasil, Caixa and Santander in Brazil; BBVA, Citibanamex, "
           "Santander, Banorte, HSBC and Scotiabank in Mexico",
           "The oligopolies Nubank was created to disrupt; Brazilian ones launched digital banks (*next*, *iti*).",
           "Their counter-attack raises the cost of neglecting Brazil, while Mexico's banks have deep pockets and "
           "political access."],
          ["Fintech rivals: Banco Inter, C6, Neon, PicPay, Mercado Pago (Brazil); Klar, Stori, albo, Ualá, RappiPay "
           "(Mexico)",
           "Compete for the same underbanked customers and the same venture capital.",
           "Speed of entry matters because these players were scaling in 2019–2020."],
          ["Partners: Mastercard, Amazon Web Services, credit bureaus (Serasa Experian, Boa Vista, Buró de Crédito, "
           "Círculo de Crédito)",
           "Provide the card network, cloud infrastructure and risk data.",
           "Their availability and pricing in Mexico condition unit economics and credit quality."],
          ["Governments, society and media (Temer's 2018 decree; AMLO's administration; social networks in both "
           "countries)",
           "Set the political climate toward foreign fintechs and bank fees; amplify the brand; financial inclusion "
           "is a public-policy goal.",
           "A presidential decree was needed in Brazil; anti-bank rhetoric in Mexico was both opportunity and risk; "
           "legitimacy depends on visibly serving the excluded."],
      ],
      widths=[Inches(2.0), Inches(2.25), Inches(2.25)])
para(doc,
     "**How the pieces connect.** The founders' regional vision could only be pursued because investors kept "
     "financing losses in exchange for growth, and investors did so because customers kept referring new customers at "
     "almost no cost—a virtuous circle that depends on employees sustaining service quality. Regulators sit at the "
     "center of the web: the BCB's decision to license Nubank and to open the market with Pix and Open Finance made "
     "the Brazilian circle possible, while the CNBV's slower licensing ladder dictated that Nu México would start with "
     "a single credit card in March 2020, add deposits only after buying Akala in 2021, launch Cuenta Nu in 2023 and "
     "become a bank in 2026. Incumbents and fintech rivals in both countries determine how much time Nubank has before "
     "the window closes, and partners such as Mastercard and AWS make the model exportable in the first place. Any "
     "solution proposed in Part 2—how, when and with what product to enter Mexico—will have to be negotiated with "
     "each of these actors.")

# ---- 7. Closing
heading(doc, "7. What is at stake")
para(doc,
     "Seen from 2026 the story has a known ending: Nu México is the largest digital bank in Mexico, with 16 million "
     "customers, a full banking license and a US$4.2 billion investment plan through 2030, and Nu Holdings earns more "
     "than US$1 billion per quarter serving 139 million people (Finextra, 2026; Mexico Business News, 2026; The "
     "Motley Fool, 2026). But in 2019 none of that was obvious. Nubank was a loss-making start-up whose advantage had "
     "been built on Brazilian regulation, Brazilian social habits and Brazilian data, and Mexico was a country where "
     "cash, informality, a foreign-owned banking oligopoly and a cautious regulator could easily have absorbed its "
     "capital without returning a single peso. This first part has reconstructed that moment—the place, the "
     "environment, the timeline, the problem and the people—so that Part 2 can evaluate the strategic routes Nubank "
     "could have taken and propose the one that best fits the differences, not only the similarities, between the two "
     "largest countries of Latin America.")

# ---- References
heading(doc, "References")
refs = [
    "Chu, M., Larangeira, C., & Levindo, P. (2020). *Nubank: Democratizing financial services* (HBS Case No. "
    "321-068). Harvard Business School. https://store.hbr.org/product/nubank-democratizing-financial-services/321068",
    "CONDUSEF. (2019, January). Educación e inclusión financiera en México: Conoce los resultados de la ENIF 2018. "
    "*Revista Proteja su Dinero*. https://revista.condusef.gob.mx/usuario-inteligente/ponlo-en-la-balanza/2019/01/"
    "educacion-e-inclusion-financiera-en-mexico/",
    "Estadão. (2018, September 27). Nubank chega a 5 milhões de clientes e muda design do cartão. "
    "https://www.estadao.com.br/link/inovacao/nubank-chega-a-5-milhoes-de-clientes-e-muda-design-do-cartao/",
    "Financial Times. (2025, March 7). Cristina Junqueira: The Brazil fintech leader shaking up banking. "
    "https://www.ft.com/content/0f3d79a2-c6bb-4ac4-813c-a21c38ca9340",
    "Finextra. (2026, July 13). Nubank receives banking authorisation in Mexico. "
    "https://www.finextra.com/newsarticle/48081/nubank-receives-banking-authorisation-in-mexico",
    "Fintech Futures. (2025, April 28). Nubank's Mexican arm secures banking licence approval from CNBV. "
    "https://www.fintechfutures.com/challenger-banks/nubanks-mexican-arm-secures-banking-licence-approval-from-cnbv",
    "Forex.com. (2021, November 22). Nubank IPO: Everything you need to know about Nubank. "
    "https://www.forex.com/en-sg/news-and-analysis/nubank-ipo/",
    "G1. (2019, August 15). Brasil tem 45 milhões de desbancarizados, aponta instituto [Instituto Locomotiva survey]. "
    "https://g1.globo.com/economia/noticia/2019/08/15/brasil-tem-45-milhoes-de-desbancarizados-aponta-instituto.ghtml",
    "Harvard Business School. (n.d.). *Latin America*. https://www.hbs.edu/global/about/Pages/latin-america.aspx",
    "IMF. (2019). An eventful two decades of reforms, economic boom, and a historic crisis. In *Brazil: Boom, bust, "
    "and the road to recovery* (Chapter 2). International Monetary Fund. "
    "https://www.elibrary.imf.org/display/book/9781484339749/ch002.xml",
    "INEGI. (2018, November 23). *Encuesta Nacional de Inclusión Financiera (ENIF) 2018* [Press release 600/18]. "
    "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2018/OtrTemEcon/ENIF2018.pdf",
    "INEGI. (2025, March 13). *Encuesta Nacional de Inclusión Financiera (ENIF) 2024: Resultados*. "
    "https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/enif/ENIF2024_RR.pdf",
    "Mexico Business News. (2026, August 25). Nu net income hits US$1.1 billion in 2Q26 as Mexico bank launches. "
    "https://mexicobusiness.news/finance/news/nu-net-income-hits-us11-billion-2q26-mexico-bank-launches",
    "Mexico News Daily. (2022, November 25). Brazilian Nubank introduces savings accounts, debit cards to Mexican "
    "market. https://mexiconewsdaily.com/business/brazil-nubank-new-products-mexico/",
    "Nu International. (2023, May 4). Nu Mexico announces the public launch of Cuenta Nu. "
    "https://international.nubank.com.br/consumers/nu-mexico-announces-the-public-launch-of-cuenta-nu/",
    "Nu International. (2025, March 26). Nu Mexico turns 6 and celebrates 5 years since the launch of its credit card. "
    "https://international.nubank.com.br/company/nu-mexico-turns-6-and-celebrates-5-years-since-the-launch-of-its-credit-card/",
    "Nubank. (2019, July). Nubank raises USD 400 M in investment round led by TCV. *Building Nubank*. "
    "https://building.nu.com/nubank-raises-usd-400-million-in-investment-round-led-by-tcv-2019/",
    "Reuters. (2023, December 21). Brazil limits debt growth on revolving credit card lines. "
    "https://www.reuters.com/world/americas/brazil-limits-debt-growth-revolving-credit-card-lines-2023-12-21/",
    "Reuters. (2025, April 24). Nubank clears major hurdle in securing Mexico banking license. "
    "https://www.reuters.com/world/americas/nubank-clears-major-hurdle-securing-mexico-banking-license-2025-04-24/",
    "Seafarer Funds. (2022, November). Brazil's fintech revolution. "
    "https://www.seafarerfunds.com/commentary/brazils-fintech-revolution/",
    "Sequoia Capital. (2021, July 31). The Latin American startup opportunity. "
    "https://sequoiacap.com/article/the-latin-american-startup-opportunity/",
    "Seu Dinheiro. (2018, December 11). BC autoriza Nubank a atuar como instituição financeira e empresa lança cartão "
    "de débito. https://www.seudinheiro.com/bc-autoriza-nubank-a-atuar-como-instituicao-financeira/",
    "Stanford Graduate School of Business. (2022, May 25). David Vélez: “Position yourself in the scarcity, not in the "
    "oversupply.” https://www.gsb.stanford.edu/insights/david-velez-position-yourself-scarcity-not-oversupply",
    "The Motley Fool. (2026, August 20). Nu (NU) Q2 2026 earnings call transcript. "
    "https://www.fool.com/earnings/call-transcripts/2026/08/20/nu-nu-q2-2026-earnings-call-transcript/",
    "U.S. Department of State. (2025). *2025 investment climate statements: Brazil*. "
    "https://www.state.gov/reports/2025-investment-climate-statements/brazil",
]
for r in refs:
    reference(doc, r)

doc.core_properties.title = "The Purple Card Goes North: Nubank and the Decision to Take Digital Banking from Brazil to Mexico"
doc.core_properties.subject = "Doing Business in the Americas - Term Project Part 1"
doc.core_properties.author = "Student"
doc.core_properties.comments = ""
doc.save(OUT)
print("saved", OUT)
