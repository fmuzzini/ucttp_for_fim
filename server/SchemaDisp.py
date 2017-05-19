from xlsschema import SchemaXls
from xlrd import xldate_as_tuple


class SchemaDisp:
    def __init__(self, file_, map_corsi, meta):
        self.dati = SchemaXls(file_)
        self.map = map_corsi
        self.meta = meta
        self.rows = self.dati.get_rows_list_schema()

        self.lista_disp = []
        for r in self.rows:
            corsi = self.get_corsi_prof(r['PROF'])
            d = self.get_n_giorno(r['GIORNO'])
            lista_h = self.get_n_ora(r['DALLE'], r['ALLE'])
            for c in corsi:
                for h in lista_h:
                    tupla = (c,d,h)
                    self.lista_disp.append(tupla)

    def get_prof_out(self):
        return self.lista_disp

    def get_corsi_prof(self, prof):
        res = []
        for k,v in self.map.items():
            if v['prof'] == prof:
                res.append(k)
        return res

    def get_n_giorno(self, giorno):
        return self.meta['giorni'][giorno]

    def get_n_ora(self, dalle_, alle_):
        dalle = xldate_as_tuple(dalle_, 0)
        dalle = '{:02d}:{:02d}'.format(dalle[3], dalle[4])
        alle = xldate_as_tuple(alle_, 0)
        alle = '{:02d}:{:02d}'.format(alle[3], alle[4])
        inizio = self.meta['ore'][dalle]
        fine = self.meta['ore'][alle]
        return range(inizio,fine)