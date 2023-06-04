e = 0
s = 1
sl = []
graphstr = ""

def findconnects(inst, sdg) :
    global e
    global s
    global sl
    global graphstr

    sl.append(inst)

    flag = 0
    for l in sdg:
        if l[0] == inst:
            flag = 1
            e = e + 1
            graphstr = graphstr + "\t" + l[0] + " -> " + l[1] + "\n"
            if len(l) == 3:
                graphstr = graphstr + "\t" + l[1] + " [shape=" + l[2] + "];" + "\n"
            if l[1] not in sl :
                findconnects(l[1], sdg)
                s = s + 1
            


def make_graph_dict(inst, sdg) :
    global e
    global s
    global sl
    global graphstr

    graphstr = graphstr + "digraph G {\n"

    findconnects(inst, sdg)

    m = e - s + 2

    graphstr = graphstr + "}"

    dic = {"graph" : graphstr, "complexity" : m}

    return dic
