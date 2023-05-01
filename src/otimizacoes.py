import json

def ses (p):
    if ("senao" not in p["selecao"]["se"] and 
            len(p["selecao"]["se"]["body"]) == 1 and 
            "selecao" in p["selecao"]["se"]["body"][0] and 
            "se" in p["selecao"]["se"]["body"][0]["selecao"] and 
            "senao" not in p["selecao"]["se"]["body"][0]["selecao"]["se"]) :
        dictlogico = {"logico": " E "}
        p["selecao"]["se"]["logica"].append(dictlogico)
        p["selecao"]["se"]["logica"].extend(p["selecao"]["se"]["body"][0]["selecao"]["se"]["logica"])
        p["selecao"]["se"]["body"] = p["selecao"]["se"]["body"][0]["selecao"]["se"]["body"]
        procurabody(p)
    else :
        percorre (p["selecao"]["se"]["body"])

def casos (p) :
    for c in p["casos"][1] :
        if "body" in c :
            percorre (c["body"])
    percorre(p["casos"][2])

def procurabody (p) :
    if "selecao" in p :
        if "se" in p["selecao"] :
            ses(p)            
        elif "casos" in p :
            casos(p)
    elif "repeticao" in p :
        if "enquanto" in p["repeticao"] :
            percorre (p["repeticao"]["enquanto"][1]["body"])
        elif "repetir" in p["repeticao"] :
            percorre (p["repeticao"]["repetir"][0]["body"])
        elif "para" in p["repeticao"] :
            percorre (p["repeticao"]["para"][2]["body"])
    elif "deffuncao" in p :
        percorre (p["deffuncao"][3]["body"])

def percorre (prog) :
    for p in prog :
        procurabody(p)

def otimizacoes(code):
    percorre(code["programa"])
    
