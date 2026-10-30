/* comum.c — implementação dos utilitários comuns aos três problemas. */

#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "comum.h"

unsigned long long operacoes = 0;

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
double agora_segundos(void) {
    LARGE_INTEGER freq, cont;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&cont);
    return (double)cont.QuadPart / (double)freq.QuadPart;
}
#else
double agora_segundos(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}
#endif

static int cmp_double(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

double mediana(double *v, int n) {
    qsort(v, (size_t)n, sizeof(double), cmp_double);
    return (n % 2) ? v[n / 2] : (v[n / 2 - 1] + v[n / 2]) / 2.0;
}

void registrar(const char *caminho, int problema, const char *algoritmo,
               const char *recorrencia, size_t n, unsigned long long ops,
               unsigned long long previsto, double tempo_s, int repeticoes) {
    FILE *fp = fopen(caminho, "a+");
    if (!fp) { perror("ERRO ao abrir o arquivo de resultados"); return; }
    fseek(fp, 0, SEEK_END);
    if (ftell(fp) == 0)
        fprintf(fp, "problema,algoritmo,recorrencia,n,operacoes,previsto,"
                    "diferenca,tempo_mediano_s,repeticoes\n");
    fprintf(fp, "%d,%s,\"%s\",%zu,%llu,%llu,%lld,%.9f,%d\n",
            problema, algoritmo, recorrencia, n, ops, previsto,
            (long long)ops - (long long)previsto, tempo_s, repeticoes);
    fclose(fp);
}
