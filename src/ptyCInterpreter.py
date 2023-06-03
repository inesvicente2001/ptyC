from lark import Discard
from lark import Lark,Token,Tree
from lark.visitors import Interpreter
import json

class PtyCInterpreter(Interpreter):
    def __init__(self):
        self.programa = {}
        self.info = {}
        self.info["variaveis"] = {}
        self.info["instrucoes"] = {
            "atribuicoes": 0,
            "leitura e escrita": 0,
            "condicionais": 0,
            "ciclos": 0,
        }
        self.info["aninhamentos"] = {
            "ciclos_dentro_de_ciclos": 0,
            "condicionais_dentro_de_condicionais": 0,
            "ciclos_dentro_de_condicionais": 0,
            "condicionais_dentro_de_ciclos": 0,
        }
        self.info["imports"] = []



        self.is_declaracao = False #para saber se estamos a declarar uma variavel
        self.tipo_variavel = "" #para saber o tipo de variavel que estamos a declarar
        self.is_variavel = False #para saber se estamos a declarar uma variavel
        self.variavel_atual = [] #para guardar o nome da variavel que estamos a declarar

        self.is_atribuicao = False #para saber se estamos a atribuir uma variavel
        self.atribuicao_expression = "" #para guardar a expressao que estamos a atribuir

        self.is_objeto = False

        self.is_expressao = False #para saber se estamos a fazer uma expressao

        self.lista_counter = 0 #contador de listas
        self.tuplo_counter = 0 #contador de tuplos
        self.array_counter = 0 #contador de arrays
        self.function_counter = 0 #contador de funcoes

        self.is_condicional = False #para saber se estamos a fazer uma condicional
        
        self.expressao_counter = 0 #contador de expressoes
        self.ciclo_counter = 0 #contador de ciclos
        self.condicao_counter = 0 #contador de condicoes
        self.last_aninhamento = "" #guardar o último aninhamento para saber o tipo de aninhamento em que estamos


    def cria_variavel(self,value, declaracao, inicializacao, utilizacao, redeclaracao, tipo_de_variavel, valores):
        # variavel: VARIAVEL
        self.info["variaveis"][value] = {
            "foi_declarada": declaracao,
            "foi_inicializada": inicializacao,
            "foi_utilizada": utilizacao,
            "foi_redeclarada": redeclaracao,
            "tipo_da_variavel": tipo_de_variavel,
            "valores": valores
        }

    def program(self,program):
        # program: statement*
        self.programa["programa"] = []
        for statement in program.children:
            stat = self.visit(statement)
            self.programa["programa"].append(stat)

        return self.programa, self.info

    def statement(self,statement):
        # statement: declaracao|atribuicao|selecao|repeticao|chamadafuncao|deffuncao|importar|comentario
        stat = {}
        for statement in statement.children:
            stat[statement.data.value] = self.visit(statement)
        return stat


    def funcao(self,funcao):
        # funcao: cons
        #        |snoc
        #        |head
        #        |tail
        #        |func
        self.function_counter += 1
        func = []
        for f in funcao.children:
            if(type(f) == Tree):
                func.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    func.append({f.type: f})

        self.function_counter -= 1
        if not self.is_atribuicao:
            self.variavel_atual = []
            self.atribuicao_expression = ""
        return func


    def cons(self,cons):
        # cons: "cons" "(" argumentosc ")"
        cs = []
        self.atribuicao_expression += "cons("
        for c in cons.children:
            if(type(c) == Tree):
                cs.append({c.data: self.visit(c)})
            else:
                if (type(c) == Token):
                    cs.append({c.type: c})
        self.atribuicao_expression += ")"

        return cs

    def argumentosc(self,argumentosc):
        # argumentosc: objeto "," argumentosh
        arg = []
        for a in argumentosc.children:
            if(type(a) == Tree):
                arg.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    arg.append({a.type: a})

        return arg

    def snoc(self,snoc):
        # snoc: "snoc" "(" argumentosc ")"
        sc = []
        
        self.atribuicao_expression += "snoc("
        for s in snoc.children:
            if(type(s) == Tree):
                sc.append({s.data: self.visit(s)})
            else:
                if (type(s) == Token):
                    sc.append({s.type: s})
        self.atribuicao_expression += ")"

        return sc

    def head(self,head):
        # head: "head" "(" argumentosh ")"
        hd = []
        self.atribuicao_expression += "head("
        for h in head.children:
            if(type(h) == Tree):
                hd.append({h.data: self.visit(h)})
            else:
                if (type(h) == Token):
                    hd.append({h.type: h})
        self.atribuicao_expression += ")"

        return hd

    def tail(self,tail):
        # tail: "tail" "(" argumentosh ")"
        tl = []
        self.atribuicao_expression += "tail("
        
        for t in tail.children:
            if(type(t) == Tree):
                tl.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tl.append({t.type: t})
        self.atribuicao_expression += ")"

        return tl

    def argumentosh(self,argumentosh):
        # argumentosh: VAR
        #            |lista
        arg = []
        for a in argumentosh.children:
            if(type(a) == Tree):
                arg.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    self.atribuicao_expression += a.value
                    arg.append({a.type: a})

        return arg

    def func(self,func):
        # func: FUNC "(" argumentos ")"
        fun_ = []
    
        
        for f in func.children:
            if(type(f) == Tree):
                fun_.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    fun_.append({f.type: f})
                    self.atribuicao_expression += f.value + "("
        
        if self.atribuicao_expression[-2] == ",":
            self.atribuicao_expression = self.atribuicao_expression[:-2]
        self.atribuicao_expression += ")"

        return fun_

    def argumentos(self,argumentos):
        # argumentos: (objeto ("," objeto)*)?
        arg = []
        for a in argumentos.children:
            if(type(a) == Tree):
                arg.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    arg.append({a.type: a})

        return arg

    def declaracao(self,declaracao):
        # declaracao: TIPO ((VAR ";")|atribuicao)
        self.is_declaracao = True
        dec = []
        for d in declaracao.children:
            if(type(d) == Tree):
                dec.append({d.data: self.visit(d)})

            else:
                if (type(d) == Token):
                    self.tipo_variavel = d.value
                    dec.append({d.type: d})
        self.variavel_atual = []
        self.tipo_variavel = ""
        self.is_declaracao = False
        return dec

    def atribuicao(self,atribuicao):
        # atribuicao: var "=" objeto ";"
        self.is_atribuicao = True
        self.info["instrucoes"]["atribuicoes"] += 1
        atrib = []


        for a in atribuicao.children:
            if(type(a) == Tree):
                if a.data == "var":
                    atrib.append({a.data: self.visit(a)})
    
                elif a.data == "objeto":
                    atrib.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    atrib.append({a.type: a})
            
        self.is_atribuicao = False


        return atrib

    def var(self,var):
        # var: VAR ("[" (expressao) "]")?
        self.is_var = True
        variable = []
        print(len(var.children))
        for v in var.children:

            if(type(v) == Tree):
                if self.is_objeto:
                    self.atribuicao_expression += "["
                variable.append({v.data: self.visit(v)})
                if self.is_objeto:
                    self.atribuicao_expression += "]"
            else:
                if (type(v) == Token):
                    self.variavel_atual.append(v.value)
                    if self.is_atribuicao: 
                        if v.value != self.variavel_atual[0]:
                            if not self.is_expressao or self.is_objeto:
                                self.atribuicao_expression += v.value
                        elif self.is_objeto:
                            self.atribuicao_expression += v.value   
                    declaracao = False
                    redeclaracao = False
                    inicializacao = False
                    utilizacao = False
                    valores = []
                    if self.is_declaracao or self.is_atribuicao or self.is_condicional or self.function_counter > 0:
                        if v.value in self.info["variaveis"]:
                            if not self.is_objeto and not self.is_expressao and self.is_declaracao and self.info["variaveis"][v.value]["foi_declarada"]:
                                self.info["variaveis"][v.value]["foi_redeclarada"] = True
                            if self.is_objeto:
                                self.info["variaveis"][v.value]["foi_utilizada"] = True
                            if self.is_declaracao and not self.is_objeto and not self.is_expressao:
                                self.info["variaveis"][v.value]["tipo_da_variavel"] = self.tipo_variavel
                        else:
                            utilizacao = self.is_objeto
                            tipo = self.tipo_variavel
                            if  not self.is_objeto and not self.is_expressao and self.is_declaracao:
                                declaracao = True
                            else:
                                tipo = ""
                            self.cria_variavel(v.value, declaracao, inicializacao, utilizacao, redeclaracao, tipo, valores)
                        if not self.is_objeto and self.is_expressao:
                            self.info["variaveis"][v.value]["foi_utilizada"] = True
                    if self.is_declaracao and not self.is_objeto and not self.is_expressao:
                        self.info["variaveis"][v.value]["foi_declarada"] = True


                    variable.append({v.type: v})
        self.is_var = False

        return variable

    def objeto(self,objeto):
        # objeto: expressao
        #        |STRING
        #        |condicao
        #        |array
        #        |tuplo
        #        |lista
        #        |funcao
        self.is_objeto = True
        obj = []
        for o in objeto.children:
            if(type(o) == Tree):
            
                obj.append({o.data: self.visit(o)})
                    
            else:
                if (type(o) == Token):
                    print(o.type)
                    if self.lista_counter > 0 or self.array_counter > 0 or self.tuplo_counter > 0:
                        self.atribuicao_expression += o.value
                    else :
                        self.atribuicao_expression = o.value
                    obj.append({o.type: o}) 
            if self.lista_counter == 0 and self.array_counter == 0 and  self.tuplo_counter == 0 and self.function_counter == 0: 
                if self.is_atribuicao:

                    if self.variavel_atual[0] in self.info["variaveis"]:
                        self.info["variaveis"][self.variavel_atual[0]]["foi_inicializada"] = True
                        self.info["variaveis"][self.variavel_atual[0]]["valores"].append(self.atribuicao_expression)
                    else:
                        inicializacao = True
                        declaracao = False
                        redeclaracao = False
                        utilizacao = False
                        tipo = ""
                        valores = []
                        self.cria_variavel(self.variavel_atual[0], declaracao, inicializacao, utilizacao, redeclaracao, tipo, valores)
                        self.info["variaveis"][self.variavel_atual[0]]["valores"].append(self.atribuicao_expression)
                    self.atribuicao_expression = ""
                if self.is_declaracao and not self.is_objeto and not self.is_expressao:
                    self.info["variaveis"][self.variavel_atual[0]]["foi_declarada"] = True
                    self.info["variaveis"][self.variavel_atual[0]]["tipo_da_variavel"] = self.tipo_variavel
                self.variavel_atual = []
            else:
                self.atribuicao_expression += ", "
        self.is_objeto = False
        return obj

    def lista(self,lista):
        # lista: "[" ((objeto) ("," objeto)*)? "]"
        self.lista_counter += 1
        list = []
        self.atribuicao_expression += "["
        for l in lista.children:
            if(type(l) == Tree):
                list.append({l.data: self.visit(l)})
            else:
                if (type(l) == Token):
                    list.append({l.type: l})

        if len(self.atribuicao_expression) > 2:
            if self.atribuicao_expression[-2] == ",":
                self.atribuicao_expression = self.atribuicao_expression[:-2]
        self.atribuicao_expression += "]"
        self.lista_counter -= 1

        return list


    def array(self,array):
        # array: "[" (NUM ("," NUM)*)? "]"
        #       |"[" (STRING ("," STRING)*)? "]"
        
        self.array_counter += 1
        arr = []
        self.atribuicao_expression += "{"
        for a in array.children:
            print(a)
            if(type(a) == Tree):

                arr.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    arr.append({a.type: a})
                    self.atribuicao_expression += a.value + ", "

        if len(self.atribuicao_expression) > 2:
            if self.atribuicao_expression[-2] == ",":
                self.atribuicao_expression = self.atribuicao_expression[:-2]
        self.atribuicao_expression += "}"
        self.array_counter -= 1
        return arr


    def tuplo(self,tuplo):
        # tuplo: "(" ((objeto) ("," objeto)*)? ")"
        self.tuplo_counter += 1
        tup = []
        self.atribuicao_expression += "("
    
        for t in tuplo.children:
            if(type(t) == Tree):
                tup.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tup.append({t.type: t})


        if len(self.atribuicao_expression) > 2:
            if self.atribuicao_expression[-2] == ",":
                self.atribuicao_expression = self.atribuicao_expression[:-2]
        self.atribuicao_expression += ")"
        self.tuplo_counter -= 1
        return tup


    def selecao(self,selecao):
        # selecao: se
        #         |casos

        self.condicao_counter += 1
        if self.condicao_counter > 1:
            if self.ciclo_counter > 1:
                if self.last_aninhamento == "ciclo":
                    self.info["aninhamentos"]["condicionais_dentro_de_ciclos"] += 1
                else:
                    self.info["aninhamentos"]["condicionais_dentro_de_condicionais"] += 1
            else:
                self.info["aninhamentos"]["condicionais_dentro_de_condicionais"] += 1
        self.last_aninhamento = "condicao"

        self.info["instrucoes"]["condicionais"] += 1
        sel = {}
        sel[selecao.children[0].data.value] = self.visit(selecao.children[0])

        self.condicao_counter -= 1
        return sel

    def se(self,se):
        # se: "SE" "(" logica ")" "{" body "}" senao?
        self.is_condicional = True
        sel = {}
        for se in se.children:
            sel[se.data.value] = self.visit(se)
        self.is_condicional = False
        self.variavel_atual = []
        return sel

    def logica(self,logica):
        # logica: condicao (logico condicao)*
        log = []
        for logica in logica.children:
            log.append(self.visit(logica))
        self.variavel_atual = []
        self.atribuicao_expression = ""
        return log

    def body(self,body):
        # body: statementbody*
        bod = []
        for b in body.children:
            bod.append(self.visit(b))
        return bod


    def casos(self,casos):
        # casos: "ESCOLHE" "(" var ")" "{" caso* casofinal "}"
        cas = []
        for c in casos.children:
            cas.append({c.data : self.visit(c)})
        return cas

    def caso(self,caso):
        # caso: ("CASO" "(" (NUM|STRING) ")" "{" body "}")*
        cas = []
        self.variavel_atual = []
        for c in caso.children:
            if(type(c) == Tree):
                cas.append({c.data: self.visit(c)})
            else:
                if (type(c) == Token):
                    cas.append({c.type: c})
        return cas


    def casofinal(self,casofinal):
        # casofinal: "CASO" "(" ")" "{" body "}"
        casf = []
        for cf in casofinal.children:
            if(type(cf) == Tree):
                casf.append({cf.data: self.visit(cf)})
            else:
                if (type(cf) == Token):
                    casf.append({cf.type: cf})
        return casf
        

    def deffuncao(self,deffuncao):
        # deffuncao: "DEF " TIPO FUNC "(" argumentos ")" "{" body retorna? "}"
        fun = []
        for df in deffuncao.children:
            if(type(df) == Tree):
                fun.append({df.data: self.visit(df)})
            else:
                if (type(df) == Token):
                    fun.append({df.type: df})
        return fun


    def repeticao(self, repeticao):
        # repeticao: enquanto
        #           |repetir
        #           |para

        self.ciclo_counter += 1
        if self.ciclo_counter > 1:
            if self.condicao_counter > 1:
                if self.last_aninhamento == "condicao":
                    self.info["aninhamentos"]["ciclo_dentro_de_condicao"] += 1
                else:
                    self.info["aninhamentos"]["ciclo_dentro_de_ciclo"] += 1 
            else:
                self.info["aninhamentos"]["ciclo_dentro_de_ciclo"] += 1
        self.last_aninhamento = "ciclo"


        self.info["instrucoes"]["ciclos"] += 1
      
        rep = {}
        for r in repeticao.children:
            rep[r.data.value] = self.visit(r)
        self.ciclo_counter -= 1
        return rep

    def enquanto(self,enquanto):
        # enquanto: "ENQ" "(" logica ")" "{" body "}"
        enq = []
        for e in enquanto.children:
            if(type(e) == Tree):
                enq.append({e.data: self.visit(e)})
            else:
                if (type(e) == Token):
                    enq.append({e.type: e})

        return enq

    def repetir(self,repetir):
        # repetir: "REPETIR" "{" body "}" "ATE" "(" logica ")"
        rep = []
        for r in repetir.children:
            if(type(r) == Tree):
                rep.append({r.data: self.visit(r)})
            else:
                if (type(r) == Token):
                    rep.append({r.type: r})

        return rep

    def para(self,para):
        # para: "PARA" "(" var " DE " varlista ")" "{" body "}"
        par = []
        for p in para.children:
            if(type(p) == Tree):
                par.append({p.data: self.visit(p)})
            else:
                if (type(p) == Token):
                    par.append({p.type: p})

        return par

    def varlista(self,varlista):
        # varlista : var
        #           |lista
        
        vl = []
        for v in varlista.children:
            if(type(v) == Tree):
                vl.append({v.data: self.visit(v)})
            else:
                if (type(v) == Token):
                    vl.append({v.type: v})

        return vl

    def retorna(self,retorna):
        # retorna: "RETORNA " objeto ";"
        ret = []
        for r in retorna.children:
            if(type(r) == Tree):
                ret.append({r.data: self.visit(r)})
            else:
                if (type(r) == Token):
                    ret.append({r.type: r})
        


        return ret



    def statementbody(self,statementbody):
        # statementbody: declaracao|atribuicao|selecao|repeticao|chamadafuncao|comentario
        stat = {}
        for statementbody in statementbody.children:
            stat[statementbody.data.value] = self.visit(statementbody)
        return stat

    def condicao(self,condicao):
        # condicao: (expressao (SINAL expressao)?)
        #          |BOOL
        #          |expressao " EM " VAR
        cond = []
        for c in condicao.children:
            if (type(c) == Tree and c.data == "expressao"):
                cond.append({c.data : self.visit(c)})
            else:
                if (type(c) == Token):
                    self.atribuicao_expression += f" {c.value} "
                    cond.append({c.type: c})
        return cond



    def logico(self,logico):
        # logico: "E"|"OU"
        return {logico.data.value: logico.children[0].value}

    def expressao(self,expressao):
        # expressao: termo
        #           |expressao MAIS termo
        #           |expressao MENOS termo
        self.is_expressao = True
        exp = []
        self.expressao_counter += 1
        for e in expressao.children:
            if(type(e) == Tree):
                exp.append({e.data: self.visit(e)})
            else:
                 if (type(e) == Token):
                
                    if self.is_atribuicao and self.is_objeto:
                        self.atribuicao_expression += f" {e.value} "
                    exp.append({e.type: e})
        self.is_expressao = False
        return exp

    def termo(self,termo):
        # termo: fator
        #       |termo VEZES fator
        #       |termo DIVIDIR fator
        ter = []
        for t in termo.children:
            if(type(t) == Tree):
                ter.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):  
                    if self.is_atribuicao and self.is_objeto:
                        self.atribuicao_expression += f" {t.value} "
                    ter.append({t.type: t})
        return ter

    def fator(self,fator):
        # fator: atomo
        #       |fator ELEVADO atomo
        fat = []
        for f in fator.children:
            if(type(f) == Tree):
                fat.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    if self.is_atribuicao and self.is_objeto:
                        self.atribuicao_expression += f" {f.value} "
                    fat.append({f.type: f})
        return fat

    def atomo(self,atomo):
        # fator: atomo
        #       |fator ELEVADO atomo
        ato = []
        for atomo in atomo.children:
            if(type(atomo) == Tree):
                ato.append({atomo.data: self.visit(atomo)})
            else:
                if (type(atomo) == Token):
                    if self.is_atribuicao:
                        if self.lista_counter > 0 or self.tuplo_counter > 0 or self.array_counter > 0:
                            self.atribuicao_expression += f"{atomo.value}"
                        elif self.is_objeto:
                            self.atribuicao_expression += atomo.value
                    ato.append({atomo.type: atomo})
        return ato

    def senao(self,senao):
        # senao: "SENAO" "{" body "}"
        sen = []
        for s in senao.children:
            sen.append(self.visit(s))
        return sen


    def chamadafuncao(self,chamadafuncao):
        # chamadafuncao: funcao ";"
        cfunc = []
        for cf in chamadafuncao.children:
            if(type(cf) == Tree):
                cfunc.append({cf.data: self.visit(cf)})
            else:
                if (type(cf) == Token):
                    cfunc.append({cf.type: cf})
        return cfunc
        

    def importar(self,importar):
        # importar: "IMPORTA" "{" IMPORTADO "}"
        self.info["imports"].append(importar.children[0].value)
        return importar.children[0].value

    def comentario(self,comentario):
        # comentario: ":-" TEXTO "-:"
        comment = comentario.children[0].value.split('\n')
        return comment