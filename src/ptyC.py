from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
from grammar import grammar


frase = open("teste.txt", "r").read()

p = Lark(grammar, start="program")

parse_tree = p.parse(frase)

pydot__tree_to_png(parse_tree, "tree.png")