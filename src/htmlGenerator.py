import json
import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_PATH, "../configs/colorThemes.json")


def processLanguageElementsClasses(languageElements):
    elements = """"""
    for k,v in languageElements.items():
        elements += f"""
        .{k} {{
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


def generateCodeHTML(code):
    # Generate the HTML file
    pass


style = generateStyleCSS()
print(style)