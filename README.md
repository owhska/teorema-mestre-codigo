# Aplicação do Teorema Mestre à Análise de Algoritmos

| | Algoritmo | Recorrência | a | b | f(n) | Caso | Complexidade |
|---|---|---|---|---|---|---|---|
| Problema 1 | Karatsuba (produto de polinômios) | T(n) = 3T(n/2) + 6n − 5 | 3 | 2 | Θ(n) | 1 | Θ(n^log₂3) |
| Problema 2 | MergeSort ternário | T(n) = 3T(n/3) + n | 3 | 3 | Θ(n) | 2 | Θ(n lg n) |
| Problema 3 | Par mais próximo em 1D | T(n) = 2T(n/2) + n²/4 | 2 | 2 | Θ(n²) | 3 | Θ(n²) |

Restrições atendidas: a ≠ 2 nos Problemas 1 e 2; a ≠ b no Problema 1.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/comum.h`, `src/comum.c` | contador de operações, medição de tempo e gravação do CSV |
| `src/problema1.c` | Karatsuba e multiplicação direta (Caso 1) |
| `src/problema2.c` | MergeSort ternário (Caso 2) |
| `src/problema3.c` | par mais próximo por divisão e conquista (Caso 3) |
| `src/main.c` | execução da bateria de experimentos |
| `resultados/resultados.csv` | arquivo único com todos os experimentos |
| `analisar.py` | confronto com a teoria e geração dos gráficos |
| `gerar_tabelas.py` | geração das tabelas LaTeX a partir do CSV |
| `graficos/` | gráficos do relatório |
| `relatorio/` | fonte LaTeX e PDF do relatório |

## Compilação

```bash
make
```

ou, manualmente:

```bash
gcc -O2 -Wall -Wextra -std=c99 -o experimentos \
    src/main.c src/comum.c src/problema1.c src/problema2.c src/problema3.c -lm
```

Funciona em Linux e no Windows (MSYS2/MinGW).

## Execução

```bash
./experimentos [arquivo.csv] [repeticoes]
```

Sem argumentos, grava em `resultados/resultados.csv` com 15 repetições por ponto.
Cada linha do CSV traz o problema, o algoritmo, a recorrência, o tamanho da
entrada, as operações contadas, o valor previsto pela forma fechada, a diferença
entre os dois, o tempo mediano e o número de repetições.

## Reproduzir a análise e o relatório

Requer Python 3 com `pandas`, `numpy` e `matplotlib`, e uma distribuição LaTeX.

```bash
./experimentos resultados/resultados.csv 15
python3 analisar.py
python3 gerar_tabelas.py
cd relatorio && latexmk -pdf relatorio.tex
```
