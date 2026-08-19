---
name: procuradoria
description: Processa automaticamente as Situações Fiscais do Departamento de Procuradoria do Grupo JB. Use quando houver Situações Fiscais (PDF, PNG ou outro formato legível) e documentos complementares (prints do e-CAC, prints do Regularize/PGFN, Termo de Exclusão do Simples Nacional) na pasta Departamento Geral/Procuradoria para identificar o contribuinte, avaliar débitos, parcelamentos e a situação na PGFN e gerar o Relatório de Procuradoria em PNG, salvando tudo somente na própria pasta Departamento Geral/Procuradoria, sem distribuição automática para as pastas dos contribuintes.
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

# 15. DATA E REFERÊNCIA DO RELATÓRIO

Utilizar mês e ano da data da Situação Fiscal.

Exemplo:

```
Situação Fiscal emitida em 14/08/2026
→ referência 08/2026
```

A referência serve apenas para nomear o relatório. Ela NÃO gera criação de pasta de ano nem de pasta mensal.

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

# 17. ARMAZENAMENTO — PASTA OPERACIONAL ÚNICA

A Procuradoria trabalha com informações VOLÁTEIS: débitos podem ser pagos, parcelados, mudar de valor, deixar de existir, ser inscritos ou retirados da PGFN, ou ter sua situação alterada por uma nova consulta.

Por isso, a única pasta operacional autorizada da Procuradoria é:

```
++++++CONTABILIDADE+++
> Departamento Geral
> Procuradoria
```

Regras:

1. A Situação Fiscal original permanece em Departamento Geral > Procuradoria.
2. Os documentos complementares permanecem nessa mesma pasta.
3. O Relatório de Procuradoria em PNG deve ser salvo SOMENTE em Departamento Geral > Procuradoria.

A pasta Departamento Geral > Procuradoria é a fonte operacional da situação fiscal atual de cada contribuinte.

Não excluir a Situação Fiscal original.

---

# 18. PROIBIÇÃO DE DISTRIBUIÇÃO AUTOMÁTICA

A automação NÃO deve distribuir automaticamente Situações Fiscais ou Relatórios para as pastas permanentes dos contribuintes.

NÃO utilizar automaticamente as raízes:

```
+++++++++++++++EMPRESAS+++++
+++++++++++FAZENDAS+++++
++++++++EMPREGADA DOMESTICA++++
```

NÃO copiar ou distribuir automaticamente:

- Situação Fiscal;
- prints;
- Termos;
- relatório PNG.

NÃO criar:

- pasta PROCURADORIA dentro do cliente;
- pasta de ano no cliente;
- pasta mensal no cliente.

Qualquer regra anterior desta Skill que determinava distribuição automática para essas raízes está revogada.

---

# 19. VOLATILIDADE DA SITUAÇÃO FISCAL

Uma nova Situação Fiscal representa uma nova fotografia do contribuinte.

Nunca presumir que um relatório antigo continua válido depois de uma nova Situação Fiscal.

O documento vigente é sempre o mais recente disponível na pasta Departamento Geral > Procuradoria.

---

# 20. DUPLICIDADE E ATUALIZAÇÃO

Antes de gerar, verificar se já existe relatório do mesmo contribuinte e mesma referência.

Nunca sobrescrever silenciosamente.

Se existir relatório do mesmo contribuinte e mesma referência e surgir uma Situação Fiscal mais recente que altere os dados:

- classificar como **ATUALIZAÇÃO NECESSÁRIA**;
- não reutilizar o relatório anterior como situação atual.

---

# 21. LIMPEZA DA PASTA

Não excluir automaticamente arquivos antigos.

A limpeza da pasta Departamento Geral > Procuradoria continuará sendo uma decisão humana.

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
- distribuir automaticamente arquivos para as pastas dos contribuintes;
- criar pastas dentro das pastas dos contribuintes;
- excluir automaticamente arquivos antigos;
- reutilizar relatório anterior como situação atual após nova Situação Fiscal;
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

O script salva o PNG final em paleta indexada adaptativa de até 256 cores, sem dithering e com compressão máxima, para reduzir o tamanho do arquivo sem alterar conteúdo, dimensões ou aparência do relatório.

A estrutura do JSON e os códigos de saída estão documentados em `.claude/skills/procuradoria/scripts/README.md`.

## Códigos de saída

- `0` — relatório gerado;
- `1` — erro (argumentos inválidos, JSON ausente ou inválido, falha de escrita);
- `2` — nenhuma condição financeira identificada: relatório NÃO deve ser gerado, conforme a seção 4.

O código `2` não é falha. É a aplicação da regra de que contribuinte sem dívida encerra silenciosamente, sem PNG e sem distribuição.

## Dependência

A dependência necessária está declarada em `requirements.txt` (`Pillow`).

## PONTE OFICIAL DE UPLOAD (HTTP)

O envio do Relatório de Procuradoria em PNG para o Google Drive deve ser feito EXCLUSIVAMENTE pela ponte HTTP oficial, configurada nas variáveis de ambiente:

- `JB_PROC_UPLOAD_URL` — endereço do Web App que recebe o arquivo;
- `JB_PROC_UPLOAD_TOKEN` — token de autenticação da ponte.

### Requisição

Método: **HTTP POST**

Cabeçalho:

```
Content-Type: application/json
```

Corpo JSON, exatamente com estes três campos:

```json
{
  "token": "<valor de JB_PROC_UPLOAD_TOKEN>",
  "filename": "<nome final do PNG>",
  "base64": "<conteúdo integral do PNG codificado em Base64>"
}
```

O `filename` é o nome final do relatório, conforme a regra da seção 15.

O Base64 deve ser produzido e enviado programaticamente, a partir do arquivo PNG local. Nunca imprimir o conteúdo Base64 completo na resposta da Routine.

### Token

O token é segredo operacional.

Nunca exibir, copiar ou reproduzir o valor de `JB_PROC_UPLOAD_TOKEN` em logs, mensagens, respostas, relatórios, commits ou qualquer saída visível.

Referenciar sempre a variável de ambiente, nunca o valor.

### Contrato definitivo

O contrato acima é definitivo.

Não sondar o endpoint, não testar nomes alternativos de campos e não tentar descobrir o formato da requisição por tentativa e erro.

Se a ponte recusar a requisição, interromper aquele contribuinte e informar o problema.

### Validação antes do upload

Antes de enviar, validar o PNG local:

- assinatura PNG válida;
- dimensões;
- tamanho em bytes;
- conteúdo financeiro coerente com a Situação Fiscal.

### Retorno do Web App

O Web App responde em JSON, no formato:

```json
{
  "ok": true,
  "fileId": "...",
  "filename": "...",
  "size": 17828
}
```

O upload só pode ser considerado bem-sucedido quando TODAS estas condições forem verdadeiras:

1. `ok` = `true`;
2. `filename` retornado corresponde ao arquivo enviado;
3. `size` retornado é exatamente igual ao tamanho local do PNG em bytes.

Se os tamanhos forem diferentes, o upload é **FALHA**: não tratar o relatório como entregue e informar a divergência.

Se o Web App retornar `arquivo_ja_existe`, não sobrescrever silenciosamente — aplicar a regra de duplicidade da seção 20.

### Destino

O destino continua sendo exclusivamente:

```
++++++CONTABILIDADE+++
> Departamento Geral
> Procuradoria
```

Nunca enviar automaticamente para EMPRESAS, FAZENDAS, EMPREGADA DOMÉSTICA ou qualquer outra pasta, conforme a seção 18.

### Conector do Google Drive

Enquanto esta ponte estiver configurada, o conector do Google Drive pode ser usado para **leitura e conferência** (localizar a Situação Fiscal, ler documentos complementares, verificar duplicidade, conferir o arquivo enviado).

O conector do Google Drive **NÃO** deve ser usado para enviar o PNG final.

### Documentos de origem

Após o upload, não excluir, mover nem renomear a Situação Fiscal, os documentos complementares ou qualquer outro documento de origem.

## Ainda não implementado

- Routine;
- leitura automática da Situação Fiscal (PDF/PNG).

Esses itens serão criados em etapas posteriores, mediante instrução expressa do usuário.

A distribuição automática para as pastas dos contribuintes NÃO é um item pendente: ela está proibida pela seção 18.

## Proteção dos recursos da Skill

Não alterar, sem instrução expressa do usuário:

- `.claude/skills/procuradoria/scripts/gerar_relatorio_procuradoria.py`;
- `.claude/skills/procuradoria/references/modelo-relatorio-procuradoria.png`;
- `requirements.txt`.
