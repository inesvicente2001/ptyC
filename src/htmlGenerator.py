import json
import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_PATH, "../configs/colorThemes.json")


# <span style="margin-left: {size}em;"></span>

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


def generateBodyHTML(code):
    
    body = f"""
    <body>
        <h2>Análise de código</h2>
        <div class="container">"""
    
    for line in code:
        type = list(line.keys())[0]
        if type == "importar":
            body += f"""
            <p class="code">
            <div class="tags">IMPORTA&nbsp</div><div class="preprocessor">{line[type]}</div>
            </p>"""
        elif type == "comentario":
            for i in range(0, len(line[type])):
                if i == 0:
                    if len(line[type]) == 1:
                        body += f"""
                        <p class="code">
                        <div class="comments">:-&nbsp</div><div class="comments">{line[type][i]}</div><div class="comments">&nbsp-:</div>
                        </p>"""
                    else:
                        body += f"""
                        <p class="code">
                        <div class="comments">:-&nbsp</div><div class="comments">{line[type][i]}</div>
                        </p>"""
                elif i == len(line[type]) - 1:
                    body += f"""
                    <p class="code">
                    <div class="comments">{line[type][i]}</div><div class="comments">&nbsp-:</div>
                    </p>"""
                else:
                    body += f"""
                    <p class="code">
                    <div class="comments">{line[type][i]}</div>
                    </p>"""
            
        
    # VER COMO TRABALHAR SEM O PRE : "<pre>"
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
    body = generateBodyHTML(code)
    html = generateHTML(body,style)
    with open(os.path.join(APP_PATH, "../generatedHTML.html"), "w") as f:
        f.write(html)
        print("HTML file generated successfully!")

