stack = []
#sdg = ""
sdg = []

def funcaotostring(p) :
    f = ""
    if "cons" in p[0] :
        f = constostring(p[0]["cons"])
    elif "snoc" in p[0] :
        f = snoctostring(p[0]["snoc"])
    elif "head" in p[0] :
        f = headtostring(p[0]["head"])
    elif "tail" in p[0] :
        f = tailtostring(p[0]["tail"])
    elif "func" in p[0] :
        f = functostring(p[0]["func"])
    
    return f

def argstostring(p) :
    args = ""
    for o in p:
        obj = objtostring(o["objeto"])
        args = args + obj + ","
    
    args = args[:-1]
    return args

def functostring(p) :
    args = argstostring(p[1]["argumentos"])
    func = p[0]["FUNC"] + " (" + args + ")"
    return func

def arghtostring(p) :
    if "VAR" in p[0] :
        argh = p[0]["VAR"]
    else:
        lista = listatostring(p[0]["lista"])
        argh = lista
    
    return argh

def argctostring(p) :
    obj = objtostring(p[0]["objeto"])
    argh = arghtostring(p[1]["argumentosh"])
    argc = obj + ", " + argh
    return argc

def tailtostring(p) :
    argh = arghtostring(p[0]["argumentosh"])
    tail = "tail (" + argh + ")"
    return tail

def headtostring(p) :
    argh = arghtostring(p[0]["argumentosh"])
    head = "head (" + argh + ")"
    return head

def snoctostring(p) :
    argc = argctostring(p[0]["argumentosc"])
    snoc = "snoc (" + argc + ")"
    return snoc

def constostring(p) :
    argc = argctostring(p[0]["argumentosc"])
    cons = "cons (" + argc + ")"
    return cons

def objtostring(p) :
    obj = ""
    if "expressao" in p[0] :
        obj = expressaotostring(p[0]["expressao"])
    elif "STRING" in p[0] :
        obj = p[0]["STRING"]
    elif "condicao" in p[0] :
        obj = condtostring(p[0]["condicao"])
    elif "array" in p[0] :
        obj = arraytostring(p[0]["array"])
    elif "tuplo" in p[0] :
        obj = tuplotostring(p[0]["tuplo"])
    elif "lista" in p[0] :
        obj = listatostring(p[0]["lista"])
    elif "funcao" in p[0] :
        obj = funcaotostring(p[0]["funcao"])
    
    return obj

def arraytostring(p) :
    arr = "{"
    for o in p:
        if "NUM" in o :
            obj = o["NUM"]
        else :
            obj = o["STRING"]
        arr = arr + obj + ","
    
    size = len(arr)
    if size > 2 :
        arr = arr[:-1] + "}"
    else:
        arr = arr + "}"
    return arr

def tuplotostring(p) :
    tuplo = "("
    for o in p:
        obj = objtostring(o["objeto"])
        tuplo = tuplo + obj + ","
    
    size = len(tuplo)
    if size > 2 :
        tuplo = tuplo[:-1] + ")"
    else:
        tuplo = tuplo + ")"
    return tuplo

def listatostring(p) :
    lista = "["
    for o in p:
        obj = objtostring(o["objeto"])
        lista = lista + obj + ","
    
    size = len(lista)
    if size > 2 :
        lista = lista[:-1] + "]"
    else:
        lista = lista + "]"
    return lista

def vartostring(p) :
    var = p[0]["VAR"]
    if len(p) > 1 :
        exp = expressaotostring(p[1]["expressao"])
        var = var + "[" + exp + "]"
    
    return var

def varlistatostring(p) :
    varlista = ""
    if "var" in p :
        var = vartostring(p["var"])
        varlista = var
    else:
        lista = listatostring(p["lista"])
        varlista = lista
    
    return varlista

def atomtostring(p) :
    atom = ""
    if "NUM" in p[0]:
        atom = p[0]["NUM"]
    else:
        var = vartostring(p[0]["var"])
        atom = var
    
    return atom

def fatortostring(p) :
    fator = ""
    if "atomo" in p[0] :
        atom = atomtostring(p[0]["atomo"])
        fator = atom
    else :
        fator2 = fatortostring(p[0]["fator"])
        atom = atomtostring(p[2]["atomo"])
        fator = fator2 + "^" + atom

    return fator

def termotostring(p) :
    termo = ""
    if "fator" in p[0] :
        fator = fatortostring(p[0]["fator"])
        termo = fator
    else :
        termo2 = termotostring(p[0]["termo"])
        fator = fatortostring(p[2]["fator"])
        if "VEZES" in p[1] :
            termo = termo2 + "*" + fator
        elif "DIVIDIR" in p[1] :
            termo = termo2 + "/" + fator
        else :
            termo = termo2 + "%" + fator

    return termo

def expressaotostring(p) :
    exp = ""
    if "termo" in p[0] :
        ter = termotostring(p[0]["termo"])
        exp = ter
    else :
        exp2 = expressaotostring(p[0]["expressao"])
        ter = termotostring(p[2]["termo"])
        if "MAIS" in p[1] :
            exp = exp2 + "+" + ter
        else :
            exp = exp2 + "-" + ter
        
    return exp

def condtostring(p) :
    cond = ""

    f = 0
    if "BOOL" in p[0] :
        cond = cond + p[0]["BOOL"]
    else:
        if len(p) > 1:
            if "EM" in p[1] :
                exp = expressaotostring(d["expressao"])
                cond = cond + exp + d["expressao"]["EM"] + d["expressao"]["VAR"]
                f = 1
        if f == 0 :
            for d in p :
                if "expressao" in d :
                    exp = expressaotostring(d["expressao"])
                    cond = cond + exp
                elif "SINAL" in d :
                    cond = cond + d["SINAL"]
    
    return cond

def logicatostring(p):
    logica = ""
    for d in p :
        if "condicao" in d :
            cond = condtostring(d["condicao"])
            logica = logica + cond
        elif "logico" in d :
            log = d["logico"]
            logica = logica + log
        else :
            cond = condtostring(d)
            logica = logica + cond

    return logica

def paras(p):
    global stack

    var = vartostring(p[1]["logica"])
    varlista = varlistatostring
    inst = "PARA (" + var + "DE" + varlista + ")"
    inst = inst.replace("\"","\\\"")
    stack.append(inst)
    percorre(p[2]["body"])
    stack.pop()

    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2, "diamond"]
    sdg.append(sdglist)

def repetes(p):
    global stack
    global sdg

    logica = logicatostring(p[1]["logica"])
    inst = "REPETE_ATE (" + logica + ")"
    inst = inst.replace("\"","\\\"")
    stack.append(inst)
    percorre(p[0]["body"])
    stack.pop()

    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2, "diamond"]
    sdg.append(sdglist)

def enquantos(p) :
    global stack
    global sdg

    logica = logicatostring(p[0]["logica"])
    inst = "ENQ (" + logica + ")"
    inst = inst.replace("\"","\\\"")
    stack.append(inst)
    percorre(p[1]["body"])
    stack.pop()

    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2, "diamond"]
    sdg.append(sdglist)

def casos(p) :
    global stack
    global sdg

    var = vartostring(p[0]["var"])
    inst = "ESCOLHE (" + var + ")"
    stack.append(inst)

    caso = ""
    i = 1
    if "caso" in p[1]:
        i = 2
        for c in p[1]["caso"] :
            if "NUM" in c:
                caso = "CASO (" + c["NUM"] + ")"
            elif "STRING" in c:
                caso = "CASO (" + c["STRING"] + ")"
            else:
                stack.append(caso)
                percorre(c["body"])
                stack.pop()
                caso = caso.replace("\"","\\\"")
                sdg1 = "\"" + stack[-1] + "\""
                sdg2 = "\"" + caso + "\""
                sdglist = [sdg1, sdg2]
                sdg.append(sdglist)

    caso = "CASO ()"
    stack.append(caso)
    percorre(p[i]["casofinal"][0]["body"])
    stack.pop()
    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + caso + "\""
    sdglist = [sdg1, sdg2]
    sdg.append(sdglist)

    stack.pop()

    inst = inst.replace("\"","\\\"")
    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2, "diamond"]
    sdg.append(sdglist)

def ses(p) :
    global stack
    global sdg

    logica = logicatostring(p["logica"])
    inst = "SE (" + logica + ")"
    inst = inst.replace("\"","\\\"")
    stack.append(inst)

    stack.append("ENTAO")
    percorre(p["body"])
    stack.pop()
    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"ENTAO\""
    sdglist = [sdg1, sdg2]
    sdg.append(sdglist)

    if "senao" in p :
        stack.append("SENAO")
        percorre(p["senao"][0])
        stack.pop()
        sdg1 = "\"" + stack[-1] + "\""
        sdg2 = "\"SENAO\""
        sdglist = [sdg1, sdg2]
        sdg.append(sdglist)

    stack.pop()

    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2, "diamond"]
    sdg.append(sdglist)

def atribs(p) :
    global stack
    global sdg

    var = vartostring(p[0]["var"])
    obj = objtostring(p[1]["objeto"])
    inst = var + "=" + obj

    if "funcao" in p[1]["objeto"][0] :
        inst = inst + "$out"
        chamadas(p[1]["objeto"])
    
    inst = inst.replace("\"","\\\"")
    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + inst + "\""
    sdglist = [sdg1, sdg2]
    sdg.append(sdglist)

def chamadas(p) :
    global stack
    global sdg

    fun = funcaotostring(p[0]["funcao"])
    fun = fun.split("(")[0]
    fun = fun.split(" ")[0]
    fun = fun.replace("\"","\\\"")

    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"chama " + fun + "\""
    sdglist = [sdg1, sdg2]
    sdg.append(sdglist)
    sdg1 = "\"chama " + fun + "\""
    sdg2 = "\"ENTRAR " + fun +"\""
    sdglist = [sdg1, sdg2, "square"]
    sdg.append(sdglist)

def defs(p) :
    global stack
    global sdg

    inst = "ENTRAR " + p[1]["FUNC"]
    stack.append(inst)
    percorre(p[3]["body"])

    if len(p) > 3 :
        obj = objtostring(p[4]["retorna"][0]["objeto"])
        obj = obj.replace("\"","\\\"")
        sdg1 = "\"" + stack[-1] + "\""
        sdg2 = "\"" + p[1]["FUNC"] + "_out " + obj + "\""
        sdglist = [sdg1, sdg2]
        sdg.append(sdglist)

    stack.pop()

def decs(p) :
    global stack
    global sdg

    tipo = p[0]["TIPO"]

    if "atribuicao" in p[1]:
        var = vartostring(p["declaracao"][1]["atribuicao"][0]["var"])
        atribs(p["declaracao"][1]["atribuicao"])
    else :
        var = vartostring(p[1]["var"])
    
    sdg1 = "\"" + stack[-1] + "\""
    sdg2 = "\"" + tipo + " " + var + "\""
    sdglist = [sdg1, sdg2]
    sdg.append(sdglist)

def procurabody (p) :
    if "selecao" in p :
        if "se" in p["selecao"] :
            ses(p["selecao"]["se"])
        elif "casos" in p["selecao"] :
            casos(p["selecao"]["casos"])
    elif "repeticao" in p :
        if "enquanto" in p["repeticao"] :
            enquantos(p["repeticao"]["enquanto"])
        elif "repetir" in p["repeticao"] :
            repetes(p["repeticao"]["repetir"])
        elif "para" in p["repeticao"] :
            paras(p["repeticao"]["para"])
    elif "atribuicao" in p:
        atribs(p["atribuicao"])
    elif "declaracao" in p:
        decs(p["declaracao"])
    elif "chamadafuncao" in p:
        chamadas(p["chamadafuncao"])
    elif "deffuncao" in p:
        defs(p["deffuncao"])

def percorre (prog) :
    for p in prog :
        procurabody(p)

def graphs_generator(dicto):
    global stack
    global sdg

    stack.append("begin")
    percorre(dicto["programa"])

    return sdg