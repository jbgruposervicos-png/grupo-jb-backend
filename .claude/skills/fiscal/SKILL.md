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

# RECURSOS OBRIGATÓRIOS DA SKILL

Esta Skill possui recursos próprios, versionados no repositório.

Eles são obrigatórios e não são opcionais.

## R1. Modelo visual oficial

O modelo visual oficial do Relatório Fiscal é:

`.claude/skills/fiscal/references/modelo-relatorio-fiscal.pdf`

Esse arquivo define o layout aceito pelo Grupo JB: cabeçalho azul com logo JB, razão social e competência por extenso, duas linhas de cards de indicadores, cards de comparação, bloco de notas não lançadas, detalhamento do DAS, gráfico de vendas mensais, comparativo de vendas e rodapé.

O relatório final deve seguir visualmente esse modelo o mais fielmente possível.

Não redesenhar o relatório, não trocar a ordem dos blocos e não inventar um layout alternativo.

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

## R4. Papel do arquivo de exemplo

O arquivo:

`.claude/skills/fiscal/references/exemplo-dados.json`

é SOMENTE uma referência de ESTRUTURA dos dados esperados pelo gerador (nomes de chaves, tipos e formato dos blocos).

Nunca utilizar os valores desse arquivo em um processamento real.

Os valores nele contidos (JB ITABOLOS PANIFICACAO E CONFEITARIA LTDA, competência 05/2026, receita, DAS, tributos, histórico de vendas, notas faltantes) são fictícios para efeito de demonstração.

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
- `.claude/skills/fiscal/references/modelo-relatorio-fiscal.pdf`;
- `requirements.txt`.

Todas as demais regras deste SKILL.md permanecem válidas e devem ser aplicadas em conjunto com esta seção.

---

# PROCESSAMENTO EM LOTE

A pasta:

Departamento Geral > Fiscal

é uma FILA ÚNICA e pode conter, ao mesmo tempo, documentos de várias empresas diferentes.

Nunca pressupor que exista apenas um DAS e apenas um PGDAS na pasta.

O processamento fiscal é, por padrão, um processamento em lote.

## L1. Varredura inicial

Ao iniciar, varra TODOS os documentos disponíveis na pasta Fiscal antes de processar qualquer coisa.

Não começar a gerar relatórios enquanto a varredura completa não estiver concluída.

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

## L5. Agrupamento

Agrupar os documentos pela chave:

CNPJ + COMPETÊNCIA

Cada grupo é um processamento INDEPENDENTE.

## L6. Elegibilidade do grupo

Para um grupo ser elegível ao processamento automático, deve existir:

- exatamente um PGDAS válido;
- exatamente um DAS válido;
- cliente correspondente na planilha permanente.

Confirmar obrigatoriamente, dentro de cada grupo:

CNPJ do DAS = CNPJ do PGDAS

e

Competência do DAS = Competência do PGDAS

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
- PENDENTE — PGDAS AUSENTE
- PENDENTE — DUPLICIDADE
- PENDENTE — COMPETÊNCIA DIVERGENTE
- PENDENTE — EMPRESA NÃO LOCALIZADA
- ERRO DE GERAÇÃO
- ERRO DE DISTRIBUIÇÃO

Cada linha do resumo deve permitir identificar a empresa, o CNPJ, a competência e o motivo do estado.

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
