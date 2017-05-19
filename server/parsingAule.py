from xlsschema import SchemaXls
import numpy as np

class SchemaAule:
    def __init__(self, file_):
        self.dati = SchemaXls(file_)
        self.aule = []

        aule = self.dati.get_rows_list_schema()

        for a in aule:
            att = {}
            for k,v in a.items():
                if k == 'NOME' or k == 'SEDE' or k == 'CAPIENZA':
                    continue
                if v.upper() == 'SI':
                    att[k] = v

            item = Aula(a['NOME'], a['SEDE'], a['CAPIENZA'], att)
            self.aule.append(item)


    def get_lista_aule(self):
        res = []
        for a in self.aule:
            res.append(a.n)
        return res

    def get_aule_from_index(self, i):
        for a in self.aule:
            if a.n == i:
                return a

    def get_lista_sedi(self):
        res = np.array([0 for i in xrange(Aula.index)])
        lista = self.get_lista_aule()
        for i in lista:
            a = self.get_aule_from_index(i)
            res[i] = a.sede.n
        return res

    def get_matrix_att(self):
        n_att = len(Aula.map_att)
        n_aule = Aula.index
        res = np.array([0 for i in xrange(n_att*n_aule)]).reshape((n_aule, n_att))
        lista = self.get_lista_aule()
        for i in lista:
            a = self.get_aule_from_index(i)
            l_att = a.list_att
            for j in l_att:
                res[i,j] = 1
        return res

    def get_set_att(self):
        return set(range(len(Aula.map_att)))

    def get_set_sedi(self):
        return set(range(len(Sede.map_sedi)))

class Aula:
    map_att = {}
    index = 0

    def __init__(self, nome, sede, cap, att):
        self.nome = nome
        self.cap = cap
        self.sede = Sede.get_sede(sede)
        self.sede.add_aula(self)
        self.att = att
        self.list_att = self.get_list_att()
        self.n = Aula.index
        Aula.index = Aula.index + 1

    def get_list_att(self):
        res = []
        for a,v in self.att.items():
            res.append(Aula.get_n_att(a))
        return res

    @classmethod
    def get_n_att(cls, a):
        if Aula.map_att.has_key(a) == False:
            Aula.map_att[a] = len(Aula.map_att)
        return Aula.map_att[a]


class Sede:
    map_sedi = {}

    def __init__(self, nome, n):
        self.nome = nome
        self.n = n
        self.aule = []

    def add_aula(self, aula):
        self.aule.append(aula)

    @classmethod
    def get_sede(cls, nome):
        if Sede.map_sedi.has_key(nome) == False:
            Sede.map_sedi[nome] = Sede(nome, len(Sede.map_sedi))
        return Sede.map_sedi[nome]