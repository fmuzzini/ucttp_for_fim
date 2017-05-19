from xlsschema import SchemaXls
import numpy as np
from xlrd import xldate_as_tuple


class SchemaPesi:
    def __init__(self, file_):
        self.dati = SchemaXls(file_)
        self.ncol = self.dati.ncol - 1
        self.nrow = self.dati.nrow - 1
        self.tab_pesi = np.array([0 for i in xrange(self.nrow * self.ncol)]).reshape((self.ncol, self.nrow))
        self.day = range(self.ncol)
        self.hour = range(self.nrow)

        self.day_nome = {}
        for k,v in self.dati.schema.items():
            if k == None or k == '':
                continue

            self.day_nome[k] = v-1;

        self.hour_nome = {}
        i = 0
        for r in self.dati.get_rows_list():
            date = xldate_as_tuple(r[0].value, 0)
            ora = '{:02d}:{:02d}'.format(date[3], date[4])
            self.hour_nome[ora] = i
            i = i+1

        for i in self.day:
            for j in self.hour:
                self.tab_pesi[i,j] = self.dati.sheet.cell(j+1,i+1).value

    def get_tab_pesi(self):
        return self.tab_pesi

    def get_d(self):
        return self.day

    def get_h(self):
        return self.hour

    def get_meta(self):
        res = {
            'giorni': self.day_nome,
            'ore': self.hour_nome
        }
        return res
