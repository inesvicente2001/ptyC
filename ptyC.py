from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

grammar = '''
start: (declaracao|atribuicao|selecao|repeticao|chamadafuncao|deffuncao)*
startfunc: (declaracao|atribuicao|selecao|repeticao|chamadafuncao)*

declaracao: TIPO ((VAR PV)|atribuicao)

atribuicao: var IGUAL objeto PV
var: VAR (PRA (atomo) PRF)?
objeto: expressao
       |STRING
       |condicao
       |array
       |tuplo
       |lista
       |funcao

array: PRA (NUM (VIR NUM)*)? PRF
      |PRA (STRING (VIR STRING)*)? PRF

tuplo: PA ((objeto) (VIR objeto)*)? PF

lista: PRA ((objeto) (VIR objeto)*)? PRF

expressao: termo
          |expressao MAIS termo
          |expressao MENOS termo
termo: fator
      |termo VEZES fator
      |termo DIVIDIR fator
      |termo RESTO fator
fator: atomo
      |fator ELEVADO atomo
atomo: NUM
      |var

selecao: se
        |casos

se: SE PA logica PF CHAVA start CHAVF senao?
logica: condicao (LOGICO condicao)*
condicao: (expressao (SINAL expressao)?)
         |BOOL
         |expressao IN VAR
senao: SENAO CHAVA start CHAVF

casos: ESCOLHE PA var PF CHAVA caso* casofinal CHAVF
caso: (CASO PA (NUM|STRING) PF CHAVA start CHAVF)*
casofinal: CASO PA PF CHAVA start CHAVF

repeticao: enquanto
          |repetir
          |para

enquanto: ENQ PA logica PF CHAVA start CHAVF

repetir: REPETIR CHAVA start CHAVF ATE PA logica PF

para: PARA PA atribsimples PV logica PF CHAVA start CHAVF
atribsimples: VAR IGUAL NUM

chamadafuncao: funcao PV

funcao: cons
       |snoc
       |head
       |tail
       |func

cons: CONS PA argumentosc PF
argumentosc: objeto VIR argumentosh

snoc: SNOC PA argumentosc PF

head: HEAD PA argumentosh PF
argumentosh: VAR
            |lista

tail: TAIL PA argumentosh PF

func: FUNC PA argumentos PF
argumentos: (objeto (VIR objeto)*)?

deffuncao: DEF FUNC PA argumentos PF CHAVA startfunc retorna? CHAVF
retorna: RETORNA objeto

TIPO: "Int"|"Boolean"|"String"|"Array"|"Tuplo"|"Lista"
VAR: /[a-z]+[\w\d_]*/
PV: ";"
IGUAL: "="
NUM: "0".."9"+
PRA: "["
PRF: "]"
VIR: ","
MAIS: "+"
MENOS: "-"
VEZES: "*"
DIVIDIR: "/"
RESTO: "%"
ELEVADO: "^"
SE: "SE"
PA: "("
PF: ")"
CHAVA: "{"
CHAVF: "}"
LOGICO: " E "|" OU "
SINAL: "=="|"<"|"<="|">"|">="|"!="
BOOL: "TRUE"|"FALSE"
IN: " IN "
SENAO: "SENAO"
ESCOLHE: "ESCOLHE"
CASO: "CASO"
STRING: /"[^"]*"/
ENQ: "ENQ"
REPETIR: "REPETIR"
ATE: "ATE"
PARA: "PARA"
CONS: "cons"
SNOC: "snoc"
HEAD: "head"
TAIL: "tail"
FUNC: /(?!head[ (]|tail[ (]|cons[ (]|snoc[ (])([a-z]+[\w\d_]*)+/
DEF: "DEF "
RETORNA: "RETORNA "
%import common.WS
%ignore WS
'''

frase = open("teste.txt", "r").read()
#print(frase)
p = Lark(grammar)


parse_tree = p.parse(frase)