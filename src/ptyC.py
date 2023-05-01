from lark import Lark,Token,Tree
from grammar import grammar
from ptyCInterpreter import PtyCInterpreter
import os
import argparse
from otimizacoes import otimizacoes
from htmlGenerator import htmlGenerator


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='ptyC: Linguagem de programação com sintaxe em português, com vista a aproveitar as vantagens das linguagens Python e C.')
    args_parser.add_argument(
        'input_file', nargs=1, type=str, metavar='input_file', help='ficheiro de entrada')
    args_parser.add_argument('output_file_name', nargs=1, type=str,
                             metavar='output_file', help='nome do ficheiro de saída')
    
    args = args_parser.parse_args()

    APP_PATH = os.path.dirname(os.path.abspath(__file__))

    # PARENT DIRECTORY NAME
    PAR_PATH = os.path.dirname(APP_PATH)

    FILE_PATH = os.path.join(PAR_PATH, args.input_file[0])

    frase = open(FILE_PATH, "r").read()

    p = Lark(grammar, start="program")

    parse_tree = p.parse(frase)

    data,info = PtyCInterpreter().visit(parse_tree)

    otimizacoes(data)

    html = htmlGenerator(data["programa"],info["variaveis"])

    OUTPUT_PATH = os.path.join(PAR_PATH,"output" ,args.output_file_name[0] + ".html")
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)


    print(info["instrucoes"])
    print(info["imports"])
    print(info["aninhamentos"])



