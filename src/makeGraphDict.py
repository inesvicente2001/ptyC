e = 0
s = 1
sl = []

def findconnects(inst, sdg) :
    global e
    global s
    global sl

    graphstr = ""
    sl.append(inst)

    for l in sdg:
        if l[0] == inst:
            e = e + 1
            graphstr = graphstr + "\t" + l[0] + " -> " + l[1] + "\n"
            if len(l) == 3:
                graphstr = graphstr + "\t" + l[1] + " [shape=" + l[2] + "];" + "\n"
            if l[1] not in sl :
                graphstr = graphstr + findconnects(l[1], sdg)
                s = s + 1
    
    return graphstr


def make_graph_dict(inst, sdg) :
    global e
    global s
    global sl

    sl = []
    graphstr = "digraph G {\n"

    graphstr = graphstr + findconnects(inst, sdg)

    m = e - s + 2

    graphstr = graphstr + "}"

    dic = {"graph" : graphstr, "complexity" : m}

    return dic