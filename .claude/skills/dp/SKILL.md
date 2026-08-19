---
name: dp
description: Organiza automaticamente os documentos do Departamento Pessoal do Grupo JB. Use quando houver documentos trabalhistas (recibos de pagamento, extratos, INSS, FGTS, férias, rescisões e outros) na pasta Departamento Geral/DP para identificar o cliente/empregador, a competência e o tipo do documento, renomear o PDF e distribuí-lo para a pasta correta do cliente no Google Drive (EMPRESAS, FAZENDAS ou EMPREGADA DOMESTICA), sem alterar o conteúdo dos arquivos.
---

# DEPARTAMENTO PESSOAL — GRUPO JB

## 1. OBJETIVO

A Skill do DP é exclusivamente para:

- identificar documentos trabalhistas colocados na pasta de entrada;
- identificar com segurança o cliente/empregador;
- identificar a competência;
- identificar o tipo do documento;
- renomear o PDF original;
- distribuir o PDF para a pasta correta do cliente.

Esta Skill NÃO deve:

- calcular folha;
- recalcular tributos;
- alterar o conteúdo dos PDFs;
- gerar novos PDFs;
- interpretar valores para fins de auditoria;
- excluir documentos de origem automaticamente.

---

## 2. PASTA DE ENTRADA

Google Drive:

++++++CONTABILIDADE+++
> Departamento Geral
> DP

Todos os documentos do lote serão lidos a partir dessa pasta.

---

## 3. DESTINOS POSSÍVEIS

O cliente deve ser localizado em uma destas três estruturas:

1. **EMPRESAS**
   - Nome: `+++++++++++++++EMPRESAS+++++`
   - ID: `1pX9jZWXniIY2NLKm-LvWBM7MDC8164WA`

2. **FAZENDAS**
   - Nome: `+++++++++++FAZENDAS+++++`
   - ID: `12tWjSAV1ucvr1ndUJJYxJNEcNx24dGO7`

3. **EMPREGADA DOMESTICA**
   - Nome: `++++++++EMPREGADA DOMESTICA++++`
   - ID: `1A0gzXFkp8UbxTY0XN5Gg1IiMwWivlp9y`

O **ID estável** é a referência preferencial para localizar a raiz correta no Google Drive.

O nome da pasta serve como conferência.

Não usar caminhos locais `G:\` como endereço operacional dentro da Routine.

Classificação geral:

- pessoa jurídica / empresa -> EMPRESAS;
- produtor rural / fazenda / empregador rural cadastrado nessa estrutura -> FAZENDAS;
- empregador doméstico -> EMPREGADA DOMESTICA.

Nunca escolher uma estrutura somente pelo nome do arquivo.

Confirmar o cliente pelo conteúdo do documento e pela pasta existente no Drive.

---

## 4. IDENTIFICAÇÃO DO CLIENTE

Usar como chave principal, sempre que disponível:

- CNPJ; ou
- CPF.

O nome é elemento de confirmação.

Após localizar com segurança o cliente no Drive, determinar o nome do cliente a ser usado no nome final do arquivo conforme a seção 9.1 (NOME OPERACIONAL DO CLIENTE NO ARQUIVO).

Não distribuir quando:

- CPF/CNPJ indicar mais de um destino possível;
- não houver identificação suficiente;
- houver dúvida material sobre qual cliente é o correto.

Nesses casos, manter o arquivo na pasta DP e classificar como FALHA / REVISÃO MANUAL.

---

## 5. PASTA INTERNA DO CLIENTE

Dentro da pasta do cliente, procurar por uma pasta existente com finalidade de Departamento Pessoal, especialmente:

- **Departamento Pessoal**
ou
- **Folha de Pagamento**

Aceitar diferenças simples de caixa, acentuação e grafia quando a finalidade for inequívoca.

Dentro dela ficam as pastas de competência.

---

## 6. COMPETÊNCIA

O padrão obrigatório das pastas de competência é:

`MM AAAA`

Exemplos:

- 08 2026
- 09 2026
- 12 2026

Não criar competência com hífen.

Não incluir nome do mês.

Se não for possível identificar a competência com segurança pelo conteúdo do documento, não inventar. Manter para revisão manual.

### 6.1 ESTRUTURA DE PASTAS POR ANO

A estrutura interna do cliente pode existir de duas formas válidas:

**FORMA A** (competência direta):

```
Departamento Pessoal / Folha de Pagamento
> MM AAAA
```

Exemplo:

```
DEPARTAMENTO PESSOAL
> 08 2026
```

**FORMA B** (competência dentro de pasta de ano):

```
Departamento Pessoal / Folha de Pagamento
> AAAA
> MM AAAA
```

Exemplo:

```
DEPARTAMENTO PESSOAL
> 2026
> 08 2026
```

A Routine deve respeitar a estrutura já utilizada pelo cliente.

Regra:

- se existir uma pasta de ano AAAA correspondente à competência, usar essa pasta e localizar/criar MM AAAA dentro dela;
- se não existir pasta de ano e as competências estiverem diretamente dentro de Departamento Pessoal/Folha de Pagamento, manter essa estrutura;
- não reorganizar pastas existentes;
- não mover competências antigas;
- não criar uma estrutura paralela diferente da já utilizada pelo cliente.

Se ainda não houver nenhuma competência que permita determinar o padrão:

- verificar se existe pasta de ano AAAA;
- se existir, criar MM AAAA dentro dela;
- se não existir, criar MM AAAA diretamente dentro de Departamento Pessoal/Folha de Pagamento.

Quando a pasta da competência correta (MM AAAA) não existir, a Routine está autorizada a criá-la, respeitando a estrutura acima.

---

## 7. REGRA PARA ESCOLHER ENTRE DEPARTAMENTO PESSOAL E FOLHA DE PAGAMENTO

Se apenas uma das duas estruturas existir, usar a existente.

Se ambas existirem:

1. verificar se a competência correspondente já existe em uma delas;
2. se somente uma possuir a competência, usar essa;
3. se ainda houver ambiguidade, não adivinhar e marcar para revisão manual.

Não criar uma nova pasta principal "Departamento Pessoal" ou "Folha de Pagamento" quando nenhuma delas puder ser identificada com segurança. A autorização automática de criação vale para a pasta de COMPETÊNCIA.

---

## 8. TIPOS MAIS COMUNS

Os documentos habituais são:

- RECIBO DE PAGAMENTO
- EXTRATO
- INSS
- FGTS

Mas a Skill NÃO possui lista fechada.

Também podem aparecer documentos esporádicos, como:

- RECIBO DE FÉRIAS
- AVISO DE FÉRIAS
- RESCISÃO
- AVISO PRÉVIO
- 13º SALÁRIO
- documentos de admissão;
- documentos relacionados a afastamentos;
- outros documentos trabalhistas.

Quando aparecer documento esporádico, identificar o tipo pela própria natureza/título/conteúdo do documento.

Não forçar um documento desconhecido para RECIBO, EXTRATO, INSS ou FGTS.

Se o tipo não puder ser identificado de forma confiável, não distribuir.

---

## 9. PADRÃO DE RENOMEAÇÃO

Todo documento deve seguir:

`TIPO DO DOCUMENTO - NOME DO CLIENTE - MM-AAAA.pdf`

Exemplos:

- RECIBO DE PAGAMENTO - EMPRESA EXEMPLO LTDA - 08-2026.pdf
- EXTRATO - EMPRESA EXEMPLO LTDA - 08-2026.pdf
- INSS - EMPRESA EXEMPLO LTDA - 08-2026.pdf
- FGTS - EMPRESA EXEMPLO LTDA - 08-2026.pdf
- RECIBO DE FÉRIAS - EMPRESA EXEMPLO LTDA - 08-2026.pdf
- RESCISÃO - EMPRESA EXEMPLO LTDA - 08-2026.pdf

Para cliente pessoa física:

- FGTS - JOÃO DA SILVA - 08-2026.pdf

A pasta usa "08 2026", mas o arquivo usa "08-2026".

### 9.1 NOME OPERACIONAL DO CLIENTE NO ARQUIVO

O nome usado no arquivo final não deve ser automaticamente o nome completo da pasta do cliente quando essa pasta possuir razão social, nome fantasia, nome pessoal ou outras identificações concatenadas.

Depois de confirmar o cliente por CPF/CNPJ, determinar o nome operacional assim:

1. Verificar os documentos já existentes nas pastas de Departamento Pessoal/Folha de Pagamento daquele mesmo cliente.
2. Se houver um nome curto utilizado de forma consistente nos arquivos existentes e a identidade estiver confirmada pelo mesmo CPF/CNPJ, usar esse nome como nome operacional.
3. Exemplo:

   pasta:

   `BEATRIZ DE BRITO CANTOR SERVICOS DE ENGENHARIA & PROJETOS - BEATRIZ DE BRITO CANTOR ENGENHARIA - BEATRIZ DE BRITO CANTOR`

   nome operacional já utilizado:

   `BEATRIZ DE BRITO CANTOR ENGENHARIA`

   portanto:

   `INSS - BEATRIZ DE BRITO CANTOR ENGENHARIA - 07-2026.pdf`

4. Se não houver histórico suficiente ou houver variação/confusão nos nomes existentes, usar a razão social ou nome do empregador identificado diretamente no documento.
5. Nunca escolher um segmento do nome da pasta por mera suposição.
6. CPF/CNPJ continua sendo a chave para confirmar que os arquivos históricos pertencem ao mesmo cliente.
7. Depois de definido para aquele processamento, usar exatamente o mesmo nome operacional em todos os documentos do mesmo cliente e competência.

---

## 10. IDENTIFICAÇÃO DO TIPO

A identificação deve ser feita pelo conteúdo do PDF, não apenas pelo nome original.

Usar títulos, cabeçalhos, órgãos emissores, natureza do documento e demais elementos internos.

O nome original pode ser usado apenas como indício complementar.

### 10.1 NORMALIZAÇÃO DO TIPO NO NOME FINAL

O nome original do arquivo NÃO determina o texto do nome final.

Após identificar o tipo pelo conteúdo, usar a nomenclatura canônica da Skill.

Normalizações obrigatórias para documentos habituais:

- "Guia INSS", "DARF Previdenciário", "DCTFWeb - DARF" ou equivalentes identificados como recolhimento previdenciário → **INSS**
- "Extrato Mensal", "Extrato da Folha" ou equivalente identificado como extrato → **EXTRATO**
- "Recibo", "Recibo Mensal", "Recibo de Salário" quando for efetivamente recibo mensal → **RECIBO DE PAGAMENTO**
- Documentos de FGTS identificados como guia/recolhimento mensal → **FGTS**

O padrão final permanece:

`TIPO CANÔNICO - NOME CANÔNICO DO CLIENTE - MM-AAAA.pdf`

---

## 11. DOCUMENTO ORIGINAL

A distribuição deve preservar integralmente o PDF recebido.

Permitido:

- renomear;
- copiar/enviar para o destino correto.

Não permitido:

- alterar páginas;
- converter o conteúdo;
- reconstruir o PDF;
- adicionar marca d'água;
- mudar valores;
- editar textos.

---

## 12. IMPLEMENTAÇÃO DA DISTRIBUIÇÃO

Os documentos de origem já estão no Google Drive, na pasta Departamento Geral > DP.

A distribuição deve preferencialmente ser feita por **operação nativa de cópia** do próprio Google Drive/conector:

- copiar o arquivo original para a pasta de competência correta;
- o arquivo copiado deve receber o nome final definido pela Skill;
- preservar o arquivo de origem intacto na pasta DP.

Não permitido na implementação:

- baixar e reenviar o PDF sem necessidade;
- converter o PDF;
- reconstruir o PDF;
- gerar Base64;
- usar a ponte HTTP da Procuradoria para arquivos do DP;
- usar scripts para recriar o documento.

A cópia distribuída deve preservar integralmente os bytes/conteúdo do documento original.

### Criação de pasta

- Se a pasta interna Departamento Pessoal ou Folha de Pagamento já estiver identificada com segurança e a competência MM AAAA não existir, criar somente a pasta da competência.
- Depois realizar a cópia para essa pasta.
- Não criar automaticamente uma nova pasta principal Departamento Pessoal/Folha de Pagamento.

---

## 13. DUPLICIDADE

A verificação de duplicidade deve usar o **NOME FINAL PADRONIZADO** que a Routine pretende criar (após a normalização da seção 10.1), e não simplesmente o nome original recebido.

Exemplo:

- arquivo de entrada: `Guia INSS - EMPRESA X - 07-2026.pdf`
- nome final: `INSS - NOME CANÔNICO DO CLIENTE - 07-2026.pdf`

A Routine deve procurar no destino pelo nome final (segundo nome), verificando-o **ANTES** da cópia.

Nunca sobrescrever silenciosamente.

Se existir exatamente o nome final:

- não copiar por cima;
- não substituir;
- não criar "(1)", "cópia" ou variantes automáticas;
- comparar a identificação disponível;
- não criar duplicata automaticamente;
- classificar como JÁ EXISTENTE;
- manter o arquivo de entrada intacto até decisão humana.

Se não existir o nome final, o documento pode estar PRONTO PARA DISTRIBUIÇÃO, desde que todas as demais validações estejam satisfeitas.

Não classificar automaticamente como REVISÃO MANUAL apenas porque existe um arquivo antigo com nomenclatura diferente.

---

## 14. SEGURANÇA

Não usar inferências frágeis.

Não distribuir arquivo para um cliente apenas porque o nome é semelhante.

Não criar CPF, CNPJ, competência ou tipo de documento que não estejam sustentados pelo documento.

Nunca mover o arquivo original da pasta Departamento Geral > DP durante o processamento automático.

A Routine faz distribuição por **cópia**.

Não excluir automaticamente arquivos da pasta Departamento Geral > DP após a distribuição.

Não mover ou limpar a fila automaticamente.

Exclusão/limpeza da fila será sempre decisão humana posterior.

---

## 15. PROCESSAMENTO EM LOTE

A Routine poderá processar vários documentos e vários clientes no mesmo lote.

Cada documento deve ser tratado individualmente.

Uma falha em um arquivo não deve impedir o processamento seguro dos demais.

---

## 16. RESULTADO DO LOTE

Ao final, informar para cada arquivo:

- nome original;
- cliente identificado;
- CPF/CNPJ quando disponível;
- tipo identificado;
- competência;
- estrutura de destino: EMPRESAS / FAZENDAS / EMPREGADA DOMESTICA;
- pasta de competência;
- nome final;
- situação:
  - DISTRIBUÍDO
  - JÁ EXISTENTE
  - REVISÃO MANUAL
  - FALHA

Ao final apresentar totais:

- arquivos analisados;
- distribuídos;
- já existentes;
- revisão manual;
- falhas.

---

## 17. PRINCÍPIO CENTRAL

Esta Skill é uma rotina de ORGANIZAÇÃO DOCUMENTAL do Departamento Pessoal.

Ela deve priorizar precisão e segurança da distribuição.

Quando houver dúvida, não distribuir.
