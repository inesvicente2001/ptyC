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

        .error {{
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black;
            color: red;
        }}
        .code {{
            position: relative;
            display: inline-block;
            margin: 0;
        }}
        .error .errortext {{
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
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
            <title>ptyC(MUDAR TITULO)</title>
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
    

def generateCasosHTML(casos,factor):
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
    html += selector(casos[0],"var",factor)
    html += """<div class="symbols">){</div></p>"""

    # caso
    html += selector(casos[1],"caso",factor+1)
 
    # casofinal
    html += selector(casos[2],"casofinal",factor+1)
 

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


def generateFinalCaseHTML(finalCase,factor):
    
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

    html += selector(finalCase[0]["body"],"body",factor)

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


def generateCaseHTML(case,factor):
    
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
                <div class="symbols">(</div>{selector(case[i],typeCase)}<div class="symbols">)</div>"""
        html += """<div class="symbols">&nbsp{</div></p>"""

        html += selector(case[i+1]["body"],"body",factor)

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


def generateSeHTML(se,factor):

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
    html += selector(se,"logica",factor)
    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(se["body"],"body",factor)

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
        html += selector(se["senao"],"senao",factor)

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


def generateBodyHTML(body,factor):
    html = """"""

    for b in body:
        html += selector(b,list(b.keys())[0],factor+1)

    return html

def generateSenaoHTML(senao,factor):
    html = """"""

    for s in senao[0]:
        html += selector(s,list(s.keys())[0],factor+1)

    return html

def generateLogicHTML(logica):

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
            html += selector(aux,"condicao")

    return html


def generateConditionHTML(condition):

    html = """"""

    for c in condition:
        html += selector(c,list(c.keys())[0])

    return html



def generateSelectionHTML(selection, factor):
    html = """"""

    if type(selection) is dict:
        if list(selection.keys())[0] == "se":
            html += generateSeHTML(selection["se"],factor)
        elif list(selection.keys())[0] == "casos":
            html += generateCasosHTML(selection["casos"],factor)
    else:    
        print("ERROR: Invalid selection type")

    return html

def generateRepetitionHTML(repetition,factor):
    html = """"""

    repetitionType = list(repetition.keys())[0]
    
    html += selector(repetition,repetitionType,factor)

    return html


def generateWhileHTML(content,factor):
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
    html += selector(content[0],"logica",factor)
    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(content[1]["body"],"body",factor)

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

def generateForHTML(content,factor):
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
    html += selector(content[0],"var",factor)

    html += """<div class="keywords">EM&nbsp</div>"""

    # varlista
    typeVar = list(content[1].keys())[0]
    html += selector(content[1],typeVar,factor)

    html += """<div class="symbols">)&nbsp{</div></p>"""

    # body
    html += selector(content[2]["body"],"body",factor)

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


def generateVarlistHTML(varlista):

    html = """"""

    typeVar = list(varlista[0].keys())[0]
    html += selector(varlista[0],typeVar)

    return html


def generateRepeatHTML(content,factor):
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
    html += selector(content[0]["body"],"body",factor)
    
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """<div class="symbols">}&nbsp<div class="keywords">ATE</div>&nbsp(</div>"""

    # logica
    html += selector(content[1],"logica",factor)
    html += """<div class="symbols">)</div></p>"""

    html += """
            <p class="code">"""
    
            

    return html


def generateDeclarationHTML(declaration, factor):
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
        html += selector(declared,"atribuicao", factor, True)
    elif list(declared.keys())[0] == "var":
        html += selector(declared,"var", factor, True)
    

    html += f"""
    </p>"""

    return html


def generateAssignmentHTML(assignment, factor, insideDec):

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
                {selector(var,"var")}
                <div class="operators">=&nbsp</div>
                {selector(assigned,"objeto")}
                <div class="symbols">;</div>
                </p>
                """
    else:
        html = f"""
                {selector(var,"var")}
                <div class="operators">=&nbsp</div>
                {selector(assigned,"objeto")}
                <div class="symbols">;</div>
                </p>
                """
        

    return html


def generateArrayHTML(array):
    html = """
    <div class="symbols">&nbsp{</div>
    """

    if len(array) > 0:
        for element in array[0:-1]:
            html += f"""{selector(element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(array[-1],list(array[-1].keys())[0])}"""

    html += """
    <div class="symbols">}</div>
    """

    return html

def generateTupleHTML(tuple):
    html = """
    <div class="symbols">(</div>
    """

    if len(tuple) > 0:
        for element in tuple[0:-1]:
            html += f"""{selector(element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(tuple[-1],list(tuple[-1].keys())[0])}"""

    html += """
    <div class="symbols">)</div>
    """

    return html

def generateListHTML(lst):
    html = """
    <div class="symbols">[</div>
    """

    if len(lst) > 0:
        for element in lst[0:-1]:
            html += f"""{selector(element,list(element.keys())[0])}"""
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += f"""{selector(lst[-1],list(lst[-1].keys())[0])}"""

    html += """
    <div class="symbols">]</div>
    """

    return html

def generateFunctionHTML(function):
    html = """"""

    html += selector(function[0],list(function[0].keys())[0])

    return html


def generateFuncHTML(func):
    html = """"""

    # function name
    html += selector(func[0],list(func[0].keys())[0])

    # arguments
    html += selector(func[1],list(func[1].keys())[0])

    return html


def generateArgumentsHTML(argumentos):
    html = """"""

    html += """
    <div class="symbols">(</div>
    """

    if len(argumentos) > 0:
        for argument in argumentos[0:-1]:
            html += selector(argument,list(argument.keys())[0])
            html += f"""<div class="symbols">&nbsp,&nbsp</div>"""

        html += selector(argumentos[-1],list(argumentos[-1].keys())[0])

    html += """
    <div class="symbols">)</div>
    """

    return html

def generateConsHTML(cons):

    

    html = """"""

    html += """
    <div class="functions">cons</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(cons[0],list(cons[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateSnocHTML(snoc):
    html = """"""

    html += """
    <div class="functions">snoc</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(snoc[0],list(snoc[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateHeadHTML(head):
    html = """"""

    html = """
    <div class="functions">head</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(head[0],list(head[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """

    return html

def generateTailHTML(tail):
    html = """"""

    html = """
    <div class="functions">tail</div>
    <div class="symbols">(&nbsp</div>
    """

    html += selector(tail[0],list(tail[0].keys())[0])

    html += """
    <div class="symbols">)&nbsp</div>
    """


    return html

def generateArgSHHTML(args):

    html = """"""

    html += selector(args[0],list(args[0].keys())[0])

    return html

def generateArgSCHTML(args):

    html = """"""

    html += selector(args[0],list(args[0].keys())[0])

    html += """
    <div class="symbols">&nbsp,&nbsp</div>
    """

    html += selector(args[1],list(args[1].keys())[0])

    return html


def generateFunctionDefHTML(functionDef,factor):
    html = """"""

    html += """
            <p class="code">"""

    
    html += f"""
            <div class="keywords">DEF&nbsp</div>
            {selector(functionDef[0],list(functionDef[0].keys())[0])}
            {selector(functionDef[1],list(functionDef[1].keys())[0])}"""
    
    html += selector(functionDef[2],list(functionDef[2].keys())[0])

    html += """
            <div class="symbols">&nbsp{</div>
            </p>
            """
    

    html += selector(functionDef[3]["body"],list(functionDef[3].keys())[0],factor)

    if len(functionDef) > 4:

        html += f"""
            <p class="code">
            <span style="margin-left: {(factor+1)*1.5}em;"></span>
            <div class="keywords">RETORNA&nbsp</div>
            """
        
        html += selector(functionDef[4],list(functionDef[4].keys())[0])

        html += """
            <div class="symbols">;</div>
            </p>"""

    html += """
            <p class="code">
            <div class="symbols">}</div>
            </p>"""    



    return html


def generateReturnHTML(returnValue):
    html = """"""

    html += selector(returnValue[0],list(returnValue[0].keys())[0])

    return html

def generateFunctionCallHTML(functionCall,factor):
    html = """"""

    html += """
            <p class="code">"""
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""


    html += f"""{selector(functionCall[0],list(functionCall[0].keys())[0])}"""

    html += """
            <div class="symbols">;</div>
            </p>"""

    return html


def generateVarHTML(var,insideDec):

    html = f"""<div class="variables">{var[0]["VAR"]}"""  

    if len(var) > 1:
        expression = var[1]
        html += f"""<div class="classMethods">[&nbsp</div><div class="operators">{selector(expression,"expressao")}</div><div class="classMethods">]</div>"""

    if insideDec:
        html += """<div class="symbols">;</div>"""


    html += """&nbsp</div>"""

    return html


def generateExpressionHTML(expression):
    html = """"""

    if len(expression) > 1:
        html += f"""{selector(expression[0],"expressao")}"""
        html += f"""<div class="operators">&nbsp{list(expression[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(expression[2],"termo")}"""
    else:
        html += f"""{selector(expression[0],"termo")}"""

    return html


def generateTermHTML(term):
    html = """"""

    if len(term) > 1:
        html += f"""{selector(term[0],"termo")}"""
        html += f"""<div class="operators">&nbsp{list(term[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(term[2],"fator")}"""
    else:
        html += f"""{selector(term[0],"fator")}"""

    return html

def generateFactorHTML(factor):
    html = """"""

    if len(factor) > 1:
        html += f"""{selector(factor[0],"fator")}"""
        html += f"""<div class="operators">&nbsp{list(factor[1].values())[0]}&nbsp</div>"""
        html += f"""{selector(factor[2],"atomo")}"""
    else:
        html += f"""{selector(factor[0],"atomo")}"""

    return html

def generateAtomHTML(atom):
    html = """"""

    atomType = list(atom[0].keys())[0]
    if atomType == "NUM":
        html += f"""<div class="numbers">{atom[0][atomType]}&nbsp</div>"""
    elif atomType == "var":
        html += f"""{selector(atom[0],"var")}"""

    return html


def generateObjectHTML(object):

    content = object[0]
    content_type = list(content.keys())[0]

    html = selector(content,content_type)

    return html


def selector(line,type,factor=0,insideDec=False):
    body = """"""
    if type == "importar":
        body += generateImportHTML(line[type])
    elif type == "comentario":
        body += generateCommentHTML(line[type],factor)
    elif type == "selecao":
        body += generateSelectionHTML(line[type],factor)
    elif type == "declaracao":
        body += generateDeclarationHTML(line[type],factor)
    elif type == "atribuicao":
        body += generateAssignmentHTML(line[type],factor, insideDec)
    elif type == "var":            
        body += generateVarHTML(line[type],insideDec)
    elif type == "expressao":
        body += generateExpressionHTML(line[type])
    elif type == "termo":
        body += generateTermHTML(line[type])
    elif type == "fator":
        body += generateFactorHTML(line[type])
    elif type == "atomo":
        body += generateAtomHTML(line[type])
    elif type == "objeto":
        body += generateObjectHTML(line[type])
    elif type == "STRING":
        body += f"""<div class="strings">{line[type]}</div>"""
    elif type == "NUM":
        body += f"""<div class="numbers">{line[type]}</div>"""
    elif type == "array":
        body += generateArrayHTML(line[type])
    elif type == "tuplo":
        body += generateTupleHTML(line[type])
    elif type == "lista":
        body += generateListHTML(line[type])
    elif type == "funcao":
        body += generateFunctionHTML(line[type])
    elif type == "condicao":
        body += generateConditionHTML(line[type])
    elif type == "logica":
        body += generateLogicHTML(line[type])
    elif type == "SINAL":
        body += f"""<div class="operators">{line[type]}&nbsp</div>"""
    elif type == "BOOL":
        body += f"""<div class="keywords">{line[type]}&nbsp</div>"""
    elif type == "EM":
        body += f"""<div class="keywords">{line[type]}&nbsp</div>"""
    elif type == "VAR":
        body += f"""<div class="variables">{line[type]}&nbsp</div>"""
    elif type == "body":
        body += generateBodyHTML(line,factor)
    elif type == "senao":
        body += generateSenaoHTML(line,factor)
    elif type == "repeticao":
        body += generateRepetitionHTML(line[type],factor)
    elif type == "enquanto":
        body += generateWhileHTML(line[type],factor)
    elif type == "para":
        body += generateForHTML(line[type],factor)
    elif type == "repetir":
        body += generateRepeatHTML(line[type],factor)
    elif type == "varlista":
        body += generateVarlistHTML(line[type])
    elif type == "casofinal":
        body += generateFinalCaseHTML(line[type],factor)
    elif type == "caso":
        body += generateCaseHTML(line[type],factor)
    elif type == "deffuncao":
        body += generateFunctionDefHTML(line[type],factor)
    elif type == "chamadafuncao":
        body += generateFunctionCallHTML(line[type],factor)
    elif type == "func":
        body += generateFuncHTML(line[type])
    elif type == "cons":
        body += generateConsHTML(line[type])
    elif type == "snoc":
        body += generateSnocHTML(line[type])
    elif type == "head":
        body += generateHeadHTML(line[type])
    elif type == "tail":
        body += generateTailHTML(line[type])
    elif type == "argumentos":
        body += generateArgumentsHTML(line[type])
    elif type == "FUNC":
        body += f"""<div class="functions">{line[type]}</div>"""
    elif type == "argumentosc":
        body += generateArgSCHTML(line[type])
    elif type == "argumentosh":
        body += generateArgSHHTML(line[type])
    elif type == "TIPO":
        body += f"""<div class="types">{line[type]}&nbsp</div>"""
    elif type == "retorna":
        body += generateReturnHTML(line[type])
    else:
        print("ERROR::Invalid type -->", type)

    return body

def generateHTMLBody(code):

    factor = 0
    
    body = f"""
    <body>
        <h2>Análise de código</h2>
        <div class="container">"""
    
    for line in code:
        type = list(line.keys())[0]
        body += selector(line,type,factor,False)
            
    body += """
        </div>
    </body>
    """

    return body


if __name__ == '__main__':
    CONFIG_TEST_PATH = os.path.join(APP_PATH, "../testesFiles/tree.json")
    data = json.load(open(CONFIG_TEST_PATH, "r"))
    code = data["programa"]
    style = generateStyleCSS()
    body = generateHTMLBody(code)
    html = generateHTML(body,style)
    with open(os.path.join(APP_PATH, "../generatedHTML.html"), "w") as f:
        f.write(html)
        print("HTML file generated successfully!")

