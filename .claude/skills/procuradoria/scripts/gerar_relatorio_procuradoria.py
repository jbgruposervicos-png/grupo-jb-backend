#!/usr/bin/env python3
"""Gerador oficial do Relatorio de Procuradoria — Grupo JB Contabilidade.

Uso:

    python gerar_relatorio_procuradoria.py dados.json saida.png

O script renderiza um PNG vertical de altura dinamica a partir de um unico
arquivo JSON. Ele NAO le PDF, NAO le imagens, NAO acessa o Google Drive e NAO
infere nenhum dado: tudo que aparece no relatorio vem do JSON de entrada.

O layout segue o modelo visual oficial em
`.claude/skills/procuradoria/references/modelo-relatorio-procuradoria.png`:
fundo cinza-azulado, folha branca arredondada com sombra suave, cabecalho azul
escuro, blocos com fundo tingido e borda na cor do tema, linhas divisorias
finas entre os itens e subtotal destacado ao pe de cada bloco.

Valores ausentes ou nulos nunca sao substituidos por zero nem estimados — sao
apresentados como nao informados e ficam fora do total.

Codigos de saida:

    0  relatorio gerado
    1  erro (JSON invalido, arquivo ausente, falha de escrita)
    2  nenhuma condicao financeira identificada — relatorio nao deve ser gerado
       (secao 4 do SKILL.md: alerta sozinho nao gera relatorio)
"""

import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:  # pragma: no cover - depende do ambiente
    sys.stderr.write(
        "ERRO: a biblioteca Pillow e necessaria para gerar o PNG.\n"
        "Instale com: pip install Pillow\n"
    )
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# Geometria e paleta, medidas sobre o modelo oficial (900 px de largura)
# ---------------------------------------------------------------------------

WIDTH = 900
PAGE_PAD = 30

SHEET_X0 = PAGE_PAD
SHEET_X1 = WIDTH - PAGE_PAD
SHEET_RADIUS = 18

CARD_INSET = 36
CARD_X0 = SHEET_X0 + CARD_INSET
CARD_X1 = SHEET_X1 - CARD_INSET
CARD_RADIUS = 10
CARD_PAD_X = 27
CARD_PAD_TOP = 22
CARD_PAD_BOTTOM = 20

HEADER_INSET = 3
HEADER_RADIUS = 14

BLOCK_GAP = 21
HEADER_GAP = 31
ROW_PAD_Y = 13
BAR_W = 6

PAGE_BG = "#EEF1F5"
SHEET_BG = "#FFFFFF"
SHADOW = (92, 106, 126, 52)

NAVY = "#12355B"
NAVY_EYEBROW = "#8FA8C4"
NAVY_META = "#AFC6DE"

INK = "#2B2B2B"
MUTED = "#8A8F98"
FOOTER_INK = "#7C8898"

# Tema: (fundo, borda, divisoria, divisoria forte, titulo, valor, subtitulo)
THEME_RED = ("#FDECEC", "#E8B4B4", "#F0DADA", "#DFC4C4", "#A5292A", "#C0392B", "#96706F")
THEME_AMBER = ("#FDF3E3", "#EFD3A0", "#F3E6CC", "#E7D3AB", "#8A5B00", "#B37700", "#8F7648")
THEME_GREEN = ("#EAF6EE", "#B6DDC4", "#D5EADD", "#C2DFCE", "#1F6B41", "#1F6B41", "#6D8A79")
THEME_BLUE = ("#EAF2FB", "#B7D0EA", "#D8E6F4", "#C6D9EC", "#1F4E7A", "#1F4E7A", "#6C8299")

ALERT_BAR = "#E8A317"
ALERT_BG = "#FDF3E3"
ALERT_INK = "#33312C"

TOTAL_BG = "#C0392B"

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/TTF",
    "/Library/Fonts",
    "C:/Windows/Fonts",
)
FONT_REGULAR = ("DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf")
FONT_BOLD = ("DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf")


def _find_font(names):
    for directory in FONT_DIRS:
        for name in names:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                return path
    return None


_REGULAR_PATH = _find_font(FONT_REGULAR)
_BOLD_PATH = _find_font(FONT_BOLD)


def font(size, bold=False):
    path = _BOLD_PATH if bold else _REGULAR_PATH
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def line_height(f):
    try:
        ascent, descent = f.getmetrics()
        return ascent + descent
    except AttributeError:  # fonte bitmap de fallback
        return f.size + 4


def has_glyph(f, char):
    """Detecta se a fonte possui o caractere, comparando com um vazio conhecido.

    Evita que icones virem quadrados de .notdef em ambientes sem DejaVu.
    """
    try:
        return f.getmask(char).getbbox() != f.getmask("\ue000").getbbox()
    except Exception:
        return False


def icon(f, char):
    return char + " " if has_glyph(f, char) else ""


# ---------------------------------------------------------------------------
# Leitura defensiva do JSON
# ---------------------------------------------------------------------------


def as_number(value):
    """Converte para float aceitando 1234.5, "1234.50" e "1.234,50".

    Retorna None para ausente, nulo ou nao numerico. Nunca retorna 0 como
    substituto de um valor desconhecido.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        for token in ("R$", "r$", " ", "\u00a0"):
            text = text.replace(token, "")
        if "," in text:
            text = text.replace(".", "").replace(",", ".")
        try:
            return float(text)
        except ValueError:
            return None
    return None


def as_int(value):
    number = as_number(value)
    if number is None:
        return None
    return int(round(number))


def as_text(value):
    if value is None:
        return ""
    return str(value).strip()


def as_list(value):
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def first_key(item, *keys):
    for key in keys:
        if key in item and item[key] is not None:
            return item[key]
    return None


def brl(value):
    """Formata no padrao brasileiro. Retorna None quando o valor e desconhecido."""
    number = as_number(value)
    if number is None:
        return None
    formatted = "{:,.2f}".format(abs(number))
    formatted = formatted.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    sign = "-" if number < 0 else ""
    return "{}R$ {}".format(sign, formatted)


def plural(count, singular, many):
    return singular if count == 1 else many


def documento_label(documento):
    """Prefixa CNPJ ou CPF conforme a quantidade de digitos ja presente."""
    texto = as_text(documento)
    if not texto:
        return ""
    if texto.upper().startswith(("CNPJ", "CPF")):
        return texto
    digitos = sum(1 for c in texto if c.isdigit())
    if digitos == 14:
        return "CNPJ " + texto
    if digitos == 11:
        return "CPF " + texto
    return texto


# ---------------------------------------------------------------------------
# Pintor com modo de medicao
# ---------------------------------------------------------------------------


class Painter:
    """Encapsula o ImageDraw. Em modo `dry` mede sem pintar.

    O layout roda duas vezes com o mesmo codigo: a primeira apenas para
    descobrir a altura final da pagina, a segunda para desenhar. Assim medida e
    desenho nunca divergem.
    """

    def __init__(self, draw, dry):
        self._draw = draw
        self.dry = dry

    def measuring(self):
        """Painter irmao que apenas mede, sem pintar."""
        return Painter(self._draw, True)

    def rect(self, box, fill):
        if not self.dry:
            self._draw.rectangle(box, fill=fill)

    def round_rect(self, box, radius, fill=None, outline=None, width=1):
        if not self.dry:
            self._draw.rounded_rectangle(
                box, radius=radius, fill=fill, outline=outline, width=width
            )

    def text(self, xy, content, f, fill, anchor="la"):
        if not self.dry:
            self._draw.text(xy, content, font=f, fill=fill, anchor=anchor)

    def spaced_text(self, xy, content, f, fill, spacing):
        x, y = xy
        for char in content:
            self.text((x, y), char, f, fill)
            x += self._draw.textlength(char, font=f) + spacing
        return x

    def spaced_width(self, content, f, spacing):
        return sum(self._draw.textlength(c, font=f) for c in content) + spacing * len(
            content
        )

    def width_of(self, content, f):
        return self._draw.textlength(content, font=f)

    def wrap(self, content, f, max_width):
        """Quebra o texto em linhas que cabem em max_width."""
        words = content.split()
        if not words:
            return [""]
        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if self.width_of(candidate, f) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def paragraph(self, x, y, content, f, fill, max_width, leading=7):
        for line in self.wrap(content, f, max_width):
            self.text((x, y), line, f, fill)
            y += line_height(f) + leading
        return y - leading

    def rich(self, x, y, segments, max_width, leading=7):
        """Escreve trechos com fontes/cores diferentes fluindo na mesma linha.

        Usado nos alertas e na linha da PGFN, onde o modelo mistura negrito e
        texto corrido dentro do mesmo paragrafo.
        """
        segments = [s for s in segments if s[0]]
        if not segments:
            return y
        alt = max(line_height(f) for _, f, _ in segments)
        cursor = x
        for content, f, fill in segments:
            space = self.width_of(" ", f)
            for word in content.split():
                w = self.width_of(word, f)
                if cursor > x and cursor + w > x + max_width:
                    cursor = x
                    y += alt + leading
                self.text((cursor, y), word, f, fill)
                cursor += w + space
        return y + alt


# ---------------------------------------------------------------------------
# Cabecalho
# ---------------------------------------------------------------------------


def draw_header(p, y, data):
    """Bloco azul escuro no topo da folha, com nome, documento e data."""
    f_eyebrow = font(12, bold=True)
    f_name = font(26, bold=True)
    f_meta = font(14)

    x0 = SHEET_X0 + HEADER_INSET
    x1 = SHEET_X1 - HEADER_INSET
    text_x = CARD_X0
    text_w = CARD_X1 - text_x

    nome = as_text(data.get("nome")) or "CONTRIBUINTE NÃO INFORMADO"
    name_lines = p.wrap(nome.upper(), f_name, text_w)

    meta_parts = []
    documento = documento_label(data.get("documento"))
    if documento:
        meta_parts.append(documento)
    data_relatorio = as_text(data.get("data_relatorio"))
    competencia = as_text(data.get("competencia")) or as_text(
        data.get("referencia_mes_ano")
    ).replace("-", "/")
    if data_relatorio:
        meta_parts.append(data_relatorio)
    elif competencia:
        meta_parts.append("Competência {}".format(competencia))

    height = 24 + line_height(f_eyebrow) + 12
    height += len(name_lines) * (line_height(f_name) + 4) - 4
    if meta_parts:
        height += 9 + line_height(f_meta)
    height += 26

    p.round_rect((x0, y, x1, y + height), HEADER_RADIUS, fill=NAVY)

    inner = y + 24
    p.spaced_text((text_x, inner), "SITUAÇÃO FISCAL", f_eyebrow, NAVY_EYEBROW, 1.6)
    inner += line_height(f_eyebrow) + 12

    for line in name_lines:
        p.text((text_x, inner), line, f_name, "#FFFFFF")
        inner += line_height(f_name) + 4

    if meta_parts:
        inner += 5
        p.text((text_x, inner), "   ·   ".join(meta_parts), f_meta, NAVY_META)

    return y + height


# ---------------------------------------------------------------------------
# Blocos com linhas (atraso, exigibilidade, parcelamentos, PGFN com divida)
# ---------------------------------------------------------------------------


def draw_rows_card(p, y, theme, title, subtitle, rows, total_label, total_value):
    """Card tingido com titulo, itens e subtotal ao pe, no estilo do modelo."""
    bg, border, divider, divider_strong, title_ink, value_ink, sub_ink = theme

    f_title = font(15, bold=True)
    f_subtitle = font(12)
    f_row = font(15)
    f_small = font(12)
    f_value = font(16, bold=True)
    f_total_label = font(13, bold=True)
    f_total_value = font(27, bold=True)

    text_x = CARD_X0 + CARD_PAD_X
    text_right = CARD_X1 - CARD_PAD_X
    text_w = text_right - text_x

    cursor = y + CARD_PAD_TOP

    marca = icon(f_title, "\u26a0") if theme is THEME_RED else ""
    p.spaced_text((text_x, cursor), marca + title, f_title, title_ink, 0.6)
    cursor += line_height(f_title)

    if subtitle:
        cursor += 6
        p.text((text_x, cursor), subtitle, f_subtitle, sub_ink)
        cursor += line_height(f_subtitle)

    cursor += 14

    for index, row in enumerate(rows):
        if index:
            p.rect((text_x, cursor, text_right, cursor + 1), divider)
            cursor += 1
        cursor += ROW_PAD_Y

        value = row.get("value")
        value_w = p.width_of(value, f_value) + 24 if value else 0

        segments = [(row.get("label") or "", f_row, INK)]
        if row.get("sub"):
            segments.append(("   ·   ", f_row, MUTED))
            segments.append((row["sub"], f_row, INK))
        if row.get("note"):
            segments.append(("  " + row["note"], f_small, MUTED))

        bottom = p.rich(text_x, cursor, segments, max(text_w - value_w, 140))
        if value:
            p.text(
                (text_right, (cursor + bottom) / 2),
                value,
                f_value,
                row.get("value_ink") or value_ink,
                anchor="rm",
            )
        cursor = bottom + ROW_PAD_Y

    if total_value:
        p.rect((text_x, cursor, text_right, cursor + 2), divider_strong)
        cursor += 2 + 18
        top = cursor
        p.spaced_text((text_x, cursor + 6), total_label, f_total_label, title_ink, 0.6)
        p.text(
            (text_right, cursor + line_height(f_total_value) / 2 - 2),
            total_value,
            f_total_value,
            value_ink,
            anchor="rm",
        )
        cursor = top + line_height(f_total_value) + 4

    cursor += CARD_PAD_BOTTOM
    return cursor - y


def render_rows_card(p, y, theme, *args, **kwargs):
    height = draw_rows_card(p.measuring(), y, theme, *args, **kwargs)
    if not p.dry:
        p.round_rect(
            (CARD_X0, y, CARD_X1, y + height),
            CARD_RADIUS,
            fill=theme[0],
            outline=theme[1],
            width=2,
        )
        draw_rows_card(p, y, theme, *args, **kwargs)
    return y + height + BLOCK_GAP


# ---------------------------------------------------------------------------
# Blocos de texto corrido (PGFN sem divida, alertas)
# ---------------------------------------------------------------------------


def draw_prose_card(p, y, segments, bg, border=None, bar=None):
    """Card compacto de texto corrido, com borda ou com barra lateral."""
    text_x = CARD_X0 + CARD_PAD_X + (BAR_W if bar else 0)
    text_right = CARD_X1 - CARD_PAD_X
    cursor = y + 18
    cursor = p.rich(text_x, cursor, segments, text_right - text_x)
    return cursor - y + 20


def render_prose_card(p, y, segments, bg, border=None, bar=None):
    height = draw_prose_card(p.measuring(), y, segments, bg, border, bar)
    if not p.dry:
        if bar:
            p.round_rect((CARD_X0, y, CARD_X1, y + height), CARD_RADIUS, fill=bar)
            p.round_rect(
                (CARD_X0 + BAR_W, y, CARD_X1, y + height), CARD_RADIUS, fill=bg
            )
        else:
            p.round_rect(
                (CARD_X0, y, CARD_X1, y + height),
                CARD_RADIUS,
                fill=bg,
                outline=border,
                width=2,
            )
        draw_prose_card(p, y, segments, bg, border, bar)
    return y + height + BLOCK_GAP


# ---------------------------------------------------------------------------
# Total geral e rodape
# ---------------------------------------------------------------------------


def draw_total(p, y, total, incompleto):
    f_label = font(15, bold=True)
    f_value = font(27, bold=True)
    f_note = font(12)

    height = 72
    p.round_rect((CARD_X0, y, CARD_X1, y + height), CARD_RADIUS, fill=TOTAL_BG)
    p.spaced_text(
        (CARD_X0 + CARD_PAD_X, y + height / 2 - line_height(f_label) / 2),
        "TOTAL GERAL",
        f_label,
        "#FFFFFF",
        0.6,
    )
    p.text(
        (CARD_X1 - CARD_PAD_X, y + height / 2),
        total or "NÃO INFORMADO",
        f_value,
        "#FFFFFF",
        anchor="rm",
    )
    y += height

    if incompleto:
        y += 10
        y = p.paragraph(
            CARD_X0 + 2,
            y,
            "Valores não informados nos documentos não foram somados ao total.",
            f_note,
            MUTED,
            CARD_X1 - CARD_X0 - 4,
        )

    return y + BLOCK_GAP


def draw_footer(p, y):
    f = font(13)
    y += 13
    texto = "Base: Relatório de Situação Fiscal — Receita Federal / PGFN"
    p.text(((CARD_X0 + CARD_X1) / 2, y), texto, f, FOOTER_INK, anchor="ma")
    return y + line_height(f)


# ---------------------------------------------------------------------------
# Consolidacao dos dados em linhas
# ---------------------------------------------------------------------------


def rows_from_groups(groups, unit_singular, unit_plural):
    """Consolida debitos por natureza: nome do grupo, quantidade e valor total."""
    rows = []
    known_total = 0.0
    has_known = False
    has_unknown = False
    quantidade_total = 0
    quantidade_conhecida = False

    for group in groups:
        tipo = as_text(first_key(group, "tipo", "grupo", "natureza", "origem"))
        if not tipo:
            tipo = "Não informado"
        quantidade = as_int(first_key(group, "quantidade", "qtd", "guias"))
        valor = as_number(first_key(group, "valor_total", "valor", "total"))

        if quantidade is not None:
            sub = "{} {}".format(
                quantidade, plural(quantidade, unit_singular, unit_plural)
            )
            quantidade_total += quantidade
            quantidade_conhecida = True
        else:
            sub = None

        row = {"label": tipo, "sub": sub, "value": brl(valor)}
        if valor is None:
            # Secao 23: valor desconhecido nunca vira zero nem entra no total.
            has_unknown = True
            row["value"] = "—"
            row["value_ink"] = MUTED
            row["note"] = "valor não informado"
        else:
            known_total += valor
            has_known = True
        rows.append(row)

    # Com um unico grupo o resumo repetiria a propria linha.
    resumo = None
    if quantidade_conhecida and len(rows) > 1:
        resumo = "{} {}".format(
            quantidade_total, plural(quantidade_total, unit_singular, unit_plural)
        )

    return {
        "rows": rows,
        "subtotal": known_total if has_known else None,
        "incompleto": has_unknown,
        "resumo": resumo,
    }


def rows_from_parcelamentos(parcelamentos):
    rows = []
    known_total = 0.0
    has_known = False
    has_unknown = False

    for item in parcelamentos:
        tipo = as_text(first_key(item, "tipo", "parcelamento", "descricao"))
        if not tipo:
            tipo = "Parcelamento não identificado"
        atrasadas = as_int(
            first_key(item, "parcelas_atrasadas", "parcelas", "quantidade")
        )
        valor = as_number(first_key(item, "valor_total", "valor"))

        if atrasadas is not None:
            sub = "{} {} em atraso".format(
                atrasadas, plural(atrasadas, "parcela", "parcelas")
            )
        else:
            sub = None

        row = {"label": tipo, "sub": sub, "value": brl(valor)}
        if valor is None:
            # Secao 7: parcelamento sem valor comprovado e informado, nao somado.
            has_unknown = True
            row["value"] = "—"
            row["value_ink"] = MUTED
            row["note"] = "valor não informado"
        else:
            known_total += valor
            has_known = True
        rows.append(row)

    return {
        "rows": rows,
        "subtotal": known_total if has_known else None,
        "incompleto": has_unknown,
        "resumo": None,
    }


def pgfn_status(pgfn):
    return as_text(pgfn.get("status")).lower().replace("-", "_").replace(" ", "_")


def pgfn_com_divida(pgfn):
    return pgfn_status(pgfn) in ("com_divida", "com_dividas", "inscrito", "irregular")


def rows_from_pgfn(pgfn):
    """Monta as linhas da divida ativa, resumindo quando ha varias inscricoes."""
    inscricoes = as_list(pgfn.get("inscricoes"))
    total_declarado = as_number(first_key(pgfn, "valor_total", "total", "valor"))

    known_total = 0.0
    has_known = False
    has_unknown = False
    for inscricao in inscricoes:
        valor = as_number(first_key(inscricao, "valor", "valor_total", "total"))
        if valor is None:
            has_unknown = True
        else:
            known_total += valor
            has_known = True

    if len(inscricoes) == 1:
        numero = as_text(first_key(inscricoes[0], "numero", "inscricao", "n_inscricao"))
        valor = as_number(first_key(inscricoes[0], "valor", "valor_total", "total"))
        rows = [
            {
                "label": "Inscrição {}".format(numero)
                if numero
                else "Inscrição não informada",
                "sub": None,
                "value": brl(valor),
            }
        ]
    elif len(inscricoes) > 1:
        # Secao 11: varias inscricoes sao agrupadas em quantidade e valor total.
        rows = [
            {
                "label": "Dívida ativa inscrita",
                "sub": "{} inscrições".format(len(inscricoes)),
                "value": brl(known_total if has_known else None),
            }
        ]
    else:
        rows = [
            {
                "label": "Débito inscrito em dívida ativa",
                "sub": None,
                "value": brl(total_declarado),
            }
        ]
        if total_declarado is None:
            has_unknown = True

    for row in rows:
        if not row["value"]:
            row["value"] = "—"
            row["value_ink"] = MUTED
            row["note"] = "valor não informado"

    subtotal = total_declarado
    if subtotal is None and has_known:
        subtotal = known_total
    if total_declarado is not None:
        has_unknown = False

    return {
        "rows": rows,
        "subtotal": subtotal,
        "incompleto": has_unknown,
        "resumo": None,
    }


# ---------------------------------------------------------------------------
# Montagem da pagina
# ---------------------------------------------------------------------------


def subtotal_para(bloco, rotulo):
    """Subtotal do bloco so aparece quando ha mais de uma linha para somar."""
    if len(bloco["rows"]) < 2 or bloco["subtotal"] is None:
        return None, None
    if bloco["incompleto"]:
        rotulo += " (SOMENTE VALORES INFORMADOS)"
    return rotulo, brl(bloco["subtotal"])


def render_content(p, data):
    """Desenha o conteudo da folha e devolve o y final.

    Blocos sem conteudo nao avancam o cursor, entao nao sobra espaco vazio.
    """
    em_atraso = as_list(data.get("em_atraso"))
    em_exigibilidade = as_list(data.get("em_exigibilidade"))
    parcelamentos = as_list(data.get("parcelamentos"))
    alertas = as_list(data.get("alertas"))
    pgfn = data.get("pgfn") if isinstance(data.get("pgfn"), dict) else {}

    f_prose = font(15)
    f_prose_bold = font(15, bold=True)

    y = draw_header(p, PAGE_PAD, data) + HEADER_GAP

    incompleto = False
    somas = []

    if em_atraso:
        bloco = rows_from_groups(em_atraso, "guia em atraso", "guias em atraso")
        incompleto = incompleto or bloco["incompleto"]
        if bloco["subtotal"] is not None:
            somas.append(bloco["subtotal"])
        rotulo, valor = subtotal_para(bloco, "TOTAL EM ATRASO")
        y = render_rows_card(
            p, y, THEME_RED, "EM ATRASO", bloco["resumo"], bloco["rows"], rotulo, valor
        )

    if em_exigibilidade:
        bloco = rows_from_groups(
            em_exigibilidade, "guia em exigibilidade", "guias em exigibilidade"
        )
        incompleto = incompleto or bloco["incompleto"]
        if bloco["subtotal"] is not None:
            somas.append(bloco["subtotal"])
        rotulo, valor = subtotal_para(bloco, "TOTAL EM EXIGIBILIDADE")
        y = render_rows_card(
            p,
            y,
            THEME_AMBER,
            "EM EXIGIBILIDADE / A VENCER",
            bloco["resumo"],
            bloco["rows"],
            rotulo,
            valor,
        )

    if parcelamentos:
        bloco = rows_from_parcelamentos(parcelamentos)
        incompleto = incompleto or bloco["incompleto"]
        if bloco["subtotal"] is not None:
            somas.append(bloco["subtotal"])
        rotulo, valor = subtotal_para(bloco, "TOTAL PARCELADO")
        y = render_rows_card(
            p, y, THEME_BLUE, "PARCELAMENTOS", None, bloco["rows"], rotulo, valor
        )

    if pgfn_com_divida(pgfn):
        bloco = rows_from_pgfn(pgfn)
        incompleto = incompleto or bloco["incompleto"]
        if bloco["subtotal"] is not None:
            somas.append(bloco["subtotal"])
        rotulo, valor = subtotal_para(bloco, "TOTAL NA PROCURADORIA")
        y = render_rows_card(
            p,
            y,
            THEME_RED,
            "DÉBITO NA PROCURADORIA",
            None,
            bloco["rows"],
            rotulo,
            valor,
        )
    elif pgfn_status(pgfn) in ("sem_divida", "sem_dividas", "regular"):
        marca = icon(f_prose_bold, "\u2714")
        y = render_prose_card(
            p,
            y,
            [
                (marca + "Sem dívidas na Procuradoria", f_prose_bold, THEME_GREEN[4]),
                ("— nenhuma inscrição em dívida ativa foi identificada.", f_prose, INK),
            ],
            THEME_GREEN[0],
            border=THEME_GREEN[1],
        )

    for alerta in alertas:
        titulo = as_text(first_key(alerta, "titulo", "title", "alerta"))
        texto = as_text(first_key(alerta, "texto", "descricao", "detalhe"))
        if not (titulo or texto):
            continue
        segments = []
        if titulo:
            segments.append((titulo.rstrip(".") + ".", f_prose_bold, ALERT_INK))
        if texto:
            segments.append((texto, f_prose, ALERT_INK))
        y = render_prose_card(p, y, segments, ALERT_BG, bar=ALERT_BAR)

    if tem_condicao_financeira(data):
        # O total do JSON prevalece; na ausencia dele, soma-se apenas o que ja
        # foi apurado nos blocos, uma unica vez cada.
        total = as_number(data.get("total_geral"))
        if total is None and somas:
            total = sum(somas)
        y = draw_total(p, y, brl(total), incompleto)

    return draw_footer(p, y - BLOCK_GAP + 8)


def parcelamento_conta_como_divida(item):
    """Parcelamento so justifica relatorio quando ha parcela em atraso.

    A quantidade de parcelas atrasadas basta, mesmo sem valor conhecido
    (secao 4). Um valor conhecido tambem caracteriza obrigacao financeira.
    """
    atrasadas = as_int(first_key(item, "parcelas_atrasadas", "parcelas", "quantidade"))
    if atrasadas is not None and atrasadas > 0:
        return True
    return as_number(first_key(item, "valor_total", "valor")) is not None


def tem_condicao_financeira(data):
    """Secao 4: so estas quatro condicoes justificam o relatorio.

    ALERTA SOZINHO NAO GERA RELATORIO — alertas apenas complementam um
    relatorio ja justificado por divida.
    """
    if as_list(data.get("em_atraso")):
        return True
    if as_list(data.get("em_exigibilidade")):
        return True
    if any(parcelamento_conta_como_divida(p) for p in as_list(data.get("parcelamentos"))):
        return True
    pgfn = data.get("pgfn") if isinstance(data.get("pgfn"), dict) else {}
    return pgfn_com_divida(pgfn)


def salvar_png_otimizado(imagem, caminho_saida):
    """Grava o PNG final em paleta indexada para reduzir o tamanho do arquivo.

    O relatorio tem poucas cores, fundos solidos, texto e formas geometricas,
    entao a paleta adaptativa de ate 256 cores preserva a aparencia. Sem
    dithering, para nao criar ruido no texto. Somente a gravacao muda: o
    desenho continua em RGB/RGBA, com as mesmas dimensoes e o mesmo conteudo.
    """
    final = imagem.convert("RGB")
    dither_none = Image.Dither.NONE if hasattr(Image, "Dither") else Image.NONE
    try:
        final = final.convert(
            "P", palette=Image.ADAPTIVE, colors=256, dither=dither_none
        )
    except Exception:
        # Se a quantizacao falhar, o RGB original ainda gera um PNG valido.
        pass
    final.save(caminho_saida, "PNG", optimize=True, compress_level=9)


def gerar(dados, caminho_saida):
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    conteudo = render_content(Painter(measure, True), dados)

    sheet_bottom = conteudo + 34
    altura = int(sheet_bottom + PAGE_PAD)

    imagem = Image.new("RGBA", (WIDTH, altura), PAGE_BG)

    sombra = Image.new("RGBA", (WIDTH, altura), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle(
        (SHEET_X0, PAGE_PAD + 4, SHEET_X1, sheet_bottom + 5),
        radius=SHEET_RADIUS,
        fill=SHADOW,
    )
    imagem = Image.alpha_composite(imagem, sombra.filter(ImageFilter.GaussianBlur(9)))

    desenho = ImageDraw.Draw(imagem)
    desenho.rounded_rectangle(
        (SHEET_X0, PAGE_PAD, SHEET_X1, sheet_bottom),
        radius=SHEET_RADIUS,
        fill=SHEET_BG,
    )

    render_content(Painter(desenho, False), dados)
    salvar_png_otimizado(imagem, caminho_saida)
    return WIDTH, altura


def main(argv):
    if len(argv) != 3:
        sys.stderr.write(
            "Uso: python gerar_relatorio_procuradoria.py dados.json saida.png\n"
        )
        return 1

    caminho_json, caminho_png = argv[1], argv[2]

    try:
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        sys.stderr.write("ERRO: arquivo JSON nao encontrado: {}\n".format(caminho_json))
        return 1
    except json.JSONDecodeError as erro:
        sys.stderr.write("ERRO: JSON invalido em {}: {}\n".format(caminho_json, erro))
        return 1

    if not isinstance(dados, dict):
        sys.stderr.write("ERRO: o JSON deve conter um objeto na raiz.\n")
        return 1

    if not tem_condicao_financeira(dados):
        sys.stderr.write(
            "SEM RELATORIO: nenhuma condicao financeira identificada (debito em "
            "atraso, debito em exigibilidade, divida na PGFN ou parcelamento com "
            "parcelas em atraso). Conforme a secao 4 do SKILL.md, alerta sozinho "
            "nao gera Relatorio de Procuradoria.\n"
        )
        return 2

    try:
        largura, altura = gerar(dados, caminho_png)
    except OSError as erro:
        sys.stderr.write("ERRO ao gravar o PNG: {}\n".format(erro))
        return 1

    print("Relatorio gerado: {} ({}x{} px)".format(caminho_png, largura, altura))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
