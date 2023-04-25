from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from grammar import grammar
import json
from ptyCInterpreter import PtyCInterpreter




frase = open("ciclos.txt", "r").read()

p = Lark(grammar, start="program")

parse_tree = p.parse(frase)

# print da arvore 
# print("AST: ", parse_tree)

data = PtyCInterpreter().visit(parse_tree)

#print("data: ", data)

# data in json file
with open('tree.json', 'w') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)

pydot__tree_to_png(parse_tree, "tree.png")