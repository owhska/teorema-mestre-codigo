# -*- coding: utf-8 -*-
"""Gera os corpos das tabelas LaTeX do relatório a partir do CSV de resultados."""
import math, os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "resultados", "resultados.csv"))
SAIDA = os.path.join(BASE, "relatorio", "tabelas")
os.makedirs(SAIDA, exist_ok=True)

def mil(x):
    return f"{int(x):,}".replace(",", ".")

def tabular(colunas, cabecalho, linhas):
    """Monta o bloco tabular completo, pronto para \\input no relatório."""
    return ("\\begin{tabular}{" + colunas + "}\n\\toprule\n"
            + cabecalho + " \\\\\n\\midrule\n"
            + "\n".join(linhas) + "\n\\bottomrule\n\\end{tabular}\n")


def num(x, casas=4):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def tempo(seg):
    """Tempo em microssegundos, com duas casas decimais."""
    return num(seg * 1e6, 2)

p1 = df[(df.problema == 1) & (df.algoritmo == "karatsuba")].sort_values("n").reset_index(drop=True)
p1d = df[(df.problema == 1) & (df.algoritmo == "direto")].sort_values("n").reset_index(drop=True)
p2 = df[df.problema == 2].sort_values("n").reset_index(drop=True)
p3 = df[df.problema == 3].sort_values("n").reset_index(drop=True)

# Tabela P1
linhas = []
for i, r in p1.iterrows():
    razao = "---" if i == 0 else num(r.operacoes / p1.operacoes[i-1], 4)
    linhas.append(f"{mil(r.n)} & {mil(r.operacoes)} & {mil(r.previsto)} & {int(r.diferenca)} & "
                  f"{razao} & {tempo(r.tempo_mediano_s)} \\\\")
open(os.path.join(SAIDA, "p1.tex"), "w").write(tabular("rrrrrr",
    "$n$ & Operações & Previsto & Dif. & $T(2n)/T(n)$ & Tempo ($\\mu$s)", linhas))

# Tabela P1 comparativa
j = p1.merge(p1d, on="n", suffixes=("_k", "_d"))
linhas = []
for _, r in j.iterrows():
    linhas.append(f"{mil(r.n)} & {mil(r.operacoes_k)} & {mil(r.operacoes_d)} & "
                  f"{num(r.operacoes_d/r.operacoes_k, 2)} & {tempo(r.tempo_mediano_s_k)} & "
                  f"{tempo(r.tempo_mediano_s_d)} & {num(r.tempo_mediano_s_d/r.tempo_mediano_s_k, 2)} \\\\")
open(os.path.join(SAIDA, "p1_comp.tex"), "w").write(tabular("rrrrrrr",
    "$n$ & Ops.\\ Karatsuba & Ops.\\ direto & Ganho & $t$ Karatsuba ($\\mu$s) & "
    "$t$ direto ($\\mu$s) & Ganho", linhas))

# Tabela P2
linhas = []
for i, r in p2.iterrows():
    k = round(math.log(r.n)/math.log(3))
    razao = "---" if i == 0 else num(r.operacoes / p2.operacoes[i-1], 4)
    prev_razao = "---" if i == 0 else num(3.0*k/(k-1), 4)
    linhas.append(f"{k} & {mil(r.n)} & {mil(r.operacoes)} & {mil(r.previsto)} & {int(r.diferenca)} & "
                  f"{razao} & {prev_razao} & {tempo(r.tempo_mediano_s)} \\\\")
open(os.path.join(SAIDA, "p2.tex"), "w").write(tabular("rrrrrrrr",
    "$k$ & $n$ & Operações & Previsto & Dif. & $T(3n)/T(n)$ & Prev. & Tempo ($\\mu$s)", linhas))

# Tabela P3
linhas = []
for i, r in p3.iterrows():
    razao = "---" if i == 0 else num(r.operacoes / p3.operacoes[i-1], 4)
    linhas.append(f"{mil(r.n)} & {mil(r.operacoes)} & {mil(r.previsto)} & {int(r.diferenca)} & "
                  f"{razao} & {tempo(r.tempo_mediano_s)} \\\\")
open(os.path.join(SAIDA, "p3.tex"), "w").write(tabular("rrrrrr",
    "$n$ & Comparações & Previsto & Dif. & $T(2n)/T(n)$ & Tempo ($\\mu$s)", linhas))

# Tabela de tempo por operação
linhas = []
for nome, d in [("Problema 1 --- Karatsuba", p1), ("Problema 2 --- MergeSort ternário", p2),
                ("Problema 3 --- Par mais próximo", p3)]:
    ns = d.tempo_mediano_s.values*1e9/d.operacoes.values
    grandes = ns[-6:]
    linhas.append(f"{nome} & {num(ns[0], 1)} & {num(grandes.min(), 2)} & {num(grandes.max(), 2)} \\\\")
open(os.path.join(SAIDA, "tempo_op.tex"), "w").write(tabular("lrrr",
    "Problema & Menor $n$ & Mínimo (maiores) & Máximo (maiores)", linhas))

print("Tabelas geradas em", SAIDA)
for f in sorted(os.listdir(SAIDA)):
    print(" -", f)
