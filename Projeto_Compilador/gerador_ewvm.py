class GeradorEWVM:
    def __init__(self):
        self.codigo = []
        self.tabela_simbolos = {}  # Dicionário para mapear nomes de variáveis a endereços
        self.proximo_endereco = 0  # Próximo endereço livre para variáveis
        self.contador_rotulos = 0

    def novo_rotulo(self):
        """Gera um novo rótulo único"""
        rotulo = f"L{self.contador_rotulos}"
        self.contador_rotulos += 1
        return rotulo
    
        # Modificar o método definir_rotulo para adicionar o rótulo sem ":" no final
    def definir_rotulo(self, rotulo):
        """Define um rótulo no ponto atual do código"""
        self.codigo.append(f"{rotulo}:")  # Adiciona com ":" para indicar que é um rótulo
    
    def gerar(self, nodo):
        if nodo is None:
            return
    
        if isinstance(nodo, tuple):
            self.gerar_tuple(nodo)
        else:
            metodo = getattr(self, f'gerar_{type(nodo).__name__}', self.nao_implementado)
            metodo(nodo)

    def nao_implementado(self, nodo):
        raise NotImplementedError(f'Geração não implementada para {type(nodo).__name__}')

    def gerar_Programa(self, nodo):
        self.codigo.append('START')
        self.gerar(nodo.bloco)
        self.codigo.append('STOP')

    def gerar_Bloco(self, nodo):
        for decl in nodo.decls:
            self.gerar(decl)
        for cmd in nodo.comandos:
            self.gerar(cmd)

    def gerar_DeclaracaoVar(self, nodo):
        # Aloca espaço para a variável (inicializa com 0)
        self.codigo.append('PUSHI 0')
        self.codigo.append(f'STOREG {nodo.endereco}')  # 'endereco' deve ser atribuído durante a análise semântica

    def gerar_ComandoAtribuicao(self, nodo):
        self.gerar(nodo.expr)
        self.codigo.append(f'STOREG {nodo.var.endereco}')

    def gerar_Const(self, nodo):
        self.codigo.append(f'PUSHI {nodo.valor}')

    def gerar_Var(self, nodo):
        self.codigo.append(f'PUSHG {nodo.endereco}')

    def gerar_BinOp(self, nodo):
        self.gerar(nodo.esq)
        self.gerar(nodo.dir)
        op = nodo.op
        if op == '+':
            self.codigo.append('ADD')
        elif op == '-':
            self.codigo.append('SUB')
        elif op == '*':
            self.codigo.append('MUL')
        elif op == 'div':
            self.codigo.append('DIV')
        elif op == 'mod':
            self.codigo.append('MOD')
        elif op == '=':
            self.codigo.append('EQUAL')
        elif op == '<':
            self.codigo.append('INF')
        elif op == '<=':
            self.codigo.append('INFEQ')
        elif op == '>':
            self.codigo.append('SUP')
        elif op == '>=':
            self.codigo.append('SUPEQ')
        elif op == 'and':
            self.codigo.append('AND')
        elif op == 'or':
            self.codigo.append('OR')
        else:
            raise NotImplementedError(f'Operador binário não suportado: {op}')

    def gerar_UnOp(self, nodo):
        self.gerar(nodo.expr)
        if nodo.op == '-':
            self.codigo.append('PUSHI -1')
            self.codigo.append('MUL')
        elif nodo.op == 'not':
            self.codigo.append('NOT')
        else:
            raise NotImplementedError(f'Operador unário não suportado: {nodo.op}')

    def gerar_tuple(self, nodo):
        if nodo[0] == 'programa':
            self.codigo.append('START')
            self.gerar(nodo[2])  # bloco
            self.codigo.append('STOP')
        elif nodo[0] == 'bloco':
            for decl in nodo[1]:  # declaracoes
                self.gerar(decl)
            for cmd in nodo[2]:  # comandos
                if cmd is not None: 
                    self.gerar(cmd)
        elif nodo[0] == 'declaracao_var':
            self.codigo.append('PUSHI 0')
        elif nodo[0] == 'declaracao_vars':
            # Lista de ids, mesmo tipo
            for id in nodo[1]:
                # Atribuir um endereço à variável
                self.tabela_simbolos[id] = self.proximo_endereco
                self.proximo_endereco += 1
                self.codigo.append('PUSHI 0')  # Inicializa com zero
        elif nodo[0] == 'rel':
                self.gerar(nodo[2])  # esquerda
                self.gerar(nodo[3])  # direita
                op = nodo[1]
                if op == '=':
                    self.codigo.append('EQUAL')
                elif op == '<>':
                    self.codigo.append('EQUAL')
                    self.codigo.append('NOT')
                elif op == '<':
                    self.codigo.append('INF')
                elif op == '<=':
                    self.codigo.append('INFEQ')
                elif op == '>':
                    self.codigo.append('SUP')
                elif op == '>=':
                    self.codigo.append('SUPEQ')
        elif nodo[0] == 'binop':
            self.gerar(nodo[2])  # esquerda
            self.gerar(nodo[3])  # direita
            op = nodo[1]
            if op == '+':
                self.codigo.append('ADD')
            elif op == '-':
                self.codigo.append('SUB')
            elif op == '*':
                self.codigo.append('MUL')
            elif op == 'div':
                self.codigo.append('DIV')
            elif op == 'mod':
                self.codigo.append('MOD')
            elif op == 'and':
                self.codigo.append('AND')
            elif op == 'or':
                self.codigo.append('OR')

        # Código para if
        elif nodo[0] == 'if':
            self.gerar(nodo[1])  # Condição
            
            rotulo_else = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()
            
            # Aqui está o problema - Use JZ com o rótulo sem ":", a definição terá o ":"
            self.codigo.append(f'JZ {rotulo_else}')
            
            # Bloco then
            self.gerar(nodo[2])
            
            if nodo[3] is not None:  # Tem bloco else
                self.codigo.append(f'JUMP {rotulo_fim}')
                # Aqui define o rótulo com ":"
                self.codigo.append(f'{rotulo_else}:')  # DEFINIÇÃO DO RÓTULO
                self.gerar(nodo[3])
                self.codigo.append(f'{rotulo_fim}:')   # DEFINIÇÃO DO RÓTULO
            else:
                self.codigo.append(f'{rotulo_else}:')  # DEFINIÇÃO DO RÓTULO
        elif nodo[0] == 'while':
            rotulo_inicio = self.novo_rotulo()
            rotulo_fim = self.novo_rotulo()
            self.codigo.append(f'{rotulo_inicio}:')  # Início do laço
            self.gerar(nodo[1])  # Condição
            self.codigo.append(f'JZ {rotulo_fim}')  # Salta para o fim se falso
            self.gerar(nodo[2])  # Corpo do laço
            self.codigo.append(f'JUMP {rotulo_inicio}')  # Volta para o início
            self.codigo.append(f'{rotulo_fim}:')  # Fim do laço
        elif nodo[0] == 'for':
            var_nome = nodo[1]  # Nome da variável de controle (i)
            var_endereco = -1
            
            # Verificar se a variável está na tabela de símbolos
            if var_nome in self.tabela_simbolos:
                var_endereco = self.tabela_simbolos[var_nome]
            else:
                # Criar variável on-the-fly se não existir
                var_endereco = self.proximo_endereco
                self.tabela_simbolos[var_nome] = var_endereco
                self.proximo_endereco += 1
                self.codigo.append('PUSHI 0')  # Aloca espaço
            
            # Inicializar a variável de controle
            self.gerar(nodo[2])  # Valor inicial (1)
            self.codigo.append(f'STOREG {var_endereco}')
            
            # Rótulos para o loop
            rotulo_inicio = self.novo_rotulo()  # Ex: L0
            rotulo_fim = self.novo_rotulo()     # Ex: L1
            
            # Início do loop - Definir rótulo
            self.codigo.append(f'{rotulo_inicio}:')  # L0:
            
            # Testar a condição de saída
            self.codigo.append(f'PUSHG {var_endereco}')  # Valor atual de i
            self.gerar(nodo[3])  # Valor final (n)
            self.codigo.append('INFEQ')  # Verifica se i <= n
            self.codigo.append(f'JZ {rotulo_fim}')  # Salta para L1 se i > n
            
            # Corpo do loop
            self.gerar(nodo[4])  # Gera o corpo do laço (fat := fat * i)
            
            # Incremento
            self.codigo.append(f'PUSHG {var_endereco}')  # Empilha i
            self.codigo.append('PUSHI 1')  # Empilha 1
            self.codigo.append('ADD')  # Incrementa i
            self.codigo.append(f'STOREG {var_endereco}')  # Armazena o novo valor de i
            
            # Voltar ao teste
            self.codigo.append(f'JUMP {rotulo_inicio}')  # Volta para L0
            
            # Rótulo de saída - Definir rótulo
            self.codigo.append(f'{rotulo_fim}:')  # L1:
        elif nodo[0] == 'atribuicao':
            # Gera o valor da expressão
            if isinstance(nodo[2], tuple) and nodo[2][0] == 'valor' and nodo[2][1] in ["true", "false"]:
                # Atribuição de booleanos como números
                valor_booleano = 1 if nodo[2][1] == "true" else 0
                self.codigo.append(f'PUSHI {valor_booleano}')
            else:
                self.gerar(nodo[2])  # Gera a expressão normalmente

            # Usar o endereço correto da variável
            if nodo[1] in self.tabela_simbolos:
                endereco = self.tabela_simbolos[nodo[1]]
                self.codigo.append(f'STOREG {endereco}')
            else:
                print(f"Warning: Undeclared variable {nodo[1]}")
                self.codigo.append('POP')  # Descartar o valor calculado
        elif nodo[0] == 'valor':
            if isinstance(nodo[1], int):
                self.codigo.append(f'PUSHI {nodo[1]}')
            elif isinstance(nodo[1], str):
                # Verificar se é uma variável
                if nodo[1] in self.tabela_simbolos:
                    endereco = self.tabela_simbolos[nodo[1]]
                    self.codigo.append(f'PUSHG {endereco}')
                else:
                    # É uma string literal
                    escaped_str = nodo[1].replace('"', '\\"')
                    self.codigo.append(f'PUSHS "{escaped_str}"')
        elif nodo[0] == 'writeln':
            if isinstance(nodo[1], list):
                for arg in nodo[1]:
                    self.gerar(arg)
                    # Determinar o comando correto com base no tipo
                    if isinstance(arg, tuple) and arg[0] == 'valor':
                        if isinstance(arg[1], int):
                            self.codigo.append('WRITEI')
                        elif isinstance(arg[1], str):
                            if arg[1] in self.tabela_simbolos:  # É uma variável
                                self.codigo.append('WRITEI')
                            else:  # É uma string
                                self.codigo.append('WRITES')
                    else:
                        self.codigo.append('WRITEI')  # Padrão para expressões
            else:
                self.gerar(nodo[1])
                # Determinar o comando correto
                if isinstance(nodo[1], tuple) and nodo[1][0] == 'valor':
                    if isinstance(nodo[1][1], int):
                        self.codigo.append('WRITEI')
                    else:
                        self.codigo.append('WRITES')
                else:
                    self.codigo.append('WRITEI')
            self.codigo.append('WRITELN')
        elif nodo[0] == 'write':
            if isinstance(nodo[1], list):
                for arg in nodo[1]:
                    self.gerar(arg)
                    # Determinar o comando correto com base no tipo
                    if isinstance(arg, tuple) and arg[0] == 'valor':
                        if isinstance(arg[1], int):
                            self.codigo.append('WRITEI')
                        elif isinstance(arg[1], str):
                            if arg[1] in self.tabela_simbolos:  # É uma variável
                                self.codigo.append('WRITEI')
                            else:  # É uma string
                                self.codigo.append('WRITES')
                    else:
                        self.codigo.append('WRITEI')  # Padrão para expressões
            else:
                self.gerar(nodo[1])
                # Determinar o comando correto
                if isinstance(nodo[1], tuple) and nodo[1][0] == 'valor':
                    if isinstance(nodo[1][1], int):
                        self.codigo.append('WRITEI')
                    else:
                        self.codigo.append('WRITES')
                else:
                    self.codigo.append('WRITEI')
        elif nodo[0] == 'readln':
            # READ empilha o endereço da string lida
            self.codigo.append('READ')
            # ATOI converte a string em inteiro
            self.codigo.append('ATOI')
            # STOREG armazena o inteiro na variável
            if nodo[1] in self.tabela_simbolos:
                endereco = self.tabela_simbolos[nodo[1]]
                self.codigo.append(f'STOREG {endereco}')
            else:
                print(f"Warning: Undeclared variable {nodo[1]}")
                self.codigo.append('POP')  # Descartar o valor lido
        else:
            print(f"Warning: Unhandled node type: {nodo[0]}")