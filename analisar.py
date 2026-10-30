# -*- coding: utf-8 -*-
"""Confronta os resultados experimentais com as previsões teóricas e gera
os gráficos do relatório a partir de resultados/resultados.csv."""

import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "resultados", "resultados.csv")
SAIDA = os.path.join(BASE, "graficos")
os.makedirs(SAIDA, exist_ok=True)

OBS = "#2a78d6"
TEO = "#d1603d"
AUX = "#555555"

plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "font.size": 10,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.edgecolor": "#c3c2b7",
    "grid.color": "#e1e0d9", "legend.frameon": False, "figure.dpi": 160,
    "axes.spines.top": False, "axes.spines.right": False,
})


def milhar(x, _):
    return f"{int(round(x)):,}".replace(",", ".")


def titulo(ax, t, sub):
    ax.set_title(t, loc="left", pad=20)
    ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=8,
            color="#6b6a64", va="bottom")


def salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(os.path.join(SAIDA, nome), bbox_inches="tight")
    plt.close(fig)


df = pd.read_csv(CSV)
p1 = df[(df.problema == 1) & (df.algoritmo == "karatsuba")].sort_values("n")
p1d = df[(df.problema == 1) & (df.algoritmo == "direto")].sort_values("n")
p2 = df[df.problema == 2].sort_values("n")
p3 = df[df.problema == 3].sort_values("n")

print("=== Conferência das formas fechadas ===")
for nome, d in [("P1 Karatsuba", p1), ("P1 direto", p1d), ("P2", p2), ("P3", p3)]:
    print(f"{nome}: diferença máxima = {d.diferenca.abs().max()}")

print("\n=== Inclinações log-log (cauda: últimos 5 pontos) e razões ===")
resumo = {}
for nome, d, exp_teo in [("P1", p1, math.log2(3)), ("P2", p2, None), ("P3", p3, 2.0)]:
    cauda = d.tail(5)
    inc_ops = np.polyfit(np.log(cauda.n), np.log(cauda.operacoes), 1)[0]
    grande = d[d.tempo_mediano_s > 1e-5].tail(5)
    inc_t = np.polyfit(np.log(grande.n), np.log(grande.tempo_mediano_s), 1)[0]
    razoes_ops = (d.operacoes.values[1:] / d.operacoes.values[:-1])
    g2 = d[d.tempo_mediano_s > 1e-5]
    razoes_t = (g2.tempo_mediano_s.values[1:] / g2.tempo_mediano_s.values[:-1])
    resumo[nome] = (inc_ops, inc_t, razoes_ops, razoes_t)
    print(f"{nome}: inclinação ops = {inc_ops:.4f}  tempo = {inc_t:.4f}"
          f"  (teórica = {exp_teo if exp_teo else 'n lg n'})")
    print(f"    razões ops:   {np.round(razoes_ops, 4)}")
    print(f"    razões tempo: {np.round(razoes_t, 3)}")

print("\n=== P2: razão ao triplicar n, medida x prevista 3(k+1)/k ===")
ks = np.round(np.log(p2.n.values) / math.log(3)).astype(int)
for i in range(len(ks) - 1):
    prev = 3.0 * (ks[i] + 1) / ks[i]
    med = p2.operacoes.values[i+1] / p2.operacoes.values[i]
    print(f"  3^{ks[i]} -> 3^{ks[i+1]}:  medida {med:.4f}  prevista {prev:.4f}"
          f"  dif {med-prev:+.6f}")

print("\n=== P2: operações / (n log_3 n) ===")
print(np.round(p2.operacoes.values / (p2.n.values * np.log(p2.n.values) / math.log(3)), 6))

print("\n=== P1: Karatsuba x direto ===")
j = p1.merge(p1d, on="n", suffixes=("_k", "_d"))
j["ganho_ops"] = j.operacoes_d / j.operacoes_k
j["ganho_tempo"] = j.tempo_mediano_s_d / j.tempo_mediano_s_k
print(j[["n", "operacoes_k", "operacoes_d", "ganho_ops", "ganho_tempo"]].to_string(index=False))

print("\n=== Tempo por operação (ns) ===")
for nome, d in [("P1", p1), ("P2", p2), ("P3", p3)]:
    ns = d.tempo_mediano_s.values * 1e9 / d.operacoes.values
    print(f"{nome}: {np.round(ns, 2)}")

# ---------------------------------------------------------------- Problema 1
fig, ax = plt.subplots(figsize=(7.2, 4.2))
g = np.linspace(2, 4096, 500)
k = np.log2(g)
ax.plot(g, (21 * 3 ** k - 24 * 2 ** k + 5) / 2, "-", color=TEO, lw=1.8,
        label=r"Previsto: $(21\cdot3^k - 24\cdot2^k + 5)/2$")
ax.plot(p1.n, p1.operacoes, "o", color=OBS, ms=6, label="Observado")
titulo(ax, "Problema 1 (Caso 1): operações do Karatsuba",
       "Os pontos medidos coincidem com a forma fechada em todos os tamanhos.")
ax.set_xlabel("n (coeficientes)")
ax.set_ylabel("Operações elementares")
ax.yaxis.set_major_formatter(FuncFormatter(milhar))
ax.grid(True, axis="y")
ax.legend()
salvar(fig, "p1_operacoes.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(p1.n, p1.operacoes, "o-", color=OBS, ms=5, lw=1.5, label="Karatsuba (observado)")
ref = p1.operacoes.iloc[-1] * (p1.n / p1.n.iloc[-1]) ** math.log2(3)
ax.plot(p1.n, ref, "--", color=TEO, lw=1.5, label=r"Referência $\propto n^{\log_2 3}$")
ax.plot(p1d.n, p1d.operacoes, "s-", color=AUX, ms=4, lw=1.2, label="Direto (observado)")
ref2 = p1d.operacoes.iloc[-1] * (p1d.n / p1d.n.iloc[-1]) ** 2
ax.plot(p1d.n, ref2, ":", color=AUX, lw=1.2, label=r"Referência $\propto n^2$")
ax.set_xscale("log"); ax.set_yscale("log")
inc = resumo["P1"][0]
titulo(ax, "Problema 1: verificação de $\\Theta(n^{\\log_2 3})$ em log-log",
       f"Inclinação medida: {inc:.4f}".replace(".", ",") +
       f" (teórica: {math.log2(3):.4f})".replace(".", ","))
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Operações (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "p1_loglog.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(p1.n, p1.tempo_mediano_s * 1e3, "o-", color=OBS, ms=5, lw=1.5,
        label="Karatsuba (tempo medido)")
ax.plot(p1d.n, p1d.tempo_mediano_s * 1e3, "s-", color=AUX, ms=4, lw=1.2,
        label="Direto (tempo medido)")
reft = p1.tempo_mediano_s.iloc[-1] * 1e3 * (p1.n / p1.n.iloc[-1]) ** math.log2(3)
ax.plot(p1.n, reft, "--", color=TEO, lw=1.5, label=r"Referência $\propto n^{\log_2 3}$")
ax.set_xscale("log"); ax.set_yscale("log")
titulo(ax, "Problema 1: tempo de execução",
       "Mediana de 15 repetições; o cruzamento das curvas ocorre perto de n = 1024.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Tempo em ms (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "p1_tempo.png")

# ---------------------------------------------------------------- Problema 2
fig, ax = plt.subplots(figsize=(7.2, 4.2))
g = np.linspace(3, 531441, 2000)
ax.plot(g, g * np.log(g) / math.log(3), "-", color=TEO, lw=1.8,
        label=r"Previsto: $n\log_3 n$")
ax.plot(p2.n, p2.operacoes, "o", color=OBS, ms=6, label="Observado")
ax.set_xscale("log"); ax.set_yscale("log")
titulo(ax, "Problema 2 (Caso 2): operações do MergeSort ternário",
       "Os pontos medidos caem exatamente sobre a curva n·log₃ n.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Operações (escala log)")
ax.grid(True, which="major")
ax.legend()
salvar(fig, "p2_operacoes.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
razao = p2.operacoes.values / p2.n.values
ax.plot(p2.n, razao, "o-", color=OBS, ms=5, lw=1.5, label="Observado: T(n)/n")
ax.plot(p2.n, np.log(p2.n.values) / math.log(3), "--", color=TEO, lw=1.5,
        label=r"Previsto: $\log_3 n$")
ax.set_xscale("log")
titulo(ax, "Problema 2: o fator logarítmico isolado",
       "Dividindo as operações por n, resta exatamente log₃ n: uma reta em escala log.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("T(n) / n")
ax.grid(True, axis="y")
ax.legend()
salvar(fig, "p2_fator_log.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(p2.n, p2.tempo_mediano_s * 1e3, "o-", color=OBS, ms=5, lw=1.5,
        label="Tempo medido")
reft = p2.tempo_mediano_s.iloc[-1] * 1e3 * (p2.n * np.log(p2.n)) / (
    p2.n.iloc[-1] * math.log(p2.n.iloc[-1]))
ax.plot(p2.n, reft, "--", color=TEO, lw=1.5, label=r"Referência $\propto n\lg n$")
ax.set_xscale("log"); ax.set_yscale("log")
titulo(ax, "Problema 2: tempo de execução",
       "Mediana de 15 repetições, para n de 3 a 531.441.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Tempo em ms (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "p2_tempo.png")

# ---------------------------------------------------------------- Problema 3
fig, ax = plt.subplots(figsize=(7.2, 4.2))
g = np.linspace(2, 8192, 1000)
ax.plot(g, g * (g - 1) / 2, "-", color=TEO, lw=1.8, label=r"Previsto: $n(n-1)/2$")
ax.plot(p3.n, p3.operacoes, "o", color=OBS, ms=6, label="Observado")
titulo(ax, "Problema 3 (Caso 3): operações do par mais próximo",
       "Cada par do vetor é comparado exatamente uma vez: coincidência exata.")
ax.set_xlabel("n (elementos)")
ax.set_ylabel("Comparações")
ax.yaxis.set_major_formatter(FuncFormatter(milhar))
ax.grid(True, axis="y")
ax.legend()
salvar(fig, "p3_operacoes.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(p3.n, p3.operacoes, "o-", color=OBS, ms=5, lw=1.5, label="Observado")
ref = p3.operacoes.iloc[-1] * (p3.n / p3.n.iloc[-1]) ** 2
ax.plot(p3.n, ref, "--", color=TEO, lw=1.5, label=r"Referência $\propto n^2$")
ax.set_xscale("log"); ax.set_yscale("log")
inc = resumo["P3"][0]
titulo(ax, "Problema 3: verificação de $\\Theta(n^2)$ em log-log",
       f"Inclinação medida: {inc:.4f}".replace(".", ",") + " (teórica: 2)")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Comparações (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "p3_loglog.png")

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(p3.n, p3.tempo_mediano_s * 1e3, "o-", color=OBS, ms=5, lw=1.5,
        label="Tempo medido")
reft = p3.tempo_mediano_s.iloc[-1] * 1e3 * (p3.n / p3.n.iloc[-1]) ** 2
ax.plot(p3.n, reft, "--", color=TEO, lw=1.5, label=r"Referência $\propto n^2$")
ax.set_xscale("log"); ax.set_yscale("log")
titulo(ax, "Problema 3: tempo de execução",
       "Mediana de 15 repetições, para n de 2 a 8.192.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Tempo em ms (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "p3_tempo.png")

# ------------------------------------------------- Comparação dos três casos
fig, ax = plt.subplots(figsize=(7.2, 4.4))
for nome, d, cor, marca in [("Caso 1 — Karatsuba, $\\Theta(n^{\\log_2 3})$", p1, "#2a78d6", "o"),
                            ("Caso 2 — MergeSort 3-vias, $\\Theta(n\\lg n)$", p2, "#1b9e77", "^"),
                            ("Caso 3 — Par mais próximo, $\\Theta(n^2)$", p3, "#d95f02", "s")]:
    ax.plot(d.n, d.operacoes, marca + "-", color=cor, ms=5, lw=1.5, label=nome)
ax.set_xscale("log"); ax.set_yscale("log")
titulo(ax, "Os três problemas em escala log-log",
       "A inclinação de cada reta é o expoente da complexidade prevista pelo Teorema Mestre.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Operações elementares (escala log)")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "comparacao_casos.png")

# ------------------------------------------------- Razões de crescimento
fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.6))
for ax, (nome, d, limite, fator, rot) in zip(axs, [
        ("Caso 1: Karatsuba", p1, 3.0, 2, "dobrar n"),
        ("Caso 2: MergeSort 3-vias", p2, 3.0, 3, "triplicar n"),
        ("Caso 3: Par mais próximo", p3, 4.0, 2, "dobrar n")]):
    r = d.operacoes.values[1:] / d.operacoes.values[:-1]
    rot_x = [f"{int(a)}→{int(b)}" for a, b in zip(d.n.values[:-1], d.n.values[1:])]
    ax.plot(range(len(r)), r, "o-", color=OBS, ms=4, lw=1.4)
    ax.axhline(limite, color=TEO, ls="--", lw=1.4)
    ax.text(len(r) - 1, limite + 0.08, f"limite = {limite:.0f}", color=TEO,
            fontsize=8, ha="right")
    ax.set_title(nome, loc="left", fontsize=10)
    ax.set_xlabel(f"transições ao {rot}")
    passo = max(1, len(r) // 3)
    idx = list(range(0, len(r), passo))
    ax.set_xticks(idx)
    ax.set_xticklabels([rot_x[i] for i in idx], fontsize=7, rotation=20)
    ax.grid(True, axis="y")
axs[0].set_ylabel("T(bn) / T(n)")
fig.suptitle("Fator de crescimento das operações, por problema", x=0.005,
             ha="left", fontsize=12, fontweight="bold")
salvar(fig, "razoes_crescimento.png")

# ------------------------------------------------- Tempo por operação
fig, ax = plt.subplots(figsize=(7.2, 4.0))
for nome, d, cor, marca in [("Caso 1 — Karatsuba", p1, "#2a78d6", "o"),
                            ("Caso 2 — MergeSort 3-vias", p2, "#1b9e77", "^"),
                            ("Caso 3 — Par mais próximo", p3, "#d95f02", "s")]:
    ns = d.tempo_mediano_s.values * 1e9 / d.operacoes.values
    ax.plot(d.n, ns, marca + "-", color=cor, ms=4, lw=1.4, label=nome)
ax.set_xscale("log")
ax.set_yscale("log")
titulo(ax, "Custo real de cada operação elementar",
       "O modelo teórico supõe custo constante; na máquina ele varia com n e com o algoritmo.")
ax.set_xlabel("n (escala log)")
ax.set_ylabel("Nanossegundos por operação")
ax.grid(True, which="major")
ax.legend(fontsize=8)
salvar(fig, "tempo_por_operacao.png")

print("\nGráficos gerados em", SAIDA)
