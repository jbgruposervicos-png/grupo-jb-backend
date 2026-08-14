#!/usr/bin/env python3
"""Gerador oficial do Relatorio de Procuradoria — Grupo JB Contabilidade.

Uso:

    python gerar_relatorio_procuradoria.py dados.json saida.png

O script renderiza um PNG vertical de altura dinamica a partir de um unico
arquivo JSON. Ele NAO le PDF, NAO le imagens, NAO acessa o Google Drive e NAO
infere nenhum dado: tudo que aparece no relatorio vem do JSON de entrada.

Valores ausentes ou nulos nunca sao substituidos por zero nem estimados — sao
apresentados como nao informados e ficam fora do total.

Codigos de saida:

    0  relatorio gerado
    1  erro (JSON invalido, arquivo ausente, falha de escrita)
    2  contribuinte sem debito, pendencia ou alerta — relatorio nao deve ser
       gerado (secao 4 do SKILL.md)
"""

import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - depende do ambiente
    sys.stderr.write(
        "ERRO: a biblioteca Pillow e necessaria para gerar o PNG.\n"
        "Instale com: pip install Pillow\n"
    )
    raise SystemExit(1)


# ---------------------------------------------------------------------------
# Paleta e metricas
# ---------------------------------------------------------------------------

WIDTH = 1100
MARGIN = 48
CONTENT_W = WIDTH - 2 * MARGIN

PAGE_BG = "#FFFFFF"
INK = "#1B2430"
INK_SOFT = "#5A6675"
HAIRLINE = "#E4E9EF"

NAVY = "#0F2E5C"
NAVY_EYEBROW = "#9FBBDF"
NAVY_META = "#CBDDF2"

# Cada tema: (barra de destaque, fundo do bloco, linha divisoria, cor do titulo)
THEME_RED = ("#C0392B", "#FCEDEB", "#F0C9C3", "#A5291C")
THEME_AMBER = ("#E0A526", "#FFF8E7", "#F3E0B4", "#8A6100")
THEME_GREEN = ("#1E8A4C", "#EAF7EF", "#C3E5D1", "#166B3B")
THEME_NEUTRAL = ("#5B7FA6", "#F1F5F9", "#D8E2EC", "#2E4C6D")

TOTAL_BG = "#B32B1E"

CARD_RADIUS = 12
ACCENT_W = 8
CARD_PAD_X = 28
CARD_PAD_TOP = 24
CARD_PAD_BOTTOM = 26
ROW_PAD_Y = 16
BLOCK_GAP = 24

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

    def round_rect(self, box, radius, fill):
        if not self.dry:
            self._draw.rounded_rectangle(box, radius=radius, fill=fill)

    def text(self, xy, content, f, fill, anchor="la"):
        if not self.dry:
            self._draw.text(xy, content, font=f, fill=fill, anchor=anchor)

    def spaced_text(self, xy, content, f, fill, spacing):
        x, y = xy
        for char in content:
            self.text((x, y), char, f, fill)
            x += self._draw.textlength(char, font=f) + spacing

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

    def paragraph(self, x, y, content, f, fill, max_width, leading=6):
        for line in self.wrap(content, f, max_width):
            self.text((x, y), line, f, fill)
            y += line_height(f) + leading
        return y - leading


# ---------------------------------------------------------------------------
# Blocos do relatorio
# ---------------------------------------------------------------------------


def draw_header(p, y, data):
    """Cabecalho azul escuro, sangrando de borda a borda."""
    f_eyebrow = font(19, bold=True)
    f_name = font(40, bold=True)
    f_meta = font(21)

    pad_top, pad_bottom = 38, 34
    x = MARGIN
    inner_y = y + pad_top

    nome = as_text(data.get("nome")) or "CONTRIBUINTE NÃO INFORMADO"
    name_lines = p.wrap(nome.upper(), f_name, CONTENT_W)

    meta_parts = []
    documento = as_text(data.get("documento"))
    if documento:
        meta_parts.append(documento)
    competencia = as_text(data.get("competencia")) or as_text(
        data.get("referencia_mes_ano")
    ).replace("-", "/")
    if competencia:
        meta_parts.append("Competência {}".format(competencia))

    # Altura do bloco precisa ser conhecida antes de pintar o fundo.
    height = pad_top + line_height(f_eyebrow) + 18
    height += len(name_lines) * (line_height(f_name) + 6) - 6
    if meta_parts:
        height += 16 + line_height(f_meta)
    height += pad_bottom

    p.rect((0, y, WIDTH, y + height), NAVY)

    p.spaced_text((x, inner_y), "RELATÓRIO DE PROCURADORIA", f_eyebrow, NAVY_EYEBROW, 2.5)
    inner_y += line_height(f_eyebrow) + 18

    for line in name_lines:
        p.text((x, inner_y), line, f_name, "#FFFFFF")
        inner_y += line_height(f_name) + 6

    if meta_parts:
        inner_y += 10
        p.text((x, inner_y), "   |   ".join(meta_parts), f_meta, NAVY_META)

    return y + height


def draw_card(p, y, theme, title, rows, subtitle=None, paragraphs=None):
    """Desenha um bloco com barra de destaque, titulo, subtotal e linhas.

    `rows` e uma lista de dicts com as chaves opcionais label, sub e value.
    `paragraphs` e uma lista de (titulo, texto) usada pelos alertas.
    """
    accent, bg, line_color, title_color = theme
    rows = rows or []
    paragraphs = paragraphs or []

    # Com uma unica linha o subtotal repetiria o valor da propria linha.
    if len(rows) < 2:
        subtitle = None

    f_title = font(25, bold=True)
    f_subtitle = font(23, bold=True)
    f_label = font(22, bold=True)
    f_sub = font(18)
    f_value = font(24, bold=True)
    f_ptitle = font(21, bold=True)
    f_ptext = font(19)

    x1, x2 = MARGIN, WIDTH - MARGIN
    text_x = x1 + ACCENT_W + CARD_PAD_X
    text_right = x2 - CARD_PAD_X
    text_w = text_right - text_x

    cursor = y + CARD_PAD_TOP

    # Titulo do bloco e subtotal alinhado a direita.
    p.text((text_x, cursor), title, f_title, title_color)
    if subtitle:
        p.text((text_right, cursor + 2), subtitle, f_subtitle, title_color, anchor="ra")
    cursor += line_height(f_title) + 16

    if rows or paragraphs:
        p.rect((text_x, cursor, text_right, cursor + 1), line_color)
        cursor += 1

    for index, row in enumerate(rows):
        if index:
            p.rect((text_x, cursor, text_right, cursor + 1), line_color)
            cursor += 1
        cursor += ROW_PAD_Y
        row_top = cursor

        label = row.get("label") or ""
        sub = row.get("sub")
        value = row.get("value")

        value_w = p.width_of(value, f_value) + 28 if value else 0
        label_lines = p.wrap(label, f_label, max(text_w - value_w, 120))

        block_h = len(label_lines) * (line_height(f_label) + 4) - 4
        if sub:
            block_h += 6 + line_height(f_sub)

        line_y = cursor
        for line in label_lines:
            p.text((text_x, line_y), line, f_label, INK)
            line_y += line_height(f_label) + 4
        if sub:
            p.text((text_x, line_y + 2), sub, f_sub, INK_SOFT)

        if value:
            p.text(
                (text_right, row_top + block_h / 2),
                value,
                f_value,
                title_color,
                anchor="rm",
            )

        cursor = row_top + block_h + ROW_PAD_Y

    for index, (ptitle, ptext) in enumerate(paragraphs):
        if index:
            p.rect((text_x, cursor, text_right, cursor + 1), line_color)
            cursor += 1
        cursor += ROW_PAD_Y
        if ptitle:
            p.text((text_x, cursor), ptitle, f_ptitle, title_color)
            cursor += line_height(f_ptitle) + 8
        if ptext:
            cursor = p.paragraph(text_x, cursor, ptext, f_ptext, INK, text_w)
            cursor += line_height(f_ptext)
        cursor += ROW_PAD_Y - 8

    cursor += CARD_PAD_BOTTOM
    height = cursor - y

    # Pintado por ultimo em modo real seria coberto pelo texto, entao o fundo e
    # desenhado antes; em modo dry nada e pintado e apenas a altura importa.
    return height


def render_card(p, y, *args, **kwargs):
    """Mede o card, pinta o fundo e so entao redesenha o conteudo por cima."""
    height = draw_card(p.measuring(), y, *args, **kwargs)
    if not p.dry:
        accent, bg = args[0][0], args[0][1]
        p.round_rect((MARGIN, y, WIDTH - MARGIN, y + height), CARD_RADIUS, accent)
        p.round_rect(
            (MARGIN + ACCENT_W, y, WIDTH - MARGIN, y + height), CARD_RADIUS, bg
        )
        draw_card(p, y, *args, **kwargs)
    return y + height + BLOCK_GAP


def rows_from_groups(groups, unit_singular, unit_plural):
    """Consolida debitos por natureza: nome do grupo, quantidade e valor total."""
    rows = []
    known_total = 0.0
    has_known = False
    has_unknown = False

    for group in groups:
        tipo = as_text(first_key(group, "tipo", "grupo", "natureza", "origem"))
        if not tipo:
            tipo = "NÃO INFORMADO"
        quantidade = as_int(first_key(group, "quantidade", "qtd", "guias"))
        valor = as_number(first_key(group, "valor_total", "valor", "total"))

        if quantidade is not None:
            sub = "{} {}".format(
                quantidade, plural(quantidade, unit_singular, unit_plural)
            )
        else:
            sub = None

        value_text = brl(valor)
        if valor is None:
            has_unknown = True
            value_text = "valor não informado"
        else:
            known_total += valor
            has_known = True

        rows.append({"label": tipo.upper(), "sub": sub, "value": value_text})

    return rows, (known_total if has_known else None), has_unknown


def rows_from_parcelamentos(parcelamentos):
    rows = []
    known_total = 0.0
    has_known = False
    has_unknown = False

    for item in parcelamentos:
        tipo = as_text(first_key(item, "tipo", "parcelamento", "descricao"))
        if not tipo:
            tipo = "PARCELAMENTO NÃO IDENTIFICADO"
        atrasadas = as_int(first_key(item, "parcelas_atrasadas", "parcelas", "quantidade"))
        valor = as_number(first_key(item, "valor_total", "valor"))

        if atrasadas is not None:
            sub = "{} {} em atraso".format(
                atrasadas, plural(atrasadas, "parcela", "parcelas")
            )
        else:
            sub = None

        value_text = brl(valor)
        if valor is None:
            # Secao 7: parcelamento sem valor comprovado e informado, mas nao somado.
            has_unknown = True
            value_text = "valor não informado"
        else:
            known_total += valor
            has_known = True

        rows.append({"label": tipo.upper(), "sub": sub, "value": value_text})

    return rows, (known_total if has_known else None), has_unknown


def pgfn_block(pgfn):
    """Retorna (tema, titulo, rows, subtotal_conhecido, tem_desconhecido) ou None."""
    status = as_text(pgfn.get("status")).lower().replace("-", "_").replace(" ", "_")

    if status in ("sem_divida", "sem_dividas", "regular"):
        rows = [
            {
                "label": "SEM DÍVIDAS NA PROCURADORIA",
                "sub": "Nenhuma inscrição em dívida ativa identificada.",
                "value": None,
            }
        ]
        return THEME_GREEN, "PROCURADORIA / PGFN", rows, None, False

    if status not in ("com_divida", "com_dividas", "inscrito", "irregular"):
        # Status ausente ou desconhecido: nada foi comprovado, nada e afirmado.
        return None

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
        numero = as_text(
            first_key(inscricoes[0], "numero", "inscricao", "n_inscricao")
        )
        valor = as_number(first_key(inscricoes[0], "valor", "valor_total", "total"))
        label = "Inscrição: {}".format(numero) if numero else "Inscrição não informada"
        rows = [
            {
                "label": label.upper(),
                "sub": None,
                "value": brl(valor) or "valor não informado",
            }
        ]
    elif len(inscricoes) > 1:
        # Secao 11: varias inscricoes sao agrupadas por quantidade e valor total.
        rows = [
            {
                "label": "DÍVIDA ATIVA INSCRITA",
                "sub": "{} inscrições".format(len(inscricoes)),
                "value": brl(known_total if has_known else None)
                or "valor não informado",
            }
        ]
    else:
        rows = [
            {
                "label": "DÉBITO NA PROCURADORIA",
                "sub": "Inscrição e valor não informados nos documentos.",
                "value": None,
            }
        ]

    subtotal = total_declarado if total_declarado is not None else (
        known_total if has_known else None
    )
    if total_declarado is not None:
        has_unknown = False

    return THEME_RED, "PROCURADORIA / PGFN", rows, subtotal, has_unknown


def draw_total(p, y, total, incompleto):
    f_label = font(27, bold=True)
    f_value = font(40, bold=True)
    f_note = font(18)

    height = 104
    p.round_rect((MARGIN, y, WIDTH - MARGIN, y + height), CARD_RADIUS, TOTAL_BG)
    p.text((MARGIN + 32, y + height / 2), "TOTAL GERAL", f_label, "#FFFFFF", anchor="lm")
    p.text(
        (WIDTH - MARGIN - 32, y + height / 2),
        total or "NÃO INFORMADO",
        f_value,
        "#FFFFFF",
        anchor="rm",
    )
    y += height

    if incompleto:
        y += 12
        y = p.paragraph(
            MARGIN + 4,
            y,
            "Valores não informados nos documentos não foram somados ao total.",
            f_note,
            INK_SOFT,
            CONTENT_W - 8,
        )
        y += line_height(f_note)

    return y + BLOCK_GAP


def draw_footer(p, y, data):
    f = font(17)
    y += 8
    p.rect((MARGIN, y, WIDTH - MARGIN, y + 1), HAIRLINE)
    y += 18

    parts = ["Grupo JB Contabilidade  |  Departamento de Procuradoria"]
    data_relatorio = as_text(data.get("data_relatorio"))
    if data_relatorio:
        parts.append("Situação Fiscal de {}".format(data_relatorio))
    p.text((MARGIN, y), "     ".join(parts), f, INK_SOFT)
    y += line_height(f) + 6

    p.text(
        (MARGIN, y),
        "Documento gerado a partir dos dados extraídos da Situação Fiscal e dos documentos complementares.",
        f,
        INK_SOFT,
    )
    return y + line_height(f) + 40


# ---------------------------------------------------------------------------
# Montagem da pagina
# ---------------------------------------------------------------------------


def render(p, data):
    """Desenha o relatorio inteiro e devolve a altura usada.

    Blocos sem conteudo simplesmente nao avancam o cursor, entao nao sobra
    espaco vazio na pagina.
    """
    em_atraso = as_list(data.get("em_atraso"))
    em_exigibilidade = as_list(data.get("em_exigibilidade"))
    parcelamentos = as_list(data.get("parcelamentos"))
    alertas = as_list(data.get("alertas"))
    pgfn = data.get("pgfn") if isinstance(data.get("pgfn"), dict) else {}

    y = draw_header(p, 0, data)
    y += 32

    incompleto = False
    somas = []

    if em_atraso:
        rows, subtotal, unknown = rows_from_groups(em_atraso, "guia em atraso", "guias em atraso")
        incompleto = incompleto or unknown
        if subtotal is not None:
            somas.append(subtotal)
        y = render_card(
            p, y, THEME_RED, "DÉBITOS EM ATRASO", rows, subtitle=brl(subtotal)
        )

    if em_exigibilidade:
        rows, subtotal, unknown = rows_from_groups(
            em_exigibilidade, "guia em exigibilidade", "guias em exigibilidade"
        )
        incompleto = incompleto or unknown
        if subtotal is not None:
            somas.append(subtotal)
        y = render_card(
            p,
            y,
            THEME_AMBER,
            "EM EXIGIBILIDADE / A VENCER",
            rows,
            subtitle=brl(subtotal),
        )

    if parcelamentos:
        rows, subtotal, unknown = rows_from_parcelamentos(parcelamentos)
        incompleto = incompleto or unknown
        if subtotal is not None:
            somas.append(subtotal)
        y = render_card(
            p, y, THEME_NEUTRAL, "PARCELAMENTOS", rows, subtitle=brl(subtotal)
        )

    bloco_pgfn = pgfn_block(pgfn)
    pgfn_com_divida = False
    if bloco_pgfn:
        theme, titulo, rows, subtotal, unknown = bloco_pgfn
        pgfn_com_divida = theme is THEME_RED
        if pgfn_com_divida:
            incompleto = incompleto or unknown
            if subtotal is not None:
                somas.append(subtotal)
        y = render_card(p, y, theme, titulo, rows, subtitle=brl(subtotal))

    if alertas:
        paragraphs = []
        for alerta in alertas:
            titulo = as_text(first_key(alerta, "titulo", "title", "alerta"))
            texto = as_text(first_key(alerta, "texto", "descricao", "detalhe"))
            if titulo or texto:
                paragraphs.append((titulo.upper(), texto))
        if paragraphs:
            y = render_card(p, y, THEME_AMBER, "ALERTAS", [], paragraphs=paragraphs)

    tem_debito = bool(em_atraso or em_exigibilidade or pgfn_com_divida or parcelamentos)
    if tem_debito:
        # O total do JSON prevalece; na ausencia dele, soma-se apenas o que ja
        # foi apurado nos blocos, uma unica vez cada.
        total = as_number(data.get("total_geral"))
        if total is None and somas:
            total = sum(somas)
        y = draw_total(p, y, brl(total), incompleto)

    y = draw_footer(p, y, data)
    return int(y)


def tem_conteudo(data):
    """Secao 4: contribuinte totalmente regular nao gera relatorio."""
    if as_list(data.get("em_atraso")):
        return True
    if as_list(data.get("em_exigibilidade")):
        return True
    if as_list(data.get("parcelamentos")):
        return True
    if as_list(data.get("alertas")):
        return True
    pgfn = data.get("pgfn") if isinstance(data.get("pgfn"), dict) else {}
    status = as_text(pgfn.get("status")).lower().replace("-", "_").replace(" ", "_")
    return status in ("com_divida", "com_dividas", "inscrito", "irregular")


def gerar(dados, caminho_saida):
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    altura = render(Painter(measure, True), dados)

    imagem = Image.new("RGB", (WIDTH, altura), PAGE_BG)
    render(Painter(ImageDraw.Draw(imagem), False), dados)
    imagem.save(caminho_saida, "PNG")
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

    if not tem_conteudo(dados):
        sys.stderr.write(
            "SEM RELATORIO: nenhum debito, parcelamento, divida na PGFN ou alerta "
            "informado. Conforme a secao 4 do SKILL.md, contribuinte regular nao "
            "gera Relatorio de Procuradoria.\n"
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
