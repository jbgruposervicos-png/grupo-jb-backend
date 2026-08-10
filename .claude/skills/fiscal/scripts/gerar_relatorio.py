import json
import sys
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
LARANJA_CLARO = colors.HexColor("#FFF5D9")
VERMELHO = colors.HexColor("#C83C32")
VERMELHO_CLARO = colors.HexColor("#FFF0EE")
VERDE = colors.HexColor("#23A566")
CINZA = colors.HexColor("#6B7280")
CINZA_CLARO = colors.HexColor("#E5E7EB")
BRANCO = colors.white
PRETO = colors.HexColor("#172033")


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


def calcular_variacao(atual, anterior):
    if anterior in (None, 0, "", "0"):
        return None, None

    atual = float(atual)
    anterior = float(anterior)

    diferenca = atual - anterior
    percentual_var = (diferenca / anterior) * 100

    return percentual_var, diferenca


def arredondar_caixa(c, x, y, w, h, preenchimento, borda=None, raio=5):
    c.setFillColor(preenchimento)
    c.setStrokeColor(borda or preenchimento)
    c.roundRect(x, y, w, h, raio, fill=1, stroke=1)


def centralizar(c, texto, x, y, w, fonte="Helvetica-Bold", tamanho=10, cor=PRETO):
    c.setFont(fonte, tamanho)
    c.setFillColor(cor)
    largura = c.stringWidth(texto, fonte, tamanho)
    c.drawString(x + (w - largura) / 2, y, texto)


def limitar_texto(c, texto, largura, fonte="Helvetica", tamanho=8):
    texto = str(texto or "")
    if c.stringWidth(texto, fonte, tamanho) <= largura:
        return texto

    while texto and c.stringWidth(texto + "...", fonte, tamanho) > largura:
        texto = texto[:-1]

    return texto + "..."


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
):
    arredondar_caixa(c, x, y, w, h, fundo, AZUL_MEDIO)

    centralizar(
        c,
        titulo.upper(),
        x,
        y + h - 13,
        w,
        tamanho=7,
        cor=AZUL,
    )

    centralizar(
        c,
        texto_seguro(valor),
        x,
        y + h / 2 - 3,
        w,
        tamanho=11,
        cor=cor_valor,
    )

    if subtitulo:
        centralizar(
            c,
            texto_seguro(subtitulo),
            x,
            y + 7,
            w,
            fonte="Helvetica",
            tamanho=6.5,
            cor=CINZA,
        )


def card_comparacao(c, x, y, w, h, titulo, competencia, anterior, atual):
    arredondar_caixa(c, x, y, w, h, AZUL_CLARO, AZUL_MEDIO)

    c.setFillColor(AZUL)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 8, y + h - 12, titulo.upper())

    c.setFont("Helvetica", 7)
    c.setFillColor(CINZA)
    c.drawString(x + 8, y + h - 24, texto_seguro(competencia))

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(AZUL)
    c.drawString(x + 8, y + h - 36, moeda(anterior))

    variacao, diferenca = calcular_variacao(atual, anterior)

    if variacao is not None:
        cor = VERDE if variacao >= 0 else VERMELHO
        seta = "▲" if variacao >= 0 else "▼"
        verbo = "Subiu" if diferenca >= 0 else "Caiu"

        c.setFillColor(cor)
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(
            x + w - 8,
            y + h - 24,
            f"{seta} {percentual(abs(variacao), 1)}",
        )

        c.setFont("Helvetica", 7)
        c.drawRightString(
            x + w - 8,
            y + 8,
            f"{verbo} {moeda(abs(diferenca))}",
        )


def desenhar_grafico_vendas(c, x, y, w, h, historico):
    c.setFillColor(AZUL)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + w / 2, y + h + 13, "Vendas Mensais")

    if not historico:
        c.setFillColor(CINZA)
        c.setFont("Helvetica", 8)
        c.drawCentredString(
            x + w / 2,
            y + h / 2,
            "Histórico mensal não disponível",
        )
        return

    valores = [float(item.get("valor", 0) or 0) for item in historico]

    maior = max(valores) if valores else 0

    if maior <= 0:
        maior = 1

    espaco = 5
    qtd = len(historico)
    barra_w = max(12, (w - espaco * (qtd - 1)) / qtd)

    # Linha base
    c.setStrokeColor(CINZA_CLARO)
    c.line(x, y, x + w, y)

    # Média
    media = sum(valores) / len(valores)
    media_y = y + (media / maior) * h

    c.setStrokeColor(VERMELHO)
    c.setDash(4, 3)
    c.line(x, media_y, x + w, media_y)
    c.setDash()

    c.setFillColor(VERMELHO)
    c.setFont("Helvetica", 5.5)
    c.drawRightString(x + w, media_y + 2, f"Média {moeda(media)}")

    for i, item in enumerate(historico):
        valor = float(item.get("valor", 0) or 0)
        altura = (valor / maior) * (h - 15)

        bx = x + i * (barra_w + espaco)

        atual = bool(item.get("atual", False))
        cor = LARANJA if atual else AZUL_MEDIO

        c.setFillColor(cor)
        c.rect(bx, y, barra_w, altura, fill=1, stroke=0)

        c.setFillColor(CINZA)
        c.setFont("Helvetica", 5.3)
        c.drawCentredString(
            bx + barra_w / 2,
            y - 8,
            texto_seguro(item.get("mes")),
        )

        c.setFillColor(PRETO)
        c.setFont("Helvetica", 4.7)
        c.drawCentredString(
            bx + barra_w / 2,
            y + altura + 3,
            moeda(valor),
        )


def gerar_pdf(dados, arquivo_saida):
    c = canvas.Canvas(str(arquivo_saida), pagesize=A4)

    largura, altura = A4

    margem = 14
    area_w = largura - margem * 2

    # ========================================================
    # CABEÇALHO
    # ========================================================

    header_h = 47
    header_y = altura - margem - header_h

    arredondar_caixa(
        c,
        margem,
        header_y,
        area_w,
        header_h,
        AZUL,
        AZUL,
        raio=6,
    )

    # Logo JB
    logo_x = margem + 10
    logo_y = header_y + 8

    c.setFillColor(LARANJA)
    c.roundRect(logo_x, logo_y, 38, 31, 3, fill=1, stroke=0)

    c.setFillColor(BRANCO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(logo_x + 6, logo_y + 11, "JB")

    razao_social = texto_seguro(dados.get("razao_social"))
    competencia_extenso = texto_seguro(
        dados.get("competencia_extenso"),
        dados.get("competencia", "-"),
    )

    c.setFillColor(BRANCO)
    c.setFont("Helvetica-Bold", 13)

    empresa_exibicao = limitar_texto(
        c,
        razao_social.upper(),
        area_w - 70,
        "Helvetica-Bold",
        13,
    )

    c.drawString(margem + 60, header_y + 27, empresa_exibicao)

    c.setFont("Helvetica", 8)
    c.drawString(margem + 60, header_y + 13, competencia_extenso.upper())

    # ========================================================
    # PRIMEIRA LINHA
    # ========================================================

    gap = 3
    card_w = (area_w - gap * 3) / 4
    card_h = 49

    y = header_y - 22 - card_h

    card_indicador(
        c,
        margem,
        y,
        card_w,
        card_h,
        "Receita do mês",
        moeda(dados.get("receita_mes")),
    )

    card_indicador(
        c,
        margem + card_w + gap,
        y,
        card_w,
        card_h,
        "Faixa",
        texto_seguro(dados.get("faixa")),
        texto_seguro(dados.get("limite_faixa"), ""),
    )

    card_indicador(
        c,
        margem + (card_w + gap) * 2,
        y,
        card_w,
        card_h,
        "Alíquota efetiva",
        percentual(dados.get("aliquota_efetiva")),
    )

    card_indicador(
        c,
        margem + (card_w + gap) * 3,
        y,
        card_w,
        card_h,
        "DAS a pagar",
        moeda(dados.get("das_total")),
        f"Vence {texto_seguro(dados.get('vencimento_das'))}",
    )

    # ========================================================
    # SEGUNDA LINHA
    # ========================================================

    compras = float(dados.get("compras") or 0)
    vendas = float(dados.get("vendas") or dados.get("receita_mes") or 0)

    resultado = dados.get("resultado_bruto")

    if resultado is None:
        resultado = vendas - compras

    margem_pct = dados.get("margem")

    if margem_pct is None and compras:
        margem_pct = (float(resultado) / compras) * 100

    y -= 56

    card_indicador(
        c,
        margem,
        y,
        card_w,
        card_h,
        "Entradas (Compras)",
        moeda(compras),
        fundo=AZUL,
        cor_valor=BRANCO,
    )

    card_indicador(
        c,
        margem + card_w + gap,
        y,
        card_w,
        card_h,
        "Saídas (Vendas)",
        moeda(vendas),
        fundo=AZUL,
        cor_valor=BRANCO,
    )

    card_indicador(
        c,
        margem + (card_w + gap) * 2,
        y,
        card_w,
        card_h,
        "Resultado bruto",
        moeda(resultado),
        fundo=AZUL,
        cor_valor=BRANCO,
    )

    card_indicador(
        c,
        margem + (card_w + gap) * 3,
        y,
        card_w,
        card_h,
        "Margem",
        percentual(margem_pct, 0),
        fundo=AZUL,
        cor_valor=BRANCO,
    )

    # ========================================================
    # COMPARATIVOS
    # ========================================================

    y -= 60

    comp_w = (area_w - gap) / 2
    comp_h = 46

    anterior = dados.get("comparativo_mes_anterior", {})

    card_comparacao(
        c,
        margem,
        y,
        comp_w,
        comp_h,
        f"Comparação de vendas do mês anterior ({texto_seguro(anterior.get('competencia'))})",
        texto_seguro(anterior.get("competencia")),
        anterior.get("valor"),
        vendas,
    )

    anual = dados.get("comparativo_ano_anterior", {})

    card_comparacao(
        c,
        margem + comp_w + gap,
        y,
        comp_w,
        comp_h,
        f"Comparação de vendas {texto_seguro(anual.get('competencia'))}",
        texto_seguro(anual.get("competencia")),
        anual.get("valor"),
        vendas,
    )

    # ========================================================
    # ALERTAS + DAS
    # ========================================================

    y -= 71
    box_h = 78

    box_w = (area_w - gap) / 2

    # Notas faltantes
    arredondar_caixa(
        c,
        margem,
        y,
        box_w,
        box_h,
        LARANJA_CLARO,
        LARANJA,
    )

    c.setFillColor(colors.HexColor("#C77C00"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(
        margem + 8,
        y + box_h - 13,
        f"■ NOTAS NÃO LANÇADAS — {texto_seguro(dados.get('competencia')).upper()}",
    )

    notas = dados.get("notas_faltantes") or []

    linha_y = y + box_h - 27

    if notas:
        for nota in notas[:4]:
            descricao = (
                f"{texto_seguro(nota.get('tipo'))} "
                f"{texto_seguro(nota.get('numero'))} "
                f"Série {texto_seguro(nota.get('serie'))}"
            )

            c.setFillColor(PRETO)
            c.setFont("Helvetica", 6.5)
            c.drawString(
                margem + 8,
                linha_y,
                limitar_texto(c, descricao, box_w - 18, tamanho=6.5),
            )

            linha_y -= 11
    else:
        c.setFillColor(CINZA)
        c.setFont("Helvetica", 7)
        c.drawString(margem + 8, linha_y, "Nenhuma nota faltante informada.")

    # Detalhamento DAS
    das_x = margem + box_w + gap

    arredondar_caixa(
        c,
        das_x,
        y,
        box_w,
        box_h,
        VERMELHO_CLARO,
        VERMELHO,
    )

    c.setFillColor(VERMELHO)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(
        das_x + 8,
        y + box_h - 13,
        f"■ DETALHAMENTO DO DAS — {moeda(dados.get('das_total'))}",
    )

    impostos = dados.get("tributos", {})

    linhas_impostos = [
        f"IRPJ {moeda(impostos.get('irpj'))}   •   CSLL {moeda(impostos.get('csll'))}",
        f"COFINS {moeda(impostos.get('cofins'))}   •   PIS {moeda(impostos.get('pis'))}",
        f"INSS/CPP {moeda(impostos.get('cpp'))}   •   ICMS {moeda(impostos.get('icms'))}",
        (
            f"Principal {moeda(dados.get('principal'))}   •   "
            f"Multa {moeda(dados.get('multa'))}   •   "
            f"Juros {moeda(dados.get('juros'))}"
        ),
    ]

    linha_y = y + box_h - 28

    for linha in linhas_impostos:
        c.setFillColor(PRETO)
        c.setFont("Helvetica", 6.2)
        c.drawString(
            das_x + 8,
            linha_y,
            limitar_texto(c, linha, box_w - 16, tamanho=6.2),
        )
        linha_y -= 11

    # ========================================================
    # GRÁFICO
    # ========================================================

    y -= 160

    historico = dados.get("historico_vendas", [])

    desenhar_grafico_vendas(
        c,
        margem + 8,
        y + 12,
        area_w - 16,
        105,
        historico,
    )

    # ========================================================
    # COMPARATIVO INFERIOR
    # ========================================================

    comparativo_y = 64
    comparativo_h = 61

    arredondar_caixa(
        c,
        margem,
        comparativo_y,
        area_w,
        comparativo_h,
        AZUL_CLARO,
        AZUL_MEDIO,
    )

    centralizar(
        c,
        "Comparativo de Vendas",
        margem,
        comparativo_y + comparativo_h - 14,
        area_w,
        tamanho=9,
        cor=AZUL,
    )

    c.setFont("Helvetica", 6.5)
    c.setFillColor(CINZA)

    linha1 = (
        f"vs. {texto_seguro(anterior.get('competencia'))}: "
        f"{moeda(anterior.get('valor'))}  →  {moeda(vendas)}"
    )

    linha2 = (
        f"vs. {texto_seguro(anual.get('competencia'))}: "
        f"{moeda(anual.get('valor'))}  →  {moeda(vendas)}"
    )

    c.drawString(margem + 12, comparativo_y + 30, linha1)
    c.drawString(margem + 12, comparativo_y + 15, linha2)

    # ========================================================
    # RODAPÉ / ALERTA
    # ========================================================

    alerta = texto_seguro(
        dados.get("alerta_principal"),
        f"DAS com vencimento em {texto_seguro(dados.get('vencimento_das'))}",
    )

    c.setFillColor(VERMELHO)
    c.setFont("Helvetica-Bold", 6.5)

    c.drawCentredString(
        largura / 2,
        43,
        limitar_texto(c, alerta, area_w - 20, "Helvetica-Bold", 6.5),
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

    c.setFillColor(CINZA)
    c.setFont("Helvetica", 5.3)
    c.drawCentredString(
        largura / 2,
        31,
        limitar_texto(c, rodape, area_w - 10, tamanho=5.3),
    )

    c.setFont("Helvetica", 5)
    c.drawCentredString(
        largura / 2,
        19,
        "Gerado automaticamente • Base: PGDAS-D + DAS + Controle Fiscal • Grupo JB",
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
