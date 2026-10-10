# PROCURADORIA — Execução agendada de 10/10/2026

Pasta verificada: `++++++CONTABILIDADE+++ > Departamento Geral > Procuradoria`
(ID `1jUmK2AwcxzvvgzlesRy6ROPR0nuveplb`)

**Status: a pasta NÃO está vazia — 130 arquivos.**

**Resultado: nenhum documento novo para processar, porém 12 relatórios 09/2026 estão
baseados em Situação Fiscal já superada → ATUALIZAÇÃO NECESSÁRIA (seções 19 e 20).**

Nada foi criado, alterado, sobrescrito, movido ou excluído nesta execução.

---

## 1. O que existe na pasta

| Tipo | Qtd. | Datas |
| --- | --- | --- |
| Situações Fiscais (PDF) | 32 | lotes de 20–22/08, 04–11/09 e 18–25/09/2026 |
| Prints / capturas de tela | 66 | 27/08 a 11/09/2026 |
| Relatórios de Procuradoria (PNG) | 32 | referências 08/2026 e 09/2026 |

Nenhum arquivo foi incluído na pasta depois de **28/09/2026**. O documento de entrada
mais recente é de **25/09/2026**. Não há, portanto, lote novo aguardando processamento.

## 2. Reconciliação do lote de setembro

O lote vigente (18–25/09/2026) contém **18 contribuintes**. Existem **20 relatórios**
com referência `09-2026`, gerados em duas rodadas:

- **11/09/2026 — 14 relatórios**
- **28/09/2026 — 6 relatórios**

Os 6 relatórios de 28/09 correspondem exatamente aos 6 contribuintes que apareceram
pela primeira vez no lote de 25/09. Ou seja: **a rodada de 28/09 processou apenas os
contribuintes novos e não reprocessou os 12 que já tinham relatório de 11/09**, embora
estes tenham recebido Situação Fiscal mais recente.

Verificação de integridade: em todos os 20 relatórios `createdTime == modifiedTime`,
confirmando que nenhum dos 14 relatórios de 11/09 foi atualizado depois.

## 3. Contribuintes em dia (6) — relatório gerado do documento vigente

| Contribuinte | CNPJ/CPF | Situação Fiscal | Relatório |
| --- | --- | --- | --- |
| E OLIVEIRA DA SILVA COMERCIO VAREJISTA DE MOVEIS | 52.814.543/0001-46 | 25/09 | 28/09 |
| ANTONIO CARLOS SOUZA SANTOS 58384030553 | 34.211.408/0001-24 | 25/09 | 28/09 |
| JOSE LUCIO ALMEIDA CHAGAS | 14.833.071/0001-80 | 25/09 | 28/09 |
| G O SILVA COMERCIO DE GAS | 44.584.815/0001-30 | 25/09 | 28/09 |
| CLEONICE ARAUJO MARQUES | 074.179.425-04 | 25/09 | 28/09 |
| SANTOS & ROCHA ESPORTES LTDA | 49.974.189/0001-02 | 25/09 | 28/09 |

## 4. Contribuintes em dia (2) — sem Situação Fiscal mais recente

| Contribuinte | CNPJ | Situação Fiscal | Relatório |
| --- | --- | --- | --- |
| GESTAO & LOGISTICA EMPRESARIAL SVC LTDA | 51.989.319/0001-22 | 11/09 | 11/09 |
| CENTRO DE TREINAMENTO BAHIA TOP TEAM LTDA | 50.833.363/0001-86 | 11/09 | 11/09 |

## 5. ATUALIZAÇÃO NECESSÁRIA (12) — relatório anterior à Situação Fiscal vigente

| Contribuinte | CNPJ | SF do relatório | SF vigente |
| --- | --- | --- | --- |
| BIANCA GUERRA OLIVEIRA MOREIRA DA SILVA PSICOLOGIA | 55.993.740/0001-68 | 11/09 | 25/09 |
| UILLIAN MESSIAS DE MACEDO 00548470529 | 47.752.610/0001-05 | 11/09 | 18/09 |
| TATHIANE COSTA PEREIRA SERVICOS METALURGICOS | 61.310.359/0001-50 | 11/09 | 25/09 |
| J R C NASCIMENTO REPRESENTACAO | 61.965.332/0001-03 | 11/09 | 25/09 |
| J M DA SILVA FILHO BATERIAS | 49.593.624/0001-59 | 11/09 | 25/09 |
| MERCEARIA CENTRAL LTDA | 54.643.528/0001-08 | 11/09 | 25/09 |
| M B MANSUR | 13.680.718/0001-18 | 04/09 | 19/09 |
| NASCIMENTO NASCIMENTO & CIA. LTDA. | 04.743.600/0001-09 | 11/09 | 25/09 |
| CENTRO INTEGRADO DE FISIO, PILATES E ESTETICA LTDA | 39.457.192/0001-03 | 11/09 | 25/09 |
| E. GONZAGA EMPREENDIMENTOS LTDA | 36.494.887/0001-69 | 11/09 | 25/09 |
| ESTETIC MED SERVICOS LTDA | 53.175.728/0001-10 | 11/09 | 25/09 |
| STUDIO FIT LTDA | 60.940.872/0001-61 | 06/09 | 19/09 |

### Causa estrutural (atinge todos os 12)

A guia federal **08/2026 com vencimento em 18/09/2026** (CP-SEGUR / IRRF, conforme o
contribuinte) aparece como **"A ANALISAR-A VENCER"** nas Situações Fiscais de até 11/09
e está **vencida** nas de 18–25/09. Pela seção 5 da Skill ela deixa de ser bloco
AMARELO (a vencer) e passa a bloco VERMELHO (em atraso), alterando a composição dos
blocos e o TOTAL GERAL de cada relatório. Somam-se a isso multa/juros acrescidos e,
em alguns casos, mudanças de fato.

### Divergências confirmadas documento a documento (6 pares conferidos)

- **BIANCA GUERRA** — SIMPLES NAC. 07/2026 passou de `245,80` para `256,29`; a guia
  CP-SEGUR 08/2026 (`181,25`) migrou para débito vencido; surgiu CP-SEGUR 09/2026
  `178,31` a vencer (venc. 20/10/2026).
- **TATHIANE COSTA PEREIRA** — a guia CP-SEGUR 07/2026 (`193,03`) **deixou de constar**
  (quitada); SIMPLES NAC. 07/2026 passou de `2.332,45` para `2.431,99`.
- **J R C NASCIMENTO** — CP-SEGUR 07/2026 de `193,03` para `201,27`; SIMPLES NAC.
  07/2026 de `146,60` para `152,85`; CP-SEGUR 08/2026 (`181,25`) agora vencida.
- **M B MANSUR** — passou a constar **parcelamento do Simples Nacional com 1 parcela em
  atraso** (em 04/09 o parcelamento estava apenas como exigibilidade suspensa, sem
  parcela em atraso). SIMPLES NAC. 06/2026 de `4.855,13` para `5.054,68`; 07/2026 de
  `4.307,11` para `4.508,34`.
- **NASCIMENTO NASCIMENTO & CIA.** — as três guias 08/2026 (IRRF `232,63`,
  CP-SEGUR `849,79`, CP-SEGUR `109,83`) migraram de "a vencer" para débito vencido;
  SIMPLES NAC. 07/2026 de `590,58` para `615,78`. Parcelamento segue com 3 parcelas
  em atraso.
- **STUDIO FIT** — valores dos débitos inalterados, mas a guia CP-SEGUR 08/2026
  (`440,00`) venceu entre as duas consultas, mudando a classificação e o TOTAL GERAL.

## 6. Por que nada foi gerado nesta execução

A seção 20 da Skill e a regra da própria rotina ("nunca sobrescrever silenciosamente
relatórios já existentes") determinam que, havendo relatório do **mesmo contribuinte e
mesma referência** (`09-2026`) e Situação Fiscal mais recente que **altere os dados**, o
caso deve ser **classificado como ATUALIZAÇÃO NECESSÁRIA**, sem reaproveitar o relatório
anterior como situação atual e sem sobrescrevê-lo. A regeneração depende de decisão
humana. A limpeza da pasta também permanece humana (seção 21).

## 7. Pontos de atenção para quem autorizar a regeneração

- **M B MANSUR** é o único com inscrição na PGFN: `50.4.24.060508-40`
  (SIMP NAC - MEI, inscrita em 08/04/2024, processo `12376.682.819/2024-88`), situação
  **ATIVA / NAO AJUIZAVEL / NEGOCIADA NO SISPAR**, em transação por adesão
  (Edital PGDAU nº 01/2024, conta `010002668`, até 60 meses, sem redução). O documento
  **não informa o valor da inscrição** — pela seção 11 o valor não pode ser estimado.
  Os demais 11 registram "não foram detectadas pendências" na PGFN (bloco VERDE).
- **Parcelamentos sem valor de parcela**: M B MANSUR (1 parcela em atraso) e
  NASCIMENTO NASCIMENTO (3 parcelas em atraso). Pela seção 7, informar a quantidade e
  **não somar** valor desconhecido ao TOTAL GERAL.
- **Risco de cancelamento de parcelamento**: não há print do e-CAC posterior a 11/09
  indicando risco. Pela seção 8, **não** declarar "PARCELAMENTO EM RISCO".
- **Termo de Exclusão do Simples Nacional**: nenhum documento individualizado na pasta.
  O aviso sobre o prazo de opção 2027 que aparece no rodapé das Situações Fiscais é
  genérico e, pela seção 10, **não** autoriza alerta de exclusão.
- **Prints complementares**: as 66 capturas de tela vão de 27/08 a 11/09. O lote de
  18–25/09 não veio acompanhado de prints novos.
- Nenhum contribuinte do lote está totalmente regular — todos os 20 têm ao menos uma
  condição financeira, logo não há caso de encerramento silencioso pela seção 4.

## 8. Observação

As Situações Fiscais vigentes têm 15 a 22 dias (18–25/09/2026) e a referência continua
sendo `09/2026`. Não chegou lote de outubro. Pela seção 19, o documento vigente é sempre
o mais recente disponível na pasta — nenhuma consulta nova foi feita por esta rotina.
