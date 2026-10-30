/* problema2.c — Caso 2 do Teorema Mestre.
 *
 * MergeSort ternário: o vetor é dividido em TRÊS partes de tamanho n/3,
 * cada uma ordenada recursivamente, e as três partes ordenadas são
 * intercaladas em uma única passagem.
 *
 * Recorrência:  T(n) = 3*T(n/3) + n,  T(1) = T(0) = 0.
 * Operação elementar contada: cada posicionamento de um elemento no vetor
 * de saída durante a intercalação. Como a intercalação de três blocos que
 * somam n elementos posiciona exatamente n elementos, a contagem independe
 * dos valores de entrada.
 */

#include <stdlib.h>
#include <string.h>
#include "comum.h"

/* Intercala os três blocos ordenados [ini,c1), [c1,c2) e [c2,fim). */
static void intercalar3(int *v, int *aux, size_t ini, size_t c1, size_t c2,
                        size_t fim) {
    size_t i = ini, j = c1, k = c2, t = ini;

    while (i < c1 || j < c2 || k < fim) {
        int menor_valor = 0;
        int origem = -1;                /* 0, 1 ou 2: bloco do menor elemento */

        if (i < c1)                       { menor_valor = v[i]; origem = 0; }
        if (j < c2 && (origem < 0 || v[j] < menor_valor))
                                          { menor_valor = v[j]; origem = 1; }
        if (k < fim && (origem < 0 || v[k] < menor_valor))
                                          { menor_valor = v[k]; origem = 2; }

        operacoes++;                    /* um elemento posicionado na saída */
        aux[t++] = menor_valor;
        if (origem == 0) i++;
        else if (origem == 1) j++;
        else k++;
    }
    memcpy(v + ini, aux + ini, (fim - ini) * sizeof(int));
}

/* Ordena recursivamente o intervalo [ini, fim). */
static void mergesort3_aux(int *v, int *aux, size_t ini, size_t fim) {
    size_t tamanho = fim - ini, c1, c2;

    if (tamanho < 2) return;            /* caso base: 0 ou 1 elemento */

    c1 = ini + tamanho / 3;
    c2 = ini + (2 * tamanho) / 3;

    mergesort3_aux(v, aux, ini, c1);
    mergesort3_aux(v, aux, c1, c2);
    mergesort3_aux(v, aux, c2, fim);

    intercalar3(v, aux, ini, c1, c2, fim);
}

void mergesort3(int *v, size_t n) {
    int *aux;
    if (n < 2) return;
    aux = malloc(n * sizeof(int));
    if (!aux) exit(EXIT_FAILURE);
    mergesort3_aux(v, aux, 0, n);
    free(aux);
}
