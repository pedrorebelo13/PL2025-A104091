# TPC6 - Recursivo Descendente para Expressões Aritméticas
- **Data:** 25 de março 2025
- **Nome:** Pedro Manuel Macedo Rebelo
- **Número Mecanográfico:** a104091
<img src="../foto.png" alt="foto" width="300">

### Resumo 
A tarefa consistiu em desenvolver um parser LL(1) recursivo descendente em Python que reconheça expressões aritméticas e calcule o respetivo valor. As expressões podem incluir operadores de adição (+), subtração (-), multiplicação (*), parênteses e números inteiros.

### Guia de Utilização
Experimentando o Parser
Vamos testar o parser com algumas expressões aritméticas! Veja os exemplos abaixo e os resultados esperados:

Expressão
Resultado Esperado

2 + 3
5

67 - (2 * 3 * 4)
43

(9 - 2) * (13 - 4)
63


Nota: Se você inserir uma expressão inválida (como 2 + * 3), o parser exibirá uma mensagem de erro, como "Parsing error: Expected a number, found a plus operator".

Como Executar o Programa
Siga estes passos para usar o parser:

Execute o programa com o comando:  
python3 expression_parser.py


Digite uma expressão aritmética quando solicitado pelo programa.


### Resultados
[Parser](parser.py)

[Lexer](token.py)
