/* problema1.c — Caso 1 do Teorema Mestre.
 *
 * Multiplicação de polinômios pelo algoritmo de Karatsuba.
 *
 * Dados dois polinômios de n coeficientes, P e Q, o algoritmo os divide ao
 * meio, P = P0 + P1*x^m e Q = Q0 + Q1*x^m com m = n/2, e obtém o produto
 * com apenas TRÊS multiplicações de tamanho m, em vez das quatro do método
 * direto:
 *     z0 = P0*Q0
 *     z2 = P1*Q1
 *     z1 = (P0+P1)*(Q0+Q1) - z0 - z2
 *     PQ = z0 + z1*x^m + z2*x^(2m)
 *
 * Recorrência:  T(n) = 3*T(n/2) + 6n - 5,  T(1) = 1.
 * Operação elementar contada: cada soma, subtração ou multiplicação de
 * coeficientes. Cópias de memória não são contadas.
 */

#include <stdlib.h>
#include <string.h>
#include "comum.h"

/* Multiplicação direta, O(n^2), usada como referência experimental. */
void multiplicar_direto(const long long *p, const long long *q, size_t n,
                        long long *res) {
    size_t i, j;
    for (i = 0; i < 2 * n - 1; i++) res[i] = 0;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++) {
            operacoes += 2;             /* uma multiplicação e uma soma */
            res[i + j] += p[i] * q[j];
        }
}

/* Karatsuba. Requer n potência de 2. O vetor res recebe 2n-1 coeficientes. */
void karatsuba(const long long *p, const long long *q, size_t n,
               long long *res) {
    size_t m, i, tam;
    long long *soma_p, *soma_q, *z0, *z1, *z2;

    if (n == 1) {                       /* caso base da recursão */
        operacoes += 1;
        res[0] = p[0] * q[0];
        return;
    }

    m = n / 2;
    tam = 2 * m - 1;                    /* coeficientes de cada produto parcial */

    soma_p = malloc(m * sizeof(long long));
    soma_q = malloc(m * sizeof(long long));
    z0 = malloc(tam * sizeof(long long));
    z1 = malloc(tam * sizeof(long long));
    z2 = malloc(tam * sizeof(long long));
    if (!soma_p || !soma_q || !z0 || !z1 || !z2) exit(EXIT_FAILURE);

    /* P0+P1 e Q0+Q1: 2m operações. */
    for (i = 0; i < m; i++) { operacoes++; soma_p[i] = p[i] + p[i + m]; }
    for (i = 0; i < m; i++) { operacoes++; soma_q[i] = q[i] + q[i + m]; }

    /* As três chamadas recursivas, todas de tamanho n/2. */
    karatsuba(p, q, m, z0);
    karatsuba(p + m, q + m, m, z2);
    karatsuba(soma_p, soma_q, m, z1);

    /* z1 = (P0+P1)(Q0+Q1) - z0 - z2: 2*(2m-1) operações. */
    for (i = 0; i < tam; i++) { operacoes++; z1[i] -= z0[i]; }
    for (i = 0; i < tam; i++) { operacoes++; z1[i] -= z2[i]; }

    /* Combinação: res = z0 + z1*x^m + z2*x^(2m), 3*(2m-1) operações. */
    for (i = 0; i < 2 * n - 1; i++) res[i] = 0;
    for (i = 0; i < tam; i++) { operacoes++; res[i] += z0[i]; }
    for (i = 0; i < tam; i++) { operacoes++; res[i + m] += z1[i]; }
    for (i = 0; i < tam; i++) { operacoes++; res[i + 2 * m] += z2[i]; }

    free(soma_p); free(soma_q); free(z0); free(z1); free(z2);
}
