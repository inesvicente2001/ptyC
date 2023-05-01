from lark import Discard
from lark import Lark,Token,Tree
from lark.visitors import Interpreter
import json

class PtyCInterpreter(Interpreter):
    def __init__(self):
        self.programa = {}
        self.info = {}
        self.info["variaveis"] = {}
        self.info["instrucoes"] = {}
        self.info["aninhamentos"] = 0
        self.is_variable = False
        self.variavel_atual = []
        self.is_expression = False
        self.expression = ""
        self.is_list = False
        self.list_value = ""
        self.is_atribuicao = False
        self.is_objeto = False
    

    def program(self,program):
        # program: statement*
        self.programa["programa"] = []
        for statement in program.children:
            stat = self.visit(statement)
            self.programa["programa"].append(stat)
        with open('info.json', 'w') as outfile:
            json.dump(self.info, outfile, indent=2, ensure_ascii=False)

        return self.programa

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
        func = []
        for f in funcao.children:
            if(type(f) == Tree):
                func.append({f.data: self.visit(f)})
            else:
                if (type(f) == Token):
                    func.append({f.type: f})

        return func


    def cons(self,cons):
        # cons: "cons" "(" argumentosc ")"
        cs = []
        for c in cons.children:
            if(type(c) == Tree):
                cs.append({c.data: self.visit(c)})
            else:
                if (type(c) == Token):
                    cs.append({c.type: c})

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
        for s in snoc.children:
            if(type(s) == Tree):
                sc.append({s.data: self.visit(s)})
            else:
                if (type(s) == Token):
                    sc.append({s.type: s})

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
        for t in tail.children:
            if(type(t) == Tree):
                tl.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tl.append({t.type: t})

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
        tipo_atual = ""
        for d in declaracao.children:
            if(type(d) == Tree):
                dec.append({d.data: self.visit(d)})
                self.info["variaveis"][self.variavel_atual[-1]]["tipo_da_variavel"] = tipo_atual
                self.info["variaveis"][self.variavel_atual[-1]]["foi_declarada"] = True
                if self.is_list:
                    self.is_list = False

            else:
                if (type(d) == Token):
                    if d.type == "TIPO":
                        tipo_atual = d.value
                    elif d.type == "VAR":
                        variaveis = self.info["variaveis"]
                        if d.value in variaveis:
                            variaveis[d.value]["foi_redeclarada"] = True
                            variaveis[d.value]["tipo_da_variavel"] = tipo_atual
                        else:
                            var_info = {
                                "foi_declarada" : True,
                                "foi_inicializada": False,
                                "foi_utilizada": False,
                                "foi_redeclarada": False,
                                "tipo_da_variavel": tipo_atual,
                                "valores": []  
                            }
                            variaveis[d.value] = var_info
                        self.info["variaveis"] = variaveis
                    dec.append({d.type: d})
        self.is_variable = False
        return dec

    def atribuicao(self,atribuicao):
        # atribuicao: var "=" objeto ";"
        self.is_variable = True
        self.is_atribuicao = True
        atrib = []

        for a in atribuicao.children:
            if(type(a) == Tree):
                if a.data == "var":
  
                    self.variavel_atual.append(a.children[0])
                    atrib.append({a.data: self.visit(a)})
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
        self.is_variable = False
        self.is_atribuicao = False

        return atrib

    def var(self,var):
        # var: VAR ("[" (expressao) "]")?
        variable = []
        first = False
        if len(var.children) > 1 and self.is_list == False:
            self.is_list = True
            first = True
        for v in var.children:

            if(type(v) == Tree):
                variable.append({v.data: self.visit(v)})
                variable_name = str(self.variavel_atual[-1]) +  "[" + str(self.list_value) + "]"
                if variable_name in self.info["variaveis"]:
                    self.info["variaveis"][variable_name]["foi_utilizada"] = True
                else:
                    foi_utilizada = False
                    if self.is_objeto:
                        foi_utilizada = True
                    self.info["variaveis"][variable_name] = {
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
                    self.variavel_atual.append(variable_name)

                self.list_value = ""


            else:
                if (type(v) == Token):
                    if self.is_list == False:
                        if v.value not  in self.info["variaveis"]:
                            inicializada = True
                            if self.is_variable:
                                inicializada = False
                            self.info["variaveis"][v.value] = {
                            "foi_declarada" : False,
                            "foi_inicializada": False,
                            "foi_utilizada": inicializada,
                            "foi_redeclarada": False,
                            "tipo_da_variavel": "",
                            "valores": []
                            }
                            self.variavel_atual.append(v.value)
                    else:
                        if first == False:
                            self.list_value += str(v.value)
                        else:
                            self.variavel_atual.append(str(v.value))
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
        if self.is_atribuicao:
            self.is_objeto = True
        obj = []
        for o in objeto.children:
            if(type(o) == Tree):
                obj.append({o.data: self.visit(o)})
                print(self.variavel_atual[-1])
                if o.data == "expressao":
                    self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(self.expression)
                    self.is_expression = False
                    self.expression = ""
            else:
                if (type(o) == Token):
                    self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(o.value)
                    obj.append({o.type: o})
        self.is_objeto = False

        return obj

    def lista(self,lista):
        # lista: "[" ((objeto) ("," objeto)*)? "]"
        list = []
        for l in lista.children:
            if(type(l) == Tree):
                list.append({l.data: self.visit(l)})
            else:
                if (type(l) == Token):
                    list.append({l.type: l})

        return list


    def array(self,array):
        array_string = ""
        if self.is_objeto:
            array_string += "["
        # array: "[" (NUM ("," NUM)*)? "]"
        #       |"[" (STRING ("," STRING)*)? "]"
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
            array_string += "]" 
            self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(array_string)
            self.info["variaveis"][self.variavel_atual[-1]]["foi_inicializada"] = True

        return arr


    def tuplo(self,tuplo):
        # tuplo: "(" ((objeto) ("," objeto)*)? ")"
        tup = []
        for t in tuplo.children:
            if(type(t) == Tree):
                tup.append({t.data: self.visit(t)})
            else:
                if (type(t) == Token):
                    tup.append({t.type: t})

        return tup


    def selecao(self,selecao):
        # selecao: se
        #         |casos
        sel = {}
        sel[selecao.children[0].data.value] = self.visit(selecao.children[0])
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
        rep = {}
        for r in repeticao.children:
            rep[r.data.value] = self.visit(r)
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
        if self.is_objeto == False:
            self.expression = ""
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
                    if(self.is_list):
                        self.list_value += str(atomo.value)
                    else:
                         if self.is_variable:
                            if(not self.is_expression):
                               self.info["variaveis"][self.variavel_atual[-1]]["valores"].append(atomo.value)
                            else:
                                self.expression += str(atomo.value)
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
        return importar.children[0].value

    def comentario(self,comentario):
        # comentario: ":-" TEXTO "-:"
        comment = comentario.children[0].value.split('\n')
        return comment