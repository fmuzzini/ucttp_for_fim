from xlsschema import SchemaXls
from parsingAule import Sede
import numpy as np


class SchemaEdi:
    def __init__(self, C, CIC, file_edi, file_corsi, map_corsi):
        self.edi = SchemaXls(file_edi)
        self.corsi = SchemaXls(file_corsi)
        self.map_corsi = map_corsi
        self.n_c = len(C)
        self.n_e = len(Sede.map_sedi)
        self.corsi_edi = np.array([0 for i in xrange(self.n_c*self.n_e)]).reshape((self.n_c,self.n_e))

        CIC_union = [c for C_ in CIC for c in C_]
        for c in CIC_union:
            l = self.get_cod(c)
            e = self.get_e(l)
            self.corsi_edi[c,e] = 1

    def get_corsi_edi(self):
        return self.corsi_edi

    def get_cod(self, c):
        l = self.map_corsi[c]['corsi effettivi'][0]['corso_di_laurea']
        return l

    def get_e(self, l):
        e = self.edi.get_campo_where('Edificio', **{'Corso di laurea': l})
        return Sede.get_sede(e).n
