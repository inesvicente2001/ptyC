from lark import Lark,Token,Tree
from grammar import grammar
from ptyCInterpreter import PtyCInterpreter
import os
import argparse
from otimizacoes import otimizacoes
from htmlGenerator import htmlGenerator
import json
from graphsPNG import storeGraphsPNG


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

    cfgInfoLst = [
        {
            "graph" : '''
            digraph G {
                inicio -> "if x"
                "if x" -> "z=2"
                "z=2" -> "z=z+1"
                "if x" -> "z=z+1"
                "z=z+1" -> "fim"
                "if x" [shape=diamond];
            }
            '''
        },
        {
            "graph" : '''
            digraph G {
                inicio -> "if x"
                "if x" -> "z=2"
                "z=2" -> "z=z+3"
                "if x" -> "z=z+3"
                "z=z+3" -> "fim"
                "if x" [shape=diamond];
            }
            '''   
        }
    ]

    # create folder if not exists
    if not os.path.exists(os.path.join(PAR_PATH,"output",args.output_file_name[0])):
        os.makedirs(os.path.join(PAR_PATH,"output",args.output_file_name[0]))

    # create folder for graphs if not exists
    if not os.path.exists(os.path.join(PAR_PATH,"output",args.output_file_name[0],"images")):
        os.makedirs(os.path.join(PAR_PATH,"output",args.output_file_name[0],"images"))
    
    # create graphs PNGs and store them in the output folder inside the project folder inside the images folder
    cfgInfoLstPath = storeGraphsPNG(PAR_PATH,cfgInfoLst,args.output_file_name[0])

    html = htmlGenerator(data["programa"],info,cfgInfoLstPath,[])

    OUTPUT_PATH = os.path.join(PAR_PATH,"output",args.output_file_name[0] ,args.output_file_name[0] + ".html")
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)

    
    print("Instruções:")
    print(json.dumps(info["instrucoes"], indent=2, sort_keys=True))
    print("\n")
    print("Imports:")
    print(json.dumps(info["imports"], indent=2, sort_keys=True))
    print("\n")
    print("Aninhamentos:")
    print(json.dumps(info["aninhamentos"], indent=2, sort_keys=True))
    print("\n")
    print("HTML gerado em: " + OUTPUT_PATH)

    print("\n")
    print(json.dumps(info, indent=2, sort_keys=True))



