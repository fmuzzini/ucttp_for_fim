#!python

import cgi
import cgitb
import os
import json

from prova import stampa_prova

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass


class Response:
    def __init__(self, meta, orario, disp):
        self.orario = [o.__dict__ for o in orario]
        ore = sorted(meta['ore'].items(), key=lambda o: o[1])
        giorni = sorted(meta['giorni'].items(), key=lambda g: g[1])
        ore = [o[0] for o in ore]
        giorni = [g[0] for g in giorni]
        self.meta = {
            'ore': ore,
            'giorni': giorni
        }
        self.disp = disp

cgitb.enable()
print "Content-type: application/json"
print ""


stampa_prova()
exit(0)

from manipulate_sol import get_nonzero_index, mapping_indici
from ParsinigXls import get_data_for_model, load_data
from modello import solve_model
from parsingAule import SchemaAule
from SchemaPesi import SchemaPesi
from SchemaDisp import SchemaDisp
from SchemaParametri import SchemaParametri
from SchemaBlocchi import SchemaBlocchi
from SchemaEdi import SchemaEdi



form = cgi.FieldStorage()

#lettura file
ins = form['insegnamenti'].file.read()
piani = form['piani'].file.read()
man = form['manifesto'].file.read()
aule = form['aule'].file.read()
blocchi = form['blocchi'].file.read()
pesi = form['pesi'].file.read()
disp = form['indisponibilita'].file.read()
param = form['parametri'].file.read()
edi = form['edifici'].file.read()

# parsing dei file xls
dict_cdl, dict_aule, dict_lez_shared, lista_cod_shared, dict_preferenze_prof = load_data(ins, man, piani, aule, blocchi)

#parsing attrezzature
schema_aule = SchemaAule(aule)
LIST_ATT = schema_aule.get_matrix_att()
ATT = schema_aule.get_set_att()
EDI = schema_aule.get_mat_sedi()
E = schema_aule.get_set_sedi()

schema_pesi = SchemaPesi(pesi)
TAB_PESI = schema_pesi.get_tab_pesi()
meta = schema_pesi.get_meta()

schema_param = SchemaParametri(param, meta)
semestre = schema_param.semestre
HI = schema_param.get_hi()

coef = {
    'edi': schema_param.edi,
    'att': schema_param.att,
    'cap': schema_param.cap,
    'comp': schema_param.comp,
    'sov': schema_param.sov
}

# ottenimento dati utili per il modello
map_corsi, C, CIC, P, CLO, NUM_STUD, CL, R, CAP_AULA, map_aule, D, H, map_giorni, map_orari = get_data_for_model(dict_cdl, dict_aule, lista_cod_shared, dict_lez_shared, dict_preferenze_prof, semestre)

map = {
     "corsi": map_corsi,
     "aule": map_aule,
     "giorni" : map_giorni,
     "orari" : map_orari
}

schema_disp = SchemaDisp(disp, map_corsi, meta)
PROF_OUT = schema_disp.get_prof_out()

schema_blocchi = SchemaBlocchi(C, schema_aule, blocchi, dict_preferenze_prof)
CORSI_ATT = schema_blocchi.get_corsi_att()
D = schema_pesi.get_d()
H = schema_pesi.get_h()
R = schema_aule.get_lista_aule()

schema_edi = SchemaEdi(C, CIC, edi, piani, map_corsi)
CORSI_EDI = schema_edi.get_corsi_edi()


# risoluzione modello
try:
    sol = solve_model(C, D, H, R, CIC, P, CLO, CL, HI, PROF_OUT, CAP_AULA, ATT, LIST_ATT, CORSI_ATT, E, EDI, CORSI_EDI,
                      NUM_STUD, TAB_PESI, coef)
except Exception as e:
    print "Problema impossibile"

# orario grezzo con indici
orario_raw = get_nonzero_index(sol.x)

# orario raffinato con nomi dei corsi e delle aulee
orario = mapping_indici(orario_raw, map)

response = Response(meta, orario, schema_disp.get_dict_disp())

#stampa in formato json
print json.dumps(response.__dict__)
