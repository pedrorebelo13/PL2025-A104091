# Representação da Árvore Sintática Abstrata (AST) e Análise Semântica Simples

class Nodo:
    pass

class Programa(Nodo):
    def __init__(self, nome, bloco):
        self.nome = nome
        self.bloco = bloco

class Bloco(Nodo):
    def __init__(self, decls, comandos):
        self.decls = decls
        self.comandos = comandos

class DeclaracaoVar(Nodo):
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

class ComandoAtribuicao(Nodo):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class ComandoSe(Nodo):
    def __init__(self, cond, entao, senao):
        self.cond = cond
        self.entao = entao
        self.senao = senao

class ComandoEnquanto(Nodo):
    def __init__(self, cond, corpo):
        self.cond = cond
        self.corpo = corpo

class ComandoPara(Nodo):
    def __init__(self, var, inicio, fim, corpo):
        self.var = var
        self.inicio = inicio
        self.fim = fim
        self.corpo = corpo

class ComandoEscrita(Nodo):
    def __init__(self, expr):
        self.expr = expr

class ComandoLeitura(Nodo):
    def __init__(self, var):
        self.var = var

class Expressao(Nodo):
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class BinOp(Expressao):
    def __init__(self, op, esq, dir):
        super().__init__('binop', None)
        self.op = op
        self.esq = esq
        self.dir = dir

class UnOp(Expressao):
    def __init__(self, op, expr):
        super().__init__('unop', None)
        self.op = op
        self.expr = expr

class Var(Expressao):
    def __init__(self, nome):
        super().__init__('var', nome)

class Const(Expressao):
    def __init__(self, valor):
        super().__init__('const', valor)

# Ambiente de símbolos simples para verificar declarações
class Ambiente:
    def __init__(self):
        self.vars = {}

    def declara(self, nome, tipo):
        if nome in self.vars:
            raise Exception(f"Variável '{nome}' já declarada.")
        self.vars[nome] = tipo

    def tipo(self, nome):
        if nome not in self.vars:
            raise Exception(f"Variável '{nome}' não declarada.")
        return self.vars[nome]

    def __contains__(self, nome):
        return nome in self.vars
