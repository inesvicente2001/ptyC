from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from grammar import grammar
import json
from ptyCInterpreter import PtyCInterpreter
import os
from otimizacoes import otimizacoes

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_PATH, "../testes/testeBig.ptyC")


frase = open(CONFIG_PATH, "r").read()



p = Lark(grammar, start="program")

parse_tree = p.parse(frase)

# print da arvore 
# print("AST: ", parse_tree)

data = PtyCInterpreter().visit(parse_tree)

#print("data: ", data)


# otimizacoes
otimizacoes(data)


# data in json file
with open(os.path.join(APP_PATH, "../tree.json"), 'w') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)

pydot__tree_to_png(parse_tree, "../tree.png")
