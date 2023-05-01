import json
import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_PATH, "../configs/colorThemes.json")



def processLanguageElementsClasses(languageElements):
    elements = """"""
    for k,v in languageElements.items():
        elements += f"""
        .{k} {{
            position: relative;
            display: inline-block;
            color: {v};
        }}
        """

    return elements


def generateStyleCSS():
    # Generate the <style> tag components
    stylingProperties = json.load(open(CONFIG_PATH, "r"))
    
    style = f"""
    <style>
        .container {{
            background-color: {stylingProperties["colorCodes"]["backgroundColor"]};
            border: solid 1px black;
            border-radius: 10px;
            padding: 2em;
            color: {stylingProperties["colorCodes"]["normalTextColor"]};
        }}

        .normal {{
            position: relative;
            display: inline-block;
            border-bottom: none;
        }}

        .error {{
            position: relative;
            display: inline-block;
            border-bottom: 2px dotted white;
            color: red;
        }}


        .warning {{
            position: relative;
            display: inline-block;
            border-bottom: 2px dotted white;
            color: #b6e0f7;
        }}
        .warning .warningtext {{
            visibility: hidden;
            width: fit-content;
            background-color: #dddd2a;
            border: solid 1.3px yellow;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -40px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .warning .warningtext::after {{
            content: "";
            position: absolute;
            top: 100%;
            left: 20%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;
        }}
        .warning:hover .warningtext {{
            visibility: visible;
            opacity: 1;
        }}


        .code {{
            position: relative;
            display: inline-block;
            margin: 0;
        }}
        .error .errortext {{
            visibility: hidden;
            width: fit-content;
            background-color: #c587c0;
            border: solid 1.3px red;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -40px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .error .errortext::after {{
            content: "";
            position: absolute;
            top: 100%;
            left: 20%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;
        }}
        .error:hover .errortext {{
            visibility: visible;
            opacity: 1;
        }}
    """

    style += processLanguageElementsClasses(stylingProperties["colorCodes"]["languageElements"])

    style += "</style>"

    return style


def generateHTML(body,style):
    # add boiler plate html for title and style?
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Analisador de Código Fonte</title>
        </head>
        {style}
        {body}
    </html>
    """

    return html


def generateImportHTML(imported):
    html = f"""
            <p class="code">
            <div class="tags">IMPORTA&nbsp</div><div class="preprocessor">{imported}</div>
            </p>"""

    return html

def generateCommentHTML(comment, factor):
    html = """"""
    
    for i in range(0, len(comment)):
        html += """
            <p class="code">"""
        
        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""

        if i == 0:
            if len(comment) == 1:
                html += f"""
                <div class="comments">:-&nbsp</div><div class="comments">{comment[i]}</div><div class="comments">&nbsp-:</div>"""
            else:
                html += f"""
                <div class="comments">:-&nbsp</div><div class="comments">{comment[i]}</div>"""
        elif i == len(comment) - 1:
            html += f"""
            <div class="comments">{comment[i]}</div><div class="comments">&nbsp-:</div>"""
        else:
            html += f"""
            <div class="comments">{comment[i]}</div>"""

        html += """
                </p>"""
    
    return html
    

def generateCasosHTML(variables,casos,factor):
    html = """"""

    # var
    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="keywords">ESCOLHE&nbsp</div>
            <div class="symbols">(</div>"""
    html += selector(variables,casos[0],"var",factor)
    html += """<div class="symbols">){</div></p>"""

    # caso
    html += selector(variables,casos[1],"caso",factor+1)
 
    # casofinal
    html += selector(variables,casos[2],"casofinal",factor+1)
 

    html += """
        <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""

    html += """
        <div class="symbols">}</div>
        </p>"""



    return html


def generateFinalCaseHTML(variables,finalCase,factor):
    
    html = """"""

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="keywords">CASO&nbsp</div>
            <div class="symbols">()</div>"""
    html += """<div class="symbols">&nbsp{</div></p>"""

    html += selector(variables,finalCase[0]["body"],"body",factor)

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="symbols">}</div>
            </p>"""


    return html


def generateCaseHTML(variables,case,factor):
    
    html = """"""

    for i in range(0, len(case), 2):

        typeCase = list(case[i].keys())[0]

        html += """
            <p class="code">"""
        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""
        html += f"""
                <div class="keywords">CASO&nbsp</div>
                <div class="symbols">(</div>{selector(variables,case[i],typeCase)}<div class="symbols">)</div>"""
        html += """<div class="symbols">&nbsp{</div></p>"""

        html += selector(variables,case[i+1]["body"],"body",factor)

        html += """
                <p class="code">"""
        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""
        html += """
                <div class="symbols">}</div>
                </p>"""


    return html


def generateSeHTML(variables,se,factor):

    html = """"""

    # logica
    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="keywords">SE&nbsp</div>
            <div class="symbols">(</div>"""
    html += selector(variables,se,"logica",factor)
    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(variables,se["body"],"body",factor)

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
            
    # senao
    if "senao" in se:
        html += """
            <div class="symbols">}</div><div class="keywords">SENAO</div><div class="symbols">&nbsp{</div></p>"""
        html += selector(variables,se["senao"],"senao",factor)

        html += """
            <p class="code">"""
        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
        <div class="symbols">}</div>
        </p>"""
            

    return html


def generateBodyHTML(variables,body,factor):
    html = """"""

    for b in body:
        html += selector(variables,b,list(b.keys())[0],factor+1)

    return html

def generateSenaoHTML(variables,senao,factor):
    html = """"""

    for s in senao[0]:
        html += selector(variables,s,list(s.keys())[0],factor+1)

    return html

def generateLogicHTML(variables,logica):

    html = """"""

    for l in logica:
        ## logico : either E or OU
        if type(l) is dict:
            signal = l["logico"]
            html += f"""
                <div class="keywords">{signal}&nbsp</div>"""
        else:
            # it is a condition
            aux = {}
            aux["condicao"] = l
            html += selector(variables,aux,"condicao")

    return html


def generateConditionHTML(variables,condition):

    html = """"""

    for c in condition:
        html += selector(variables,c,list(c.keys())[0])

    return html



def generateSelectionHTML(variables,selection, factor):
    html = """"""

    if type(selection) is dict:
        if list(selection.keys())[0] == "se":
            html += generateSeHTML(variables,selection["se"],factor)
        elif list(selection.keys())[0] == "casos":
            html += generateCasosHTML(variables,selection["casos"],factor)
    else:    
        print("ERROR: Invalid selection type")

    return html

def generateRepetitionHTML(variables,repetition,factor):
    html = """"""

    repetitionType = list(repetition.keys())[0]
    
    html += selector(variables,repetition,repetitionType,factor)

    return html


def generateWhileHTML(variables,content,factor):
    html = """"""

    # logica
    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="keywords">ENQ&nbsp</div>
            <div class="symbols">(</div>"""
    html += selector(variables,content[0],"logica",factor)
    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(variables,content[1]["body"],"body",factor)

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
            

    html += """
        <div class="symbols">}</div>
        </p>"""

    return html

def generateForHTML(variables,content,factor):
    html = """"""

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""

    html += """
            <div class="keywords">PARA&nbsp</div>
            <div class="symbols">(</div>"""
    
    # var
    html += selector(variables,content[0],"var",factor)

    html += """<div class="keywords">EM&nbsp</div>"""

    # varlista
    typeVar = list(content[1].keys())[0]
    html += selector(variables,content[1],typeVar,factor)

    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(variables,content[2]["body"],"body",factor)

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""

    html += """
        <div class="symbols">}</div>
        </p>"""


    return html


def generateVarlistHTML(variables,varlista):

    html = """"""

    typeVar = list(varlista[0].keys())[0]
    html += selector(variables,varlista[0],typeVar)

    return html


def generateRepeatHTML(variables,content,factor):
    html = """"""

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
            <div class="keywords">REPETIR&nbsp</div>
            <div class="symbols">&nbsp{</div></p>"""
    # body
    html += selector(variables,content[0]["body"],"body",factor)
    
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """<div class="symbols">}&nbsp<div class="keywords">ATE</div>&nbsp(</div>"""

    # logica
    html += selector(variables,content[1],"logica",factor)
    html += """<div class="symbols">)</div></p>"""

    html += """
            <p class="code">"""
    
            

    return html


def generateDeclarationHTML(variables,declaration, factor):
    # get the type of declaration
    type = declaration[0]["TIPO"]

    # get what it is declaring
    # atribuicao ou var
    declared = declaration[1]

    html = """"""
    html += f"""<p class="code">"""

    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""

    html += f"""
            <div class="types">{type}&nbsp</div>
            """
    
    if list(declared.keys())[0] == "atribuicao":
        html += selector(variables,declared,"atribuicao", factor, True)
    elif list(declared.keys())[0] == "var":
        html += selector(variables,declared,"var", factor, True)
    

    html += f"""
    </p>"""

    return html


def generateAssignmentHTML(variables,assignment, factor, insideDec):

    var = assignment[0]
    assigned = assignment[1]

    html = """"""
    
    if insideDec == False:
        html += f"""<p class="code">"""

        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""

        html += f"""
                {selector(variables,var,"var")}
                <div class="operators">=&nbsp</div>
                {selector(variables,assigned,"objeto")}
                <div class="symbols">;</div>
                </p>
                """
    else:
        html = f"""
                {selector(variables,var,"var")}
                <div class="operators">=&nbsp</div>
                {selector(variables,assigned,"objeto")}
                <div class="symbols">;</div>
                </p>
                """
        

    return html


def generateArrayHTML(variables,array):
    html = """
    <div class="symbols">&nbsp{</div>
    """

    if len(array) > 0:
        for element in array[0:-1]:
            html += f"""{selector(variables,element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(variables,array[-1],list(array[-1].keys())[0])}"""

    html += """
    <div class="symbols">}</div>
    """

    return html

def generateTupleHTML(variables,tuple):
    html = """
    <div class="symbols">(</div>
    """

    if len(tuple) > 0:
        for element in tuple[0:-1]:
            html += f"""{selector(variables,element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(variables,tuple[-1],list(tuple[-1].keys())[0])}"""

    html += """
    <div class="symbols">)</div>
    """

    return html

def generateListHTML(variables,lst):
    html = """
    <div class="symbols">[</div>
    """

    if len(lst) > 0:
        for element in lst[0:-1]:
            html += f"""{selector(variables,element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(variables,lst[-1],list(lst[-1].keys())[0])}"""

    html += """
    <div class="symbols">]</div>
    """

    return html

def generateFunctionHTML(variables,function):
    html = """"""

    html += selector(variables,function[0],list(function[0].keys())[0])

    return html


def generateFuncHTML(variables,func):
    html = """"""

    # function name
    html += selector(variables,func[0],list(func[0].keys())[0])

    # arguments
    html += selector(variables,func[1],list(func[1].keys())[0])

    return html


def generateArgumentsHTML(variables,argumentos):
    html = """"""

    html += """
    <div class="symbols">(</div>
    """

    if len(argumentos) > 0:
        for argument in argumentos[0:-1]:
            html += selector(variables,argument,list(argument.keys())[0])
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += selector(variables,argumentos[-1],list(argumentos[-1].keys())[0])

    html += """
    <div class="symbols">)</div>
    """

    return html

def generateConsHTML(variables,cons):

    

    html = """"""

    html += """
    <div class="functions">cons</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(variables,cons[0],list(cons[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateSnocHTML(variables,snoc):
    html = """"""

    html += """
    <div class="functions">snoc</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(variables,snoc[0],list(snoc[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateHeadHTML(variables,head):
    html = """"""

    html = """
    <div class="functions">head</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(variables,head[0],list(head[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateTailHTML(variables,tail):
    html = """"""

    html = """
    <div class="functions">tail</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(variables,tail[0],list(tail[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """


    return html

def generateArgSHHTML(variables,args):

    html = """"""

    html += selector(variables,args[0],list(args[0].keys())[0])

    return html

def generateArgSCHTML(variables,args):

    html = """"""

    html += selector(variables,args[0],list(args[0].keys())[0])

    html += """
    <div class="symbols">&nbsp,&nbsp</div>
    """

    html += selector(variables,args[1],list(args[1].keys())[0])

    return html


def generateFunctionDefHTML(variables,functionDef,factor):
    html = """"""

    html += """
            <p class="code">"""

    
    html += f"""
            <div class="keywords">DEF&nbsp</div>
            {selector(variables,functionDef[0],list(functionDef[0].keys())[0])}
            {selector(variables,functionDef[1],list(functionDef[1].keys())[0])}"""
    
    html += selector(variables,functionDef[2],list(functionDef[2].keys())[0])

    html += """
            <div class="symbols">&nbsp{</div>
            </p>
            """
    

    html += selector(variables,functionDef[3]["body"],list(functionDef[3].keys())[0],factor)

    if len(functionDef) > 4:

        html += f"""
            <p class="code">
            <span style="margin-left: {(factor+1)*1.5}em;"></span>
            <div class="keywords">RETORNA&nbsp</div>
            """
        
        html += selector(variables,functionDef[4],list(functionDef[4].keys())[0])

        html += """
            <div class="symbols">;</div>
            </p>"""

    html += """
            <p class="code">
            <div class="symbols">}</div>
            </p>"""    



    return html


def generateReturnHTML(variables,returnValue):
    html = """"""

    html += selector(variables,returnValue[0],list(returnValue[0].keys())[0])

    return html

def generateFunctionCallHTML(variables,functionCall,factor):
    html = """"""

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""


    html += f"""{selector(variables,functionCall[0],list(functionCall[0].keys())[0])}"""

    html += """
            <div class="symbols">;</div>
            </p>"""

    return html


def generateVarHTML(variables,var,insideDec):

    html = """"""

    html += f"""<div class="variables">{selector(variables,var[0],list(var[0].keys())[0])}""" 


    if len(var) > 1:
        expression = var[1]
        html += """<div class="operators">[&nbsp</div>"""
        html += selector(variables,expression,"expressao")
        html += """<div class="operators">]</div>"""

    if insideDec:
        html += """<div class="symbols">;</div>"""


    html += """&nbsp</div>"""

    return html


def generateExpressionHTML(variables,expression):
    html = """"""

    if len(expression) > 1:
        html += f"""{selector(variables,expression[0],"expressao")}"""
        html += f"""<div class="operators">&nbsp{list(expression[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(variables,expression[2],"termo")}"""
    else:
        html += f"""{selector(variables,expression[0],"termo")}"""

    return html


def generateTermHTML(variables,term):
    html = """"""

    if len(term) > 1:
        html += f"""{selector(variables,term[0],"termo")}"""
        html += f"""<div class="operators">&nbsp{list(term[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(variables,term[2],"fator")}"""
    else:
        html += f"""{selector(variables,term[0],"fator")}"""

    return html

def generateFactorHTML(variables,factor):
    html = """"""

    if len(factor) > 1:
        html += f"""{selector(variables,factor[0],"fator")}"""
        html += f"""<div class="operators">&nbsp{list(factor[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(variables,factor[2],"atomo")}"""
    else:
        html += f"""{selector(variables,factor[0],"atomo")}"""

    return html

def generateAtomHTML(variables,atom):
    html = """"""

    atomType = list(atom[0].keys())[0]
    if atomType == "NUM":
        html += f"""<div class="numbers">{atom[0][atomType]}&nbsp</div>"""
    elif atomType == "var":
        html += f"""{selector(variables,atom[0],"var")}"""

    return html


def generateObjectHTML(variables,object):

    content = object[0]
    content_type = list(content.keys())[0]

    html = selector(variables,content,content_type)

    return html


def selector(variables,line,type,factor=0,insideDec=False):
    body = """"""
    if type == "importar":
        body += generateImportHTML(line[type])
    elif type == "comentario":
        body += generateCommentHTML(line[type],factor)
    elif type == "selecao":
        body += generateSelectionHTML(variables,line[type],factor)
    elif type == "declaracao":
        body += generateDeclarationHTML(variables,line[type],factor)
    elif type == "atribuicao":
        body += generateAssignmentHTML(variables,line[type],factor, insideDec)
    elif type == "var":            
        body += generateVarHTML(variables,line[type],insideDec)
    elif type == "expressao":
        body += generateExpressionHTML(variables,line[type])
    elif type == "termo":
        body += generateTermHTML(variables,line[type])
    elif type == "fator":
        body += generateFactorHTML(variables,line[type])
    elif type == "atomo":
        body += generateAtomHTML(variables,line[type])
    elif type == "objeto":
        body += generateObjectHTML(variables,line[type])
    elif type == "STRING":
        body += f"""<div class="strings">{line[type]}</div>"""
    elif type == "NUM":
        body += f"""<div class="numbers">{line[type]}</div>"""
    elif type == "array":
        body += generateArrayHTML(variables,line[type])
    elif type == "tuplo":
        body += generateTupleHTML(variables,line[type])
    elif type == "lista":
        body += generateListHTML(variables,line[type])
    elif type == "funcao":
        body += generateFunctionHTML(variables,line[type])
    elif type == "condicao":
        body += generateConditionHTML(variables,line[type])
    elif type == "logica":
        body += generateLogicHTML(variables,line[type])
    elif type == "SINAL":
        body += f"""<div class="operators">{line[type]}&nbsp</div>"""
    elif type == "BOOL":
        body += f"""<div class="keywords">{line[type]}&nbsp</div>"""
    elif type == "EM":
        body += f"""<div class="keywords">{line[type]}&nbsp</div>"""
    elif type == "VAR":
        #body += f"""<div class="variables">{line[type]}&nbsp</div>"""

        if line[type] in variables:
            if variables[line[type]]["foi_declarada"]==False:
                body += f"""<div class="error">{line[type]}<span class="errortext">Variável não declarada!</span></div>"""
            elif variables[line[type]]["foi_inicializada"]==False and variables[line[type]]["foi_utilizada"]==True:
                body += f"""<div class="warning">{line[type]}<span class="warningtext">Variável não inicializada!</span></div>"""
            else:
                body += f"""<div class="variables">{line[type]}&nbsp</div>"""
        else:
            body += f"""<div class="variables">{line[type]}&nbsp</div>"""

    elif type == "body":
        body += generateBodyHTML(variables,line,factor)
    elif type == "senao":
        body += generateSenaoHTML(variables,line,factor)
    elif type == "repeticao":
        body += generateRepetitionHTML(variables,line[type],factor)
    elif type == "enquanto":
        body += generateWhileHTML(variables,line[type],factor)
    elif type == "para":
        body += generateForHTML(variables,line[type],factor)
    elif type == "repetir":
        body += generateRepeatHTML(variables,line[type],factor)
    elif type == "varlista":
        body += generateVarlistHTML(variables,line[type])
    elif type == "casofinal":
        body += generateFinalCaseHTML(variables,line[type],factor)
    elif type == "caso":
        body += generateCaseHTML(variables,line[type],factor)
    elif type == "deffuncao":
        body += generateFunctionDefHTML(variables,line[type],factor)
    elif type == "chamadafuncao":
        body += generateFunctionCallHTML(variables,line[type],factor)
    elif type == "func":
        body += generateFuncHTML(variables,line[type])
    elif type == "cons":
        body += generateConsHTML(variables,line[type])
    elif type == "snoc":
        body += generateSnocHTML(variables,line[type])
    elif type == "head":
        body += generateHeadHTML(variables,line[type])
    elif type == "tail":
        body += generateTailHTML(variables,line[type])
    elif type == "argumentos":
        body += generateArgumentsHTML(variables,line[type])
    elif type == "FUNC":
        body += f"""<div class="functions">{line[type]}</div>"""
    elif type == "argumentosc":
        body += generateArgSCHTML(variables,line[type])
    elif type == "argumentosh":
        body += generateArgSHHTML(variables,line[type])
    elif type == "TIPO":
        body += f"""<div class="types">{line[type]}&nbsp</div>"""
    elif type == "retorna":
        body += generateReturnHTML(variables,line[type])
    else:
        print("ERROR::Invalid type -->", type)

    return body

def generateHTMLBody(code,variables):

    factor = 0
    
    body = f"""
    <body>
        <h2>Analisador de Código Fonte</h2>
        <div class="container">"""
    
    for line in code:
        type = list(line.keys())[0]
        body += selector(variables,line,type,factor,False)
            
    body += """
        </div>
    </body>
    """

    return body



def htmlGenerator(code, variables):
    style = generateStyleCSS()
    body = generateHTMLBody(code,variables)
    html = generateHTML(body,style)
    return html


if __name__ == '__main__':
    CONFIG_TEST_PATH = os.path.join(APP_PATH, "../tree.json")
    INFOS_PATH = os.path.join(APP_PATH, "../info.json")
    data = json.load(open(CONFIG_TEST_PATH, "r"))
    infos = json.load(open(INFOS_PATH, "r"))
    variables = infos["variaveis"]
    code = data["programa"]
    style = generateStyleCSS()
    body = generateHTMLBody(code,variables)
    html = generateHTML(body,style)
    with open(os.path.join(APP_PATH, "../generatedHTML.html"), "w") as f:
        f.write(html)
        print("HTML file generated successfully!")

