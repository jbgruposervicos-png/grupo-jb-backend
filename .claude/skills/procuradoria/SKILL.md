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

Somente gerar Relatório de Procuradoria quando houver débito, pendência financeira ou obrigação em exigibilidade relevante identificada.

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
- duplicar dívida no total;
- escolher destino incerto;
- alterar documentos originais;
- bloquear todo o lote por um erro isolado.

---

# 24. IMPLEMENTAÇÃO

Nesta etapa, existe apenas a estrutura da Skill e este SKILL.md.

Ainda NÃO existem:

- `gerar_relatorio_procuradoria.py`;
- Routine;
- alteração em `requirements.txt`.

Enquanto o gerador oficial não existir, não improvisar um gerador paralelo nem produzir o PNG à mão: registrar que a etapa de geração ainda não está implementada.

Esses itens serão criados em etapas posteriores, mediante instrução expressa do usuário.
