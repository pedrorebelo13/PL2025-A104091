def somador(sequencia):
    ativo = True
    soma = 0
    i = 0
    
    while i < len(sequencia):
        if i + 2 < len(sequencia) and sequencia[i].lower() == "o":
            if sequencia[i+1].lower() == "f" and sequencia[i+2].lower() == "f":
                ativo = False
                i += 2
            elif sequencia[i+1].lower() == "n":
                ativo = True
                i += 1
        
        elif ativo and sequencia[i].isdigit():
            numero = 0
            while i < len(sequencia) and sequencia[i].isdigit():
                numero = numero * 10 + int(sequencia[i])
                i += 1
            soma += numero
            continue  # Evita incremento extra de i
        
        elif ativo and sequencia[i] == "=":
            print(soma)
        
        i += 1

def main():
    nome_ficheiro = input("Digite o nome do ficheiro: ")
    try:
        with open(nome_ficheiro, 'r') as f:
            conteudo = f.read()
            somador(conteudo)
    except FileNotFoundError:
        print("Erro: O ficheiro nÃ£o foi encontrado.")
    except Exception as erro:
        print(f"Ocorreu um erro: {erro}")
        

if __name__ == "__main__":
    main()