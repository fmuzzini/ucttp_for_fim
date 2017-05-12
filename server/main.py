#!python

import json
from manipulate_sol import get_nonzero_index, mapping_indici
from ParsinigXls import get_data_for_model, load_data
from modello import solve_model

# file contenenti i dati
file_ins = open('Insegnamenti easy2016_completo.xls', mode="rb")
file_man = open('Manifesto easy2016.xls', mode="rb")
file_piani = open('piani easy2016_con_blocchi.xls', mode="rb")
file_aule = open('Aule.xls', mode="rb")

# parsing dei file xls
dict_cdl, dict_aule = load_data(file_ins.read(), file_man.read(), file_piani.read(), file_aule.read())

semestre = 1;
#semestre = input("Inserisci il semestre deisderato -> 1: primo semestre, 2: secondo semestre: ")
#while (semestre != 1 and semestre != 2):
#    semestre = raw_input("Inserisci il semestre deisderato -> 1: primo semestre, 2: secondo semestre: ")


# ottenimento dati utili per il modello
map_corsi, C, CIC, P, CLO, NUM_STUD, R, CAP_AULA, map_aule, D, H, map_giorni, map_orari = get_data_for_model(dict_cdl, dict_aule, semestre)
map = {
     "corsi": map_corsi,
     "aule": map_aule,
     "giorni" : map_giorni,
     "orari" : map_orari
}
HI = [0,4] #ore di inizio lezioni, prima ora e dopo pranzo


# risoluzione modello
try:
    sol = solve_model(C, D, H, R, CIC, P, CLO, HI, CAP_AULA, NUM_STUD)
except Exception as e:
    print e.message
    exit(0)

#orario grezzo con indici
orario_raw = get_nonzero_index(sol.x)

#orario raffinato con nomi dei corsi e delle aulee
orario = mapping_indici(orario_raw, map)

j = json.dumps([o.__dict__ for o in orario])
print j
