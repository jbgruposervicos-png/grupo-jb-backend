# Scripts da Skill Procuradoria

Scripts oficiais responsáveis pela geração do Relatório de Procuradoria em PNG.

## `gerar_relatorio_procuradoria.py`

Gerador oficial do Relatório de Procuradoria. É a única forma autorizada de produzir o PNG.

Não gerar o relatório manualmente nem por caminho paralelo (HTML, impressão, desenho ad hoc ou outra biblioteca) enquanto este script estiver disponível.

### Uso

```
python .claude/skills/procuradoria/scripts/gerar_relatorio_procuradoria.py dados.json saida.png
```

O primeiro argumento é o JSON com os dados já extraídos e validados; o segundo é o PNG de saída, que depois deve ser renomeado conforme a regra da seção 15 do `SKILL.md`:

```
RELATORIO PROCURADORIA - NOME DO CONTRIBUINTE - MM-AAAA.png
```

### Limites do script

O script:

- usa **somente** os dados do JSON de entrada;
- **não** lê PDF nem imagens (a extração da Situação Fiscal é feita antes, pelo Claude);
- **não** acessa o Google Drive (a distribuição é feita depois, conforme as seções 17 a 20 do `SKILL.md`);
- **não** infere, estima ou completa nenhum valor.

### Códigos de saída

| Código | Significado |
| --- | --- |
| `0` | Relatório gerado |
| `1` | Erro: argumentos inválidos, JSON ausente/inválido ou falha de escrita |
| `2` | Contribuinte sem débito, parcelamento, dívida na PGFN ou alerta — relatório **não deve** ser gerado (seção 4 do `SKILL.md`) |

O código `2` não é falha: é a aplicação da regra de que contribuinte regular encerra silenciosamente, sem PNG e sem distribuição.

### Estrutura do JSON

```json
{
  "nome": "NOME DO CONTRIBUINTE",
  "documento": "CNPJ OU CPF",
  "competencia": "08/2026",
  "referencia_mes_ano": "08-2026",
  "data_relatorio": "14/08/2026",
  "em_atraso": [
    { "tipo": "DAS / SIMPLES NACIONAL", "quantidade": 6, "valor_total": 3658.00 }
  ],
  "em_exigibilidade": [
    { "tipo": "INSS", "quantidade": 2, "valor_total": 850.00 }
  ],
  "parcelamentos": [
    { "tipo": "PARCELAMENTO DO SIMPLES NACIONAL", "parcelas_atrasadas": 6, "valor_total": null }
  ],
  "pgfn": {
    "status": "sem_divida",
    "inscricoes": []
  },
  "alertas": [
    { "titulo": "SEM CERTIDÃO", "texto": "Existem débitos em aberto..." }
  ],
  "total_geral": 4508.00
}
```

Todos os campos são opcionais e o script é tolerante a ausências. `status` da PGFN aceita `sem_divida` ou `com_divida`; qualquer outro valor (ou ausência) faz o bloco da PGFN **não** ser renderizado, porque nada foi comprovado.

Cada inscrição da PGFN aceita `numero` e `valor`. Valores podem vir como número (`3658.00`) ou como texto (`"3.658,00"`, `"R$ 3.658,00"`).

### Regras de renderização

- Bloco cujo array esteja vazio ou ausente **não é renderizado** e não deixa espaço vazio.
- `pgfn.status = "sem_divida"` → bloco **verde** compacto; `"com_divida"` → bloco **vermelho** com inscrições resumidas; qualquer outro valor (ou ausência) → bloco **não renderizado**, porque nada foi comprovado.
- Várias inscrições na PGFN são agrupadas em quantidade + valor total (seção 11).
- `TOTAL GERAL` em vermelho sempre que houver qualquer débito, parcelamento ou dívida na PGFN. Contribuinte só com alerta não gera Total Geral.
- Se `total_geral` estiver ausente, o script soma **apenas** os subtotais já apurados nos blocos, cada um uma única vez.
- Valor nulo ou ausente exibe `—` na coluna de valor e a observação `valor não informado` na linha, nunca `R$ 0,00`, e **não** entra no total. Quando isso ocorre, uma nota abaixo do total registra que valores não informados não foram somados, e o subtotal do bloco recebe o sufixo `(SOMENTE VALORES INFORMADOS)`.
- Subtotal de bloco e resumo de quantidade só aparecem quando o bloco tem duas linhas ou mais — com uma única linha repetiriam o próprio conteúdo.
- O PNG tem largura fixa de 900 px (a mesma do modelo oficial) e altura dinâmica, crescendo conforme a quantidade de blocos.

### Fidelidade ao modelo oficial

O layout reproduz `../references/modelo-relatorio-procuradoria.png`: fundo `#EEF1F5`, folha branca arredondada com sombra suave, cabeçalho azul `#12355B` alinhado à borda dos cards, blocos com fundo tingido e borda de 2 px na cor do tema, linhas divisórias finas entre itens, subtotal destacado ao pé do bloco e rodapé centralizado.

Três pontos divergem do modelo **por exigência das regras do `SKILL.md`**:

| Ponto | Modelo | Gerador | Motivo |
| --- | --- | --- | --- |
| Exigibilidade / a vencer | bloco azul | bloco **amarelo** | Seção 6 do `SKILL.md` define amarelo |
| Bloco de "a vencer" vazio | exibe "nenhuma guia a vencer" | **não renderiza** | Bloco inexistente não deve deixar espaço |
| Total Geral | não existe (só o total do bloco) | faixa **vermelha** ao pé | Seções 12 e 16 exigem Total Geral em vermelho |

O modelo é referência visual, nunca fonte de valores: nenhum nome, número, competência ou texto do exemplo é reaproveitado.

### Dependência

O script usa **Pillow** para desenhar o PNG. A dependência ainda não está declarada em `requirements.txt`, que hoje contém apenas `reportlab` (usado pela Skill Fiscal para PDF). Incluir `Pillow` em `requirements.txt` depende de instrução expressa do usuário.

## Referência visual

- `../references/modelo-relatorio-procuradoria.png` — modelo visual oficial (900×1257 px), versionado no repositório. A geometria e a paleta deste gerador foram extraídas dele.
