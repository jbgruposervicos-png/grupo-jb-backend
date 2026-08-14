---
name: procuradoria
description: Processa automaticamente as Situações Fiscais do Departamento de Procuradoria do Grupo JB. Use quando houver Situações Fiscais (PDF, PNG ou outro formato legível) e documentos complementares (prints do e-CAC, prints do Regularize/PGFN, Termo de Exclusão do Simples Nacional) na pasta Departamento Geral/Procuradoria para identificar o contribuinte, avaliar débitos, parcelamentos e a situação na PGFN, gerar o Relatório de Procuradoria em PNG e distribuir os documentos para a pasta correta do contribuinte no Google Drive.
---

# PROCESSAMENTO DE PROCURADORIA — GRUPO JB

Esta Skill é independente da Skill Fiscal.

Nenhuma regra da Skill Fiscal se aplica aqui, e nenhum arquivo da Skill Fiscal deve ser lido, alterado ou reutilizado por este fluxo.

---

# 1. OBJETIVO

A Skill controla o processamento automático da Procuradoria.

Pasta de entrada no Google Drive:

```
++++++CONTABILIDADE+++
> Departamento Geral
> Procuradoria
```

A pasta pode conter Situações Fiscais e documentos complementares de vários clientes simultaneamente.

Cada contribuinte é processado independentemente.

Um erro em um contribuinte nunca interrompe todo o lote.

---

# 2. DOCUMENTO PRINCIPAL

A SITUAÇÃO FISCAL é o documento principal.

Ela pode estar em PDF, PNG ou outro formato legível disponível no Google Drive.

A identificação deve ser feita pelo conteúdo do documento, nunca apenas pelo nome físico do arquivo.

Ler integralmente todas as páginas/imagens.

Extrair prioritariamente:

- razão social ou nome;
- CNPJ ou CPF;
- data da consulta;
- débitos;
- parcelamentos;
- situação na Receita Federal;
- situação na Procuradoria/PGFN.

CNPJ ou CPF é a chave principal de identificação.

---

# 3. DOCUMENTOS COMPLEMENTARES

O colaborador da Procuradoria poderá colocar, junto da Situação Fiscal:

- prints do e-CAC;
- prints do Regularize/PGFN;
- Termo de Exclusão do Simples Nacional;
- outros prints relacionados à situação fiscal do mesmo contribuinte.

Esses documentos complementam a Situação Fiscal.

Só utilizar um documento complementar quando houver segurança de que ele pertence ao mesmo contribuinte.

Não inventar informação a partir de imagem ilegível, cortada ou sem contexto suficiente.

---

# 4. REGRA PARA GERAR RELATÓRIO

NÃO gerar relatório para contribuinte totalmente regular.

Somente gerar Relatório de Procuradoria quando houver pelo menos UMA destas condições financeiras identificadas:

- débito em atraso;
- débito em exigibilidade / a vencer;
- dívida na PGFN;
- parcelamento com parcelas em atraso.

## ALERTA SOZINHO NÃO GERA RELATÓRIO

Alerta não é condição financeira.

Alertas apenas COMPLEMENTAM um relatório já justificado pela existência de dívida.

Não geram relatório isoladamente:

- Termo de Exclusão sem dívida identificada;
- print do e-CAC com aviso, mas sem dívida;
- alerta de certidão sem dívida;
- qualquer outro alerta complementar sem obrigação financeira identificada.

Havendo alerta e nenhuma das quatro condições financeiras acima, encerrar aquele contribuinte sem gerar PNG e sem distribuir.

## PARCELAMENTO COM PARCELAS EM ATRASO

Parcelamento com parcelas em atraso conta como condição financeira MESMO quando o valor das parcelas não estiver disponível.

Nesse caso:

- pode gerar relatório;
- informar a quantidade de parcelas;
- não inventar valor;
- não somar valor desconhecido ao TOTAL GERAL.

## CONTRIBUINTE REGULAR

Se a Situação Fiscal estiver regular:

- não gerar PNG;
- não gerar aviso;
- não gerar relatório;
- não distribuir relatório.

Encerrar silenciosamente aquele contribuinte e seguir para o próximo.

---

# 5. DÉBITOS EM ATRASO

Débitos cuja data de vencimento já tenha ocorrido devem ser classificados como:

**EM ATRASO**

Cor visual do bloco:
VERMELHO.

Extrair valores reais do documento.

Quando houver vários débitos da mesma natureza, NÃO é necessário listar cada competência individualmente.

Agrupar por tipo/origem.

Exemplo:

```
DAS / SIMPLES NACIONAL
6 guias em atraso
Total: R$ X.XXX,XX

INSS
3 guias em atraso
Total: R$ X.XXX,XX

FGTS
2 guias em atraso
Total: R$ X.XXX,XX
```

Utilizar para totalização apenas valores efetivamente encontrados.

---

# 6. DÉBITOS EM EXIGIBILIDADE / A VENCER

Débitos existentes cuja data de vencimento seja posterior à data da Situação Fiscal devem ser classificados como:

**EM EXIGIBILIDADE / A VENCER**

Cor visual:
AMARELO.

Também podem ser consolidados por tipo.

Exemplo:

```
DAS
2 guias em exigibilidade
Total: R$ X.XXX,XX
```

Não aplicar multa ou juros futuros por estimativa.

---

# 7. PARCELAMENTOS

Parcelamentos devem ser apresentados de forma resumida.

Exemplo:

```
PARCELAMENTO DO SIMPLES NACIONAL
6 parcelas em atraso
```

Se o valor das parcelas estiver efetivamente disponível em documento ou print válido:

informar o valor.

Se não estiver:

não inventar e não incluir valor desconhecido no total geral.

A existência de parcelas atrasadas NÃO autoriza automaticamente informar risco de cancelamento.

---

# 8. RISCO DE CANCELAMENTO DE PARCELAMENTO

Somente informar:

**PARCELAMENTO EM RISCO**

quando o colaborador tiver anexado print/mensagem do e-CAC que indique claramente risco de cancelamento ou situação equivalente para aquele contribuinte.

Nunca deduzir risco apenas pela quantidade de parcelas atrasadas.

---

# 9. CERTIDÃO

Quando existirem débitos em aberto que não estejam regularizados/parcelados e que impeçam a regularidade fiscal:

gerar alerta relacionado à certidão.

Texto deve ser simples, por exemplo:

```
SEM CERTIDÃO

Existem débitos em aberto que precisam ser regularizados para possibilitar a emissão da certidão.
```

Não criar esse alerta quando os próprios documentos indicarem situação diversa, exigibilidade suspensa ou outra condição que preserve a regularidade.

---

# 10. SIMPLES NACIONAL / TERMO DE EXCLUSÃO

A existência de débitos, sozinha, NÃO autoriza gerar alerta de exclusão do Simples Nacional.

Somente gerar alerta de risco/exclusão quando existir TERMO DE EXCLUSÃO ou outro documento individualizado do próprio contribuinte anexado pelo colaborador.

Avisos genéricos presentes em rodapés da Situação Fiscal não são prova de que aquele contribuinte recebeu Termo de Exclusão.

---

# 11. PROCURADORIA / PGFN

Verificar obrigatoriamente o diagnóstico da PGFN.

Se o documento indicar ausência de pendências:

informar:

**SEM DÍVIDAS NA PROCURADORIA**

Bloco visual:
VERDE.

Se houver dívida inscrita:

bloco visual:
VERMELHO.

O colaborador deverá anexar print do Regularize/PGFN quando necessário para complementar:

- número da inscrição;
- valor da inscrição.

Exemplo:

```
DÉBITO NA PROCURADORIA

Inscrição: XXXXX
Valor: R$ X.XXX,XX
```

Se houver várias inscrições:

agrupar de forma resumida e mostrar quantidade + valor total.

Nunca inventar número de inscrição ou valor.

---

# 12. TOTAL GERAL

TOTAL significa o total financeiro identificado para o contribuinte.

```
TOTAL GERAL =
  débitos em atraso
+ débitos em exigibilidade/a vencer
+ débitos da PGFN
+ parcelamentos quando seus valores estiverem efetivamente conhecidos
```

Nunca contar a mesma dívida duas vezes.

Valores desconhecidos não entram no total.

Parcelamento com apenas quantidade de parcelas conhecida deve ser informado, mas não somado sem valor comprovado.

O TOTAL GERAL deve aparecer em destaque na cor VERMELHA.

---

# 13. CONSOLIDAÇÃO

O relatório deve ser executivo e resumido.

Quando houver muitos débitos:

não listar cada débito individualmente.

Agrupar por natureza/origem.

Priorizar:

- tipo;
- quantidade;
- valor total.

Detalhar individualmente somente quando isso for relevante para compreensão de uma situação excepcional.

---

# 14. ALERTAS

Alertas só podem surgir de:

1. regra operacional expressamente definida nesta Skill; ou
2. documento complementar válido anexado pelo colaborador.

Não criar alertas livremente.

Alerta nunca justifica, sozinho, a geração do relatório: ele apenas complementa um relatório já justificado por condição financeira, conforme a seção 4.

Possíveis alertas incluem:

- parcelamento em risco, somente com mensagem do e-CAC;
- sem certidão, conforme regra desta Skill;
- Termo de Exclusão do Simples, somente com documento específico;
- outros alertas expressamente comprovados por documento complementar.

---

# 15. DATA E COMPETÊNCIA DE ARQUIVAMENTO

Utilizar mês e ano da data da Situação Fiscal.

Exemplo:

```
Situação Fiscal emitida em 14/08/2026
→ referência 08/2026
→ pasta 08 2026
```

Nome do relatório:

```
RELATORIO PROCURADORIA - NOME DO CONTRIBUINTE - 08-2026.png
```

---

# 16. MODELO VISUAL

A referência oficial deverá ficar em:

`.claude/skills/procuradoria/references/modelo-relatorio-procuradoria.png`

O modelo deve possuir:

- cabeçalho azul escuro;
- nome do contribuinte;
- CNPJ/CPF;
- mês/ano;
- blocos vermelhos para débitos;
- blocos amarelos para exigibilidade/alertas;
- bloco verde para PGFN sem pendências;
- bloco vermelho para PGFN com dívida;
- Total Geral em vermelho;
- visual limpo e executivo.

O conteúdo é dinâmico.

Blocos inexistentes não devem gerar espaços vazios desnecessários.

O PNG pode crescer verticalmente quando necessário.

## DECISÕES VISUAIS DEFINITIVAS

As regras abaixo estão decididas e não são mais objeto de dúvida:

- EM EXIGIBILIDADE / A VENCER = AMARELO;
- se não houver débito a vencer, o bloco não aparece;
- TOTAL GERAL = destaque VERMELHO.

Estas regras da Skill PREVALECEM mesmo que o modelo visual de referência apresente pequenas diferenças.

O modelo é referência de layout, não fonte de regra nem fonte de valores.

---

# 17. PASTA DE SAÍDA INICIAL

Após gerar, salvar primeiro em:

```
++++++CONTABILIDADE+++
> Departamento Geral
> Procuradoria
```

Não excluir a Situação Fiscal original.

---

# 18. DESTINOS POSSÍVEIS

O contribuinte pode estar em:

```
+++++++++++++++EMPRESAS+++++
```

ou

```
+++++++++++FAZENDAS+++++
```

ou

```
++++++++EMPREGADA DOMESTICA++++
```

Pesquisar o contribuinte nas três raízes quando necessário.

Prioridade:

1. CNPJ/CPF;
2. razão social/nome;
3. nome da pasta como validação.

Nunca escolher destino incerto.

---

# 19. ESTRUTURA DE DESTINO

Dentro do contribuinte:

```
PROCURADORIA
> ANO
> MM AAAA
```

Exemplo:

```
PROCURADORIA
> 2026
> 08 2026
```

A automação pode criar SOMENTE a pasta:

```
MM AAAA
```

Não criar automaticamente:

- cliente;
- PROCURADORIA;
- ano.

---

# 20. DISTRIBUIÇÃO

Quando houver relatório:

copiar para o destino:

- Situação Fiscal original;
- Relatório de Procuradoria em PNG.

Preservar os originais na pasta Departamento Geral > Procuradoria.

Não mover.

Não excluir.

---

# 21. DUPLICIDADE

Antes de gerar ou distribuir, verificar se já existe relatório do mesmo contribuinte e mesmo mês/ano.

Nunca sobrescrever silenciosamente.

Se já estiver corretamente distribuído:

**JÁ DISTRIBUÍDO.**

---

# 22. PROCESSAMENTO EM LOTE

Pode haver vários clientes simultaneamente na pasta.

Cada Situação Fiscal inicia um processamento independente.

Erro de um cliente:

→ registrar internamente;
→ pular aquele cliente;
→ continuar com os demais.

---

# 23. SEGURANÇA

Nunca:

- inventar débitos;
- inventar valores;
- inventar inscrições;
- inventar risco de parcelamento;
- inventar risco de exclusão do Simples;
- interpretar aviso genérico como aviso individual;
- gerar relatório sem condição financeira identificada, apenas por existir alerta;
- duplicar dívida no total;
- escolher destino incerto;
- alterar documentos originais;
- bloquear todo o lote por um erro isolado.

---

# 24. IMPLEMENTAÇÃO

## Gerador oficial

O script oficial responsável pela geração do PNG é:

`.claude/skills/procuradoria/scripts/gerar_relatorio_procuradoria.py`

Esse script é a ÚNICA forma autorizada de produzir o Relatório de Procuradoria.

Não produzir o PNG manualmente nem por caminho paralelo (HTML, impressão, desenho ad hoc ou outra biblioteca) quando o script estiver disponível.

Se o script estiver comprovadamente indisponível, interromper aquele contribuinte e informar o problema — nunca improvisar um gerador paralelo.

## Execução

Antes de executar, construir um JSON contendo SOMENTE dados já extraídos e validados da Situação Fiscal e dos documentos complementares.

Campo sem origem comprovada nesses documentos deve ficar ausente ou nulo, nunca preenchido por conveniência.

Executar no formato:

`python .claude/skills/procuradoria/scripts/gerar_relatorio_procuradoria.py dados.json saida.png`

O segundo argumento é o PNG de saída, que depois deve ser renomeado conforme a regra de nome da seção 15.

A estrutura do JSON e os códigos de saída estão documentados em `.claude/skills/procuradoria/scripts/README.md`.

## Códigos de saída

- `0` — relatório gerado;
- `1` — erro (argumentos inválidos, JSON ausente ou inválido, falha de escrita);
- `2` — nenhuma condição financeira identificada: relatório NÃO deve ser gerado, conforme a seção 4.

O código `2` não é falha. É a aplicação da regra de que contribuinte sem dívida encerra silenciosamente, sem PNG e sem distribuição.

## Dependência

A dependência necessária está declarada em `requirements.txt` (`Pillow`).

## Ainda não implementado

- Routine;
- leitura automática da Situação Fiscal (PDF/PNG);
- distribuição automática no Google Drive.

Esses itens serão criados em etapas posteriores, mediante instrução expressa do usuário.

## Proteção dos recursos da Skill

Não alterar, sem instrução expressa do usuário:

- `.claude/skills/procuradoria/scripts/gerar_relatorio_procuradoria.py`;
- `.claude/skills/procuradoria/references/modelo-relatorio-procuradoria.png`;
- `requirements.txt`.
