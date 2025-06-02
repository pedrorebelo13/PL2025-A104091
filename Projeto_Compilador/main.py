import sys
from lexer_pascal import lexer
from parser_pascal import parser
from gerador_ewvm import GeradorEWVM

# Verifica se um argumento foi fornecido
if len(sys.argv) < 2:
    print("Uso: python3 main.py <ficheiro.pas>")
    print("Exemplo: python3 main.py exemplo1.pas")
    print("\nO ficheiro deve estar na pasta 'exemplos/'")
    exit(1)

input_file = sys.argv[1]

try:
    with open(f'exemplos/{input_file}') as f:
        source_code = f.read()
except FileNotFoundError:
    print(f"Erro: O ficheiro 'exemplos/{input_file}' não foi encontrado.")
    print("Certifique-se que o ficheiro existe na pasta 'exemplos/'")
    exit(1)

print(f"Parsing source code from {input_file}...")
ast = parser.parse(source_code)

if ast is None:
    print("Parsing failed! Check the syntax errors above.")
    exit(1)

print("AST generated successfully!")

# Gera o código EWVM
print("\nGenerating EWVM code...")
gerador = GeradorEWVM()
gerador.gerar(ast)

print("\nCódigo EWVM gerado (com rótulos):")
for line in gerador.codigo:
    print(f"  {line}")



# Gera o arquivo de saída com o mesmo nome, mas extensão .ewvm
output_file = input_file.replace('.pas', '.ewvm')
with open(f'exemplos/{output_file}', 'w') as f:
    f.write('\n'.join(gerador.codigo))
print(f"\nCódigo EWVM gerado com sucesso em exemplos/{output_file}!")

print("\nPara executar o código EWVM gerado:")
print("1. Acesse o simulador EWVM em: https://ewvm.epl.di.uminho.pt/run")
print("2. Carregue o arquivo gerado")
print("3. Execute o programa no simulador")