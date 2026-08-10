---
name: fiscal
description: Processa automaticamente documentos do Departamento Fiscal do Grupo JB. Use quando houver DAS e PGDAS na pasta Departamento Geral/Fiscal para identificar a empresa e competência, consultar a planilha fiscal, gerar o Relatório Fiscal e distribuir os documentos para a pasta correta da empresa no Google Drive.
---

# PROCESSAMENTO FISCAL — GRUPO JB

## 1. OBJETIVO

Executar o processamento fiscal a partir dos documentos existentes em:

Departamento Geral > Fiscal

A pasta Fiscal funciona como uma área temporária de processamento.

Dentro dela existirão normalmente:

- uma planilha permanente de controle fiscal;
- um arquivo PGDAS;
- um arquivo DAS;
- eventualmente um Relatório Fiscal já produzido.

A planilha é permanente.

DAS, PGDAS e Relatório Fiscal são documentos relacionados ao processamento de uma determinada empresa e competência.

---

# 2. REGRA DE COMPETÊNCIA

O Departamento Fiscal trabalha sempre com a competência anterior ao mês de processamento.

Exemplos:

- processamento em agosto/2026 → competência 07/2026;
- processamento em setembro/2026 → competência 08/2026;
- processamento em janeiro/2027 → competência 12/2026.

Não determine a competência apenas pela data atual.

A competência encontrada no PGDAS é a referência principal.

O DAS deve possuir competência compatível com o PGDAS.

Se DAS e PGDAS apresentarem competências diferentes, interrompa o processamento.

---

# 3. DOCUMENTOS OBRIGATÓRIOS

Para iniciar um processamento, devem existir:

1. PGDAS;
2. DAS;
3. planilha permanente de controle fiscal.

A ausência de qualquer um desses elementos impede a geração do relatório definitivo.

Nunca invente dados ausentes.

---

# 4. IDENTIFICAÇÃO DA EMPRESA

Leia primeiro o PGDAS.

Extraia obrigatoriamente:

- razão social;
- CNPJ;
- período de apuração / competência;
- receita declarada;
- RBT12 quando disponível;
- alíquota efetiva;
- valor total do Simples Nacional;
- composição tributária disponível.

Depois leia o DAS.

Extraia:

- CNPJ;
- período de apuração;
- valor;
- vencimento;
- principal;
- multa;
- juros, quando existentes.

Antes de prosseguir confirme:

CNPJ PGDAS = CNPJ DAS

e

Competência PGDAS = Competência DAS

Se não forem iguais, interrompa.

---

# 5. PLANILHA FISCAL PERMANENTE

A planilha localizada dentro da pasta Fiscal é uma fonte permanente de dados.

Nunca excluir, mover, renomear ou sobrescrever essa planilha.

Por padrão, utilizar a planilha somente para leitura.

## Identificação do cliente na planilha

Utilize o CNPJ como chave principal.

Ignore pontos, barras, traços e diferenças de formatação do CNPJ.

O nome do cliente é uma validação secundária.

Não associe empresas somente porque os nomes são parecidos.

---

# 6. REGRA DAS ABAS MENSAIS

As abas mensais da planilha representam o mês em que o Departamento Fiscal está executando o trabalho.

A competência correspondente é o mês anterior.

Exemplo:

ABA AGOSTO
→ dados utilizados para a competência JULHO.

ABA JULHO
→ dados utilizados para a competência JUNHO.

ABA JANEIRO
→ dados utilizados para a competência DEZEMBRO do ano anterior.

Utilize essa regra para localizar os dados complementares da competência.

---

# 7. DADOS DA PLANILHA

Depois de localizar o cliente correto pelo CNPJ, procure os campos pelo NOME DO CABEÇALHO e não por posição fixa de coluna.

A estrutura da planilha pode mudar entre as abas.

Quando disponíveis, utilizar:

- EMPREGADOR / CLIENTE;
- CNPJ DA EMPRESA;
- VALOR SAÍDA;
- COMPRA;
- demais campos necessários ao relatório.

Não assumir que uma determinada informação estará sempre na mesma letra de coluna.

Para o relatório fiscal:

VALOR SAÍDA
→ vendas/receita utilizada nos comparativos, quando aplicável.

COMPRA
→ entradas/compras utilizadas no relatório.

Se houver dúvida sobre qual campo corresponde a uma informação, não escolher outro campo arbitrariamente.

---

# 8. NOTAS FALTANTES

Consultar também a aba:

NOTAS FALTANTES

Localizar o cliente pelo CNPJ.

Se houver informações em:

NOTAS FALTANTES

ou

NOTAS INUTILIZADAS

utilizá-las no bloco correspondente do Relatório Fiscal.

Se os campos estiverem vazios, não inventar nenhuma pendência.

---

# 9. CÁLCULOS DO RELATÓRIO

Utilizar os dados efetivamente encontrados nos documentos e na planilha.

## Receita do mês

Priorizar a receita declarada no PGDAS.

## DAS a pagar

Utilizar o valor efetivamente encontrado no DAS/PGDAS após validação.

## Entradas / Compras

Utilizar o campo correspondente a COMPRA da planilha.

## Saídas / Vendas

Utilizar a receita validada para a competência.

## Resultado bruto

Resultado bruto = Vendas - Compras

## Margem

Seguir a metodologia definida no modelo oficial do Relatório Fiscal.

Não substituir a fórmula do modelo por outra definição de margem sem autorização.

## Comparação com mês anterior

Comparar a receita da competência atual com a competência imediatamente anterior.

## Comparação anual

Comparar com o mesmo mês do ano anterior quando houver histórico disponível.

Nunca inventar histórico ausente.

---

# 10. SITUAÇÃO DO DAS

A simples existência de uma guia DAS não prova que ela esteja em aberto.

Não escrever "DAS não pago" sem evidência suficiente.

Se somente a guia estiver disponível, informar:

"DAS com vencimento em DD/MM/AAAA"

Se existir fonte confiável comprovando inadimplência:

"DAS não pago"

Se existir comprovação de pagamento:

"DAS pago"

---

# 11. GERAÇÃO DO RELATÓRIO FISCAL

Gerar o Relatório Fiscal seguindo o modelo oficial do Grupo JB.

O relatório deve conter, conforme disponibilidade dos dados:

- razão social;
- competência;
- receita do mês;
- faixa;
- alíquota efetiva;
- DAS a pagar;
- vencimento;
- entradas/compras;
- saídas/vendas;
- resultado bruto;
- margem;
- comparação com o mês anterior;
- comparação com o mesmo mês do ano anterior;
- notas faltantes;
- notas inutilizadas, quando aplicável;
- detalhamento do DAS;
- gráfico de vendas;
- comparativos;
- alertas relevantes.

Nunca preencher um campo com dado estimado apenas para completar o layout.

---

# 12. NOME DO RELATÓRIO

Utilizar:

RELATORIO FISCAL - [RAZAO SOCIAL] - [MM-AAAA].pdf

Exemplo:

RELATORIO FISCAL - BEATRIZ DE BRITO CANTOR - 07-2026.pdf

---

# 13. PRIMEIRO DESTINO DO RELATÓRIO

Após gerar o PDF, salvar inicialmente uma cópia dentro de:

Departamento Geral > Fiscal

Não remover DAS ou PGDAS da pasta de entrada.

---

# 14. LOCALIZAÇÃO DA EMPRESA

Depois de gerar o relatório, acessar a raiz de empresas do Google Drive.

Localizar a pasta correspondente à empresa identificada no PGDAS.

Utilizar:

1. CNPJ, quando houver informação que permita validação;
2. razão social;
3. nomes complementares existentes na pasta.

A pasta poderá possuir mais informações além da razão social.

Exemplo:

BEATRIZ DE BRITO CANTOR SERVICOS DE ENGENHARIA & PROJETOS - BEATRIZ DE BRITO CANTOR ENGENHARIA - BEATRIZ DE BRITO CANTOR

Isso pode corresponder à razão social encontrada nos documentos.

Não exigir correspondência textual de 100% quando a identidade da empresa for inequivocamente comprovada.

Por outro lado, nunca selecionar uma pasta com base somente em uma aproximação fraca.

Se houver duas ou mais empresas possíveis e não for possível determinar com segurança qual é a correta:

INTERROMPER.

---

# 15. ESTRUTURA DA EMPRESA

Depois de identificar com segurança a pasta da empresa, entrar obrigatoriamente em:

DEPARTAMENTO FISCAL

Depois localizar o ano da competência.

Exemplo:

competência 07/2026
→ 2026

Não criar a pasta da empresa.

Não criar DEPARTAMENTO FISCAL.

Se essas estruturas não existirem, interromper o processamento.

---

# 16. PASTA DA COMPETÊNCIA

Dentro do ano, localizar uma pasta no padrão:

MM AAAA

Exemplo:

07 2026

Se a pasta da competência já existir:

utilizá-la.

Se não existir:

está autorizado a criar somente a pasta da competência.

O nome deve seguir exatamente:

MM AAAA

---

# 17. DISTRIBUIÇÃO

Copiar para a pasta definitiva da competência:

1. DAS;
2. PGDAS;
3. Relatório Fiscal produzido.

O objetivo é terminar com uma estrutura semelhante a:

EMPRESA
└── DEPARTAMENTO FISCAL
    └── 2026
        └── 07 2026
            ├── DAS
            ├── PGDAS
            └── RELATORIO FISCAL

Não apagar os arquivos existentes na pasta de origem.

---

# 18. PROTEÇÃO CONTRA DUPLICIDADE

Antes de copiar ou gerar novamente, verifique se já existe relatório para:

- mesmo CNPJ;
- mesma competência.

Se existir arquivo aparentemente referente ao mesmo processamento, valide antes de criar duplicata.

Não sobrescrever silenciosamente documentos existentes.

---

# 19. VALIDAÇÃO FINAL

O processo somente pode ser considerado concluído quando todos os itens abaixo forem verdadeiros:

- PGDAS foi localizado;
- DAS foi localizado;
- planilha foi localizada;
- razão social foi identificada;
- CNPJ foi identificado;
- CNPJ do DAS corresponde ao PGDAS;
- competência foi identificada;
- competência do DAS corresponde ao PGDAS;
- cliente foi encontrado corretamente na planilha;
- dados necessários foram extraídos;
- Relatório Fiscal foi criado;
- Relatório Fiscal existe na pasta Fiscal;
- empresa de destino foi identificada com segurança;
- DEPARTAMENTO FISCAL foi localizado;
- ano foi localizado;
- competência foi localizada ou criada;
- DAS foi copiado ao destino;
- PGDAS foi copiado ao destino;
- Relatório Fiscal foi copiado ao destino;
- os três documentos foram confirmados na pasta destino.

Se algum item falhar:

não declarar o processo concluído.

---

# 20. REGRA DE SEGURANÇA

Nunca:

- excluir arquivo original;
- apagar a planilha fiscal;
- criar empresa nova;
- escolher cliente incerto;
- alterar documentos originais;
- inventar números;
- inventar notas faltantes;
- inventar situação de pagamento;
- substituir arquivos existentes sem validação;
- continuar quando CNPJ ou competência forem incompatíveis.

Quando houver dúvida material, interrompa e informe exatamente qual validação falhou.
