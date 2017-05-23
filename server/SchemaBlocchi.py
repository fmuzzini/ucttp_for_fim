from xlsschema import SchemaXls
from parsingAule import Aula
import numpy as np


class SchemaBlocchi:
    def __init__(self, C, schema_aule, file_, dict_):
        self.dati = SchemaXls(file_)
        self.schema = dict((k.upper(), v) for k, v in self.dati.schema.iteritems())
        self.dict = dict_
        self.n_c = len(C)
        self.n_att = len(schema_aule.get_set_att())
        self.corsi_att = np.array([0 for i in xrange(self.n_att*self.n_c)]).reshape((self.n_c, self.n_att))
        self.list_att = Aula.map_att.keys()
        self.list_col_att = dict((a,self.schema[a] - 2) for a in self.list_att)

        for k,block_list in self.dict.items():
            for block in block_list:
                for att in self.list_att:
                    c = block['index']
                    t = Aula.get_n_att(att)
                    if 'S' in block['att'][self.list_col_att[att]].upper():
                        self.corsi_att[c,t] = 1

    def get_corsi_att(self):
        return self.corsi_att