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

        self.is_variable = False #para identificar se estamos a ler uma variavel
        self.variavel_atual = [] #para guardar o nome da variavel, tem de ser uma lista por causa de variaveis em atribuicoes
        self.tipo_atual = "" #para guardar o tipo da variavel
        self.is_expression = False #ver se é uma expressao
        self.expression = "" #para guardar a expressao
        self.is_list = False #para atribuicoes de variaveis q têm []
        self.list_value = "" #para guardar o valor da lista
        self.is_atribuicao = False #para ver se estavamos dentro de uma atribuição
        self.is_objeto = False #para ver se estamos num objeto dentro de uma atribuicao
        self.is_lista = False #para identificar se estamos numa lista
        self.listinha = "" #para guardar o valor da lista
        self.is_loop = False #para ver se estamos dentro de um loop
        self.is_declaracao = False #para ver se estamos dentro de uma declaracao
        self.list_counter = 0 #contador de listas
        self.is_tuplo = False #para ver se estamos dentro de um tuplo
        self.tuplo_expression = "" #para guardar a expressao do tuplo
        self.is_varlista = False #para ver se estamos dentro de uma varlista
        self.is_expressao = False #para ver se estamos dentro de uma expressao
        self.expressao_counter = 0 #contador de expressoes
        self.is_funcao = False #para ver se estamos dentro de uma funcao
        self.funcao_expression = "" 

        self.ciclo_counter = 0 #contador de ciclos
        self.condicao_counter = 0 #contador de condicoes
        self.last_aninhamento = "" #guardar o último aninhamento para saber o tipo de aninhamento em que estamos
    

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
        if self.is_atribuicao:
            self.is_funcao = True
        func = []
        for f in funcao.children:
            if(type(f) == Tree):
                func.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    func.append({f.type: f})
        if self.is_funcao:
            if self.funcao_expression[-1] == ",":
                self.funcao_expression = self.funcao_expression[:-1]
            self.funcao_expression += ")"
            if self.variavel_atual != []:
                self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(self.funcao_expression)
            self.is_funcao = False

        return func


    def cons(self,cons):
        # cons: "cons" "(" argumentosc ")"
        cs = []
        if self.is_lista:
            self.listinha += "cons("
        if self.is_expression:
            self.expression += "cons("
        if self.is_tuplo:
            self.tuplo_expression += "cons("
        for c in cons.children:
            if(type(c) == Tree):
                cs.append({c.data: self.visit(c)})
            else:
                if (type(c) == Token):
                    cs.append({c.type: c})
        
        if self.is_lista:
            self.listinha += "),"
        if self.is_expression:
            self.expression += "),"
        if self.is_tuplo:
            self.tuplo_expression += "),"

        return cs

    def argumentosc(self,argumentosc):
        # argumentosc: objeto "," argumentosh
        arg = []
        for a in argumentosc.children:
            if(type(a) == Tree):
                arg.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    if a.value in self.info["variaveis"]:
                        if self.info["vairiaveis"][a.value]["foi_utilizada"] == False:
                            self.info["variaveis"][a.value]["foi_utilizada"] = True
                    else: 
                        self.info["variaveis"][a.value] = {
                            "foi_declarada": False,
                            "foi_inicializada": False,
                            "foi_utilizada": True,
                            "foi_redeclarada": False,
                            "tipo_da_variavel": "",
                            "valores": []
                        }
                    arg.append({a.type: a})

        return arg

    def snoc(self,snoc):
        # snoc: "snoc" "(" argumentosc ")"
        sc = []
        if self.is_lista:
            self.listinha += "snoc("
        if self.is_expression:
            self.expression += "snoc("
        if self.is_tuplo:
            self.tuplo_expression += "snoc("
        
        for s in snoc.children:
            if(type(s) == Tree):
                sc.append({s.data: self.visit(s)})
            else:
                if (type(s) == Token):
                    sc.append({s.type: s})
        
        if self.is_lista:
            self.listinha += "),"
        if self.is_expression:
            self.expression += "),"
        if self.is_tuplo:
            self.tuplo_expression += "),"

        return sc

    def head(self,head):
        # head: "head" "(" argumentosh ")"
        hd = []
        for h in head.children:
            if(type(h) == Tree):
                hd.append({h.data: self.visit(h)})
            else:
                if (type(h) == Token):
                    hd.append({h.type: h})

        return hd

    def tail(self,tail):
        # tail: "tail" "(" argumentosh ")"
        tl = []
        if self.is_lista:
            self.listinha += "tail("
        if self.is_expression:
            self.expression += "tail("
        if self.is_tuplo:
            self.tuplo_expression += "tail("
        
        for t in tail.children:
            if(type(t) == Tree):
                tl.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tl.append({t.type: t})
        if self.is_lista:
            self.listinha += "),"
        if self.is_expression:
            self.expression += "),"
        if self.is_tuplo:
            self.tuplo_expression += "),"

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
                    if a.value in self.info["variaveis"]:
                        if self.info["variaveis"][a.value]["foi_utilizada"] == False:
                            self.info["variaveis"][a.value]["foi_utilizada"] = True
                    else: 
                        self.info["variaveis"][a.value] = {
                            "foi_declarada": False,
                            "foi_inicializada": False,
                            "foi_utilizada": True,
                            "foi_redeclarada": False,
                            "tipo_da_variavel": "",
                            "valores": []
                        }
                    arg.append({a.type: a})

        return arg

    def func(self,func):
        # func: FUNC "(" argumentos ")"
        fun_ = []
        expressao = func.children[0].value + "("
        if self.is_lista:
            self.listinha += expressao 
        elif self.is_expression:
            self.expression += expressao 
        elif self.is_tuplo:
            self.tuplo_expression += expressao
        
        for f in func.children:
            if(type(f) == Tree):
                fun_.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    fun_.append({f.type: f})
                    if self.is_funcao:
                        self.funcao_expression += f.value + "("
        if self.is_lista:
            if self.listinha[-1] == ",":
                self.listinha = self.listinha[:-1] + "),"
            else:
                self.listinha += "),"
        elif self.is_expression:
            if self.expression != "":
                if self.expression[-1] == ",":
                    self.expression = self.expression[:-1] +  "),"
                else:
                    self.expression += "),"
        elif self.is_tuplo:
            if self.tuplo_expression[-1] == ",":
                self.tuplo_expression = self.tuplo_expression[:-1] +  "),"
        elif self.is_funcao:
            if self.funcao_expression[-1] == ",":
                self.funcao_expression = self.funcao_expression[:-1] +  ")"

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
        dec = []
        self.is_variable = True
        self.is_declaracao = True
        for d in declaracao.children:
            if(type(d) == Tree):
                dec.append({d.data: self.visit(d)})
                if self.is_list:
                    self.is_list = False

            else:
                if (type(d) == Token):
                    if d.type == "TIPO":
                        self.tipo_atual = d.value
                    elif d.type == "VAR":
                        variaveis = self.info["variaveis"]
                        if d.value in variaveis:
                            variaveis[d.value]["foi_redeclarada"] = True
                            variaveis[d.value]["tipo_da_variavel"] = self.tipo_atual
                        else:
                            var_info = {
                                "foi_declarada" : True,
                                "foi_inicializada": False,
                                "foi_utilizada": False,
                                "foi_redeclarada": False,
                                "tipo_da_variavel": self.tipo_atual,
                                "valores": []  
                            }
                            variaveis[d.value] = var_info
                        self.info["variaveis"] = variaveis
                    dec.append({d.type: d})
        self.is_variable = False
        self.is_declaracao = False
        return dec

    def atribuicao(self,atribuicao):
        # atribuicao: var "=" objeto ";"
        self.info["instrucoes"]["atribuicoes"] += 1
        self.is_variable = True
        self.is_atribuicao = True
        atrib = []

        for a in atribuicao.children:
            if(type(a) == Tree):
                if a.data == "var":
                    atrib.append({a.data: self.visit(a)})
                    if len(a.children) == 1:
                    
                        self.variavel_atual.append(a.children[0].value)
                        
                        if a.children[0] not in self.info["variaveis"] and self.is_list == False:
                            self.info["variaveis"][a.children[0]] = {
                                "foi_declarada" : False,
                                "foi_inicializada": True,
                                "foi_utilizada": False,
                                "foi_redeclarada": False,
                                "tipo_da_variavel": "",
                                "valores": []
                            }
                        if self.is_list:
                            self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True
                        self.is_list = False
                elif a.data == "objeto":
                    atrib.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    atrib.append({a.type: a})
        self.variavel_atual = [self.variavel_atual[0]]

        self.is_variable = False
        self.is_atribuicao = False
        self.expression = ""
        self.listinha = ""
        self.list_value = ""
        self.tuplo_expression = ""

        return atrib

    def var(self,var):
        # var: VAR ("[" (expressao) "]")?
        variable = []
        entered_list = False
        if self.is_list:
            entered_list = True
        first = False
        if len(var.children) > 1 and self.is_list == False:
            self.is_list = True
            first = True
        for v in var.children:

            if(type(v) == Tree):
                variable.append({v.data: self.visit(v)})
                variable_name = str(self.variavel_atual[-1]) +  "[" + str(self.list_value) + "]"
                if self.variavel_atual[-1] in self.info["variaveis"]:
                    self.info["variaveis"][self.variavel_atual[-1]]["foi_utilizada"] = True
                else:
                    foi_utilizada = False
                    if self.is_objeto or self.is_lista or self.is_tuplo or self.expressao_counter > 0:
                        foi_utilizada = True
                    self.info["variaveis"][self.variavel_atual[-1]] = {
                        "foi_declarada" : False,
                        "foi_inicializada": False,
                        "foi_utilizada": foi_utilizada,
                        "foi_redeclarada": False,
                        "tipo_da_variavel": "",
                        "valores": []
                    }
                if self.is_objeto:
                    self.expression += variable_name
                    self.variavel_atual.pop()
                else:
                    self.variavel_atual.append(self.variavel_atual[-1])

                self.list_value = ""
                self.is_list = False


            else:
                if (type(v) == Token):
                    if self.is_list == False:
                        if v.value not  in self.info["variaveis"]:
                            inicializada = True
                            if self.is_variable and self.is_lista == False and self.is_tuplo == False and self.expressao_counter == 0:
                                inicializada = False
                            self.info["variaveis"][v.value] = {
                            "foi_declarada" : False,
                            "foi_inicializada": False,
                            "foi_utilizada": inicializada,
                            "foi_redeclarada": False,
                            "tipo_da_variavel": "",
                            "valores": []
                            }
                            
                            if self.is_declaracao:
                                self.info["variaveis"][v.value]["foi_declarada"] = True
                                self.info["variaveis"][v.value]["tipo_da_variavel"] = self.tipo_atual
                            if self.is_objeto == False:
                                self.variavel_atual.append(str(v.value))
                    else:
                        if first == False:
                            if entered_list == False:
                                self.list_value += str(v.value)
                        else:
                            self.variavel_atual.append(str(v.value))
                    
                    if self.is_objeto and self.is_list == False and self.is_expression == False and self.is_tuplo == False and self.is_lista == False:
                        self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(v.value)
                        if self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] == False:
                            self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True
                    if self.is_lista and self.is_list == False:
                        self.listinha += str(v.value) + ","
                    elif self.is_lista and self.is_list:
                        self.listinha += str(v.value) + "["
                    if self.is_expressao and self.is_objeto and self.variavel_atual[-1] in self.info["variaveis"]:
                        self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"]= True
                    if self.is_funcao:
                        self.funcao_expression += str(v.value)
                    variable.append({v.type: v})

        return variable

    def objeto(self,objeto):
        # objeto: expressao
        #        |STRING
        #        |condicao
        #        |array
        #        |tuplo
        #        |lista
        #        |funcao
        recursive = False
        if self.is_objeto:
            recursive = True
        if self.is_atribuicao:
            self.is_objeto = True
        obj = []
        for o in objeto.children:
            if(type(o) == Tree):
            
                obj.append({o.data: self.visit(o)})
                if o.data == "expressao":
                    if self.expression != "" and not self.is_funcao:
                        self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(self.expression)

                        if self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] == False:
                            self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True
                        self.is_expression = False
                        self.expression = ""
            else:
                if (type(o) == Token):
                    if self.is_lista:
                        self.listinha += str(o.value) + ","
                    elif self.is_tuplo:
                        self.tuplo_expression += str(o.value) + ","
                    else:
                        if self.is_varlista == False and self.variavel_atual != []:
                            self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(o.value)
                    if self.is_varlista == False and self.variavel_atual != []:
                        if self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] == False:
                            self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True
                    obj.append({o.type: o})
        if recursive == False:
            self.is_objeto = False

        return obj

    def lista(self,lista):
        # lista: "[" ((objeto) ("," objeto)*)? "]"
        self.list_counter += 1
        if self.is_loop == False:
            self.is_lista = True
            self.listinha += "["
        list = []
        for l in lista.children:
            if(type(l) == Tree):
                list.append({l.data: self.visit(l)})
            else:
                if (type(l) == Token):
                    list.append({l.type: l})
        if self.is_loop == False:
            if self.listinha[-1] == ",":
                self.listinha = self.listinha[:-1]
            self.listinha += "]"
        if self.variavel_atual[-1] not in self.info["variaveis"]:
            self.info["variaveis"][self.variavel_atual[-1]] = {
                "foi_declarada" : False,
                "foi_inicializada": True,
                "foi_utilizada": False,
                "foi_redeclarada": False,
                "tipo_da_variavel": "",
                "valores": []

            }
        if self.is_funcao:
            self.funcao_expression += self.listinha + ","
        if self.is_tuplo:
            self.tuplo_expression += self.listinha + ","
        if self.is_loop == False and self.is_funcao == False:
            self.info["variaveis"][self.variavel_atual[-1]]["valores"] = [self.listinha]  
            self.list_counter -= 1
            if self.list_counter == 0:
                self.listinha = ""
                self.is_lista = False

        return list


    def array(self,array):
        # array: "[" (NUM ("," NUM)*)? "]"
        #       |"[" (STRING ("," STRING)*)? "]"
        array_string = ""
        if self.is_objeto:
            array_string += "{"
        arr = []
        for a in array.children:
            if(type(a) == Tree):

                arr.append({a.data: self.visit(a)})
            else:
                if (type(a) == Token):
                    if self.is_objeto:
                        array_string += str(a.value)
                        array_string += ","
                    arr.append({a.type: a})
        if self.is_objeto:
            array_string = array_string[:-1]
            array_string += "}" 
            if self.is_lista:
                self.listinha += array_string
            elif self.is_expression:
                self.expression += array_string
            elif self.is_tuplo:
                self.tuplo_expression += array_string + ","
            else:
                self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(array_string)
                self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True

        return arr


    def tuplo(self,tuplo):
        # tuplo: "(" ((objeto) ("," objeto)*)? ")"
        tup = []
        self.is_tuplo = True
        if self.is_lista:
            self.listinha += "("
        elif self.is_expression:
            self.expression += "("
        else:
            self.tuplo_expression += "("
        for t in tuplo.children:
            if(type(t) == Tree):
                tup.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tup.append({t.type: t})

        if self.is_lista:
            if self.listinha[-1] == ",":
                self.listinha = self.listinha[:-1]
            self.listinha += ")"
        elif self.is_expression:
            if self.expression[-1] == ",": 
                self.expression = self.expression[:-1]
            self.expression += ")"
        else:
            if self.tuplo_expression[-1] == ",": 
                self.tuplo_expression = self.tuplo_expression[:-1]
            self.tuplo_expression += ")"
        self.info["variaveis"][self.variavel_atual[-1]]["valores"] = [self.tuplo_expression]
        self.is_tuplo = False
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
        sel = {}
        for se in se.children:
            sel[se.data.value] = self.visit(se)
        return sel

    def logica(self,logica):
        # logica: condicao (logico condicao)*
        log = []
        for logica in logica.children:
            log.append(self.visit(logica))
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
        recursive = False
        if self.is_loop == True:
            recursive = True
        self.is_loop = True
        rep = {}
        for r in repeticao.children:
            rep[r.data.value] = self.visit(r)
        if recursive == False:
            self.is_loop = False
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
        self.is_varlista = True
        
        vl = []
        for v in varlista.children:
            if(type(v) == Tree):
                vl.append({v.data: self.visit(v)})
            else:
                if (type(v) == Token):
                    vl.append({v.type: v})
        self.is_varlista = False

        return vl

    def retorna(self,retorna):
        # retorna: "RETORNA " objeto ";"
        ret = []
        self.is_lista = False
        self.is_list = False
        self.is_atribuicao = False
        self.is_declaracao = False
        self.is_funcao = False
        self.is_expressao = False
        self.is_loop = False
        self.is_tuplo = False
        self.is_expression = False
        self.is_objeto = False
        self.is_variable = False
        self.is_varlista = False
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
                    if (c.type == "VAR") and (c.value not in self.info["variaveis"]):
                        self.info["variaveis"][c.value] = {
                            "foi_declarada" : False,
                            "foi_inicializada": False,
                            "foi_utilizada": True,
                            "foi_redeclarada": False,
                            "tipo_da_variavel": "",
                            "valores": []
                            }
                    cond.append({c.type: c})
        return cond



    def logico(self,logico):
        # logico: "E"|"OU"
        return {logico.data.value: logico.children[0].value}

    def expressao(self,expressao):
        # expressao: termo
        #           |expressao MAIS termo
        #           |expressao MENOS termo
        exp = []
        self.is_expressao = True
        self.expressao_counter += 1
        if(len(expressao.children) > 1):
            self.is_expression = True
        for e in expressao.children:
            if(type(e) == Tree):
                exp.append({e.data: self.visit(e)})
            else:
                 if (type(e) == Token):
                    if self.is_list:
                        self.list_value += e.value
                    else:
                        self.expression += e.value
                    exp.append({e.type: e})
        if self.is_objeto == False :
            self.expression = ""
        self.is_expressao = False
        self.expressao_counter -= 1
        return exp

    def termo(self,termo):
        # termo: fator
        #       |termo VEZES fator
        #       |termo DIVIDIR fator
        ter = []

        if(len(termo.children) > 1):
            self.is_expression = True
        for t in termo.children:
            if(type(t) == Tree):
                ter.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    if self.is_list:
                        self.list_value += t.value
                    else:
                        self.expression += t.value
                    ter.append({t.type: t})
        return ter

    def fator(self,fator):
        # fator: atomo
        #       |fator ELEVADO atomo
        fat = []

        if(len(fator.children) > 1):
            self.is_expression = True
        for f in fator.children:
            if(type(f) == Tree):
                fat.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    if self.is_list:
                        self.list_expression += f.value
                    else:
                        self.expression += f.value
                    fat.append({f.type: f})
        return fat

    def atomo(self,atomo):
        # fator: atomo
        #       |fator ELEVADO atomo
        ato = []
        for atomo in atomo.children:
            if(type(atomo) == Tree):
                if atomo.data == "var":
                    if atomo.children[0].value in self.info["variaveis"]:
                        if self.info["variaveis"][atomo.children[0]]["foi_inicializada"] == True or self.info["variaveis"][atomo.children[0]]["foi_declarada"] == True:
                            self.info["variaveis"][atomo.children[0]]["foi_utilizada"] = True
                if self.is_expression == True and len(atomo.children) < 2:
                    self.expression += atomo.children[0].value
                ato.append({atomo.data: self.visit(atomo)})
            else:
                if (type(atomo) == Token):
                    if self.is_list:

                        self.list_value += str(atomo.value)
                    else:
                         if self.is_variable:
                            if(not self.is_expression and not self.is_funcao):
                                self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(atomo.value)
                                if self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] == False:
                                    self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True
                            else:
                                self.expression += str(atomo.value)
                    ato.append({atomo.type: atomo})
                    if self.is_lista:
                        self.listinha += atomo.value 
                        if self.is_list:
                            self.listinha += "]"
                        else:
                            self.listinha += ","
                    if self.is_tuplo and self.is_lista == False:
                        self.tuplo_expression += atomo.value + ","
                    if self.is_funcao:
                        if self.is_lista == False:
                            self.funcao_expression += atomo.value + ","
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