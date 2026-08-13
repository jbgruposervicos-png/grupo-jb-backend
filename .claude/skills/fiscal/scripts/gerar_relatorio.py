import json
import sys
import unicodedata
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ============================================================
# CONFIGURAÇÕES VISUAIS
# ============================================================

AZUL = colors.HexColor("#173F73")
AZUL_CLARO = colors.HexColor("#DDEAF7")
AZUL_MEDIO = colors.HexColor("#3166A8")
LARANJA = colors.HexColor("#F6A91A")
LARANJA_ESCURO = colors.HexColor("#C77C00")
LARANJA_CLARO = colors.HexColor("#FFF5D9")
VERMELHO = colors.HexColor("#C83C32")
VERMELHO_CLARO = colors.HexColor("#FFF0EE")
VERDE = colors.HexColor("#23A566")
CINZA = colors.HexColor("#6B7280")
CINZA_CLARO = colors.HexColor("#E5E7EB")
BRANCO = colors.white
PRETO = colors.HexColor("#172033")

# Todo o texto usa as fontes base-14 (Helvetica), cujo encoding é o
# WinAnsi. Símbolos como ▲ ▼ ■ → NÃO existem nesse encoding e quebram o
# PDF, portanto são desenhados como vetores (ver seção SÍMBOLOS VETORIAIS).
FONTE = "Helvetica"
FONTE_BOLD = "Helvetica-Bold"


# ============================================================
# ALTURAS DO LAYOUT (uma única página A4)
# ============================================================

MARGEM = 14

H_CABECALHO = 56
H_CARD = 58
H_COMPARATIVO = 58
H_ALERTAS = 100
H_GRAFICO = 264
H_RESUMO = 72
H_RODAPE = 48

GAP_CABECALHO = 14
GAP_CARDS = 8
GAP_LINHA = 14
GAP_ALERTAS = 14
GAP_GRAFICO = 16
GAP_RESUMO = 18
GAP_RODAPE = 16

GAP_COLUNAS = 3


# ============================================================
# FORMATAÇÃO
# ============================================================


def moeda(valor):
    if valor is None or valor == "":
        return "-"
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return str(valor)

    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def moeda_curta(valor):
    """Valor sem centavos, para caber acima das barras do gráfico."""
    if valor is None or valor == "":
        return "-"
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return str(valor)

    texto = f"{valor:,.0f}".replace(",", ".")
    return f"R$ {texto}"


def moeda_milhar(valor):
    """Forma ainda mais compacta: R$ 125,8 mil."""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return str(valor)

    if abs(valor) < 1000:
        return moeda_curta(valor)

    texto = f"{valor / 1000:,.1f}".replace(",", "X").replace(".", ",")
    return f"R$ {texto.replace('X', '.')} mil"


def percentual(valor, casas=2):
    if valor is None or valor == "":
        return "-"
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    return f"{valor:.{casas}f}%".replace(".", ",")


def texto_seguro(valor, padrao="-"):
    if valor is None or valor == "":
        return padrao
    return str(valor)


def natureza_empresa(dados):
    """Natureza da empresa conforme a planilha permanente: serviço ou comércio.

    A natureza NUNCA é deduzida da ausência ou do valor zerado de compras —
    ela vem exclusivamente do campo informado no JSON, que por sua vez é
    lido da planilha (ver seção 7A do SKILL.md).

    Aceita variações de caixa e acentuação ("SERVIÇO", "servico",
    "Prestação de Serviços"). Qualquer valor não reconhecido — inclusive a
    ausência do campo — mantém o comportamento histórico de COMÉRCIO, com o
    layout completo de Compras/Resultado/Margem.
    """
    bruto = dados.get("natureza")
    if bruto in (None, ""):
        bruto = dados.get("natureza_empresa")

    texto = str(bruto or "").strip().lower()
    texto = (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    return "servico" if "servic" in texto else "comercio"


def calcular_variacao(atual, anterior):
    if anterior in (None, 0, "", "0"):
        return None, None

    try:
        atual = float(atual)
        anterior = float(anterior)
    except (TypeError, ValueError):
        return None, None

    if anterior == 0:
        return None, None

    diferenca = atual - anterior
    percentual_var = (diferenca / anterior) * 100

    return percentual_var, diferenca


# ============================================================
# PRIMITIVAS DE DESENHO
# ============================================================


def arredondar_caixa(c, x, y, w, h, preenchimento, borda=None, raio=5):
    c.setFillColor(preenchimento)
    c.setStrokeColor(borda or preenchimento)
    c.roundRect(x, y, w, h, raio, fill=1, stroke=1)


def centralizar(c, texto, x, y, w, fonte=FONTE_BOLD, tamanho=10, cor=PRETO):
    c.setFont(fonte, tamanho)
    c.setFillColor(cor)
    largura = c.stringWidth(texto, fonte, tamanho)
    c.drawString(x + (w - largura) / 2, y, texto)


def limitar_texto(c, texto, largura, fonte=FONTE, tamanho=8):
    texto = str(texto or "")
    if c.stringWidth(texto, fonte, tamanho) <= largura:
        return texto

    while texto and c.stringWidth(texto + "...", fonte, tamanho) > largura:
        texto = texto[:-1]

    return texto + "..."


def escrever_ajustado(
    c,
    texto,
    x,
    y,
    largura,
    tamanhos,
    fonte=FONTE,
    cor=PRETO,
    ancora="left",
):
    """Escreve usando o maior tamanho da lista que couber em `largura`.

    Só recorre a truncamento se nem o menor tamanho couber, de modo que
    nenhum texto sai cortado sem necessidade.
    """
    texto = str(texto or "")

    tamanho = tamanhos[-1]
    for candidato in tamanhos:
        if c.stringWidth(texto, fonte, candidato) <= largura:
            tamanho = candidato
            break
    else:
        texto = limitar_texto(c, texto, largura, fonte, tamanho)

    c.setFont(fonte, tamanho)
    c.setFillColor(cor)

    if ancora == "center":
        c.drawString(x + (largura - c.stringWidth(texto, fonte, tamanho)) / 2, y, texto)
    elif ancora == "right":
        c.drawString(x + largura - c.stringWidth(texto, fonte, tamanho), y, texto)
    else:
        c.drawString(x, y, texto)

    return tamanho


# ============================================================
# SÍMBOLOS VETORIAIS
# ------------------------------------------------------------
# Substituem ▲ (U+25B2), ▼ (U+25BC), ■ (U+25A0) e → (U+2192), que não
# existem no WinAnsiEncoding das fontes base-14 e sairiam quebrados.
# ============================================================


def triangulo(c, x, y, tamanho, para_cima, cor):
    c.setFillColor(cor)
    c.setStrokeColor(cor)

    meio = tamanho / 2.0
    caminho = c.beginPath()

    if para_cima:
        caminho.moveTo(x + meio, y + tamanho)
        caminho.lineTo(x, y)
        caminho.lineTo(x + tamanho, y)
    else:
        caminho.moveTo(x + meio, y)
        caminho.lineTo(x, y + tamanho)
        caminho.lineTo(x + tamanho, y + tamanho)

    caminho.close()
    c.drawPath(caminho, fill=1, stroke=0)


def quadrado(c, x, y, tamanho, cor):
    c.setFillColor(cor)
    c.rect(x, y, tamanho, tamanho, fill=1, stroke=0)


def seta_direita(c, x, y, comprimento, cor, espessura=0.7):
    """Seta horizontal simples, no lugar de '→'."""
    c.setStrokeColor(cor)
    c.setFillColor(cor)
    c.setLineWidth(espessura)

    meio = y + 2
    c.line(x, meio, x + comprimento - 2.6, meio)

    ponta = c.beginPath()
    ponta.moveTo(x + comprimento, meio)
    ponta.lineTo(x + comprimento - 3.2, meio + 1.9)
    ponta.lineTo(x + comprimento - 3.2, meio - 1.9)
    ponta.close()
    c.drawPath(ponta, fill=1, stroke=0)

    c.setLineWidth(1)


def titulo_bloco(c, x, y, texto, cor, largura):
    """Título de bloco precedido por um marcador quadrado vetorial."""
    quadrado(c, x, y + 0.5, 5, cor)
    escrever_ajustado(
        c,
        texto,
        x + 9,
        y,
        largura - 9,
        [8.5, 8, 7.5, 7],
        fonte=FONTE_BOLD,
        cor=cor,
    )


# ============================================================
# COMPONENTES
# ============================================================


def card_indicador(
    c,
    x,
    y,
    w,
    h,
    titulo,
    valor,
    subtitulo=None,
    fundo=AZUL_CLARO,
    cor_valor=AZUL,
    cor_titulo=AZUL,
):
    arredondar_caixa(c, x, y, w, h, fundo, AZUL_MEDIO)

    interno = w - 12

    escrever_ajustado(
        c,
        titulo.upper(),
        x + 6,
        y + h - 15,
        interno,
        [8, 7.5, 7, 6.5],
        fonte=FONTE_BOLD,
        cor=cor_titulo,
        ancora="center",
    )

    escrever_ajustado(
        c,
        texto_seguro(valor),
        x + 6,
        y + h / 2 - 6,
        interno,
        [13, 12, 11, 10, 9],
        fonte=FONTE_BOLD,
        cor=cor_valor,
        ancora="center",
    )

    if subtitulo:
        escrever_ajustado(
            c,
            texto_seguro(subtitulo),
            x + 6,
            y + 9,
            interno,
            [7.5, 7, 6.5],
            fonte=FONTE,
            cor=CINZA if fundo is AZUL_CLARO else CINZA_CLARO,
            ancora="center",
        )


def card_comparacao(c, x, y, w, h, titulo, competencia, anterior, atual):
    """Card de comparação.

    A competência aparece UMA única vez (na linha de referência); o título
    descreve apenas o tipo de comparação.
    """
    arredondar_caixa(c, x, y, w, h, AZUL_CLARO, AZUL_MEDIO)

    variacao, diferenca = calcular_variacao(atual, anterior)

    # Reserva a metade direita para o indicador de variação.
    largura_titulo = w - 16
    largura_esquerda = (w * 0.55) - 16

    escrever_ajustado(
        c,
        titulo.upper(),
        x + 8,
        y + h - 15,
        largura_titulo,
        [8, 7.5, 7],
        fonte=FONTE_BOLD,
        cor=AZUL,
    )

    escrever_ajustado(
        c,
        texto_seguro(competencia),
        x + 8,
        y + h - 30,
        largura_esquerda,
        [8, 7.5, 7],
        fonte=FONTE,
        cor=CINZA,
    )

    escrever_ajustado(
        c,
        moeda(anterior),
        x + 8,
        y + 12,
        largura_esquerda,
        [11, 10, 9],
        fonte=FONTE_BOLD,
        cor=AZUL,
    )

    if variacao is None:
        escrever_ajustado(
            c,
            "sem histórico comparável",
            x + w / 2,
            y + 12,
            w / 2 - 8,
            [8, 7.5, 7],
            fonte=FONTE,
            cor=CINZA,
            ancora="right",
        )
        return

    subiu = diferenca >= 0
    cor = VERDE if subiu else VERMELHO

    rotulo = percentual(abs(variacao), 1)
    tamanho = 12
    largura_rotulo = c.stringWidth(rotulo, FONTE_BOLD, tamanho)

    base_y = y + h - 32
    triangulo(c, x + w - 8 - largura_rotulo - 11, base_y + 1, 8, subiu, cor)

    c.setFont(FONTE_BOLD, tamanho)
    c.setFillColor(cor)
    c.drawRightString(x + w - 8, base_y, rotulo)

    escrever_ajustado(
        c,
        f"{'Subiu' if subiu else 'Caiu'} {moeda(abs(diferenca))}",
        x + w / 2,
        y + 12,
        w / 2 - 8,
        [8.5, 8, 7.5],
        fonte=FONTE,
        cor=cor,
        ancora="right",
    )


# ============================================================
# GRÁFICO DE VENDAS
# ============================================================


def desenhar_grafico_vendas(c, x, y, w, h, historico):
    """Desenha o bloco do gráfico dentro do retângulo (x, y, w, h)."""
    arredondar_caixa(c, x, y, w, h, BRANCO, CINZA_CLARO)

    centralizar(
        c,
        "VENDAS MENSAIS",
        x,
        y + h - 17,
        w,
        fonte=FONTE_BOLD,
        tamanho=10,
        cor=AZUL,
    )

    if not historico:
        centralizar(
            c,
            "Histórico mensal não disponível",
            x,
            y + h / 2,
            w,
            fonte=FONTE,
            tamanho=9,
            cor=CINZA,
        )
        return

    # Área útil do plot
    plot_x = x + 16
    plot_w = w - 32
    eixo_y = y + 30
    altura_max = (y + h - 34) - eixo_y - 14

    valores = [float(item.get("valor", 0) or 0) for item in historico]
    maior = max(valores) if valores else 0
    if maior <= 0:
        maior = 1

    qtd = len(historico)
    espaco = 5 if qtd <= 14 else 3
    barra_w = max(6, (plot_w - espaco * (qtd - 1)) / qtd)

    def altura_de(valor):
        return (valor / maior) * altura_max

    # --- linhas de grade ---
    c.setStrokeColor(CINZA_CLARO)
    c.setLineWidth(0.4)
    for fracao in (0.25, 0.5, 0.75, 1.0):
        gy = eixo_y + altura_max * fracao
        c.line(plot_x, gy, plot_x + plot_w, gy)

    # --- linha base ---
    c.setStrokeColor(CINZA)
    c.setLineWidth(0.7)
    c.line(plot_x, eixo_y, plot_x + plot_w, eixo_y)

    # --- barras ---
    posicoes = []
    for i, item in enumerate(historico):
        valor = float(item.get("valor", 0) or 0)
        altura = altura_de(valor)
        bx = plot_x + i * (barra_w + espaco)
        posicoes.append(bx)

        atual = bool(item.get("atual", False))

        c.setFillColor(LARANJA if atual else AZUL_MEDIO)
        c.rect(bx, eixo_y, barra_w, altura, fill=1, stroke=0)

        escrever_ajustado(
            c,
            texto_seguro(item.get("mes")),
            bx,
            eixo_y - 13,
            barra_w,
            [7.5, 7, 6.5, 6],
            fonte=FONTE,
            cor=CINZA,
            ancora="center",
        )

        # Valor acima da barra: tenta a forma completa e, se não couber na
        # largura da barra, recorre à forma em milhares.
        rotulo = moeda_curta(valor)
        if c.stringWidth(rotulo, FONTE_BOLD, 7) > barra_w:
            rotulo = moeda_milhar(valor)

        escrever_ajustado(
            c,
            rotulo,
            bx,
            eixo_y + altura + 4,
            barra_w,
            [7.5, 7, 6.5, 6],
            fonte=FONTE_BOLD,
            cor=PRETO if atual else CINZA,
            ancora="center",
        )

    # --- média (mesma escala vertical das barras) ---
    media = sum(valores) / len(valores)
    media_y = eixo_y + altura_de(media)

    c.setStrokeColor(VERMELHO)
    c.setLineWidth(0.9)
    c.setDash(4, 3)
    c.line(plot_x, media_y, plot_x + plot_w, media_y)
    c.setDash()
    c.setLineWidth(1)

    # Rótulo da média: posicionado sobre um trecho em que nenhuma barra
    # alcança a linha, e desenhado DEPOIS das barras para nunca ficar
    # escondido atrás delas.
    rotulo = f"Média {moeda_curta(media)}"
    tam = 7.5
    largura_rotulo = c.stringWidth(rotulo, FONTE_BOLD, tam) + 8
    altura_rotulo = 11

    destino = None
    for i, valor in enumerate(valores):
        if eixo_y + altura_de(valor) < media_y - 3:
            destino = posicoes[i]
            break

    if destino is None:
        # Nenhum vão livre: coloca acima da barra mais alta.
        rotulo_y = eixo_y + altura_max + 2
        destino = plot_x
    else:
        rotulo_y = media_y + 3

    destino = min(max(destino, plot_x), plot_x + plot_w - largura_rotulo)

    c.setFillColor(BRANCO)
    c.setStrokeColor(VERMELHO)
    c.setLineWidth(0.5)
    c.roundRect(destino, rotulo_y, largura_rotulo, altura_rotulo, 2.5, fill=1, stroke=1)
    c.setLineWidth(1)

    centralizar(
        c,
        rotulo,
        destino,
        rotulo_y + 3,
        largura_rotulo,
        fonte=FONTE_BOLD,
        tamanho=tam,
        cor=VERMELHO,
    )


# ============================================================
# BLOCOS DE NOTAS E DAS
# ============================================================


def bloco_notas(c, x, y, w, h, competencia, notas):
    arredondar_caixa(c, x, y, w, h, LARANJA_CLARO, LARANJA)

    titulo_bloco(
        c,
        x + 8,
        y + h - 16,
        f"NOTAS NÃO LANÇADAS — {texto_seguro(competencia).upper()}",
        LARANJA_ESCURO,
        w - 16,
    )

    notas = notas or []

    if not notas:
        escrever_ajustado(
            c,
            "Nenhuma nota faltante informada.",
            x + 8,
            y + h - 33,
            w - 16,
            [8, 7.5],
            fonte=FONTE,
            cor=CINZA,
        )
        return

    passo = 13
    topo = y + h - 33
    base = y + 10

    # Quantas linhas cabem de fato no bloco.
    cabem = max(1, int((topo - base) // passo) + 1)

    # Se sobrar nota de fora, a última linha vira o aviso de quantidade.
    if len(notas) > cabem:
        exibidas = cabem - 1
    else:
        exibidas = len(notas)

    linha_y = topo

    for nota in notas[:exibidas]:
        descricao = " ".join(
            parte
            for parte in (
                texto_seguro(nota.get("tipo"), ""),
                texto_seguro(nota.get("numero"), ""),
                (
                    f"Série {texto_seguro(nota.get('serie'))}"
                    if nota.get("serie") not in (None, "")
                    else ""
                ),
            )
            if parte
        )

        escrever_ajustado(
            c,
            descricao,
            x + 8,
            linha_y,
            w - 16,
            [8, 7.5, 7],
            fonte=FONTE,
            cor=PRETO,
        )
        linha_y -= passo

    restantes = len(notas) - exibidas
    if restantes > 0:
        escrever_ajustado(
            c,
            f"+ {restantes} outra{'s' if restantes > 1 else ''} nota"
            f"{'s' if restantes > 1 else ''} não lançada"
            f"{'s' if restantes > 1 else ''} "
            f"({len(notas)} no total)",
            x + 8,
            linha_y,
            w - 16,
            [8, 7.5, 7],
            fonte=FONTE_BOLD,
            cor=LARANJA_ESCURO,
        )


def bloco_das(c, x, y, w, h, dados, impostos):
    arredondar_caixa(c, x, y, w, h, VERMELHO_CLARO, VERMELHO)

    titulo_bloco(
        c,
        x + 8,
        y + h - 16,
        f"DETALHAMENTO DO DAS — {moeda(dados.get('das_total'))}",
        VERMELHO,
        w - 16,
    )

    linhas = [
        f"IRPJ {moeda(impostos.get('irpj'))}   •   CSLL {moeda(impostos.get('csll'))}",
        f"COFINS {moeda(impostos.get('cofins'))}   •   PIS {moeda(impostos.get('pis'))}",
        f"INSS/CPP {moeda(impostos.get('cpp'))}   •   ICMS {moeda(impostos.get('icms'))}",
    ]

    if impostos.get("iss") not in (None, ""):
        linhas.append(f"ISS {moeda(impostos.get('iss'))}")

    # Principal/multa/juros numa linha só quando couber, para não deixar o
    # bloco alto demais; caso contrário, quebra em duas.
    encargos = (
        f"Principal {moeda(dados.get('principal'))}   •   "
        f"Multa {moeda(dados.get('multa'))}   •   "
        f"Juros {moeda(dados.get('juros'))}"
    )

    if c.stringWidth(encargos, FONTE, 7.5) <= w - 16:
        linhas.append(encargos)
    else:
        linhas.append(f"Principal {moeda(dados.get('principal'))}")
        linhas.append(
            f"Multa {moeda(dados.get('multa'))}   •   "
            f"Juros {moeda(dados.get('juros'))}"
        )

    passo = 13
    linha_y = y + h - 33

    for linha in linhas:
        if linha_y < y + 8:
            break
        escrever_ajustado(
            c,
            linha,
            x + 8,
            linha_y,
            w - 16,
            [8, 7.5, 7, 6.5],
            fonte=FONTE,
            cor=PRETO,
        )
        linha_y -= passo


# ============================================================
# RELATÓRIO
# ============================================================


def gerar_pdf(dados, arquivo_saida):
    c = canvas.Canvas(str(arquivo_saida), pagesize=A4)

    largura, altura = A4
    area_w = largura - MARGEM * 2

    card_w = (area_w - GAP_COLUNAS * 3) / 4
    meia_w = (area_w - GAP_COLUNAS) / 2

    # A natureza vem da planilha permanente (campo "natureza" do JSON) e
    # define qual dos dois layouts será renderizado.
    servico = natureza_empresa(dados) == "servico"

    # ========================================================
    # CABEÇALHO
    # ========================================================

    y = altura - MARGEM - H_CABECALHO

    arredondar_caixa(c, MARGEM, y, area_w, H_CABECALHO, AZUL, AZUL, raio=6)

    logo_x = MARGEM + 10
    logo_y = y + 8

    c.setFillColor(LARANJA)
    c.roundRect(logo_x, logo_y, 44, H_CABECALHO - 16, 3, fill=1, stroke=0)

    centralizar(
        c,
        "JB",
        logo_x,
        logo_y + (H_CABECALHO - 16) / 2 - 4,
        44,
        fonte=FONTE_BOLD,
        tamanho=13,
        cor=BRANCO,
    )

    texto_x = logo_x + 54
    texto_w = largura - MARGEM - 10 - texto_x

    escrever_ajustado(
        c,
        texto_seguro(dados.get("razao_social")).upper(),
        texto_x,
        y + 31,
        texto_w,
        [14, 13, 12, 11, 10],
        fonte=FONTE_BOLD,
        cor=BRANCO,
    )

    escrever_ajustado(
        c,
        texto_seguro(
            dados.get("competencia_extenso"),
            dados.get("competencia", "-"),
        ).upper(),
        texto_x,
        y + 15,
        texto_w,
        [9.5, 9, 8.5],
        fonte=FONTE,
        cor=AZUL_CLARO,
    )

    # ========================================================
    # PRIMEIRA LINHA DE INDICADORES
    # ========================================================

    y -= GAP_CABECALHO + H_CARD

    card_indicador(
        c, MARGEM, y, card_w, H_CARD,
        "Receita do mês", moeda(dados.get("receita_mes")),
    )

    # Em empresa de SERVIÇO o RBT12 é exibido no bloco FAIXA (seção 7A):
    # ele continua obrigatório e não pode sumir junto com os campos de
    # compras. Sem RBT12 informado, e em COMÉRCIO, o subtítulo segue sendo
    # o limite da faixa, como sempre foi.
    if servico and dados.get("rbt12") not in (None, ""):
        subtitulo_faixa = f"RBT12 {moeda(dados.get('rbt12'))}"
    else:
        subtitulo_faixa = texto_seguro(dados.get("limite_faixa"), "")

    card_indicador(
        c, MARGEM + card_w + GAP_COLUNAS, y, card_w, H_CARD,
        "Faixa", texto_seguro(dados.get("faixa")),
        subtitulo_faixa,
    )

    card_indicador(
        c, MARGEM + (card_w + GAP_COLUNAS) * 2, y, card_w, H_CARD,
        "Alíquota efetiva", percentual(dados.get("aliquota_efetiva")),
    )

    card_indicador(
        c, MARGEM + (card_w + GAP_COLUNAS) * 3, y, card_w, H_CARD,
        "DAS a pagar", moeda(dados.get("das_total")),
        f"Vence {texto_seguro(dados.get('vencimento_das'))}",
    )

    # ========================================================
    # SEGUNDA LINHA DE INDICADORES
    # ========================================================

    vendas = float(dados.get("vendas") or dados.get("receita_mes") or 0)

    if servico:
        # EMPRESA DE SERVIÇO — seção 7A do SKILL.md.
        #
        # Entradas (Compras), Resultado bruto e Margem são OMITIDOS: a
        # coluna COMPRA não é lida, nenhum cálculo derivado de compras é
        # feito e nada ocupa o lugar desses campos — nem R$ 0,00, nem
        # "NÃO SE APLICA", nem traço ou placeholder. O único indicador da
        # linha é o FATURAMENTO (Receita Total Apurada), que passa a ocupar
        # a largura útil inteira.
        indicadores = [("Faturamento", moeda(vendas))]
    else:
        # EMPRESA DE COMÉRCIO — comportamento histórico, inalterado.
        compras = float(dados.get("compras") or 0)

        resultado = dados.get("resultado_bruto")
        if resultado is None:
            resultado = vendas - compras

        # Metodologia do modelo oficial:
        #   Resultado bruto = Vendas - Compras
        #   Margem = Resultado bruto / Compras * 100
        margem_pct = dados.get("margem")
        if margem_pct is None and compras:
            margem_pct = (float(resultado) / compras) * 100

        indicadores = [
            ("Entradas (Compras)", moeda(compras)),
            ("Saídas (Vendas)", moeda(vendas)),
            ("Resultado bruto", moeda(resultado)),
            ("Margem", percentual(margem_pct, 0)),
        ]

    y -= GAP_CARDS + H_CARD

    qtd_indicadores = len(indicadores)
    indicador_w = (
        area_w - GAP_COLUNAS * (qtd_indicadores - 1)
    ) / qtd_indicadores

    for indice, (titulo, valor) in enumerate(indicadores):
        card_indicador(
            c,
            MARGEM + (indicador_w + GAP_COLUNAS) * indice,
            y,
            indicador_w,
            H_CARD,
            titulo,
            valor,
            fundo=AZUL,
            cor_valor=BRANCO,
            cor_titulo=AZUL_CLARO,
        )

    # ========================================================
    # COMPARATIVOS
    # ========================================================

    anterior = dados.get("comparativo_mes_anterior") or {}
    anual = dados.get("comparativo_ano_anterior") or {}

    y -= GAP_LINHA + H_COMPARATIVO

    card_comparacao(
        c, MARGEM, y, meia_w, H_COMPARATIVO,
        "Comparação com o mês anterior",
        anterior.get("competencia"),
        anterior.get("valor"),
        vendas,
    )

    card_comparacao(
        c, MARGEM + meia_w + GAP_COLUNAS, y, meia_w, H_COMPARATIVO,
        "Comparação com o mesmo mês do ano anterior",
        anual.get("competencia"),
        anual.get("valor"),
        vendas,
    )

    # ========================================================
    # NOTAS NÃO LANÇADAS + DETALHAMENTO DO DAS
    # ========================================================

    impostos = dados.get("tributos") or {}

    y -= GAP_ALERTAS + H_ALERTAS

    bloco_notas(
        c, MARGEM, y, meia_w, H_ALERTAS,
        dados.get("competencia"),
        dados.get("notas_faltantes"),
    )

    bloco_das(
        c, MARGEM + meia_w + GAP_COLUNAS, y, meia_w, H_ALERTAS,
        dados, impostos,
    )

    # ========================================================
    # GRÁFICO
    # ========================================================

    y -= GAP_GRAFICO + H_GRAFICO

    desenhar_grafico_vendas(
        c, MARGEM, y, area_w, H_GRAFICO,
        dados.get("historico_vendas", []),
    )

    # ========================================================
    # COMPARATIVO DE VENDAS
    # ========================================================

    y -= GAP_RESUMO + H_RESUMO

    arredondar_caixa(c, MARGEM, y, area_w, H_RESUMO, AZUL_CLARO, AZUL_MEDIO)

    centralizar(
        c,
        "COMPARATIVO DE VENDAS",
        MARGEM,
        y + H_RESUMO - 17,
        area_w,
        fonte=FONTE_BOLD,
        tamanho=10,
        cor=AZUL,
    )

    linhas_resumo = [
        (texto_seguro(anterior.get("competencia")), anterior.get("valor")),
        (texto_seguro(anual.get("competencia")), anual.get("valor")),
    ]

    linha_y = y + H_RESUMO - 38

    for competencia, valor in linhas_resumo:
        c.setFont(FONTE, 8.5)
        c.setFillColor(CINZA)

        rotulo = f"vs. {competencia}:"
        c.drawString(MARGEM + 14, linha_y, rotulo)

        valor_x = MARGEM + 14 + 92

        c.setFont(FONTE_BOLD, 8.5)
        c.setFillColor(AZUL)
        c.drawString(valor_x, linha_y, moeda(valor))

        seta_x = valor_x + 86
        seta_direita(c, seta_x, linha_y, 16, CINZA)

        c.setFont(FONTE_BOLD, 8.5)
        c.setFillColor(AZUL)
        c.drawString(seta_x + 24, linha_y, moeda(vendas))

        variacao, diferenca = calcular_variacao(vendas, valor)
        if variacao is not None:
            subiu = diferenca >= 0
            cor = VERDE if subiu else VERMELHO
            rotulo_var = percentual(abs(variacao), 1)
            largura_var = c.stringWidth(rotulo_var, FONTE_BOLD, 8.5)

            triangulo(
                c,
                MARGEM + area_w - 14 - largura_var - 10,
                linha_y + 0.5,
                7,
                subiu,
                cor,
            )

            c.setFont(FONTE_BOLD, 8.5)
            c.setFillColor(cor)
            c.drawRightString(MARGEM + area_w - 14, linha_y, rotulo_var)

        linha_y -= 20

    # ========================================================
    # RODAPÉ
    # ========================================================

    y -= GAP_RODAPE

    alerta = texto_seguro(
        dados.get("alerta_principal"),
        f"DAS com vencimento em {texto_seguro(dados.get('vencimento_das'))}",
    )

    escrever_ajustado(
        c,
        alerta,
        MARGEM,
        y - 10,
        area_w,
        [9, 8.5, 8, 7.5],
        fonte=FONTE_BOLD,
        cor=VERMELHO,
        ancora="center",
    )

    rodape = (
        f"Total DAS: {moeda(dados.get('das_total'))}  •  "
        f"IRPJ {moeda(impostos.get('irpj'))}  •  "
        f"CSLL {moeda(impostos.get('csll'))}  •  "
        f"COFINS {moeda(impostos.get('cofins'))}  •  "
        f"PIS {moeda(impostos.get('pis'))}  •  "
        f"INSS/CPP {moeda(impostos.get('cpp'))}  •  "
        f"ICMS {moeda(impostos.get('icms'))}"
    )

    if impostos.get("iss") not in (None, ""):
        rodape += f"  •  ISS {moeda(impostos.get('iss'))}"

    escrever_ajustado(
        c,
        rodape,
        MARGEM,
        y - 25,
        area_w,
        [7.5, 7, 6.5, 6],
        fonte=FONTE,
        cor=CINZA,
        ancora="center",
    )

    escrever_ajustado(
        c,
        "Gerado automaticamente • Base: PGDAS-D + DAS + Controle Fiscal • Grupo JB",
        MARGEM,
        y - 38,
        area_w,
        [7, 6.5, 6],
        fonte=FONTE,
        cor=CINZA,
        ancora="center",
    )

    c.save()


def main():
    if len(sys.argv) < 3:
        print(
            "Uso: python gerar_relatorio.py "
            "dados_relatorio.json relatorio_fiscal.pdf"
        )
        sys.exit(1)

    arquivo_json = Path(sys.argv[1])
    arquivo_saida = Path(sys.argv[2])

    if not arquivo_json.exists():
        raise FileNotFoundError(
            f"Arquivo JSON não encontrado: {arquivo_json}"
        )

    with arquivo_json.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    gerar_pdf(dados, arquivo_saida)

    print(f"Relatório gerado com sucesso: {arquivo_saida}")


if __name__ == "__main__":
    main()
