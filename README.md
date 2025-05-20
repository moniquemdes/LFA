# Simulador de AFD – Linguagens Formais e Autômatos

Este projeto implementa um simulador de **Autômato Finito Determinístico (AFD)** em linguagem **C**, permitindo a definição de estados, transições, alfabeto e a verificação se uma determinada string é aceita pelo autômato.

## 🧠 Objetivo

Trabalho desenvolvido para a disciplina de **Linguagens Formais e Autômatos** do curso de **Ciência da Computação** da **Universidade do Estado de Santa Catarina – UDESC**.

### Discentes:
- Monique Hemily Almeida Mendes  
- Thiago Luiz Watambak

---

## ⚙️ Funcionalidades

- Definição de estados, alfabeto, estado inicial e estados finais.
- Definição de transições no formato `estadoOrigem -> símbolo -> estadoDestino`.
- Leitura de string e validação segundo as regras do AFD.
- Retorno indicando se a string é **aceita** ou **rejeitada**.

---

## 🖥️ Como compilar e executar

### Compilação:
```bash
gcc simulador_afd.c -o simulador_afd
