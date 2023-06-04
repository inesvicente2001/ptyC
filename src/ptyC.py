from lark import Lark,Token,Tree
from grammar import grammar
from ptyCInterpreter import PtyCInterpreter
import os
import argparse
from otimizacoes import otimizacoes
from htmlGenerator import htmlGenerator
import json
from graphsPNG import storeGraphs
from makeGraphDict import make_graph_dict
from graphsGenerator import graphs_generator


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='ptyC: Linguagem de programação com sintaxe em português, com vista a aproveitar as vantagens das linguagens Python e C.\nUma diretoria com o ficheiro HTML e respetivas imagens é gerado na diretoria output.\nPara mais informações sobre a documentação da linguagem, consulte o README.md.')
    args_parser.add_argument(
        'input_file', nargs=1, type=str, metavar='input_file', help='ficheiro de entrada')
    args_parser.add_argument('output_folder_name', nargs=1, type=str,
                             metavar='output_folder', help='nome da diretoria gerada')
    
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

    sdg = graphs_generator(data)

    dict_sdg = make_graph_dict("\"begin\"", sdg)
    #print(dict_sdg["graph"])

    dicts_cfg = []
    shapes = []
    for g in sdg:
        if len(g) == 3:
            if g[2] == "diamond" :
                if g[1] not in shapes :
                    cfg = make_graph_dict(g[1], sdg)
                    dicts_cfg.append(cfg)
                    shapes.append(g[1])

    
    # create folder if not exists
    if not os.path.exists(os.path.join(PAR_PATH,"output",args.output_folder_name[0])):
        os.makedirs(os.path.join(PAR_PATH,"output",args.output_folder_name[0]))

    # create folder for graphs if not exists
    if not os.path.exists(os.path.join(PAR_PATH,"output",args.output_folder_name[0],"images")):
        os.makedirs(os.path.join(PAR_PATH,"output",args.output_folder_name[0],"images"))
    else:
        # delete all files in the folder
        for file in os.listdir(os.path.join(PAR_PATH,"output",args.output_folder_name[0],"images")):
            os.remove(os.path.join(PAR_PATH,"output",args.output_folder_name[0],"images",file))
    
    # create graphs PNGs and store them in the output folder inside the project folder inside the images folder
    cfgInfoLst = storeGraphs(PAR_PATH,dicts_cfg,args.output_folder_name[0],"cfg")
    sdgInfo = storeGraphs(PAR_PATH,[dict_sdg],args.output_folder_name[0],"sdg")

    html = htmlGenerator(data["programa"],info,cfgInfoLst,sdgInfo)

    OUTPUT_PATH = os.path.join(PAR_PATH,"output",args.output_folder_name[0] ,args.output_folder_name[0] + ".html")
    
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)

    
    #print("Instruções:")
    #print(json.dumps(info["instrucoes"], indent=2, sort_keys=True))
    #print("\n")
    #print("Imports:")
    #print(json.dumps(info["imports"], indent=2, sort_keys=True))
    #print("\n")
    #print("Aninhamentos:")
    #print(json.dumps(info["aninhamentos"], indent=2, sort_keys=True))
    #print("\n")
    print("No HTML gerado em " + OUTPUT_PATH + " é possível ver o analisador de código e os gráficos CFG e SDG gerados, bem como algumas informações estatísticas sobre o código do seu programa em ptyC.")




