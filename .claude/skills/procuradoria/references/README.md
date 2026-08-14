# Referências da Skill Procuradoria

Arquivos de referência utilizados para geração e validação do Relatório de Procuradoria.

## Modelo visual oficial

- `modelo-relatorio-procuradoria.png` — **referência visual oficial** do Relatório de Procuradoria (seção 16 do `SKILL.md`), versionada no repositório. Tamanho: 900×1257 px.

A geometria e a paleta do gerador oficial (`../scripts/gerar_relatorio_procuradoria.py`) foram extraídas deste arquivo: fundo `#EEF1F5`, folha branca arredondada com sombra suave, cabeçalho azul escuro `#12355B`, blocos com fundo tingido e borda de 2 px na cor do tema, linhas divisórias finas entre itens, subtotal destacado ao pé de cada bloco e rodapé centralizado.

O modelo define o layout aceito pelo Grupo JB: cabeçalho azul escuro, nome do contribuinte, CNPJ/CPF, mês/ano, blocos vermelhos para débitos, blocos amarelos para exigibilidade/alertas, bloco verde para PGFN sem pendências, bloco vermelho para PGFN com dívida e Total Geral em vermelho.

O conteúdo é dinâmico: blocos inexistentes não geram espaços vazios, e o PNG cresce verticalmente quando necessário.

## Limites de uso

O modelo é **referência visual, nunca fonte de valores**. Nenhum nome, número, inscrição, competência ou texto do exemplo pode ser reaproveitado em um processamento real.

Quando as regras do `SKILL.md` divergirem do modelo, **as regras prevalecem**. Divergências já decididas e definitivas:

| Ponto | Modelo | Regra vigente |
| --- | --- | --- |
| Exigibilidade / a vencer | bloco azul | bloco **amarelo** (seção 6) |
| Bloco de "a vencer" sem débito | exibe aviso de que nada há a vencer | **não é renderizado** (seção 16) |
| Total Geral | apenas o total do bloco de atraso | faixa **vermelha** ao pé (seções 12 e 16) |

Não alterar este arquivo de modelo sem instrução expressa do usuário.
