# PROCURADORIA — Diagnóstico da execução agendada

**Data da execução:** 10/10/2026
**Pasta analisada:** `++++++CONTABILIDADE+++ > Departamento Geral > Procuradoria`
**Arquivos na pasta:** 135 (Situações Fiscais em PDF, prints/capturas em PNG e Relatórios de Procuradoria já gerados)

---

## RESULTADO: 12 contribuintes em ATUALIZAÇÃO NECESSÁRIA

Nenhum documento novo entrou na pasta desde 28/09/2026.

Porém existe pendência real e não resolvida do lote anterior:

- Em **11/09/2026** entraram 14 Situações Fiscais e foram gerados 14 Relatórios com referência **09-2026**.
- Em **25/09/2026** entrou um lote novo com **18 Situações Fiscais** (consultas de 18, 19 e 25/09).
- Em **28/09/2026** foram gerados apenas **6 Relatórios** — exatamente os 6 contribuintes que ainda **não** tinham relatório.
- Os **12 contribuintes restantes** do lote de 25/09 **já tinham** relatório 09-2026 (gerado em 11/09) e **não foram atualizados**.

Os 12 relatórios de 11/09 têm `modifiedTime` igual ao `createdTime` — confirmam que nunca foram regerados.

Pela Skill, seções 19 e 20: uma nova Situação Fiscal é uma nova fotografia do contribuinte e o
relatório anterior **não pode ser tratado como situação atual**. Logo, esses 12 relatórios 09-2026
estão **vencidos** e classificados como **ATUALIZAÇÃO NECESSÁRIA**.

---

## Contribuintes afetados

| # | Contribuinte | CNPJ | SF vigente | Relatório existente | Situação na SF vigente |
|---|---|---|---|---|---|
| 1 | M B MANSUR | 13.680.718/0001-18 | 19/09/2026 | 09-2026 (11/09) | Débitos em atraso CP-SEGUR 06/2026 + SIMPLES NAC 06 e 07/2026; parcelamento SN com 1 parcela em atraso; **inscrição na PGFN 50.4.24.060508-40** (exigibilidade suspensa, negociada no SISPAR) |
| 2 | NASCIMENTO NASCIMENTO & CIA. LTDA. | 04.743.600/0001-09 | 25/09/2026 | 09-2026 (11/09) | Débitos em atraso SIMPLES NAC 04, 05 e 07/2026; parcelamento SN com 3 parcelas em atraso; parcelamento SIEFPAR suspenso R$ 25.142,91; débitos a vencer IRRF e CP-SEGUR |
| 3 | E. GONZAGA EMPREENDIMENTOS LTDA | 36.494.887/0001-69 | 25/09/2026 | 09-2026 (11/09) | Débitos em atraso CP-SEGUR 07/2026 (2 receitas) + SIMPLES NAC 07/2026; débitos a vencer 08 e 09/2026; parcelamento SIEFPAR suspenso R$ 2.710,02 |
| 4 | J M DA SILVA FILHO BATERIAS | 49.593.624/0001-59 | 25/09/2026 | 09-2026 (11/09) | Débitos em atraso CP-SEGUR 07/2026 + SIMPLES NAC 06/2026 (R$ 3.437,74); débitos a vencer 08 e 09/2026 |
| 5 | STUDIO FIT LTDA | 60.940.872/0001-61 | 19/09/2026 | 09-2026 (11/09) | Débitos em atraso CP-SEGUR 02, 03 e 04/2026; débito em exigibilidade suspensa 08/2026 |
| 6 | ESTETIC MED SERVICOS LTDA | 53.175.728/0001-10 | 25/09/2026 | 09-2026 (11/09) | **Mudança material:** o parcelamento saiu de "1 parcela em atraso (R$ 524,70)" para **exigibilidade suspensa (R$ 15.741,03)**; o débito CP-SEGUR 06/2026 deixou de constar |
| 7 | TATHIANE COSTA PEREIRA SERVICOS METALURGICOS | 61.310.359/0001-50 | 25/09/2026 | 09-2026 (11/09) | Débito em atraso SIMPLES NAC 07/2026 (R$ 2.431,99); débitos a vencer 08 e 09/2026 |
| 8 | J R C NASCIMENTO REPRESENTACAO | 61.965.332/0001-03 | 25/09/2026 | 09-2026 (11/09) | Débitos em atraso CP-SEGUR 07/2026 + SIMPLES NAC 07/2026; débitos a vencer 08 e 09/2026 |
| 9 | UILLIAN MESSIAS DE MACEDO 00548470529 | 47.752.610/0001-05 | 18/09/2026 | 09-2026 (11/09) | 25 guias de SIMPLES NAC em atraso (01/2024 a 07/2026) |
| 10 | CENTRO INTEGRADO DE FISIO, PILATES E ESTETICA LTDA | 39.457.192/0001-03 | 25/09/2026 | 09-2026 (11/09) | Débitos MEI em atraso 03 a 06/2025; parcelamento MEI com exigibilidade suspensa; débito a vencer 09/2026 |
| 11 | BIANCA GUERRA OLIVEIRA MOREIRA DA SILVA PSICOLOGIA | 55.993.740/0001-68 | 25/09/2026 | 09-2026 (11/09) | Débito em atraso SIMPLES NAC 07/2026; débitos a vencer 08 e 09/2026 |
| 12 | MERCEARIA CENTRAL LTDA | 54.643.528/0001-08 | 25/09/2026 | 09-2026 (11/09) | Quadro melhorou: **nenhum débito marcado DEVEDOR**; resta CP-SEGUR 08/2026 e 09/2026 — ver divergência abaixo |

Em todos os 12 há ao menos uma condição financeira da seção 4, portanto o relatório continua
justificado — mas precisa ser **regerado a partir da Situação Fiscal mais recente**.

---

## Por que a rotina não gerou os PNGs automaticamente

A regra de nome (seção 15) usa apenas mês/ano. Um relatório regerado a partir da SF de 25/09
teria **exatamente o mesmo nome** do relatório de 11/09:

```
RELATORIO PROCURADORIA - <CONTRIBUINTE> - 09-2026.png
```

Gerar e enviar sobrescreveria o relatório existente. Isso é proibido pela seção 20
("nunca sobrescrever silenciosamente") e pela regra da execução agendada.

**Decisão humana necessária.** Duas opções:

1. **Autorizar a sobrescrita** dos 12 relatórios 09-2026 pela versão da SF de 18–25/09
   (a Situação Fiscal mais recente é a vigente pela seção 19).
2. **Definir um nome distinto** para a nova versão (ex.: sufixo com a data da consulta),
   preservando o relatório de 11/09 como histórico.

Assim que a opção for informada, os 12 PNGs podem ser gerados pelo script oficial e enviados
pela ponte HTTP, sem novas consultas.

---

## Pontos de atenção

**REVISÃO MANUAL — MERCEARIA CENTRAL LTDA (54.643.528/0001-08)**
Na SF de 25/09 o débito CP-SEGUR 08/2026 vence em **18/09/2026**, ou seja **antes** da data da
consulta, mas o próprio documento da Receita o rotula como "A ANALISAR-A VENCER".
A seção 5 da Skill classificaria como EM ATRASO (vermelho); a seção 6 e o rótulo do documento
apontam A VENCER (amarelo). Divergência não resolvida pela Skill — não classifiquei por conta própria.

**Sem pendência — 2 contribuintes**
`51.989.319/0001-22` e `50.833.363/0001-86` receberam SF em 11/09 e **não** receberam SF nova no
lote de 25/09. O relatório 09-2026 deles continua sendo o vigente. Nada a fazer.

**Lote de agosto**
As SFs de 20–22/08 e os 17 relatórios 08-2026 estão consistentes. Nada a fazer.

---

## Ações executadas nesta rotina

- Nenhum documento de origem foi excluído, movido ou renomeado.
- Nenhum relatório foi sobrescrito.
- Nenhum arquivo foi criado na pasta do Drive.
- Nenhuma distribuição para pastas de contribuintes (proibido pela seção 18).
