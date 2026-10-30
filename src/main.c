/* main.c — executa os experimentos dos três problemas e registra cada
 * execução no mesmo arquivo CSV.
 *
 * Uso:  ./experimentos [arquivo.csv] [repeticoes]
 *
 * Cada problema é executado para uma sequência de tamanhos de entrada; para
 * cada tamanho, o programa repete a execução e registra o tempo mediano,
 * o número de operações elementares contadas e o valor previsto pela forma
 * fechada demonstrada no relatório.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "comum.h"

void karatsuba(const long long *p, const long long *q, size_t n, long long *res);
void multiplicar_direto(const long long *p, const long long *q, size_t n, long long *res);
void mergesort3(int *v, size_t n);
long long par_mais_proximo(const long long *v, size_t ini, size_t fim);

#define MAX_REP 64

/* Gerador pseudoaleatório próprio, para que as entradas sejam idênticas em
   qualquer máquina ou compilador. */
static unsigned long long semente = 20261029ULL;
static unsigned long long aleatorio(void) {
    semente = semente * 6364136223846793005ULL + 1442695040888963407ULL;
    return semente >> 33;
}
static void reiniciar_semente(void) { semente = 20261029ULL; }

/* Previsões das formas fechadas demonstradas no relatório. */

/* P1: T(n) = (21*3^k - 24*2^k + 5)/2, com n = 2^k. */
static unsigned long long previsto_p1(size_t n) {
    unsigned long long tres = 1, dois = 1;
    while (dois < n) { tres *= 3; dois *= 2; }
    return (21 * tres - 24 * dois + 5) / 2;
}

/* P1 direto: 2*n^2. */
static unsigned long long previsto_p1_direto(size_t n) {
    return 2ULL * n * n;
}

/* P2: T(n) = n * log_3(n), com n = 3^k. */
static unsigned long long previsto_p2(size_t n) {
    unsigned long long k = 0, p = 1;
    while (p < n) { p *= 3; k++; }
    return (unsigned long long)n * k;
}

/* P3: T(n) = n(n-1)/2. */
static unsigned long long previsto_p3(size_t n) {
    return (unsigned long long)n * (n - 1) / 2;
}

static void experimento_p1(const char *csv, int reps) {
    size_t tamanhos[] = { 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096 };
    size_t qtd = sizeof(tamanhos) / sizeof(tamanhos[0]), t, i;
    int r;

    for (t = 0; t < qtd; t++) {
        size_t n = tamanhos[t];
        long long *p = malloc(n * sizeof(long long));
        long long *q = malloc(n * sizeof(long long));
        long long *res = malloc((2 * n) * sizeof(long long));
        double tempos[MAX_REP];
        unsigned long long ops = 0;

        reiniciar_semente();
        for (i = 0; i < n; i++) p[i] = (long long)(aleatorio() % 1000);
        for (i = 0; i < n; i++) q[i] = (long long)(aleatorio() % 1000);

        for (r = 0; r < reps; r++) {
            double t0 = agora_segundos();
            operacoes = 0;
            karatsuba(p, q, n, res);
            tempos[r] = agora_segundos() - t0;
            ops = operacoes;
        }
        registrar(csv, 1, "karatsuba", "T(n) = 3T(n/2) + 6n - 5", n, ops,
                  previsto_p1(n), mediana(tempos, reps), reps);

        if (n <= 2048) {
            for (r = 0; r < reps; r++) {
                double t0 = agora_segundos();
                operacoes = 0;
                multiplicar_direto(p, q, n, res);
                tempos[r] = agora_segundos() - t0;
                ops = operacoes;
            }
            registrar(csv, 1, "direto", "T(n) = 2n^2 (sem recursao)", n, ops,
                      previsto_p1_direto(n), mediana(tempos, reps), reps);
        }
        free(p); free(q); free(res);
    }
}

static void experimento_p2(const char *csv, int reps) {
    size_t tamanhos[] = { 3, 9, 27, 81, 243, 729, 2187, 6561, 19683, 59049,
                          177147, 531441 };
    size_t qtd = sizeof(tamanhos) / sizeof(tamanhos[0]), t, i;
    int r;

    for (t = 0; t < qtd; t++) {
        size_t n = tamanhos[t];
        int *original = malloc(n * sizeof(int));
        int *v = malloc(n * sizeof(int));
        double tempos[MAX_REP];
        unsigned long long ops = 0;

        reiniciar_semente();
        for (i = 0; i < n; i++) original[i] = (int)(aleatorio() % 1000000);

        for (r = 0; r < reps; r++) {
            double t0;
            for (i = 0; i < n; i++) v[i] = original[i];
            t0 = agora_segundos();
            operacoes = 0;
            mergesort3(v, n);
            tempos[r] = agora_segundos() - t0;
            ops = operacoes;
        }
        for (i = 1; i < n; i++)
            if (v[i - 1] > v[i]) {
                fprintf(stderr, "ERRO: vetor nao ordenado para n = %zu\n", n);
                exit(EXIT_FAILURE);
            }
        registrar(csv, 2, "mergesort3", "T(n) = 3T(n/3) + n", n, ops,
                  previsto_p2(n), mediana(tempos, reps), reps);
        free(original); free(v);
    }
}

static void experimento_p3(const char *csv, int reps) {
    size_t tamanhos[] = { 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048,
                          4096, 8192 };
    size_t qtd = sizeof(tamanhos) / sizeof(tamanhos[0]), t, i;
    int r;

    for (t = 0; t < qtd; t++) {
        size_t n = tamanhos[t];
        long long *v = malloc(n * sizeof(long long));
        double tempos[MAX_REP];
        unsigned long long ops = 0;

        reiniciar_semente();
        for (i = 0; i < n; i++) v[i] = (long long)(aleatorio() % 100000000ULL);

        for (r = 0; r < reps; r++) {
            double t0 = agora_segundos();
            operacoes = 0;
            par_mais_proximo(v, 0, n);
            tempos[r] = agora_segundos() - t0;
            ops = operacoes;
        }
        registrar(csv, 3, "par_mais_proximo", "T(n) = 2T(n/2) + n^2/4", n, ops,
                  previsto_p3(n), mediana(tempos, reps), reps);
        free(v);
    }
}

int main(int argc, char *argv[]) {
    const char *csv = (argc >= 2) ? argv[1] : "resultados/resultados.csv";
    int reps = (argc >= 3) ? atoi(argv[2]) : 15;

    if (reps < 1 || reps > MAX_REP) reps = 15;

    printf("Executando os experimentos (%d repeticoes por ponto)...\n", reps);
    printf("  Problema 1: Karatsuba (Caso 1)\n");
    experimento_p1(csv, reps);
    printf("  Problema 2: MergeSort ternario (Caso 2)\n");
    experimento_p2(csv, reps);
    printf("  Problema 3: Par mais proximo (Caso 3)\n");
    experimento_p3(csv, reps);
    printf("Resultados gravados em %s\n", csv);
    return EXIT_SUCCESS;
}
