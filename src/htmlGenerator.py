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
            <div class="comma">(</div>"""
    html += selector(se,"logica",factor)
    html += """<div class="comma">){</div></p>"""

    # body
    if factor > 0:
        sizeIdentation = factor*1.5
        html += f"""
        <span style="margin-left: {sizeIdentation}em;"></span>"""
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
            <div class="comma">}</div><div class="keywords">SENAO</div><div class="comma">{</div></p>"""
        html += selector(se["senao"],"senao",factor)

        html += """
            <p class="code">"""
        if factor > 0:
            sizeIdentation = factor*1.5
            html += f"""
            <span style="margin-left: {sizeIdentation}em;"></span>"""
    html += """
        <div class="comma">}</div>
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
            pass
    else:
        print("ERROR: Invalid selection type")

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
            <div class="keywords">{type}&nbsp</div>
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
                <div class="comma">;</div>
                </p>
                """
    else:
        html = f"""
                {selector(var,"var")}
                <div class="operators">=&nbsp</div>
                {selector(assigned,"objeto")}
                <div class="comma">;</div>
                </p>
                """
        

    return html


def generateVarHTML(var,insideDec):

    html = f"""<div class="variables">{var[0]["VAR"]}"""  

    if len(var) > 1:
        expression = var[1]
        html += f"""<div class="classMethods">[&nbsp</div><div class="operators">{selector(expression,"expressao")}</div><div class="classMethods">]</div>"""

    if insideDec:
        html += """<div class="comma">;</div>"""


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
    elif type == "array":
        pass
    elif type == "tuplo":
        pass
    elif type == "lista":
        pass
    elif type == "funcao":
        pass
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
    CONFIG_TEST_PATH = os.path.join(APP_PATH, "../tree.json")
    data = json.load(open(CONFIG_TEST_PATH, "r"))
    code = data["programa"]
    style = generateStyleCSS()
    body = generateHTMLBody(code)
    html = generateHTML(body,style)
    with open(os.path.join(APP_PATH, "../generatedHTML.html"), "w") as f:
        f.write(html)
        print("HTML file generated successfully!")

