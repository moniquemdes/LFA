//Monique Hemily Almeida Mendes
//Thiago Luiz Watambak
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TRANSICOES 100
#define MAX_ESTADOS 100
#define MAX_ALFABETO 100

// Estrutura de uma transição do AFD
typedef struct Transicao {
  int estadoOrigem;
  char variavel;
  int estadoDestino;
} Transicao;

// Estrutura do Autômato Finito Determinístico
typedef struct AFD {
  char alfabeto[MAX_ALFABETO];
  int tamanhoAlfabeto;
  int estados[MAX_ESTADOS];
  int estadoInicial;
  int estadosFinais[MAX_ESTADOS];
  int qtdEstados;
  int qtdEstadosFinais;
  Transicao transicoes[MAX_TRANSICOES];
  int qtdTransicoes;
} AFD;

// Verifica se uma string é aceita pelo AFD
int validarString(AFD afd, char *str) {
  int estadoAtual = afd.estadoInicial;
  int strLength = strlen(str);

  for (int i = 0; i < strLength; i++) {
    char c = str[i];
    int transicaoEncontrada = 0;

    // Verifica se existe uma transição para o estado atual com a variável atual
    for (int j = 0; j < afd.qtdTransicoes; j++) {
      if (afd.transicoes[j].estadoOrigem == estadoAtual &&
          afd.transicoes[j].variavel == c) {
        estadoAtual = afd.transicoes[j].estadoDestino;
        transicaoEncontrada = 1;
        break;
      }
    }

    // Se não existir transição para o estado atual com a variável atual, rejeita a string
    if (!transicaoEncontrada) {
      return 0;
    }
  }

  // Verifica se o estado atual é um estado final
  for (int i = 0; i < afd.qtdEstadosFinais; i++) {
    if (estadoAtual == afd.estadosFinais[i]) {
      return 1;
    }
  }

  return 0;
}

// Verifica se uma variável pertence ao alfabeto do AFD
int contemChar(char c, AFD afd) {
  for (int i = 0; i < afd.tamanhoAlfabeto; i++) {
    if (c == afd.alfabeto[i]) {
      return 1;
    }
  }
  return 0;
}

// Função principal
int main() {
  AFD afd;

  // Leitura do número de estados, estado inicial, número de transições e tamanho do alfabeto
  printf("Qual a quantidade de estados?\n");
  scanf("%d", &afd.qtdEstados);
  printf("\n");
  printf("Qual o estado inicial?\n");
  scanf("%d", &afd.estadoInicial);
  printf("\n");
  printf("Qual a quantidade de estados finais?\n");
  scanf("%d", &afd.qtdEstadosFinais);
  printf("\n");
  printf("Qual a quantidade de transições?\n");
  scanf("%d", &afd.qtdTransicoes);
  printf("\n");
  printf("Qual a quantidade de letras no alfabeto?\n");
  scanf("%d", &afd.tamanhoAlfabeto);
  printf("\n");
  // Leitura do alfabeto
  printf("Digite as letras do alfabeto separadas por espaço:\n");
  for (int i = 0; i < afd.tamanhoAlfabeto; i++) {
    scanf(" %c", &afd.alfabeto[i]);
  }
  printf("\n");
  // Leitura dos estados finais
  printf("Digite os estados finais separados por espaço:\n");
  for (int i = 0; i < afd.qtdEstadosFinais; i++) {
    scanf("%d", &afd.estadosFinais[i]);
  }
  printf("\n");
  // Leitura das transições
  printf("Digite as transições no formato Origem -> Variavel -> Destino (Exemplo: 0 -> a -> 1):\n");
  for (int i = 0; i < afd.qtdTransicoes; i++) {
    scanf("%d->%c->%d", &afd.transicoes[i].estadoOrigem, &afd.transicoes[i].variavel, &afd.transicoes[i].estadoDestino);
  }
  printf("\n");
  // Leitura da string a ser validada
  char str[100];
  printf("Digite a string a ser validada:\n");
  scanf("%s", str);
  printf("\n");
  // Validação da string
  int aceita = validarString(afd, str);

  if (aceita) {
    printf("String aceita pelo AFD\n");
  } else {
    printf("String rejeitada pelo AFD\n");
  }

  return 0;
}