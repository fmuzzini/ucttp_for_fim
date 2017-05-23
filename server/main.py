#!python

import json
from manipulate_sol import get_nonzero_index, mapping_indici
from ParsinigXls import get_data_for_model, load_data
from modello import solve_model
from parsingAule import SchemaAule
from SchemaPesi import SchemaPesi
from SchemaDisp import SchemaDisp
from SchemaParametri import SchemaParametri
from SchemaBlocchi import SchemaBlocchi
from SchemaEdi import SchemaEdi

# file contenenti i dati
file_ins = open('Insegnamenti easy2016_completo.xls', mode="rb").read()
file_man = open('Manifesto easy2016.xls', mode="rb").read()
file_piani = open('piani easy2016_con_blocchi.xls', mode="rb").read()
file_aule = open('Aule.xls', mode="rb").read()
file_pesi = open('Pesi.xls', mode='rb').read()
file_disp = open('Indisponibilita.xls', mode='rb').read()
file_param = open('Parametri.xls', mode='rb').read()
file_blocchi = open("Blocchi.xls", mode='rb').read()
file_edi = open("Edifici.xls", mode="rb").read()

# parsing dei file xls
dict_cdl, dict_aule, dict_lez_shared, lista_cod_shared, dict_preferenze_prof = load_data(file_ins, file_man, file_piani, file_aule, file_blocchi)

#parsing attrezzature
schema_aule = SchemaAule(file_aule)
LIST_ATT = schema_aule.get_matrix_att()
ATT = schema_aule.get_set_att()
EDI = schema_aule.get_mat_sedi()
E = schema_aule.get_set_sedi()

schema_pesi = SchemaPesi(file_pesi)
TAB_PESI = schema_pesi.get_tab_pesi()
meta = schema_pesi.get_meta()

schema_param = SchemaParametri(file_param, meta)
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

schema_disp = SchemaDisp(file_disp, map_corsi, meta)
PROF_OUT = schema_disp.get_prof_out()

schema_blocchi = SchemaBlocchi(C, schema_aule, file_blocchi, dict_preferenze_prof)
CORSI_ATT = schema_blocchi.get_corsi_att()
D = schema_pesi.get_d()
H = schema_pesi.get_h()
R = schema_aule.get_lista_aule()

schema_edi = SchemaEdi(C, CIC, file_edi, file_piani, map_corsi)
CORSI_EDI = schema_edi.get_corsi_edi()

# risoluzione modello
try:
    sol = solve_model(C, D, H, R, CIC, P, CLO, CL, HI, PROF_OUT, CAP_AULA, ATT, LIST_ATT, CORSI_ATT, E, EDI, CORSI_EDI, NUM_STUD, TAB_PESI, coef)
except Exception as e:
    print e.message
    exit(0)

#orario grezzo con indici
orario_raw = get_nonzero_index(sol.x)

#orario raffinato con nomi dei corsi e delle aulee
orario = mapping_indici(orario_raw, map)

j = json.dumps([o.__dict__ for o in orario])
#print j
