/* comum.h — contador de operações, medição de tempo e gravação do CSV. */
#ifndef COMUM_H
#define COMUM_H

#include <stddef.h>

/* Contador global de operações elementares. Cada algoritmo o incrementa
   exatamente uma vez por operação elementar, conforme definido no relatório. */
extern unsigned long long operacoes;

/* Relógio monotônico de alta resolução (Windows e Linux/macOS). */
double agora_segundos(void);

/* Mediana de um vetor de tempos (ordena uma cópia). */
double mediana(double *v, int n);

/* Acrescenta uma linha ao arquivo CSV de resultados, criando o cabeçalho
   se o arquivo ainda não existir. Todos os experimentos dos três problemas
   são gravados neste mesmo arquivo. */
void registrar(const char *caminho, int problema, const char *algoritmo,
               const char *recorrencia, size_t n, unsigned long long ops,
               unsigned long long previsto, double tempo_s, int repeticoes);

#endif
