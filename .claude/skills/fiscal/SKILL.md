---
name: fiscal
description: Processa automaticamente documentos do Departamento Fiscal do Grupo JB. Use quando houver DAS e PGDAS na pasta Departamento Geral/Fiscal para identificar a empresa e competência, consultar a planilha fiscal, gerar o Relatório Fiscal e distribuir os documentos para a pasta correta da empresa no Google Drive. Use também quando houver outros documentos fiscais na mesma pasta (DAE, guias estaduais, guias municipais, documentos de ICMS ou ISS e demais documentos destinados ao cliente) que devam apenas ser identificados, renomeados e distribuídos para a competência correta, sem geração de Relatório Fiscal.
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

# RECURSOS OBRIGATÓRIOS DA SKILL

Esta Skill possui recursos próprios, versionados no repositório.

Eles são obrigatórios e não são opcionais.

## R1. Modelos visuais oficiais

Existem DOIS modelos visuais oficiais do Relatório Fiscal, escolhidos pela natureza da empresa registrada na planilha permanente (seção 7A):

1. COMÉRCIO:

`.claude/skills/fiscal/references/modelo-relatorio-fiscal.pdf`

Esse arquivo define o layout aceito pelo Grupo JB para empresas de comércio: cabeçalho azul com logo JB, razão social e competência por extenso, duas linhas de cards de indicadores, cards de comparação, bloco de notas não lançadas, detalhamento do DAS, gráfico de vendas mensais, comparativo de vendas e rodapé.

2. SERVIÇO:

`.claude/skills/fiscal/references/modelo_relatorio_fiscal_servico.pdf`

Esse arquivo define o layout aceito pelo Grupo JB para empresas de serviço: cabeçalho centralizado com a competência por extenso, identificação da empresa e filete dourado; quatro cards (Receita do mês, Faixa com Anexo, Alíquota efetiva, DAS a pagar com vencimento); bloco FATOR R (condicional, ver seção 7C); comparação da receita (mês anterior e mesmo mês do ano anterior); bloco "Dentro do DAS deste mês"; gráfico de receitas mensais; rodapé com data de geração.

O relatório final deve seguir visualmente o modelo correspondente o mais fielmente possível.

Não redesenhar os relatórios, não trocar a ordem dos blocos e não inventar um layout alternativo.

## R2. Script oficial de geração

O script oficial responsável pela geração do PDF é:

`.claude/skills/fiscal/scripts/gerar_relatorio.py`

Esse script é a única forma autorizada de produzir o Relatório Fiscal quando estiver disponível.

O Claude NÃO deve criar o PDF manualmente (HTML, impressão, desenho ad hoc, outra biblioteca ou geração à mão) quando o script estiver disponível.

Somente se o script estiver comprovadamente indisponível, o Claude deve interromper e informar o problema — nunca improvisar um gerador paralelo.

A dependência necessária está declarada em `requirements.txt` (`reportlab`).

## R3. Construção do JSON antes de executar o script

Antes de executar o script, o Claude deve construir um arquivo JSON contendo SOMENTE dados já extraídos e validados de:

1. PGDAS;
2. DAS;
3. planilha permanente de controle fiscal.

Nenhum outro dado pode entrar nesse arquivo.

Campo sem origem comprovada nesses três documentos deve ficar ausente ou vazio, nunca preenchido por conveniência.

## R4. Papel dos arquivos de exemplo

Os arquivos:

`.claude/skills/fiscal/references/exemplo-dados.json` (COMÉRCIO)

`.claude/skills/fiscal/references/exemplo-dados-servico.json` (SERVIÇO)

são SOMENTE referências de ESTRUTURA dos dados esperados pelo gerador (nomes de chaves, tipos e formato dos blocos), cada um para o seu layout.

Nunca utilizar os valores desses arquivos em um processamento real.

Os valores neles contidos (JB ITABOLOS PANIFICACAO E CONFEITARIA LTDA, competência 05/2026, receita, DAS, tributos, histórico de vendas, notas faltantes; CLINICA ODONTOLOGICA DE BUERAREMA LTDA, competência 07/2026, Fator R, folha e faturamento de 12 meses) são fictícios para efeito de demonstração.

Em processamento real, todos os valores devem vir dos documentos reais (PGDAS e DAS) e da planilha permanente de controle fiscal.

O Claude não pode inventar, estimar ou reutilizar valores do exemplo para preencher campos ausentes.

Se um dado obrigatório não existir nos documentos reais, interromper e informar qual dado está faltando.

## R5. Metodologia de margem

A metodologia de margem atualmente utilizada pelo modelo oficial deve ser preservada:

`Resultado bruto = Vendas - Compras`

`Margem = Resultado bruto / Compras × 100`

Não alterar essa metodologia sem instrução expressa.

Não substituir por margem sobre vendas, margem líquida ou qualquer outra definição.

## R6. Faixa e alíquota efetiva do Simples Nacional

A faixa e a alíquota efetiva do Simples Nacional devem ser obtidas prioritariamente do PGDAS real.

Não inferir faixa tributária a partir do gráfico, do histórico de vendas ou de cálculos próprios se o PGDAS fornecer essa informação.

Somente quando o PGDAS não trouxer o dado é que se pode recorrer a outra fonte documental, informando explicitamente a origem utilizada.

## R7. Execução do gerador

Após produzir o JSON real, executar o gerador no formato:

`python .claude/skills/fiscal/scripts/gerar_relatorio.py dados_relatorio.json relatorio_fiscal.pdf`

O primeiro argumento é o JSON real construído conforme R3.

O segundo argumento é o PDF de saída, que depois deve ser renomeado conforme a regra de nome do relatório.

## R8. Validação pós-geração

Depois da geração, validar obrigatoriamente:

- PDF criado;
- exatamente uma página;
- razão social correta;
- competência correta;
- valores correspondentes aos dados extraídos.

Se qualquer um desses itens falhar, o relatório não pode ser considerado gerado nem distribuído.

## R9. Proteção dos recursos da Skill

Não alterar, sem instrução expressa do usuário:

- `.claude/skills/fiscal/scripts/gerar_relatorio.py`;
- `.claude/skills/fiscal/references/exemplo-dados.json`;
- `.claude/skills/fiscal/references/exemplo-dados-servico.json`;
- `.claude/skills/fiscal/references/modelo-relatorio-fiscal.pdf` (modelo oficial de COMÉRCIO);
- `.claude/skills/fiscal/references/modelo_relatorio_fiscal_servico.pdf` (modelo oficial de SERVIÇO);
- `requirements.txt`.

Todas as demais regras deste SKILL.md permanecem válidas e devem ser aplicadas em conjunto com esta seção.

---

# PROCESSAMENTO EM LOTE

A pasta:

Departamento Geral > Fiscal

é uma FILA ÚNICA e pode conter, ao mesmo tempo, documentos de várias empresas diferentes.

Nunca pressupor que exista apenas um DAS e apenas um PGDAS na pasta.

O processamento fiscal é, por padrão, um processamento em lote.

## L0. REGRA PRINCIPAL — O PGDAS DETERMINA O ESCOPO

A existência de PGDAS é o critério que determina quais empresas devem receber Relatório Fiscal.

Cada PGDAS encontrado na pasta Fiscal inicia um possível processamento.

Empresas que possuem somente DAS, mas não possuem PGDAS na pasta Fiscal:

- NÃO são consideradas pendentes;
- NÃO precisam de Relatório Fiscal.

A ausência de PGDAS significa que aquela empresa não foi selecionada pelo Departamento Fiscal para receber Relatório Fiscal naquela competência.

Portanto, para empresa sem PGDAS:

- não tentar gerar Relatório Fiscal;
- não consultar a planilha permanente;
- não tentar distribuir Relatório Fiscal.

Um DAS sem PGDAS correspondente não representa erro, pendência nem documento faltante.

## L1. Varredura inicial

Ao iniciar, varra TODOS os documentos disponíveis na pasta Fiscal antes de processar qualquer coisa.

Não começar a gerar relatórios enquanto a varredura completa não estiver concluída.

Na varredura, identificar primeiro TODOS os PGDAS existentes — eles definem a lista de empresas a processar no lote.

## L2. Planilha permanente

A planilha permanente de controle fiscal NÃO é um documento de lote.

Ela é uma fonte de consulta compartilhada por todas as empresas e não pertence a nenhum grupo.

Ignorá-la na classificação dos documentos do lote, mantendo todas as regras de proteção já definidas para ela (seção 5).

## L3. Identificação de cada PDF

Para cada PDF fiscal encontrado, identificar, quando possível:

- tipo do documento;
- CNPJ;
- razão social;
- competência.

## L4. Classificação

Classificar os PDFs em:

- DAS;
- PGDAS;
- Relatório Fiscal já existente;
- outros documentos.

## L5. Agrupamento a partir do PGDAS

Agrupar os documentos pela chave:

CNPJ + COMPETÊNCIA

Cada grupo é um processamento INDEPENDENTE.

O grupo nasce de um PGDAS, nunca de um DAS.

Para cada PGDAS encontrado:

1. identificar razão social;
2. identificar CNPJ;
3. identificar competência;
4. procurar o DAS correspondente pelo MESMO CNPJ e MESMA competência.

DAS que não corresponderem a nenhum PGDAS não formam grupo e ficam FORA DO ESCOPO DO RELATÓRIO (ver L6 e L14).

## L6. Elegibilidade do grupo

Para um grupo ser elegível ao processamento automático, deve existir:

- exatamente um PGDAS válido;
- exatamente um DAS válido correspondente;
- cliente correspondente na planilha permanente.

Confirmar obrigatoriamente, dentro de cada grupo:

CNPJ do DAS = CNPJ do PGDAS

e

Competência do DAS = Competência do PGDAS

Resultados possíveis da conferência entre PGDAS e DAS:

- exatamente 1 PGDAS e exatamente 1 DAS
  → grupo apto às demais validações e à geração do relatório;

- PGDAS presente e nenhum DAS correspondente
  → PENDENTE — DAS AUSENTE;

- PGDAS presente e mais de um DAS correspondente
  → PENDENTE — DUPLICIDADE DE DAS;

- mais de um PGDAS para o mesmo CNPJ e competência
  → PENDENTE — DUPLICIDADE DE PGDAS;

- DAS sem PGDAS correspondente
  → FORA DO ESCOPO DO RELATÓRIO — SEM PGDAS (não é pendência).

DAS fora do escopo devem ser ignorados pelo fluxo de Relatório Fiscal: apenas registrados no resumo, sem consulta à planilha, sem geração e sem distribuição de relatório.

## L7. Isolamento de falhas

Se um grupo apresentar erro, inconsistência, duplicidade ou documento ausente:

- não processar esse grupo;
- registrar claramente o motivo;
- continuar o processamento dos demais grupos.

Um erro em uma empresa NUNCA deve interromper todo o lote.

As regras de interrupção definidas nas demais seções aplicam-se ao grupo em questão, não ao lote inteiro.

## L8. Competência esperada

A competência automática esperada normalmente é o mês anterior ao mês de execução.

Exemplo:

execução em agosto/2026
→ competência esperada 07/2026.

Documentos de outras competências devem permanecer separados e não podem ser pareados com a competência atual.

## L9. Duplicidade

Se houver mais de um DAS ou mais de um PGDAS para o mesmo CNPJ e a mesma competência:

- tratar como duplicidade;
- não escolher arbitrariamente;
- não processar esse grupo até que a situação esteja resolvida.

Distinguir os dois casos no resumo:

- mais de um DAS para o PGDAS → PENDENTE — DUPLICIDADE DE DAS;
- mais de um PGDAS para o mesmo CNPJ e competência → PENDENTE — DUPLICIDADE DE PGDAS.

## L10. Relatório já existente

Antes de gerar um novo relatório, verificar se já existe na própria pasta Fiscal um Relatório Fiscal para o mesmo CNPJ e a mesma competência.

Se o relatório já existir:

- não gerar duplicata;
- verificar se DAS, PGDAS e Relatório já foram distribuídos para o destino;
- se o trio estiver corretamente arquivado, marcar o grupo como JÁ PROCESSADO e seguir para o próximo grupo.

## L11. Grupo completo sem relatório

Se DAS + PGDAS estiverem presentes e não houver relatório para aquele CNPJ e competência:

1. consultar a planilha permanente;
2. gerar o JSON real (conforme R3);
3. executar o gerador oficial (conforme R2 e R7);
4. salvar o Relatório Fiscal na própria pasta Fiscal;
5. depois realizar a distribuição definida nesta Skill (seções 14 a 17).

## L12. Nome do relatório no lote

O nome do relatório deve identificar empresa e competência, seguindo a regra da seção 12:

RELATORIO FISCAL - [RAZAO SOCIAL] - [MM-AAAA].pdf

Exemplo:

RELATORIO FISCAL - BEATRIZ DE BRITO CANTOR - 07-2026.pdf

## L13. Permanência dos arquivos

Após gerado, o relatório deve permanecer também na pasta Fiscal enquanto os documentos temporários não forem removidos pelo usuário.

Nunca mover DAS ou PGDAS para fora da pasta Fiscal durante o processamento.

Copiar para o destino e preservar os originais.

## L14. Resumo do lote

Ao final da execução, produzir um resumo do lote, por empresa / CNPJ / competência, com estados semelhantes a:

- PROCESSADO
- JÁ PROCESSADO
- PENDENTE — DAS AUSENTE
- PENDENTE — DUPLICIDADE DE DAS
- PENDENTE — DUPLICIDADE DE PGDAS
- PENDENTE — COMPETÊNCIA DIVERGENTE
- PENDENTE — EMPRESA NÃO LOCALIZADA
- PENDENTE — REVISÃO MANUAL (FATOR R)
- ERRO DE GERAÇÃO
- ERRO DE DISTRIBUIÇÃO
- FORA DO ESCOPO DO RELATÓRIO — SEM PGDAS

Cada linha do resumo deve permitir identificar a empresa, o CNPJ, a competência e o motivo do estado.

FORA DO ESCOPO DO RELATÓRIO — SEM PGDAS não é pendência e não deve ser contabilizado como falha do lote.

Não existe o estado "PENDENTE — PGDAS AUSENTE": a falta de PGDAS é uma decisão do Departamento Fiscal, não uma pendência.

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

# 7A. NATUREZA DA EMPRESA — SERVIÇO OU COMÉRCIO

## Regra principal

A natureza da empresa (SERVIÇO ou COMÉRCIO) deve ser obtida OBRIGATORIAMENTE da planilha permanente de controle fiscal.

NUNCA determinar que uma empresa é de serviço apenas porque não possui compras ou porque o valor de compras está zerado.

A ausência ou o valor zerado de compras nunca pode ser utilizado, sozinho, para determinar se a empresa é serviço ou comércio.

## Ordem obrigatória de consulta

Para cada empresa selecionada pelo PGDAS:

1. Ler o DAS correspondente.

2. Identificar obrigatoriamente no DAS:
   - CNPJ;
   - competência / PA.

3. A competência do DAS é a referência para determinar qual aba mensal da planilha deve ser consultada.

4. Aplicar obrigatoriamente a regra de correspondência de abas já definida na seção 6.

Exemplo:

DAS competência 07/2026
→ consultar a aba AGOSTO.

5. Nunca consultar uma aba mensal diferente daquela correspondente à competência do DAS.

6. Dentro da aba correta, localizar a empresa prioritariamente pelo CNPJ, conforme a seção 5.

7. Após localizar a empresa, ler na própria planilha a informação que determina se a empresa é:
   - SERVIÇO;
   - COMÉRCIO.

8. Essa classificação da planilha é a FONTE DE VERDADE para decidir como tratar compras e margem.

## Empresa de SERVIÇO

Quando a planilha classificar expressamente a empresa como SERVIÇO, os campos baseados em compras são OMITIDOS INTEGRALMENTE do Relatório Fiscal.

Não exibir:

- campo Compras;
- Resultado bruto baseado em compras;
- Margem baseada em compras.

Não exibir, nesses campos, nenhum conteúdo substituto:

- não exibir R$ 0,00;
- não exibir NÃO SE APLICA;
- não exibir traço, vazio ou qualquer texto de preenchimento.

Também não fazer:

- não calcular resultado como Receita - 0;
- não calcular margem;
- não dividir por zero;
- não utilizar qualquer conteúdo existente na coluna COMPRA da planilha para esses campos;
- não inventar valor de compras.

Essas informações simplesmente não existem no relatório de empresa de serviço.

O layout deve se reorganizar automaticamente para não deixar campos vazios nem espaços visualmente incorretos.

A ausência de compras não deve, por si só, classificar o relatório como incompleto.

Todos os demais dados continuam normalmente: razão social, CNPJ, competência, receita, comparações de faturamento, RBT12, faixa, anexo e alíquota quando disponíveis, DAS, vencimento, composição tributária, histórico/gráfico e as demais informações previstas no modelo oficial de serviço (R1).

O layout de SERVIÇO também NÃO exibe os blocos exclusivos do modelo de comércio: Notas não lançadas, Principal/Multa/Juros e Comparativo de Vendas horizontal. Pendências de notas faltantes continuam sendo verificadas na planilha (seção 8) e registradas no resumo do lote — apenas não aparecem no layout do relatório de serviço.

## Empresa de COMÉRCIO

Quando a planilha classificar expressamente a empresa como COMÉRCIO:

- consultar obrigatoriamente o valor de compras da empresa na aba correspondente à competência;
- não aplicar a regra de "serviço sem compras";
- utilizar o valor efetivamente registrado na planilha;
- se o valor registrado for R$ 0,00, preservar R$ 0,00 e não inventar outro valor;
- não calcular margem dividindo por zero;
- qualquer necessidade de validação adicional deve ser registrada sem alterar os dados da planilha.

Exemplo conhecido:

E. GONZAGA EMPREENDIMENTOS LTDA é classificada como COMÉRCIO na planilha e deve seguir as regras de comércio, mesmo que o campo de compras da competência esteja zerado.

## Reflexo no gerador oficial

O gerador oficial (R2) produz dois layouts completos e escolhe entre eles pelo campo `natureza` do JSON construído conforme R3.

O JSON deve conter obrigatoriamente:

`"natureza": "SERVICO"` ou `"natureza": "COMERCIO"`

exatamente conforme a classificação lida na planilha, nunca deduzida da ausência de compras.

Comportamento do gerador:

- natureza SERVIÇO
  → caminho de renderização próprio (`gerar_pdf_servico`), seguindo o modelo oficial de serviço (R1): cabeçalho centralizado com filete dourado, quatro cards, bloco FATOR R condicional (seção 7C), comparação da receita, "Dentro do DAS deste mês", gráfico de receitas mensais e rodapé com data de geração. Sem Compras, sem Resultado bruto, sem Margem, sem Notas não lançadas, sem Principal/Multa/Juros e sem Comparativo de Vendas horizontal;

- natureza COMÉRCIO
  → layout histórico completo e inalterado, com Entradas (Compras), Saídas (Vendas), Resultado bruto e Margem.

Se o campo `natureza` estiver ausente, o gerador assume COMÉRCIO e mantém o layout completo.

Por isso, para empresa de serviço, o campo `natureza` é obrigatório no JSON.

Para empresa de serviço, não incluir o campo `compras` no JSON: o gerador ignora a coluna COMPRA nesse layout, e nenhum valor de compras deve ser transportado para o relatório.

Campos próprios do JSON de serviço (estrutura completa em `exemplo-dados-servico.json`, conforme R4):

- `nome_exibicao` — opcional; sigla/nome de exibição mostrado antes da razão social no cabeçalho. Se ausente, mostrar somente a razão social — nunca criar sigla ou nome fantasia;
- `anexo` — anexo do Simples Nacional exibido no card FAIXA (ex.: "Anexo III"), extraído do PGDAS;
- `fator_r` — objeto do bloco Fator R (seção 7C);
- `municipio_iss` — opcional; município de destino do ISS no bloco "Dentro do DAS deste mês". Se ausente, mostrar o valor do ISS sem inventar município;
- `gerado_em` — data de geração exibida no rodapé (DD/MM/AAAA). Quando presente, o gerador NÃO consulta o relógio.

## Competência como origem da consulta

Toda consulta de dados mensais da planilha deve partir da competência identificada no DAS.

Não usar:

- nome do arquivo;
- mês em que o arquivo foi enviado;
- data de execução da Routine;
- aba escolhida arbitrariamente.

A competência do DAS, combinada com a regra de correspondência de abas da seção 6, determina a aba correta.

## Demais validações

Esta seção não elimina nenhuma outra validação da Skill.

Divergência de receita, CNPJ, competência, matriz/filial, DAS, PGDAS ou qualquer outro dado obrigatório continua devendo ser analisada normalmente.

---

# 7B. COMPOSIÇÃO DA RECEITA — XML, CARTÃO E PIX E OUTRAS RECEITAS

## Origem dos valores

A coluna de vendas/saídas originada dos XMLs representa o faturamento documentado por notas fiscais.

A planilha também possui os valores de vendas recebidas por CARTÃO E PIX.

Quando o total de Cartão e Pix for superior ao faturamento identificado nos XMLs/notas fiscais, a diferença deve ser tratada como OUTRAS RECEITAS.

## Metodologia

Se CARTÃO E PIX > XML:

OUTRAS RECEITAS = CARTÃO E PIX - XML

RECEITA TOTAL APURADA = XML + OUTRAS RECEITAS

Nesse caso, a Receita Total Apurada será igual ao valor de Cartão e Pix.

Se XML >= CARTÃO E PIX:

OUTRAS RECEITAS = R$ 0,00

RECEITA TOTAL APURADA = XML

De forma equivalente:

RECEITA TOTAL APURADA = maior valor entre XML e CARTÃO E PIX.

## Validação com o PGDAS

Não considerar como divergência o simples fato de a receita do PGDAS ser superior à coluna de vendas/saídas dos XMLs.

Antes de registrar divergência:

1. Ler o faturamento proveniente de XML/notas.
2. Ler o valor de Cartão e Pix.
3. Calcular Outras Receitas conforme a metodologia acima.
4. Calcular a Receita Total Apurada.
5. Comparar a Receita Total Apurada com a receita declarada no PGDAS.

Se:

RECEITA TOTAL APURADA = RECEITA PGDAS

considerar a receita VALIDADA.

Somente registrar divergência de faturamento quando a Receita Total Apurada, após considerar Outras Receitas, for diferente da receita declarada no PGDAS.

## Reflexo no Relatório Fiscal

A receita/vendas apresentada como faturamento total no Relatório Fiscal deve corresponder à receita total declarada/apurada da competência.

Quando houver Outras Receitas, elas fazem parte do faturamento total.

A planilha deve ser utilizada para demonstrar e validar a composição:

XML/Notas + Outras Receitas = Receita Total

Não tratar Outras Receitas como erro ou inconsistência.

Não inventar valores de Cartão e Pix nem de Outras Receitas: se o campo não existir na planilha, não estimar — aplicar a regra apenas com os valores efetivamente encontrados.

---

# 7C. FATOR R — METODOLOGIA OFICIAL (EMPRESAS DE SERVIÇO)

O bloco FATOR R do relatório de serviço explica por que a empresa é tributada pelo Anexo III ou pelo Anexo V do Simples Nacional.

## Identificação de empresa sujeita ao Fator R

A Routine deve usar os controles existentes da planilha permanente para identificar as empresas que possuem Fator R.

Não considerar toda empresa de SERVIÇO automaticamente sujeita ao Fator R.

Não deduzir "não se aplica" apenas porque um valor está vazio.

Se houver ambiguidade sobre a aplicabilidade:

- não inventar;
- não inferir pela simples ausência de dados;
- sinalizar REVISÃO MANUAL no resumo do lote e não afirmar enquadramento por Fator R no relatório.

## Fonte da folha de salários

A fonte oficial da folha para o Relatório Fiscal é a PLANILHA PERMANENTE.

A planilha já possui campos mensais de folha destinados ao controle do Fator R.

A Routine NÃO deve reconstruir a folha utilizando recibos, e-mails ou documentos de DP.

## Folha de 12 meses (numerador)

Somar os valores mensais de folha dos 12 meses ANTERIORES ao Período de Apuração analisado, conforme os campos da planilha permanente.

Exemplo:

PA 07/2026
→ janela de referência: 07/2025 a 06/2026.

## Regra operacional de alimentação da folha na planilha

Regra de alimentação da base (não altera o uso no relatório):

- a importação automática desses dados começa a partir de agosto;
- na fonte de importação utilizada, o mês apresentado é um mês à frente;
- portanto, quando a planilha de origem indicar setembro, o dado corresponde a agosto;
- os meses anteriores ao início dessa implantação não devem ser alterados automaticamente;
- alterações nesses meses somente manualmente.

No Relatório Fiscal, usar os valores efetivamente armazenados na planilha permanente para a janela de 12 meses.

## Faturamento de 12 meses (denominador)

Usar o RBT12 oficial extraído do PGDAS para o mesmo PA.

NÃO calcular o denominador pela soma das barras do gráfico.

NÃO substituir o RBT12 do PGDAS pelo histórico visual de receitas.

## Cálculo e regra de enquadramento

fator_r = folha_12m / rbt12

percentual = fator_r × 100

Regra:

- percentual >= 28% → Anexo III;
- percentual < 28% → Anexo V.

Para a comparação com 28%, usar o valor calculado SEM arredondamento visual.

O valor exibido pode ser formatado de forma amigável, mas o arredondamento de apresentação não pode alterar a decisão III/V.

Se o RBT12 for zero, ausente ou inválido:

- não dividir;
- não inventar percentual;
- sinalizar revisão.

## Contrato JSON do bloco Fator R

O JSON de serviço carrega o objeto `fator_r`:

```
"fator_r": {
  "aplicavel": true,
  "folha_12m": ...,
  "faturamento_12m": ...,
  "percentual": ...,
  "anexo_aplicado": "Anexo III"
}
```

- `aplicavel: true` → o bloco é desenhado e exige `folha_12m` e `faturamento_12m` válidos;
- `aplicavel: false` → o bloco NÃO é desenhado;
- objeto ausente → o bloco NÃO é desenhado, mas a ausência do objeto NÃO é prova automática de "não aplicável" na etapa analítica da Routine — a aplicabilidade deve ser verificada na planilha (ver acima).

## Consistência validada pelo gerador

Quando `fator_r.aplicavel = true`, o gerador oficial valida:

- `folha_12m` presente e numérico;
- `faturamento_12m` presente, numérico e maior que zero;
- `rbt12` OBRIGATÓRIO, numérico e maior que zero — rbt12 ausente, nulo, zerado ou inválido gera erro de validação; o relatório nunca é gerado usando apenas `fator_r.faturamento_12m`, pois a origem oficial do denominador é o RBT12 do PGDAS;
- `faturamento_12m` igual ao campo `rbt12`, aceitando apenas diferença técnica de arredondamento monetário de no máximo R$ 0,01 — divergência maior gera erro claro, e o gerador nunca escolhe silenciosamente um dos dois valores;
- `percentual` informado coerente com folha_12m / faturamento_12m;
- `anexo_aplicado` informado coerente com o limite de 28%;
- o campo `anexo` (card FAIXA) coerente com o enquadramento do Fator R: >= 28% deve resultar em Anexo III nos dois campos e < 28% em Anexo V nos dois campos — o PDF nunca pode mostrar um Anexo no card FAIXA e explicar outro no bloco Fator R.

Se houver inconsistência, o gerador gera erro de validação claro e NÃO produz um relatório com enquadramento contraditório.

## Comportamento visual

Empresa de serviço SEM Fator R (não sujeita, ou `aplicavel: false`):

- omitir completamente o bloco;
- não mostrar N/A;
- não mostrar zero;
- não reservar espaço vazio;
- os blocos seguintes sobem automaticamente.

Nunca afirmar enquadramento por Fator R quando a atividade não estiver identificada como sujeita a essa regra.

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

A composição dessa receita (XML/Notas + Outras Receitas) deve ser apurada e validada conforme a seção 7B.

## DAS a pagar

Utilizar o valor efetivamente encontrado no DAS/PGDAS após validação.

## Entradas / Compras

Utilizar o campo correspondente a COMPRA da planilha.

Antes de tratar compras, aplicar a seção 7A para determinar, pela planilha, se a empresa é SERVIÇO ou COMÉRCIO.

## Saídas / Vendas

Utilizar a receita validada para a competência.

Entende-se por receita validada a Receita Total Apurada definida na seção 7B, já incluídas as Outras Receitas quando existirem.

## Resultado bruto

Resultado bruto = Vendas - Compras

## Margem

Seguir a metodologia definida no modelo oficial do Relatório Fiscal.

Não substituir a fórmula do modelo por outra definição de margem sem autorização.

Nunca dividir por zero: se as compras forem inexistentes ou iguais a zero, tratar conforme a seção 7A, de acordo com a natureza registrada na planilha.

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

Quando a planilha classificar a empresa como SERVIÇO, os campos de compras, resultado baseado em compras e margem baseada em compras são OMITIDOS do relatório, conforme a seção 7A — não aparecem com valor zerado, com NÃO SE APLICA nem com qualquer outro texto de preenchimento.

Empresa de SERVIÇO segue o modelo oficial de serviço (R1), com os blocos descritos nas seções 7A e 7C — incluindo o bloco FATOR R quando aplicável e o bloco "Dentro do DAS deste mês" no lugar do detalhamento do DAS do comércio.

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

---

# 21. DOCUMENTOS FISCAIS DE DISTRIBUIÇÃO

A pasta:

Departamento Geral > Fiscal

poderá receber vários tipos de documentos, e não apenas DAS e PGDAS.

Exemplos:

- PGDAS;
- DAS;
- DAE;
- guias estaduais;
- guias municipais;
- documentos de ICMS;
- documentos de ISS;
- outros documentos fiscais destinados ao cliente.

A lista NÃO é fechada.

Novos tipos de documento fiscal podem aparecer e devem ser tratados normalmente.

## 21.1. Identificação do tipo

A Routine deve identificar o tipo do documento pelo CONTEÚDO do documento.

O nome original do arquivo é apenas apoio, nunca a fonte principal da classificação.

Não inventar tipo de documento.

Se o tipo não puder ser determinado com segurança pelo conteúdo, não classificar por suposição: registrar o documento como não identificado e seguir para os demais.

---

# 22. DUAS MODALIDADES DE PROCESSAMENTO

Existem dois comportamentos distintos na pasta Fiscal.

## 22.1. Modalidade 1 — DOCUMENTO SOMENTE PARA DISTRIBUIÇÃO

Quando um documento fiscal NÃO for PGDAS e não exigir processamento analítico pela metodologia existente, ele segue apenas o fluxo de distribuição:

1. identificar com segurança o contribuinte;
2. identificar o CNPJ;
3. identificar a competência;
4. identificar o tipo do documento;
5. localizar a pasta de destino da empresa;
6. renomear conforme o padrão fiscal adotado;
7. distribuir o documento para a competência correta.

Exemplos:

- DAE;
- guia estadual;
- guia municipal;
- outros documentos fiscais.

Esses documentos, isoladamente, NÃO geram Relatório Fiscal.

NÃO exigir a existência de PGDAS para distribuir esses documentos.

Se o documento estiver corretamente identificado, pode ser distribuído independentemente.

Nessa modalidade:

- não consultar a planilha permanente para efeito de relatório;
- não executar o gerador oficial;
- não produzir Relatório Fiscal.

## 22.2. Modalidade 2 — PROCESSAMENTO COM RELATÓRIO FISCAL

O PGDAS é o documento que aciona o processamento analítico e a geração do Relatório Fiscal.

Quando houver PGDAS:

- aplicar integralmente a metodologia Fiscal já existente neste SKILL.md;
- identificar contribuinte e competência;
- associar o DAS correspondente quando houver;
- associar outros documentos fiscais da mesma empresa e da mesma competência quando forem pertinentes;
- consultar a planilha permanente e a competência correta conforme as regras existentes (seções 5, 6 e 7);
- aplicar as regras de receitas (seção 7B), classificação SERVIÇO/COMÉRCIO (seção 7A) e demais regras já existentes;
- gerar o Relatório Fiscal pelo gerador oficial (R2 e R7);
- distribuir os documentos correspondentes e o relatório conforme a metodologia atual (seções 13 a 19).

A presença de DAE, guia estadual, guia municipal ou qualquer outro documento NÃO substitui o PGDAS como gatilho do Relatório Fiscal.

As regras das seções 3, 19 e L6 (documentos obrigatórios, validação final e elegibilidade do grupo) aplicam-se à Modalidade 2 — o fluxo que gera Relatório Fiscal — e não bloqueiam a distribuição prevista na Modalidade 1.

---

# 23. ASSOCIAÇÃO DOS DOCUMENTOS

Sempre associar documentos por:

1. CNPJ;
2. competência;
3. identificação do contribuinte.

NUNCA associar documentos apenas pela proximidade na pasta ou pela semelhança do nome do arquivo.

Documentos de empresas diferentes ou de competências diferentes NUNCA devem ser agrupados no mesmo processamento.

Essa regra complementa e reforça o agrupamento CNPJ + COMPETÊNCIA já definido em L5.

---

# 24. EXEMPLOS DE COMPORTAMENTO

## Exemplo A

Empresa X
DAE 07/2026

Resultado:

- distribuir o DAE;
- não gerar Relatório Fiscal.

## Exemplo B

Empresa X
DAS 07/2026
DAE 07/2026

Resultado:

- distribuir os documentos identificados;
- não gerar Relatório Fiscal apenas por causa desses documentos.

## Exemplo C

Empresa X
PGDAS 07/2026
DAS 07/2026
DAE 07/2026

Resultado:

- executar toda a metodologia Fiscal;
- gerar o Relatório Fiscal de 07/2026;
- distribuir PGDAS, DAS, DAE e o relatório para a competência correta, conforme aplicável.

## Exemplo D

Empresa X possui PGDAS 07/2026.
Empresa Y possui apenas DAE 07/2026.

Resultado:

- Empresa X: gerar Relatório Fiscal e distribuir documentos;
- Empresa Y: apenas distribuir o DAE;
- nunca misturar os documentos das duas empresas.

---

# 25. SEGURANÇA NA DISTRIBUIÇÃO

- Um documento de distribuição NÃO deve disparar relatório sem PGDAS.
- Não inventar competência.
- Não inventar tipo de documento.
- Não distribuir quando não houver identificação segura do cliente.
- Não sobrescrever documentos existentes silenciosamente.
- Uma falha em um documento não deve impedir o processamento seguro dos demais.
- Manter todas as regras atuais de duplicidade, armazenamento e distribuição desta Skill (seções 13 a 20 e L7, L9, L13).

---

# 26. PRINCÍPIO

PGDAS = gatilho para a análise e para o Relatório Fiscal.

DAS, DAE e outros documentos fiscais = documentos que podem ser distribuídos normalmente, mas não geram relatório por si só.

Nenhuma regra já existente sobre cálculo, receitas, planilha permanente, geração do relatório ou destino dos arquivos é alterada por estas seções.

---

# METODOLOGIA OFICIAL DA PASTA PROCESSADOS

As seções P1 a P13 acrescentam a metodologia oficial de arquivamento operacional PROCESSADOS ao Departamento Fiscal.

Elas definem o ciclo de vida dos documentos ORIGINAIS da fila Fiscal APÓS a conclusão e validação do processamento previsto nesta Skill.

Elas NÃO alteram nenhuma regra fiscal existente (ver P13).

## P1. FILA OPERACIONAL

A pasta de entrada é:

++++++CONTABILIDADE+++
> Departamento Geral
> Fiscal

Dentro dela poderá existir a subpasta:

PROCESSADOS

A Routine deve considerar como fila pendente SOMENTE os arquivos localizados diretamente na raiz da pasta Fiscal.

Nunca tratar documentos dentro de:

Fiscal > PROCESSADOS

como documentos pendentes.

Nunca reprocessar arquivos arquivados em PROCESSADOS.

A planilha permanente de controle fiscal NÃO é documento de fila (L2): ela permanece sempre na raiz da pasta Fiscal e NUNCA deve ser movida para PROCESSADOS, mantendo integralmente as proteções da seção 5.

## P2. ESTRUTURA DE PROCESSADOS

Dentro de PROCESSADOS, organizar por competência:

PROCESSADOS
> MM AAAA

Exemplos:

PROCESSADOS
> 07 2026

PROCESSADOS
> 08 2026

PROCESSADOS
> 09 2026

A Routine está autorizada a criar:

- a pasta PROCESSADOS, quando inexistente;
- a pasta MM AAAA necessária.

Não criar uma pasta intermediária por ano dentro de PROCESSADOS.

A competência usada para nomear a pasta MM AAAA é a competência identificada no próprio documento, conforme as regras já existentes de identificação de competência.

## P3. PRINCÍPIO DE SEGURANÇA

PROCESSADOS é arquivo operacional, não lixeira.

Nunca excluir automaticamente documentos da fila Fiscal ou de PROCESSADOS.

Nunca mover um documento original para PROCESSADOS antes de concluir e validar todas as operações que dependem dele.

O arquivo ORIGINAL não precisa ser renomeado quando for arquivado em PROCESSADOS.

Somente a cópia destinada ao cliente recebe o nome final padronizado definido por esta Skill.

Conciliação com as regras existentes:

- PROCESSADOS é uma subpasta da própria pasta Fiscal; arquivar um original ali NÃO é excluí-lo nem movê-lo para fora da pasta Fiscal, portanto não viola a seção 20 nem a regra L13;
- a proibição de L13 ("nunca mover DAS ou PGDAS para fora da pasta Fiscal durante o processamento") continua valendo integralmente: a movimentação para PROCESSADOS só ocorre DEPOIS que o processamento daquele documento estiver concluído e validado, e sempre dentro da própria pasta Fiscal;
- a distribuição continua sendo feita por CÓPIA para o destino (seções 13 a 17); o que a metodologia PROCESSADOS acrescenta é apenas o arquivamento do ORIGINAL após a validação.

## P4. DOCUMENTOS DE DISTRIBUIÇÃO SIMPLES

Para documentos que não geram relatório analítico por si mesmos (Modalidade 1, seção 22.1), como:

- DAE;
- guias estaduais;
- guias municipais;
- ICMS;
- ISS;
- outros documentos fiscais de distribuição simples;

o fluxo é:

1. identificar contribuinte;
2. identificar competência;
3. identificar tipo;
4. determinar nome final;
5. localizar destino;
6. verificar duplicidade;
7. criar a cópia no destino correto;
8. validar a cópia (P8);
9. somente depois mover o ORIGINAL para:
   Fiscal > PROCESSADOS > MM AAAA.

Se a distribuição falhar ou houver dúvida:

- manter o original na raiz da pasta Fiscal;
- classificar como FALHA ou REVISÃO MANUAL (P9).

## P5. PGDAS E PROCESSAMENTO ANALÍTICO

PGDAS continua sendo o gatilho do processamento fiscal analítico conforme a metodologia atual desta Skill (L0 e seção 22.2).

Quando houver PGDAS:

NÃO mover o PGDAS para PROCESSADOS imediatamente após sua leitura.

Antes de arquivar o PGDAS, concluir todas as etapas aplicáveis ao contribuinte e à competência, incluindo:

- identificação do contribuinte;
- identificação da competência;
- associação segura dos documentos relacionados (seção 23);
- leitura/apuração conforme a metodologia atual;
- atualização da planilha permanente, quando aplicável;
- geração do relatório fiscal, quando aplicável (R2, R7 e R8);
- validação do relatório gerado;
- distribuição dos documentos fiscais;
- distribuição do relatório;
- validação das cópias criadas (P8).

Somente depois que o processamento analítico daquele contribuinte/competência estiver concluído e validado (incluindo a validação final da seção 19) poderá o PGDAS original ser movido para:

Fiscal > PROCESSADOS > MM AAAA.

## P6. DOCUMENTOS ASSOCIADOS AO PGDAS

DAS, DAE e outros documentos associados ao mesmo contribuinte e competência devem respeitar sua participação no processamento.

Quando o documento fizer parte do conjunto necessário ao processamento analítico:

- não arquivá-lo antecipadamente;
- mantê-lo disponível na raiz da pasta Fiscal até concluir o processamento daquele contribuinte/competência;
- depois da validação completa, mover o original para PROCESSADOS > MM AAAA.

Cada documento deve ser tratado individualmente no resultado final (P12).

## P7. JÁ EXISTENTE

Quando o nome final padronizado já existir no destino:

- não sobrescrever;
- não criar "(1)";
- não criar "cópia";
- não gerar variante automática.

Antes de retirar o original da fila, confirmar que o arquivo existente no destino corresponde ao documento da fila.

Usar, conforme disponibilidade:

- mesmo contribuinte/CNPJ/CPF;
- mesma competência;
- mesmo tipo;
- mesmo tamanho em bytes;
- demais identificadores confiáveis disponíveis.

Se houver confirmação suficiente:

classificar como:

JÁ EXISTENTE CONFIRMADO

e mover o original para:

Fiscal > PROCESSADOS > MM AAAA

Se houver divergência ou dúvida:

classificar como:

REVISÃO MANUAL

e manter o original na raiz de Fiscal.

Nunca assumir igualdade apenas porque o nome é igual.

Esta regra complementa — e não substitui — as proteções contra duplicidade já existentes (seções 18 e 25 e regras L9 e L10).

## P8. VALIDAÇÃO DA CÓPIA

Quando uma nova cópia for criada no destino:

- confirmar que a cópia existe;
- confirmar o nome final;
- comparar o tamanho em bytes da origem e da cópia, quando a operação disponibilizar essa informação.

Se houver divergência:

- classificar como FALHA;
- não arquivar o original;
- manter o original na fila Fiscal.

## P9. FALHA E REVISÃO MANUAL

Documentos classificados como:

- FALHA
- REVISÃO MANUAL

permanecem diretamente na raiz de:

Departamento Geral > Fiscal

Não mover para PROCESSADOS.

Uma falha em um documento ou contribuinte não deve impedir o processamento seguro dos demais (mesmo princípio de isolamento de falhas de L7 e da seção 25).

## P10. PROCESSAMENTO POR CONTRIBUINTE/COMPETÊNCIA

Quando vários documentos estiverem relacionados ao mesmo contribuinte e competência, tratar esse conjunto como uma unidade lógica para as etapas analíticas (agrupamento CNPJ + COMPETÊNCIA de L5 e seção 23).

Porém, registrar individualmente o resultado de cada arquivo.

Não arquivar antecipadamente um documento que ainda possa ser necessário para concluir outra etapa segura daquele mesmo processamento.

## P11. EXECUÇÕES FUTURAS

Em novas execuções:

- ignorar integralmente a pasta PROCESSADOS;
- contar como pendentes somente os arquivos diretamente na raiz de Fiscal.

Se não houver arquivos pendentes na raiz:

encerrar informando:

"FISCAL: nenhuma pendência encontrada."

Não pesquisar dentro de PROCESSADOS para procurar trabalho novo.

## P12. RESULTADO DO LOTE

Para cada arquivo da fila informar:

- arquivo original;
- contribuinte;
- competência;
- tipo;
- nome final de distribuição;
- destino;
- situação;
- arquivado em PROCESSADOS: SIM/NÃO;
- pasta de PROCESSADOS (MM AAAA), quando aplicável.

Situações possíveis:

- DISTRIBUÍDO
- PROCESSAMENTO ANALÍTICO CONCLUÍDO
- JÁ EXISTENTE CONFIRMADO
- REVISÃO MANUAL
- FALHA

Ao final informar:

- arquivos encontrados na fila;
- contribuintes/competências processados;
- relatórios gerados;
- documentos distribuídos;
- já existentes confirmados;
- enviados para PROCESSADOS;
- revisão manual;
- falhas;
- documentos que permaneceram pendentes na raiz Fiscal.

Este resultado por arquivo complementa o resumo do lote por empresa/CNPJ/competência já definido em L14 — os estados de L14 continuam sendo usados para o processamento analítico; as situações acima registram o ciclo de vida de cada arquivo na fila e seu arquivamento em PROCESSADOS.

## P13. NÃO ALTERAR A METODOLOGIA FISCAL

As seções P1 a P12 apenas acrescentam a metodologia PROCESSADOS.

Elas não mudam:

- cálculo fiscal;
- relatório;
- PGDAS;
- DAS;
- DAE;
- classificação serviço/comércio (seção 7A);
- Fator R (seção 7C);
- planilha permanente (seções 5, 6 e 7);
- fontes de dados;
- modelos de relatório (R1);
- nomes de arquivos finais (seção 12 e L12);
- destinos já definidos (seções 13 a 17).

Em caso de aparente conflito, prevalece a leitura conciliada de P3: a metodologia fiscal existente rege TODO o processamento; a metodologia PROCESSADOS rege apenas o arquivamento do ORIGINAL dentro da própria pasta Fiscal, depois que o processamento estiver concluído e validado.
