from xlsschema import SchemaXls
from xlrd import xldate_as_tuple


class SchemaParametri:
    def __init__(self, file_, meta):
        self.dati = SchemaXls(file_)
        self.meta = meta
        self.semestre = int(self.dati.get_campo_where('Valore', Parametro='semestre'))
        self.pranzo = self.dati.get_campo_where('Valore', Parametro='ora fine pausa pranzo')
        self.cap = self.dati.get_campo_where('Valore', Parametro='valore capienza aule')
        self.att = self.dati.get_campo_where('Valore', Parametro='valore attrezzature')
        self.sov = self.dati.get_campo_where('Valore', Parametro='valore sovrapposizione corsi')
        self.edi = self.dati.get_campo_where('Valore', Parametro='valore edifici')
        self.comp = self.dati.get_campo_where('Valore', Parametro='valore compattezza orario')

    def get_hi(self):
        ora = xldate_as_tuple(self.pranzo, 0)
        o = self.meta['ore']['{:02d}:{:02d}'.format(ora[3], ora[4])]
        return [0,o]