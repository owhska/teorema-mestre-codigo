/* problema3.c — Caso 3 do Teorema Mestre.
 *
 * Par mais próximo em uma dimensão, por divisão e conquista com etapa de
 * combinação por força bruta: o vetor é dividido ao meio, a menor distância
 * de cada metade é obtida recursivamente, e a etapa de combinação compara
 * TODOS os pares formados por um elemento de cada metade.
 *
 * Recorrência:  T(n) = T(ceil(n/2)) + T(floor(n/2)) + ceil(n/2)*floor(n/2),
 *               T(1) = 0.
 * Operação elementar contada: cada comparação de distância entre dois
 * elementos na etapa de combinação. A contagem independe dos valores.
 *
 * O custo da combinação domina o das chamadas recursivas, o que caracteriza
 * o Caso 3 do Teorema Mestre.
 */

#include <stdlib.h>
#include "comum.h"

static long long valor_absoluto(long long x) { return x < 0 ? -x : x; }

/* Devolve a menor distância entre dois elementos de v[ini..fim). */
long long par_mais_proximo(const long long *v, size_t ini, size_t fim) {
    size_t meio, i, j;
    long long melhor, esquerda, direita, distancia;

    if (fim - ini < 2) return -1;       /* caso base: nenhum par existe */

    meio = ini + (fim - ini) / 2;

    esquerda = par_mais_proximo(v, ini, meio);
    direita  = par_mais_proximo(v, meio, fim);

    melhor = -1;
    if (esquerda >= 0) melhor = esquerda;
    if (direita >= 0 && (melhor < 0 || direita < melhor)) melhor = direita;

    /* Combinação: todos os pares com um elemento em cada metade. */
    for (i = ini; i < meio; i++)
        for (j = meio; j < fim; j++) {
            operacoes++;
            distancia = valor_absoluto(v[i] - v[j]);
            if (melhor < 0 || distancia < melhor) melhor = distancia;
        }

    return melhor;
}
