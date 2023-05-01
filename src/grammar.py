grammar = '''
program: statement*
statement: declaracao|atribuicao|selecao|repeticao|chamadafuncao|deffuncao|importar|comentario
body: statementbody*
statementbody: declaracao|atribuicao|selecao|repeticao|chamadafuncao|comentario

declaracao: TIPO ((var ";")|atribuicao)

atribuicao: var "=" objeto ";"
var: VAR ("[" (expressao) "]")?
objeto: expressao
       |STRING
       |condicao
       |array
       |tuplo
       |lista
       |funcao

array: "{" (NUM ("," NUM)*)? "}"
      |"{" (STRING ("," STRING)*)? "}"

tuplo: "(" ((objeto) ("," objeto)*)? ")"

lista: "[" ((objeto) ("," objeto)*)? "]"

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

se: "SE" "(" logica ")" "{" body "}" senao?
logica: condicao (logico condicao)*
condicao: (expressao (SINAL expressao)?)
         |BOOL
         |expressao EM VAR
logico: E
       |OU
senao: "SENAO" "{" body "}"

casos: "ESCOLHE" "(" var ")" "{" caso* casofinal "}"
caso: ("CASO" "(" (NUM|STRING) ")" "{" body "}")*
casofinal: "CASO" "(" ")" "{" body "}"

repeticao: enquanto
          |repetir
          |para

enquanto: "ENQ" "(" logica ")" "{" body "}"

repetir: "REPETIR" "{" body "}" "ATE" "(" logica ")"

para: "PARA" "(" var " DE " varlista ")" "{" body "}"
varlista: var
         |lista

chamadafuncao: funcao ";"

funcao: cons
       |snoc
       |head
       |tail
       |func

cons: "cons" "(" argumentosc ")"
argumentosc: objeto "," argumentosh

snoc: "snoc" "(" argumentosc ")"

head: "head" "(" argumentosh ")"
argumentosh: VAR
            |lista

tail: "tail" "(" argumentosh ")"

func: FUNC "(" argumentos ")"
argumentos: (objeto ("," objeto)*)?

deffuncao: "DEF " TIPO FUNC "(" argumentos ")" "{" body retorna? "}"
retorna: "RETORNA " objeto ";"

importar: "IMPORTA" "{" IMPORTADO "}"

comentario: ":-" TEXTO "-:"

TIPO: "Int"|"Boolean"|"String"|"Array"|"Tuplo"|"Lista"
VAR: /[a-z]+[\w\d_]*/
NUM: "0".."9"+
MAIS: "+"
MENOS: "-"
VEZES: "*"
DIVIDIR: "/"
RESTO: "%"
ELEVADO: "^"
E: " E "
OU: " OU "
SINAL: "=="|"<"|"<="|">"|">="|"!="
BOOL: "VERDADE"|"FALSO"
STRING: /"[^"]*"/
FUNC: /(?!head[ (]|tail[ (]|cons[ (]|snoc[ (])([a-z]+[\w\d_]*)+/
IMPORTADO: /[\w\d\.\-_]+/
TEXTO: /[^-]+|(-[^:])+/
EM: " EM "
%import common.WS
%ignore WS
'''