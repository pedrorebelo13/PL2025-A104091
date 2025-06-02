# TPC5 - Máquina de Vending

- **Data:** 10 de março 2025
- **Nome:** Pedro Manuel Macedo Rebelo
- **Número Mecanográfico:** a104091
<img src="../foto.png" alt="foto" width="300">

### Resumo 
Desenvolver um programa em Python que simula uma máquina de vending, permitindo listar produtos, inserir moedas, selecionar produtos, adicionar produtos ao stock e sair.

##Guia de Uso da Máquina de Vending
###Instruções de Uso

##Este guia explica de forma simples e prática como utilizar cada comando da máquina de vending.
###Comando LISTAR

O que faz: Apresenta uma tabela com todos os produtos disponíveis, mostrando o código, nome, estoque e preço de cada um.

###Comando MOEDA

O que faz: Permite adicionar moedas para aumentar seu saldo. As moedas aceitas são: 1e, 50c, 20c, 10c, 5c, 2c, 1c.
Como usar: Digite MOEDA seguido das moedas que deseja inserir, separadas por vírgulas.
Exemplo: MOEDA 50c, 10c, 5cIsso adiciona 50 cêntimos, 10 cêntimos e 5 cêntimos, totalizando 65 cêntimos no seu saldo.

###Comando SELECIONAR

O que faz: Permite escolher um produto pelo seu código. Se houver estoque e saldo suficiente, a máquina entrega o produto e atualiza o saldo.
Como usar: Digite SELECIONAR seguido do código do produto.
Exemplo: SELECIONAR A01A máquina verifica:  
Se o código A01 existe (neste caso, é “Water 500ml”).  
Se há estoque (por exemplo, 10 unidades).  
Se o seu saldo (por exemplo, 85 cêntimos) cobre o preço (€0,70).Se tudo estiver correto, você verá: “Dispensing product ‘Water 500ml’” e o saldo será atualizado (ex.: Saldo = €0 15c).Caso o saldo seja insuficiente ou o produto esteja esgotado, uma mensagem de erro será exibida.


###Comando ADICIONAR

O que faz: Adiciona um novo produto ao estoque ou atualiza a quantidade e o preço de um produto existente.
Como usar: Digite ADICIONAR seguido do código, nome, quantidade e preço do produto.
Exemplo: ADICIONAR B03 Cookies 5 1.5Isso adiciona o produto “Cookies” com o código B03, 5 unidades, ao preço de €1,50.A máquina confirma a adição ou atualização com uma mensagem.

###Comando SAIR

O que faz: Encerra a interação, devolve o troco (se houver) e salva o estoque atualizado no arquivo stock.json.
Como usar: Digite SAIR e pressione Enter.
Exemplo: Se o saldo for 72 cêntimos, a máquina dirá: “Please take your change: 50c, 20c, 2c” e depois “Goodbye! See you next time.”.

##Funcionalidades da Solução
###A solução implementada oferece as seguintes funcionalidades:

Armazenamento contínuo do estoque em um arquivo JSON.
Interface de usuário interativa que suporta os comandos LISTAR, MOEDA, SELECIONAR, ADICIONAR e SAIR.




### Resultados
[Resolução](TPC5.py)
[stock json](stock.json)
