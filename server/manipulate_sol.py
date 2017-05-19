import numpy as np

def get_nonzero_index(sol):
    s = get_solution_index_value(sol)
    s = [i for i in s if i.value == 1]

    return s

def get_solution_index_value(sol):
    s = np.nonzero(sol)
    s = np.array(s)
    s = np.transpose(s)

    res = []
    for i in s:
        c = i[0]
        d = i[1]
        h = i[2]
        r = i[3]
        value = sol[c, d, h, r]
        item = IndexValue(c, d, h, r, value)
        res.append(item)

    return res

def mapping_indici(orario_raw, map):
    res = [mapping(o, map) for o in orario_raw]
    return res

def mapping(o, map):
    corsi = map["corsi"]
    aule = map["aule"]

    c = corsi[o.c]
    r = aule[o.r]
    n = o.c

    res = Ora(c, o.d, o.h, r, n)

    return res


class IndexValue:
    def __init__(self, c, d, h, r, value):
        self.c = int(c)
        self.d = int(d)
        self.h = int(h)
        self.r = int(r)
        self.value = float(value)


class Ora:
    def __init__(self, c, d, h, r, n):
        self.c = c
        self.d = d
        self.h = h
        self.r = r
        self.n = n