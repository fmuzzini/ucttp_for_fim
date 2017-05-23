import random

import xlrd
from copy import deepcopy
import math


# funzione che individua il numero della colonna avente come label una particolare stringa
# parametri:
#   - label_col: stringa spesso breve che deve essere contenuta nella label di una colonna
#   - worksheet: foglio di calcolo in cui cercare tale stringa
#   - exact_match: boolean di default a falso, impostato a vero per fare una ricerca esatta (ivece che di sola inclusione) della label
# return:
#   - i: indice della colonna con quella stringa nella relativa label
#   - -1: stringa non trovata

def from_string_to_label_col(label_col, worksheet, exact_match=False):
    for i in xrange(worksheet.ncols):
        for j in worksheet.col_values(i):
            if (exact_match):
                if (label_col.lower() == j.lower()):
                    return i
            else:
                if (label_col.lower() in j.lower()):
                    return i
    return -1

# funzione che permette di fare il parsing di file xls e di estrarne il contenuto significativo in dizionari
# parametri:
#   - file_ins: nome file dei dati degli insegnamenti
#   - file_man: nome file dei dati del manifesto
#   - file_piani: nome file dei dati dei piani di studio
#   - file_aule: nome file dei dati sulle aule
#   - file_blocchi: nome file dei dati sulle preferenze dei prof
# return:
#   - dict_cdl: dizionario dei dati dei corsi
#   - dict_aule: dizionario dei dati delle aule
#   - dict_lez_shared: dizionario dei corsi condivisi
#   - lista_cod_shared: lista dei corsi condivisi a coppie
#   dict_preferenze_prof: dizionario delle preferenze di un prof per un proprio corso

def load_data(file_ins, file_man, file_piani, file_aule, file_blocchi):

    ####################
    # caricamento dati #
    ####################

    workbook_ins = xlrd.open_workbook(file_contents=file_ins, encoding_override="cp1252")
    worksheet_ins = workbook_ins.sheet_by_index(0)  # ottengo il primo foglio

    workbook_man = xlrd.open_workbook(file_contents=file_man, encoding_override="cp1252")
    worksheet_man = workbook_man.sheet_by_index(0)  # ottengo il primo foglio

    workbook_piani = xlrd.open_workbook(file_contents=file_piani, encoding_override="cp1252")
    worksheet_piani = workbook_piani.sheet_by_index(0)  # ottengo il primo foglio

    workbook_aule = xlrd.open_workbook(file_contents=file_aule, encoding_override="cp1252")
    worksheet_aule = workbook_aule.sheet_by_index(0)  # ottengo il primo foglio

    workbook_blocchi = xlrd.open_workbook(file_contents=file_blocchi, encoding_override="cp1252")
    worksheet_blocchi = workbook_blocchi.sheet_by_index(0)  # ottengo il primo foglio

    ########################################################################################################################
    # - PER I CORSI -> voglio costrutire un dizionario che contiene tutti i dati, fatto nel seguente modo:
    #   - 'INFORMATICA':
    #           - 'L2':
    #                   - 1:
    #                       - 'S1':
    #                               - 'consigliato':
    #                                       'cod-gen-materia':
    #                                           - caratteristiche: ore di lezione, prof, nome_materia, blocchi_ore, num_studenti_frequentanti)
    #                               - 'obbligatorio'
    #                       - 'S2':
    #                   - 2: uguale 1
    #                   - 3: uguale 1
    #           - 'LM':
    #                   - 1: uguale 1
    #                   - 2: uguale 1
    #   - 'MATEMATICA': uguale INFORMATICA
    #   - 'FISICA': uguale INFORMATICA
    # - PER LE AULE -> voglio costruire un dizionario fatto nel seguente modo:
    #     - 'FISICA':
    #         - 'nome_aula':
    #             - caratteristiche: capienza, videoproiettore, lim, gesso
    #     - 'MATEMATICA': uguale FISICA
    ########################################################################################################################

    ######################################
    ############### CORSI ################
    ######################################

    cdl = ['INFORMATICA', 'MATEMATICA', 'FISICA']

    #######################################
    # ottengo la durata delle cdl: L2, LM #
    #######################################

    #durata_cdl = ['L2', 'LM']
    nrows_man = worksheet_man.nrows

    # ottengo gli identificativi delle colonne che utilizzo
    col_durata = from_string_to_label_col('tipo di laurea', worksheet_man) #6
    if (col_durata == -1):
        print "errore lettura dati 1"
        exit(1)

    d_cdl = set()
    for i in xrange(1, nrows_man):
        d_cdl.add(worksheet_man.cell_value(i, col_durata))
    durata_cdl = list(d_cdl)
    #print durata_cdl

    #################################################
    # ottengo i simboli identificativi dei semestri #
    #################################################

    #semestri = ['S1', 'S2']
    nrows_piani = worksheet_piani.nrows

    # ottengo gli identificativi delle colonne che utilizzo
    col_sem = from_string_to_label_col('codice periodo didattico', worksheet_piani) # 22
    if (col_sem == -1):
        print "errore lettura dati 2"
        exit(1)

    sem = set()
    for i in xrange(1, nrows_piani):
        sem.add(worksheet_piani.cell_value(i, col_sem))
    semestri = list(sem)
    #print semestri

    #########################################################
    # ottengo gli identificativi degli anni del L2 e del LM #
    #########################################################

    #anni_l2 = [1,2,3]
    #anni_lm = [1,2]

    # ottengo gli identificativi delle colonne che utilizzo
    col_anno = from_string_to_label_col('anno di corso', worksheet_man) #7
    if (col_anno == -1):
        print "errore lettura dati 3"
        exit(1)

    a_l2 = set()
    a_lm = set()
    for i in xrange(1, nrows_man):
        if (worksheet_man.cell_value(i, col_durata) == 'L2'):
            a_l2.add(int(worksheet_man.cell_value(i, col_anno)))
        if (worksheet_man.cell_value(i, col_durata) == 'LM'):
            a_lm.add(int(worksheet_man.cell_value(i, col_anno)))

    anni_l2 = list(a_l2)
    anni_lm = list(a_lm)
    #print anni_lm
    #print anni_l2

    ###########################################################
    # ottengo gli identificativi per corsi obbligatori o meno #
    ###########################################################

    #tipo_lezioni = ['consigliato', 'obbligatorio']

    # ottengo gli identificativi delle colonne che utilizzo
    col_tipo = from_string_to_label_col('obbligatorio', worksheet_piani) #20
    if (col_tipo == -1):
        print "errore lettura dati 4"
        exit(1)

    type_lez = set()
    for i in xrange(1, nrows_piani):
        type_lez.add(worksheet_piani.cell_value(i, col_tipo))
    tipo_lezioni = list(type_lez)
    #print tipo_lezioni

    #######################################################
    # creo il dizionario di tutti i dati incrementalmente #
    #######################################################

    # dizionario inizialmente vuoto -> aggiungero' dopo i nomi dei corsi
    dict_tipo_lez = {}
    for i in tipo_lezioni:
        dict_tipo_lez.setdefault(i, [])

    # dizionario dei semestri che contiene quello precedente
    dict_sem = {}
    for i in semestri:
        dict_sem[i]= deepcopy(dict_tipo_lez)

    # dizionario degli anni che contiene quello precedente
    dict_anni_l2 = {}
    for i in anni_l2:
        dict_anni_l2[i] = deepcopy(dict_sem)
    dict_anni_lm = {}
    for i in anni_lm:
        dict_anni_lm[i] = deepcopy(dict_sem)

    # dizionario della durata dei corsi che contiene quello precedente
    dict_durata_cdl = {}
    for i in durata_cdl:
        dict_durata_cdl.setdefault(i, {})
    dict_durata_cdl['L2']= deepcopy(dict_anni_l2)
    dict_durata_cdl['LM']= deepcopy(dict_anni_lm)

    # dizionario dei cdl che contiene quello precedente
    dict_cdl = {}
    for i in cdl:
        dict_cdl[i] = deepcopy(dict_durata_cdl)

    # print dict_cdl

    #####################################################
    # ottenimento codice cdl in comune tra piu file xls #
    #####################################################

    # utilizzo dei set per creare una lista di codici distiniti e non ripetuti

    # ottengo gli identificativi delle colonne che utilizzo
    col_cod_cdl = from_string_to_label_col('codice corso di laurea', worksheet_man) #2
    if (col_tipo == -1):
        print "errore lettura dati 5"
        exit(1)

    c_cdl_l2 = set()            # codici dei soli corsi del l2
    c_cdl_lm = set()            # codici dei soli corsi del lm
    c_cdl = set()               # tutti i codici
    for i in xrange(1, nrows_man):
        c_cdl_value = worksheet_man.cell_value(i, col_cod_cdl)
        c_cdl.add(c_cdl_value)
        # divido il codice cdl tra quelli della triennale e quelli della magistrale
        if (worksheet_man.cell_value(i, col_durata) == 'L2'):
            c_cdl_l2.add(c_cdl_value)
        if (worksheet_man.cell_value(i, col_durata) == 'LM'):
            c_cdl_lm.add(c_cdl_value)
    cod_cdl_lm = list(c_cdl_lm)
    cod_cdl_l2 = list(c_cdl_l2)
    cod_cdl = list(c_cdl)

    #print cod_cdl
    #print cod_cdl_l2
    #print cod_cdl_lm

    # creo un dizionario di corrispondenza tra i codici dei cdl, i loro nomi e il tipo (lm o l2):
    #   - 1234 : ['INFORMATICA', 'LM']
    #   - 4567 : ['FISICA', 'L2']
    col_name = from_string_to_label_col('corso di laurea', worksheet_man, True) #4
    if (col_name == -1):
        print "errore lettura dati 6"
        exit(1)

    old_value_cod_cdl = []
    map_codcdl_nomecdl = {}
    for i in xrange(1, nrows_man):
        c_cdl_value = worksheet_man.cell_value(i, col_cod_cdl)
        if (c_cdl_value not in old_value_cod_cdl):
            old_value_cod_cdl.append(c_cdl_value)

            map_lista_cdl = []
            nome_cdl = worksheet_man.cell_value(i, col_name) #4
            if ("INFORMATICA" in nome_cdl):
                map_lista_cdl.append("INFORMATICA")
                #print "info"
            if ("FISICA" in nome_cdl or "PHYSICS" in nome_cdl):
                map_lista_cdl.append("FISICA")
                #print "fis"
            if ("MATEMATICA" in nome_cdl):
                map_lista_cdl.append("MATEMATICA")
                #print "mat"

            if (c_cdl_value in cod_cdl_l2):
                map_lista_cdl.append("L2")
            else:
                map_lista_cdl.append("LM")

            #print map_lista_cdl

            map_codcdl_nomecdl[c_cdl_value] = map_lista_cdl

    #print map_codcdl_nomecdl

    nrows = worksheet_ins.nrows

    # riempio il dizionario creato all'inizio con nomi delle lezioni e le loro relative caratteristiche (prof, ore)
    ############################################################################################
    # NOTA: FINO AD ORA I CORSI CONDIVISI TRA PIU' CDL VENGONO INDICATI IN ENTRAMBI I CDL,     #
    # MA IL MODELLO XPRESS POTREBBE METTERLI IN ORARI DIVERSI SE NON LI INDICHIAMO COME COMUNI #
    ############################################################################################

    # prendo gli identificativi delle colonne che utilizzo
    col_cod_cdl_piani = from_string_to_label_col('codice corso di laurea', worksheet_piani) #0
    col_anno_corso = from_string_to_label_col('anno di corso', worksheet_piani) #3
    col_nome_ins = from_string_to_label_col('nome insegnamento', worksheet_piani) #14
    col_nome_ins_ins = from_string_to_label_col('nome insegnamento', worksheet_ins, True)  # 8
    col_cod_gen = from_string_to_label_col('codice insegnamento', worksheet_piani) #13
    col_cod_gen_ins = from_string_to_label_col('codice insegnamento', worksheet_ins) #7
    col_ore = from_string_to_label_col('ore frontali', worksheet_ins) #12
    col_nome_prof = from_string_to_label_col('nome docente', worksheet_ins) #14
    col_cognome_prof = from_string_to_label_col('cognome docente', worksheet_ins) #15
    col_cod_gen_piani = from_string_to_label_col('codice generale insegnamento', worksheet_piani) #10
    col_blocchi_ore = from_string_to_label_col('blocchi ore', worksheet_piani) #24
    col_num_stud = from_string_to_label_col('numero studenti', worksheet_ins)  # 19
    #print col_nome_ins_ins
    if (col_cod_cdl_piani == -1 or col_anno_corso == -1 or col_nome_ins == -1 or col_cod_gen == -1 or
                col_cod_gen_ins == -1 or col_ore == -1 or col_nome_prof == -1 or col_cognome_prof == -1 or
                col_cod_gen_piani == -1 or col_blocchi_ore == -1 or col_num_stud == -1):
        print "errore lettura dati 7"
        exit(1)

    old_cod_ins = []
    for i in xrange(1, nrows_piani):
        # ottengo i principali dati di accesso al dictionary creato all'inizio dal file dei piani
        cod_cdl =  worksheet_piani.cell_value(i, col_cod_cdl_piani)
        #print cod_cdl
        anno_corso = int(worksheet_piani.cell_value(i, col_anno_corso))
        codice_gen = worksheet_piani.cell_value(i, col_cod_gen_piani) #10
        lista_cod_cdl = map_codcdl_nomecdl.get(cod_cdl)
        tipo_lez = worksheet_piani.cell_value(i, col_tipo)
        semestre = worksheet_piani.cell_value(i, col_sem)
        #nome_lez = worksheet_piani.cell_value(i, col_nome_ins)
        blocchi_ore = int(worksheet_piani.cell_value(i, col_blocchi_ore))
        #print nome_lez
        codice_ins = worksheet_piani.cell_value(i, col_cod_gen)
        #print codice_ins

        # ottengo le relative informazioni aggiuntive della lezione dal file insegnamenti per mezzo della chiave
        # della lezione che lo unisce con il file dei piani
        for j in xrange(1, nrows):
            if ((worksheet_ins.cell_value(j, col_cod_gen_ins) == codice_ins) and (codice_ins not in old_cod_ins)):
                #print "iterazione: " + str(j)
                old_cod_ins.append(codice_ins)
                #print old_cod_ins
                lista_campi_lez = []
                ore_lez = int(worksheet_ins.cell_value(j, col_ore))
                #print ore_lez
                lista_campi_lez.append(ore_lez)
                prof = worksheet_ins.cell_value(j, col_nome_prof) + ' ' + worksheet_ins.cell_value(j, col_cognome_prof)
                nome_lez = worksheet_ins.cell_value(j, col_nome_ins_ins)
                #print prof
                lista_campi_lez.append(prof)
                lista_campi_lez.append(nome_lez) #codice_ins + nome_lez) #nome_lez)
                #print
                lista_campi_lez.append(blocchi_ore)
                # per il momento creo il numero di studenti per ogni corso in modo casuale
                num_studenti_per_corso = worksheet_ins.cell_value(j, col_num_stud)
                lista_campi_lez.append(num_studenti_per_corso)
                dict_nomi_cdl = {}
                #########MODIFICATO##########dict_nomi_cdl[codice_gen] = lista_campi_lez
                dict_nomi_cdl[codice_ins] = lista_campi_lez
                #############################dict_nomi_cdl[codice_ins] = lista_campi_lez
                #print dict_nomi_cdl
                #print lista_cod_cdl[0] + "/" + lista_cod_cdl[1] + "/" + str(anno_corso) + "/" + semestre + "/" + tipo_lez
                dict_cdl[lista_cod_cdl[0]][lista_cod_cdl[1]][anno_corso][semestre][tipo_lez].append(deepcopy(dict_nomi_cdl))

                break
        #print "######################################################"
        #if (i == 9):
        #   break

    #print dict_cdl

    #############################################
    # gestione dei corsi condivisi tra piu' cdl #
    #############################################

    # ottengo i codici di insegnamento dei corsi condivisi
    col_erog_cond = from_string_to_label_col('erogato', worksheet_ins) #0
    col_shared = from_string_to_label_col('erogante', worksheet_ins) #1
    col_name_lez = from_string_to_label_col('nome insegnamento', worksheet_ins, True) #8
    col_cdl = from_string_to_label_col('corso di laurea', worksheet_piani, True) #1
    if (col_erog_cond == -1 or col_shared == -1 or col_name_lez == -1 or col_cdl == -1):
        print "errore lettura dati 7"
        exit(1)

    # creo un dizionario fatto cosi':
    # - nome_materia:
    #       - lista di caratteristiche (es. [caratteristiche_codice_condiviso_1, caratteristiche_codice_condiviso_2])
    dict_lez_shared = {}
    lista_cod_shared = []
    for i in xrange(nrows):
        if (worksheet_ins.cell_value(i, col_erog_cond) == 'condiviso'):     # prendo i soli corsi condivisi
            nome_lez = worksheet_ins.cell_value(i, col_name_lez) #8
            dict_lez_shared.setdefault(nome_lez, [])

            # prendo i 2 codici identificativi dei due codici condivisi
            codice_ins_ins = worksheet_ins.cell_value(i, col_cod_gen_ins)
            codice_shared = worksheet_ins.cell_value(i, col_shared)

            # creo una lista di coppie di chiavi ([[],[],[],...])
            lista_tmp = []
            lista_tmp.append(codice_ins_ins)
            lista_tmp.append(codice_shared)
            lista_cod_shared.append(lista_tmp)

            # creo 2 liste che conterranno le caratteristiche di ogni corso condiviso
            caratt_first_lez_shared = []
            caratt_second_lez_shared = []
            for j in xrange(1, worksheet_piani.nrows):

                # ottengo il tipo di cdl con le sole tre stringhe possibile (info.., mat.., fis..)
                for k in cdl:
                    if (k in worksheet_piani.cell_value(j, col_cdl)): #1
                        cdl_nome = k
                        break

                cella = worksheet_piani.cell_value(j, col_cod_gen)
                # ottengo le caratteristiche solo se trovo uno dei due
                if (codice_ins_ins == cella or codice_shared == cella):

                    anno = int(worksheet_piani.cell_value(j, col_anno_corso))
                    tipo = worksheet_piani.cell_value(j, col_tipo)
                    semes = worksheet_piani.cell_value(j, col_sem)
                    durata = worksheet_piani.cell_value(j, col_cod_cdl)

                    # se corrisponde con il primo codice condiviso
                    if (codice_ins_ins == cella):
                        caratt_first_lez_shared.append(cdl_nome)
                        caratt_first_lez_shared.append(cella)
                        caratt_first_lez_shared.append(durata)
                        caratt_first_lez_shared.append(anno)
                        caratt_first_lez_shared.append(tipo)
                        caratt_first_lez_shared.append(semes)

                    # se corrisponde con il secondo codice condiviso
                    if (codice_shared == cella):
                        caratt_second_lez_shared.append(cdl_nome)
                        caratt_second_lez_shared.append(cella)
                        caratt_second_lez_shared.append(durata)
                        caratt_second_lez_shared.append(anno)
                        caratt_second_lez_shared.append(tipo)
                        caratt_second_lez_shared.append(semes)

                    # se trovati tutte e due i codici
                    if (caratt_first_lez_shared.__len__()*caratt_second_lez_shared.__len__() != 0):
                        dict_lez_shared[nome_lez].append(caratt_first_lez_shared)
                        dict_lez_shared[nome_lez].append(caratt_second_lez_shared)
                        break

    #print dict_lez_shared
    #print lista_cod_shared

    ######################################
    ################ AULE ################
    ######################################

    sede_aule = ['MATEMATICA', 'FISICA']

    # - costruisco un dizionario fatto nel seguente modo:
    #     - 'FISICA':
    #         - 'nome_aula':
    #             - caratteristiche (es. capienza, videoproiettore, lim, gesso)
    #     - 'MATEMATICA': uguale FISICA

    # creo inizialmente il dizionario ancora vuoto dei nomi delle aule
    dict_aule = {}
    for i in sede_aule:
        dict_aule.setdefault(i, {})

    # ottengo gli identificativi delle colonne che utilizzo
    col_sede = from_string_to_label_col('sede', worksheet_aule) #1
    col_nome_aule = from_string_to_label_col('nome', worksheet_aule) #0
    if (col_sede == -1 or col_nome_aule == -1):
        print "errore lettura dati 8 (aule)"
        exit(1)

    # aggiungo i nomi delle aule e le varie caratteritische al dizionario precedente
    dict_nomi_aule = {}
    for i in xrange(1, worksheet_aule.nrows):
        caratt_aule = []
        # aggiungo le caratteristiche
        for j in xrange(2, worksheet_aule.ncols):
            caratt_aule.append(worksheet_aule.cell_value(i, j))
        if ('MATEMATICA' in worksheet_aule.cell_value(i, col_sede).upper()):
            #print "mat"
            sede = sede_aule[0]
        else:
            sede = sede_aule[1]
            #print "fis"
        dict_aule[sede][worksheet_aule.cell_value(i, col_nome_aule)] = caratt_aule

    #print dict_aule

    ################################################################
    # raccolta dati preferenze professore (blocchi ore, strumenti) #
    ################################################################

    # creo un dizionario che raccoglie le preferenze di un prof
    #   - codice corso 1:
    #       - lista di preferenze (es. 2 ore, lab si ...)
    #   - codice corso 1:
    #       - lista di preferenze (es. 3 ore, lab si ...)
    #   - codice corso 1 ripetuto per tutti i blocchi di ore della settimana
    #   - codice corso 2:
    #       - .....
    dict_preferenze_prof = {}

    col_key = from_string_to_label_col('codice corso completo', worksheet_blocchi)  # 0
    col_ore_blocco = from_string_to_label_col('ore blocco', worksheet_blocchi)  # 1
    if (col_key == -1 or col_ore_blocco == -1):
        print 'errore dati 9 (blocchi)'
        exit(1)

    # popolo il dizionario dei dati
    for i in xrange(1, worksheet_blocchi.nrows):
        key = worksheet_blocchi.cell_value(i, col_key)

        # ottengo i dati delle preferenze
        lista_att = []
        for j in xrange(col_ore_blocco+1, worksheet_blocchi.ncols):
            data = worksheet_blocchi.cell_value(i, j)
            lista_att.append(data)

        item = {
            'ore': int(worksheet_blocchi.cell_value(i, col_ore_blocco)),
            'index': None,
            'att': lista_att
        }
        try:
            dict_preferenze_prof[key].append(item)
        except KeyError:
            dict_preferenze_prof.setdefault(key, [item])

    return dict_cdl, dict_aule, dict_lez_shared, lista_cod_shared, dict_preferenze_prof

# funzione che estrae dai vari dizionari solo le informazioni relative ad un particolare semestre
# parametri:
#   - dict_corsi_s1_s2: dizionario di mapping dei corsi con il proprio identificativo
#   - dict_set_C_s1_s2: dizionario degli insiemi delle ore
#   - dict_CIC_s1_s2: dizionario delle ore iniziali dei corsi
#   - dict_P_s1_s2: dizionario dei corsi dei prof
#   - dict_CLO_s1_s2: dizionario dei corsi obbligatori
#   - dict_num_stud: dizionario del numero degli studenti frequentanti
#   - dictCL: dizionario delle ore di CL (anche consigliate)
#   - sem: chiave di accesso e filtro dei dati contenuti nei precedenti dizionari
# return:
#   - CORSI: lista di mapping dei corsi di un particolare semestre con i rispettivi identificativi
#   - C: insieme delle ore dei corsi di un particolare semestre
#   - CIC: lista delle ore iniziali dei corsi di un particolare semestre
#   - P: lista dei corsi dei prof di un particolare semestre
#   - CLO: lista dei corsi obbligatori di un particolare semestre
#   - NUM_STUD: lista degli studenti frequentanti i corsi di un particolare semestre
#   - CL: lista delle ore dei corsi (anche consigliate) di un particolare semestre
def extract_semestre_from_dict(dict_corsi_s1_s2, dict_set_C_s1_s2, dict_CIC_s1_s2, dict_P_s1_s2, dict_CLO_s1_s2, dict_num_stud, dict_CL, sem):
    CORSI = dict_corsi_s1_s2[sem]
    C = dict_set_C_s1_s2[sem]
    CIC = dict_CIC_s1_s2[sem]
    P = dict_P_s1_s2[sem]
    CLO = dict_CLO_s1_s2[sem]
    NUM_STUD = dict_num_stud[sem]
    CL = dict_CL[sem]
    return CORSI, C, CIC, P, CLO, NUM_STUD, CL

#funzione che resituisce le informazioni principali di un corso condiviso, preso dal dizionario dei corsi condivisi (utile sia per i CLO che per i CL)
# parametri:
#   - dict_lez_shared: dizionario dei corsi condivisi
#   - key_shared: chiave del corso condiviso da cercare
# return:
#   - tupla delle caratteristiche (vuota se non lo trova)
def get_data_course_cond(dict_lez_shared, key_shared):
    index_key = 1
    for key, value in dict_lez_shared.iteritems():
        for corso_shared in value:
            if (corso_shared[index_key] == key_shared):
                list_tmp = []
                for val in corso_shared:
                    list_tmp.append(str(val))
                return tuple(list_tmp)

    return ()

# funzione che permette di aggiungere alla lista delle ore dei corsi sia di CLO che di CL le ore dei corsi condivisi (sia obbligatorie che consigliate)
# parametri:
#   - dict_map_ore_course_shared: dizionario di mapping tra ore e corsi condivisi
#   - k_cdl: tipologia di corso di laurea del corso
#   - k_durata: durata degli studi (es. L2 o LM)
#   - k_anni: anno del corso
#   - k_sem: semestre del corso
#   - lista_ore_semestre: lista delle ore (certe volte di CLO altre di CL)
#   - flag: selettore di scelta tra CLO e CL (default a True per i CLO)
# return:
#   - aggiornamento della lista passata
def add_ore_corso_cond(dict_map_ore_course_shared, k_cdl, k_durata, k_anni, k_sem, lista_ore_semestre, flag=True):
    for chiave, valore in dict_map_ore_course_shared.iteritems():
        lista_chiave = chiave.split('/')
        if (flag):              # per i CLO
            if (lista_chiave[0] == k_cdl and lista_chiave[2] == k_durata and int(lista_chiave[3]) == k_anni and lista_chiave[4] == 'obbligatorio'
                and lista_chiave[5] == k_sem):
                for ora in valore:
                    if (ora not in lista_ore_semestre):
                        lista_ore_semestre.append(ora)
        else:                   # per i CL
            if (lista_chiave[0] == k_cdl and lista_chiave[2] == k_durata and int(lista_chiave[3]) == k_anni and lista_chiave[5] == k_sem):
                for ora in valore:
                    if (ora not in lista_ore_semestre):
                        lista_ore_semestre.append(ora)

# funzione che permette di ottenere il codice del corso condiviso in coppia con quello la cui chiave e' richiesta in ingresso
# parametri:
#   - lista_cod_shared: lista di coppie di codici di corsi condivisi
#   - key: chiave del corso condiviso che permette la ricerca
# return:
#   - chiave del corso condiviso con quello ricevuto in ingresso
def search_cod_shared(lista_cod_shared, key):
    #trovo in che coppia (intesa come lista e' presente)
    index = 0
    for i in xrange(len(lista_cod_shared)):
        if (key in lista_cod_shared[i]):
            index = i
            break

    # restituisco l'altro codice della coppia
    if (lista_cod_shared[index][0] == key):
        return lista_cod_shared[index][1]
    return lista_cod_shared[index][0]

num_settimane_semestre = 12
# funzione che converte il numero di ore semestrali (presenti nei dati) in ore settimanali
# parametri:
#   - ore_sem: ore di un corso in un semestre
# return:
#   - ore settimanli di quel corso arrotondate per eccesso
def from_ore_semestrali_to_ore_settimanali(ore_sem):
    return int(math.ceil(ore_sem / float(num_settimane_semestre)))

# funzione che trova nel dizionario generale dei corsi uno stesso corso in piu' cdl
# parametri:
#   - cdl: nome del cdl della lezione corrente nel ciclo for
#   - sem: semestre della lezione corrente nel ciclo for
#   - key_corso: chiave della lezione corrente nel ciclo for
#   - dict_cdl: dizionario generale dei corsi
# return:
#   - lista: lista contenente stessa lezione di eventuali altri cdl
def search_same_course_in_other_cdl(cdl, sem, key_corso, dict_cdl):
    lista = []
    index_nome = 2
    for k_cdl, v_cdl in dict_cdl.iteritems():
        for k_durata, v_durata in v_cdl.iteritems():
            for k_anni, v_anni in v_durata.iteritems():
                for k_sem, v_sem in v_anni.iteritems():
                    for k_tipo, v_tipo in v_sem.iteritems():
                        for corso in v_tipo:
                            for key, value in corso.iteritems():

                                if (key == key_corso and k_cdl != cdl and k_sem == sem):
                                    lista.append({'corso_di_laurea': k_cdl, 'mag_tr': k_durata, 'anno': k_anni,
                                                'tipo': k_tipo, 'nome': value[index_nome], 'chiave': key_corso})
    return lista


# funzione che estrae dai dizionari dei dati dei corsi e delle aule le informazioni utili per il modello
# parametri:
#   - dict_cdl: dizionario dei dati dei corsi
#   - dict_aule: dizionario dei dati delle aule
#   - dict_lez_shared: dizionario dei corsi condivisi
#   - lista_cod_shared: lista dei corsi condivisi a coppie
#   - dict_preferenze_prof: dizionario delle preferenze di un prof per un proprio corso
#   - semestre_scelto: identificativo numerico del semestre di interesse
# return:
#   - CORSI: dizionario di mapping tra corsi e ore
#   - C: insieme delle ore dei corsi di un particolare semestre
#   - CIC: lista delle ore iniziali dei corsi di un particolare semestre
#   - P: lista dei corsi dei prof di un particolare semestre
#   - CLO: lista dei corsi obbligatori di un particolare semestre
#   - NUM_STUD: lista degli studenti frequentanti i corsi di un particolare semestre
#   - R: identificativi delle aule
#   - lista_cap_aule: lista delle capienze delle aule
#   - dict_id_aule: dizionario mapping tra identificativi e nomi aule
#   - D: giorni
#   - H: fasce orarie
#   - dict_giorni: dizionario di mapping per i giorni
#   - dict_orari: dizionario di mapping per le fasce orarie
def get_data_for_model(dict_cdl, dict_aule, lista_cod_shared, dict_lez_shared, dict_preferenze_prof, semestre_scelto):

    #######################################################
    # raccolta dati singoli che servono al modello xpress #
    #######################################################

    ###############
    # PER I CORSI #
    ###############

    # creo dizionario di mapping tra identificativi delle ore e corsi (anche condivisi tra cdl) diviso nei due semestri
    # - s1:
    #   - 0: {  prof: 'nome prof 1'
    #           corsi_effettivi:
    #               [
    #                   {   corso_di_laurea: 'informatica'
    #                       mag_tr: 'LM'
    #                       anno: 1
    #                       tipo: 'obbligatorio'
    #                       nome: 'nome corso'
    #                    },
    #                   {   corso_di_laurea: 'matematica'
    #                       mag_tr: 'LM'
    #                       anno: 1
    #                       tipo: 'obbligatorio'
    #                       nome: 'stesso nome corso'
    #                   },
    #                   {   corso_di_laurea: 'fisica'
    #                       mag_tr: 'LM'
    #                       anno: 2
    #                       tipo: 'consigliato'
    #                       nome: 'stesso nome corso'
    #                    }
    #              ]
    #         }
    #   - 1: uguale a 0(tutto uguale per tutte le ore di tale corso)
    #   - 6: stessa struttura, ma altro corso.
    # - s2: uguale a s1
    dict_map_ore_corso_s1 = {}
    dict_map_ore_corso_s2 = {}
    index_c_s1 = 0
    index_c_s2 = 0
    index_copia_s1 = 0
    index_copia_s2 = 0
    key_dict_inside = ['prof', 'corsi effettivi']
    dict_inside_map_ore_corso_s1 = {}
    dict_inside_map_ore_corso_s2 = {}
    for i in key_dict_inside:
        dict_inside_map_ore_corso_s1.setdefault(i, [])
        dict_inside_map_ore_corso_s2.setdefault(i, [])

    # creo un dizionario di tutti gli identificativi delle ore dei corsi diviso nei due semestri
    # (di fatto prendo i numeri del dizionario precedente)
    # - s1: (1,2,3,4 ...)
    # - s2: uguale a s1
    set_C_S1 = set()
    set_C_S2 = set()

    # creo un dizionario che conterra' gli identificativi delle ore di inizio delle lezioni
    # separate (lista di liste), divise nei due semestri
    # - s1: [[0,2], [3,5,7],[9,12]]
    # - s2: uguale a s1
    lista_CI_s1 = []
    lista_CI_s2 = []

    # creo un dizionario dei corsi obbligatori (intesi come ore) di ogni semestre e di ogni anno (lista di liste) diviso nei due semestri
    # - s1: [[0,1,2,3],[4,5,6,7], [10], [13]]
    # - s2: uguale a s1
    lista_CO_s1 = []
    lista_CO_s2 = []
    index_corsi_s1 = -1
    index_corsi_s2 = -1

    # creo un dizionario di identificazione dei prof
    # - s1:
    #   - 0: prof 1
    #   - 1: prof 2
    # - s2: uguale a s1
    dict_prof_s1 = {}
    dict_prof_s2 = {}
    index_prof_s1 = 0
    index_prof_s2 = 0
    old_prof_s1 = []
    old_prof_s2 = []

    # creo un dizionario dei prof con i loro rispettivi corsi intesi come le ore relative, il tutto diviso per i due semestri
    # - s1:
    #       - 0: [corsi prof 1 in ore]
    #       - 1: [corsi prof 2 in ore]
    # - s2:
    #       - uguale a s1
    # NOTA: come indici utilizzo quelli dei corsi gia' usati precedentemente
    dict_map_prof_corsi_s1 = {}
    dict_map_prof_corsi_s2 = {}

    # creo un dizionario del numero degli studenti ripetuti per ogni ora di ogni corso diviso per i due semestri
    # - s1: [33, 33, 33, 33, 53, 53, 53, 53]
    # - s2: uguale a s1
    lista_num_stud_s1 = []
    lista_num_stud_s2 = []

    # creo un dizionario dei corsi diviso nei vari semestri
    # - s1:
    #   - 0: corso 0
    #   - 1: corso 1
    # - s2: uguale a s1
    dict_corsi_s1 = {}
    dict_corsi_s2 = {}

    # creo una versione srotolata della lista dei codici condivisi
    # utile per fare un controllo di esistenza di codici in maniera immediata
    lista_cod_shared_srotolata = []
    for i in lista_cod_shared:
        lista_cod_shared_srotolata += i

    # creo dei dizionari di mapping tra corso condiviso e ore in comune
    # carattersitche_corso_shared_1 = [0 1 2 3 4]
    # carattersitche_corso_shared_2 = [100 101 102 103]
    dict_map_ore_course_shared_s1 = {}
    dict_map_ore_course_shared_s2 = {}

    # creo i dizionari di CL per entrambi i semestri
    # tali dizionari contengono le ore dei relativi corsi di laurea (anche quelli consigliati)
    # [[0,1,2,3,4,5..], [10,11,12..], ...]
    lista_CL_s1 = []
    lista_CL_s2 = []
    # NOTA: sfrutto gli stessi dizionari di mapping tra ore e corsi condivisi

    old_cod_gen_ins = []
    index_ore = 0
    index_prof = 1
    index_nome = 2
    index_blocchi_ore = 3
    index_num_stud = 4
    for k_cdl, v_cdl in dict_cdl.iteritems():
        for k_durata, v_durata in v_cdl.iteritems():
            for k_anni, v_anni in v_durata.iteritems():
                for k_sem, v_sem in v_anni.iteritems():
                    # per i CLO
                    lista_co_semestre_s1 = []
                    lista_co_semestre_s2 = []
                    # per i CL
                    lista_CL_semestre_s1 = []
                    lista_CL_semestre_s2 = []
                    for k_tipo, v_tipo in v_sem.iteritems():
                        for corso in v_tipo:
                            for key, value in corso.iteritems():
                                ore_semestrali_corso = value[index_ore]
                                blocchi_ore_corso = value[index_blocchi_ore]
                                ore_settimanali = from_ore_semestrali_to_ore_settimanali(ore_semestrali_corso)
                                prof = value[index_prof]
                                num_stud = value[index_num_stud]

                                # creo due liste che utilizzero' anche piu' avanti
                                # servono per memorizzare le ore dei corsi condivisi
                                lista_tmp_ore_anche_cons_s1 = []
                                lista_tmp_ore_anche_cons_s2 = []
                                if (k_sem == 'S1'):
                                    # per gli indici delle ore (sia per CLO che per CL)
                                    lista_tmp_ore_anche_cons_s1 = range(index_c_s1, index_c_s1 + ore_settimanali)

                                else:           # s2
                                    # per gli indici delle ore (sia per CLO che per CL)
                                    lista_tmp_ore_anche_cons_s2 = range(index_c_s2, index_c_s2 + ore_settimanali)

                                # nuovo corso (e anche solo uno dei corsi condivisi della coppia)
                                if (key not in old_cod_gen_ins):
                                    key_shared = ''
                                    if (key in lista_cod_shared_srotolata):
                                        # cerco codice corso con il quale il corso corrente e' condiviso

                                        key_shared = search_cod_shared(lista_cod_shared, key)
                                        old_cod_gen_ins.append(key_shared)

                                    # contatore per i corsi (dict_corsi_s1 e s2)
                                    if (k_sem == 'S1'):
                                        index_corsi_s1 += 1

                                        # appendo al dizionario di mapping tra corso condiviso e ore condivise

                                        # cerco le caratteristiche dell'altro corso; le utilizzero' come chiave
                                        # fatta a path (tale dizionario serve sia a CLO che ha CL)

                                        if (key_shared != ''):
                                            tupla_caratt_corso_shared = get_data_course_cond(dict_lez_shared, key_shared)
                                            if (tupla_caratt_corso_shared):
                                                key_dict_map_ore_course_shared_s1 = '/'.join(tupla_caratt_corso_shared)
                                                dict_map_ore_course_shared_s1[key_dict_map_ore_course_shared_s1] = lista_tmp_ore_anche_cons_s1

                                        # per il dizionario di mapping dei corsi
                                        dict_tmp = {'corso_di_laurea': k_cdl, 'mag_tr': k_durata, 'anno': k_anni,
                                                    'tipo': k_tipo, 'nome': value[index_nome], 'chiave': key}
                                        list_tmp = []
                                        list_tmp.append(dict_tmp)

                                        new_lista = []
                                        if (key_shared != ''):      # se corso condiviso
                                            new_lista = search_same_course_in_other_cdl(k_cdl, k_sem, key_shared,
                                                                                        dict_cdl)
                                        list_tmp += new_lista
                                        dict_inside_map_ore_corso_s1['prof'] = prof
                                        dict_inside_map_ore_corso_s1['corsi effettivi'] = list_tmp

                                        try:
                                            lista_blocchi_ore = dict_preferenze_prof[key]
                                            lista_ore_iniz = []
                                            lista_ore_iniz.append(index_c_s1)
                                            index_copia_c = index_c_s1
                                            last_block = 0
                                            first_field_pref = 'ore'
                                            fine_ore_real = index_c_s1 + ore_settimanali
                                            sum_ore = 0
                                            max_ore = 3
                                            for bo in xrange(len(lista_blocchi_ore)):
                                                last_block = lista_blocchi_ore[bo][first_field_pref]
                                                sum_ore += last_block
                                                index_copia_c += last_block

                                                lista_blocchi_ore[bo]['index'] = index_copia_c - last_block

                                                if (fine_ore_real - index_copia_c > max_ore):       # se lo scarto e' grande e posso aggiungere ore
                                                    lista_ore_iniz.append(index_copia_c)
                                                else:
                                                    # non aggiungo l'inizio ora se e' l'utlima lista o se si va oltre le ore possibili
                                                    if (bo != len(lista_blocchi_ore)-1 and index_copia_c < fine_ore_real):
                                                        lista_ore_iniz.append(index_copia_c)

                                            fine_ore = index_c_s1 + sum_ore

                                            # se non ho raggiunto tutte le ore di quel corso attraverso le preferenze indicate
                                            if (fine_ore < fine_ore_real):
                                                remain = fine_ore_real - fine_ore       # prendo lo scarto
                                                blocchi_default = 2
                                                lista_ore_iniz += range(lista_ore_iniz[-1] + blocchi_default, fine_ore + remain, blocchi_default)

                                            lista_CI_s1.append(lista_ore_iniz)
                                        except KeyError:                # se non e' stata inserita una preferenza per quel corso
                                            lista_CI_s1.append(range(index_c_s1, index_c_s1 + ore_settimanali, blocchi_ore_corso))

                                    else:
                                        index_corsi_s2 += 1

                                        # appendo al dizionario di mapping tra corso condiviso e ore condivise

                                        # cerco le caratteristiche dell'altro corso; le utilizzero' come chiave
                                        # fatta a path (tale dizionario serve sia a CLO che ha CL)
                                        if (key_shared != ''):
                                            tupla_caratt_corso_shared = get_data_course_cond(dict_lez_shared,
                                                                                             key_shared)
                                            if (tupla_caratt_corso_shared):
                                                key_dict_map_ore_course_shared_s2 = '/'.join(tupla_caratt_corso_shared)
                                                dict_map_ore_course_shared_s2[
                                                    key_dict_map_ore_course_shared_s2] = lista_tmp_ore_anche_cons_s2

                                        # per il dizionario di mapping dei corsi
                                        dict_tmp = {'corso_di_laurea': k_cdl, 'mag_tr': k_durata, 'anno': k_anni,
                                                    'tipo': k_tipo, 'nome': value[index_nome], 'chiave': key}
                                        list_tmp = []
                                        list_tmp.append(dict_tmp)

                                        new_lista = []
                                        if (key_shared != ''):  # se corso condiviso
                                            new_lista = search_same_course_in_other_cdl(k_cdl, k_sem, key_shared,
                                                                                        dict_cdl)
                                        list_tmp += new_lista
                                        dict_inside_map_ore_corso_s2['prof'] = prof
                                        dict_inside_map_ore_corso_s2['corsi effettivi'] = list_tmp

                                        try:
                                            lista_blocchi_ore = dict_preferenze_prof[key]
                                            lista_ore_iniz = []
                                            lista_ore_iniz.append(index_c_s2)
                                            index_copia_c = index_c_s2
                                            last_block = 0
                                            first_field_pref = 0
                                            fine_ore_real = index_c_s2 + ore_settimanali
                                            sum_ore = 0
                                            max_ore = 3
                                            for bo in xrange(len(lista_blocchi_ore)):
                                                last_block = lista_blocchi_ore[bo][first_field_pref]
                                                sum_ore += last_block
                                                index_copia_c += last_block

                                                if (fine_ore_real - index_copia_c > max_ore):       # se lo scarto e' grande e posso aggiungere ore
                                                    lista_ore_iniz.append(index_copia_c)
                                                else:
                                                    # non aggiungo l'inizio ora se e' l'utlima lista o se si va oltre le ore possibili
                                                    if (bo != len(lista_blocchi_ore)-1 and index_copia_c < fine_ore_real):
                                                        lista_ore_iniz.append(index_copia_c)

                                            fine_ore = index_c_s2 + sum_ore

                                            # se non ho raggiunto tutte le ore di quel corso attraverso le preferenze indicate
                                            if (fine_ore < fine_ore_real):
                                                remain = fine_ore_real - fine_ore       # prendo lo scarto
                                                blocchi_default = 2
                                                lista_ore_iniz += range(lista_ore_iniz[-1] + blocchi_default, fine_ore + remain, blocchi_default)

                                            lista_CI_s2.append(lista_ore_iniz)
                                        except KeyError:                # se non e' stata inserita una preferenza per quel corso
                                            lista_CI_s2.append(range(index_c_s2, index_c_s2 + ore_settimanali, blocchi_ore_corso))

                                    # per ripetere lo stesso corso in base a quante ore settimanali dispone
                                    for t in xrange(ore_settimanali):
                                        if (k_sem == 'S1'):

                                            dict_corsi_s1[index_corsi_s1] = value[index_nome]

                                            # per i professori
                                            # nuovo prof
                                            if (prof not in old_prof_s1):
                                                old_prof_s1.append(prof)
                                                dict_prof_s1[index_prof_s1] = prof

                                                # creo una lista (anche per un corso), cosi' mi risulta piu' facile
                                                #  appendere altri eventuali corsi dello stesso prof
                                                tmp_list = []
                                                tmp_list.append(index_c_s1)
                                                dict_map_prof_corsi_s1[index_prof_s1] = tmp_list

                                                index_prof_s1 += 1
                                            else:           # prof gia' incontrato
                                                index_prof_searched = old_prof_s1.index(prof)           # cerco il prof gia' incontrato
                                                dict_map_prof_corsi_s1[index_prof_searched].append(index_c_s1)

                                            # per i corsi obbligatori
                                            if (k_tipo == 'obbligatorio'):
                                                lista_co_semestre_s1.append(index_c_s1)

                                            # per i CL
                                            lista_CL_semestre_s1.append(index_c_s1)

                                            # per gli studenti
                                            lista_num_stud_s1.append(num_stud)

                                            # per il dizionario di mapping dei corsi
                                            dict_map_ore_corso_s1[index_c_s1] = deepcopy(dict_inside_map_ore_corso_s1) #value[index_nome]
                                            #print dict_map_ore_corso_s1
                                            set_C_S1.add(index_c_s1)
                                            index_c_s1 += 1
                                            index_copia_s1 += 1

                                        else:       # s2

                                            dict_corsi_s2[index_corsi_s2] = value[index_nome]

                                            # per i professori
                                            # nuovo prof
                                            if (prof not in old_prof_s2):
                                                old_prof_s2.append(prof)
                                                dict_prof_s2[index_prof_s2] = prof

                                                # creo una lista (anche per un corso), cosi' mi risulta piu' facile
                                                #  appendere altri eventuali corsi dello stesso prof
                                                tmp_list = []
                                                tmp_list.append(index_c_s2)
                                                dict_map_prof_corsi_s2[index_prof_s2] = tmp_list

                                                index_prof_s2 += 1
                                            else:  # prof gia' incontrato
                                                index_prof_searched = old_prof_s2.index(prof)           # cerco il prof gia' incontrato
                                                dict_map_prof_corsi_s2[index_prof_searched].append(index_c_s2)

                                            # per i corsi obbligatori
                                            if (k_tipo == 'obbligatorio'):
                                                lista_co_semestre_s2.append(index_c_s2)

                                            # per i CL
                                            lista_CL_semestre_s2.append(index_c_s2)

                                            # per gli studenti
                                            lista_num_stud_s2.append(num_stud)

                                            # per il dizionario di mapping dei corsi
                                            dict_map_ore_corso_s2[index_c_s2] = deepcopy(dict_inside_map_ore_corso_s2)  # value[index_nome]
                                            set_C_S2.add(index_c_s2)
                                            index_c_s2 += 1
                                            index_copia_s2 += 1
                                else:           # uno dei due corsi condivisi della coppia
                                    if (k_sem == 'S1'):
                                        # per i CLO
                                        add_ore_corso_cond(dict_map_ore_course_shared_s1, k_cdl, k_durata, k_anni,
                                                           k_sem, lista_co_semestre_s1)
                                        # per i CL
                                        add_ore_corso_cond(dict_map_ore_course_shared_s1, k_cdl, k_durata, k_anni,
                                                           k_sem, lista_CL_semestre_s1, False)

                                    if (k_sem == 'S2'):
                                        # per i CLO
                                        add_ore_corso_cond(dict_map_ore_course_shared_s2, k_cdl, k_durata, k_anni, k_sem, lista_co_semestre_s2)
                                        # per i CL
                                        add_ore_corso_cond(dict_map_ore_course_shared_s2, k_cdl, k_durata, k_anni, k_sem, lista_CL_semestre_s2, False)

                                    index_copia_s1 += 1
                                    index_copia_s2 += 1

                    # per i CLO
                    if (lista_co_semestre_s1 != []):
                        #print k_cdl + k_durata + str(k_anni)
                        lista_CO_s1.append(lista_co_semestre_s1)
                    if (lista_co_semestre_s2 != []):
                        lista_CO_s2.append(lista_co_semestre_s2)
                    # per i CL
                    if (lista_CL_semestre_s1 != []):
                        lista_CL_s1.append(lista_CL_semestre_s1)
                    if (lista_CL_semestre_s2 != []):
                        lista_CL_s2.append(lista_CL_semestre_s2)

    # raggruppo i dizionari dei CL
    dict_CL = {}
    dict_CL['S1'] = lista_CL_s1
    dict_CL['S2'] = lista_CL_s2
    #print 'CL: ' + str(dict_CL)

    # raggruppo i dizionari del mapping ore e corso con le chiavi dei due semestri
    dict_map_ore_corso_s1_s2 = {}
    dict_map_ore_corso_s1_s2['S1'] = dict_map_ore_corso_s1
    dict_map_ore_corso_s1_s2['S2'] = dict_map_ore_corso_s2
    #print 'MAP CIC E CORSI: ' + str(dict_map_ore_corso_s1_s2)

    #print dict_map_ore_course_shared_s1

    # raggruppo i dizionari dei corsi con le chiavi dei due semestri
    dict_corsi_s1_s2 = {}
    dict_corsi_s1_s2['S1'] = dict_corsi_s1
    dict_corsi_s1_s2['S2'] = dict_corsi_s2
    #print dict_corsi_s1.__len__()
    #print dict_corsi_s2.__len__()
    #print 'CORSI: ' + str(dict_corsi_s1_s2)

    # raggruppo i dizionari delle ore con le chiavi dei due semestri
    dict_set_C_s1_s2 = {}
    dict_set_C_s1_s2['S1'] = set_C_S1
    dict_set_C_s1_s2['S2'] = set_C_S2
    #print set_C_S1.__len__()
    #print set_C_S2.__len__()
    #print 'C: ' + str(dict_set_C_s1_s2)

    # raggruppo i dizionari delle ore iniziali con le chiavi dei due semestri
    dict_CIC_s1_s2 = {}
    dict_CIC_s1_s2['S1'] = lista_CI_s1
    dict_CIC_s1_s2['S2'] = lista_CI_s2
    #print 'CIC: ' + str(dict_CIC_s1_s2)

    # raggruppo i dizionari dei corsi obbligatori con le chiavi dei due semestri
    dict_CLO_s1_s2 = {}
    dict_CLO_s1_s2['S1'] = lista_CO_s1
    dict_CLO_s1_s2['S2'] = lista_CO_s2
    #print bo1
    #print bo2
    #print 'CLO: ' + str(dict_CLO_s1_s2)

    # raggruppo i dizionari dei prof con le chiavi dei due semestri
    dict_prof_s1_s2 = {}
    dict_prof_s1_s2['S1'] = dict_prof_s1
    dict_prof_s1_s2['S2'] = dict_prof_s2
    #print 'PROF: ' + str(dict_prof_s1_s2)

    # creo un dizionario di tutti i corsi, divisi per i due semestri, dei professori
    # - s1: [[corsi professore 1 in ore], [corsi professore 2 in ore], ...]
    # - s2: uguale a s1
    lista_corsi_prof_s1 = []
    lista_corsi_prof_s2 = []
    dict_P_s1_s2 = {}
    for k, v in dict_map_prof_corsi_s1.iteritems():
        lista_corsi_prof_s1.append(v)
    for k, v in dict_map_prof_corsi_s2.iteritems():
        lista_corsi_prof_s2.append(v)

    #print dict_map_prof_corsi_s1

    # raggruppo i dizionari dei corsi dei prof con le chiavi dei due semestri
    dict_P_s1_s2['S1'] = lista_corsi_prof_s1
    dict_P_s1_s2['S2'] = lista_corsi_prof_s2
    #print 'P: ' + str(dict_P_s1_s2)

    dict_map_prof_corsi_s1_s2 = {}
    dict_map_prof_corsi_s1_s2['S1'] = dict_map_prof_corsi_s1
    dict_map_prof_corsi_s1_s2['S2'] = dict_map_prof_corsi_s2
    #print dict_map_prof_corsi_s1_s2
    #print dict_map_prof_corsi_s1

    # raggruppo i dizionari del numero degli studneti dei corsi con le chiavi dei due semestri
    dict_num_stud = {}
    dict_num_stud['S1'] = lista_num_stud_s1
    dict_num_stud['S2'] = lista_num_stud_s2
    #print 'NUM_STUD: ' + str(dict_num_stud)

    ###############
    # PER LE AULE #
    ###############

    # costruisco un dizionario delle aule
    # 0: aula 0
    # 1: aula 1
    dict_id_aule = {}
    index_aule = 0

    # creo una lista delle capacita' delle aule
    lista_cap_aule = []
    index_cap_aule = 0
    for k_sede, v_sede in dict_aule.iteritems():
        for key, value in v_sede.iteritems():
            dict_id_aule[index_aule] = key          # key contiente il nome delle aule
            lista_cap_aule.append(int(value[index_cap_aule]))       # capacita' aule
            index_aule += 1
    #print 'AULE: ' + str(dict_id_aule)
    #print 'CAP_AULE: ' + str(lista_cap_aule)

    # lista degli identificativi delle aule
    R = range(index_aule)

    # creo dizionario di mapping per i giorni della settimana
    giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi']
    dict_giorni = {}
    for i in xrange(giorni.__len__()):
        dict_giorni[i] = giorni[i]
    #print dict_giorni
    D = range(giorni.__len__())
    #print D

    # creo dizionario di mapping delle fasce orarie in cui si ha lezione
    fasce_orarie = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00']
    dict_orari = {}
    for i in xrange(fasce_orarie.__len__()):
        dict_orari[i] = fasce_orarie[i]
    #print dict_orari
    H = range(fasce_orarie.__len__())
    #print H

    if (semestre_scelto == 1):
        CORSI, C, CIC, P, CLO, NUM_STUD, CL = extract_semestre_from_dict(dict_map_ore_corso_s1_s2, dict_set_C_s1_s2, dict_CIC_s1_s2, dict_P_s1_s2, dict_CLO_s1_s2, dict_num_stud, dict_CL, 'S1')
        return CORSI, C, CIC, P, CLO, NUM_STUD, CL, R, lista_cap_aule, dict_id_aule, D, H, dict_giorni, dict_orari
    # se semstre 2
    CORSI, C, CIC, P, CLO, NUM_STUD, CL = extract_semestre_from_dict(dict_map_ore_corso_s1_s2, dict_set_C_s1_s2, dict_CIC_s1_s2, dict_P_s1_s2, dict_CLO_s1_s2, dict_num_stud, dict_CL, 'S2')
    return CORSI, C, CIC, P, CLO, NUM_STUD, CL, R, lista_cap_aule, dict_id_aule, D, H, dict_giorni, dict_orari