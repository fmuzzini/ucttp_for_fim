resultsTest = []

# funzione che permette di chiamare tutti i test (controllo la bonta' della soluzione ottenuta dal modello)
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - resultsTest: lista degli esiti dei test
def check_constraints_model(out, map_corsi, NUM_STUD, map_aule, CAP_AULA):

    # ordino l'orario
    out = ordina_orario(out)

    # test 1 -> vincolo unicita' quadrupla c,d,h,r
    resultsTest.append(testUniqueQuadrupla(out))

    # test 2 -> vincolo prof di un corso in un ora, non puo' avere un altro corso nella stessa ora dello stesso giorno
    resultsTest.append(testNotUbiquityProf(out))

    # vincolo di non sovrapposizione corsi obbligatori
    resultsTest.append(testNotOverlapMandatoryCourse(out))

    # test 4 -> vincolo tutte le ore di lezione devono essere nell'orario
    resultsTest.append(testAllCoursesPresent(out, map_corsi))

    # test 5 -> vincolo capienza aula
    lista_tol = testRespectRoomCapacity(out, map_corsi, NUM_STUD, map_aule, CAP_AULA)

    # test 6 -> vincolo un solo blocco di lezioni della stessa materia in un giorno (max 3 ore)
    resultsTest.append(testSingleBlockCoursePerDay(out))

    # test 7 -> vincolo consecutivita' ore (guarda che non ci siano buchi nelle ore)
    resultsTest.append(testHourConsecutiveness(out))

    # test 8 -> vincolo blocco di singola ora
    resultsTest.append(testSingleHour(out))

    # controllo finale dei test
    print resultsTest
    if (all(resultsTest)):
        print 'Test superati con successo'
    else:
        print 'Test non superati'

# funzione che cerca i corsi di uno stesso prof
# parametri:
#   - out: orario ottenuto dal modello
#   - prof: nome del prof
# return:
#   corsi: lista dei corsi che il prof insegna
def search_courses_prof(out, prof):
    # cerco prima il prof in questione
    key_corsi = 'corsi effettivi'
    key_prof = 'prof'
    id_corsi = 0        # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    # prof = ''
    # for key, value in map_corsi.iteritems():
    #     prof = value[key_prof]
    #     new_corso = value[key_corsi][id_corsi][key_nome_corso]
    #     if (new_corso == corso):
    #         break

    # cerco altri corsi del prof
    corsi = []
    for j in xrange(out.__len__()):
        new_prof = out[j]['c'][key_prof]
        new_corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
        if (new_prof == prof):
             if (new_corso not in corsi):
                corsi.append(new_corso)

    return corsi

# test che permette di verificare che la quadrupla (corso, ora, giorno, fascia_oraria) sia unica
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testUniqueQuadrupla(out):
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'

    for j in xrange(out.__len__()):
        orario = out[j]['h']
        corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
        aula = out[j]['r']
        giorno = out[j]['d']
        for i in range(0,j)+range(j+1, out.__len__()):          #per tutte le altre ore dell'orario
            if (out[i]['h'] == orario and out[i]['c'][key_corsi][id_corsi][key_nome_corso] == corso and out[i]['r'] == aula and out[i]['d'] == giorno):
                return False
    return True

# test che permette di verificare che un prof faccia una sola lezione in una data ora di un dato giorno
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testNotUbiquityProf(out):
    corsi = []
    index_corsi = 0
    key_corsi = 'corsi effettivi'
    key_prof = 'prof'
    key_nome_corso = 'nome'
    for j in xrange(out.__len__()):
        orario = out[j]['h']
        corso = out[j]['c'][key_corsi][index_corsi][key_nome_corso]
        giorno = out[j]['d']
        if (corso not in corsi):
            corsi.append(corso)
            prof = out[j]['c'][key_prof]
            altri_corsi_prof = search_courses_prof(out, prof)
            for i in range(0,j)+range(j+1, out.__len__()):          #per tutte le altre ore dell'orario
                if (out[i]['h'] == orario and out[i]['c'][key_corsi][index_corsi][key_nome_corso] in altri_corsi_prof and out[i]['d'] == giorno):
                    return False
    return True

# funzione che cerca il tipo di un corso
# parametri:
#   - out: orario ottenuto da modello
#   - corso: nome corso corrente nel ciclo for
# return:
#   - tipo del corso (consigliato o obbligatorio)
# def search_type_course(out, corso):
#     key_corsi = 'corsi effettivi'
#     id_corsi = 0  # per evitare di guardare i corsi condivisi
#     key_nome_corso = 'nome'
#     key_tipo = 'tipo'
#     for j in xrange(out.__len__()):
#         if (out[j]['c'][key_corsi][id_corsi][key_nome_corso] == corso):
#             return out[j]['c'][key_corsi][id_corsi][key_tipo]

# test che permette di verificare la non sovrapposizione di corsi obbligatori
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testNotOverlapMandatoryCourse(out):
    corso_obb = 'obbligatorio'
    index_corsi = 0
    key_corsi = 'corsi effettivi'
    key_nome_corso = 'nome'
    key_tipo = 'tipo'
    key_anno = 'anno'
    key_cdl = 'corso_di_laurea'
    key_mag_tr = 'mag_tr'

    for j in xrange(out.__len__()):
        corso = out[j]['c'][key_corsi][index_corsi][key_nome_corso]
        # if (j == 120):
        #     break
        # print corso
        #print search_type_course(corso, map_corsi)
        #if (search_type_course(out, corso) == corso_obb):
        if (out[j]['c'][key_corsi][index_corsi][key_tipo] == corso_obb):
            # print '###########################'
            # print corso
            orario = out[j]['h']
            giorno = out[j]['d']
            anno = out[j]['c'][key_corsi][index_corsi][key_anno]
            cdl = out[j]['c'][key_corsi][index_corsi][key_cdl]
            mag_tr = out[j]['c'][key_corsi][index_corsi][key_mag_tr]
            for i in range(0,j)+range(j+1, out.__len__()):          #per tutte le altre ore dell'orario
                for k in xrange(len(out[i]['c'][key_corsi])):       #per tutta la lista dei corsi condivisi tra i cdl
                    new_corso = out[i]['c'][key_corsi][index_corsi][key_nome_corso]
                    if (out[i]['c'][key_corsi][k][key_tipo] == corso_obb and
                                out[i]['h'] == orario and out[i]['d'] == giorno and
                         out[i]['c'][key_corsi][k][key_cdl] == cdl and
                                out[i]['c'][key_corsi][k][key_mag_tr] == mag_tr and
                                out[i]['c'][key_corsi][k][key_anno] == anno):
                        # print new_corso
                        # print orario
                        # print giorno
                        # print cdl
                        # print mag_tr
                        # print anno
                        # print out[i]['d']
                        # print '###########################'
                        return False
    return True

# test che permette di verificare che tutti i corsi siano presentanti
# parametri:
#   - out: orario ottenuto da modello
#   - map_corsi: dizionario di mapping tra ore e corsi
# return:
#   - True: test ok
#   - False: test fallito
def testAllCoursesPresent(out, map_corsi):
    lista_corsi_orario_modello = []
    lista_corsi_orario_reali = []
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    for i in out:
        #print i
        lista_corsi_orario_modello.append(i['c'][key_corsi][id_corsi][key_nome_corso])
    lista_corsi_orario_modello.sort()
    for key, value in map_corsi.iteritems():
        lista_corsi_orario_reali.append(value[key_corsi][id_corsi][key_nome_corso])
    lista_corsi_orario_reali.sort()
    #print lista_corsi_orario_reali
    #print lista_corsi_orario_modello
    # for i in xrange(lista_corsi_orario_modello.__len__()):
    #     if (lista_corsi_orario_modello[i] != lista_corsi_orario_reali[i]):
    #         print i
    #         print 'caio'
    #         print lista_corsi_orario_modello[i]
    #         print lista_corsi_orario_reali[i]
    if (lista_corsi_orario_modello == lista_corsi_orario_reali):
        return True
    return False

# funzione che permette di cercare un corso e di restituirne l'id
# parametri:
#   - corso: nome aula da cercare
#   - map_corsi: dizionario di mapping tra ore e corsi
# return:
#   - key: identificativo del corso
#   - -1: in caso in cui non venga trovato
def search_ora_corso(corso, map_corsi):
    key_corsi = 'corsi effettivi'
    key_corso = 0
    key_nome_corso = 'nome'

    for key, value in map_corsi.iteritems():
        if (value[key_corsi][key_corso][key_nome_corso] == corso):
            return key
    return -1

# funzione che permette di cercare un'aula e di restituirne l'id
# parametri:
#   - aula: nome aula da cercare
#   - map_aule: dizionario di mapping tra id e aule
# return:
#   - key: identificativo dell'aula
#   - -1: in caso in cui non venga trovata
def search_cap_aula(aula, map_aule):
    for key, value in map_aule.iteritems():
        if (value == aula):
            return key
    return -1


# test che permette di verificare che la capacita' delle aule sia rispettata
# parametri:
#   - out: orario ottenuto da modello
#   - map_corsi: dizionario di mapping tra ore e corsi
#   - NUM_STUD: dizionario del numero di studenti per ogni ora
#   - map_aule: dizionario di mapping tra id e aule
#   - CAP_AULA: dizionario di capienza delle aule
# return:
#   - True: test ok
#   - False: test fallito
def testRespectRoomCapacity(out, map_corsi, NUM_STUD, map_aule, CAP_AULA):
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'

    # print NUM_STUD
    # print map_corsi[30]
    # print map_aule[17]
    lista_tol = []      # lista dei valori in cui si e' sforato la capacita' delle aule
    old_corsi = []
    for i in xrange(out.__len__()):
        corso = out[i]['c'][key_corsi][id_corsi][key_nome_corso]
        if (corso not in old_corsi):
            old_corsi.append(corso)
            aula = out[i]['r']
            # print aula
            # print corso

            # cerco l'ora del corso
            ora = search_ora_corso(corso, map_corsi)
            # cerco l'id dell'aula
            id_aula = search_cap_aula(aula, map_aule)

            # print map_corsi
            # print ora
            # print corso
            # print map_aule
            # print id_aula

            if (ora == -1 or id_aula == -1):
                print 'errore test'
                exit(0)
            # se non c'e' stato l'errore e se gli studenti eccedono la capienza
            if (NUM_STUD[ora] > CAP_AULA[id_aula]):
                lista_tol.append(NUM_STUD[ora] - CAP_AULA[id_aula])
                # print out[i]
                # print id_aula
                # print corso
                # print aula
                # print NUM_STUD[ora]
                # print CAP_AULA[id_aula]

    if (lista_tol):      # se la lista e' piena
        #print lista_tol
        return False
    return True



# test che permette di verificare che ci sia un singolo blocco di ore di un corso in uno stesso giorno
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testSingleBlockCoursePerDay(out):
    #giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi']
    giorni = range(5)
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    key_anno = 'anno'
    key_cdl = 'corso_di_laurea'
    key_tipo = 'tipo'
    key_mag_tr = 'mag_tr'

    num_max_ore_cons = 3  # al massimo una lezione dura 3 ore consecutive
    for gg in giorni:
        old_corsi = []
        for j in xrange(out.__len__()):
            giorno = out[j]['d']
            corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
            anno = corso = out[j]['c'][key_corsi][id_corsi][key_anno]
            cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
            mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]
            tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]
            # print corso
            # print giorno
            if (giorno == gg and corso not in old_corsi):  # in questo modo dovrei prendere solo la prima ora di uno stesso corso nello stesso giorno
                old_corsi.append(corso)
                count = 0
                for i in range(0, j) + range(j + 1, out.__len__()):  # per tutte le altre ore dell'orario
                    if (out[i]['c'][key_corsi][id_corsi][key_nome_corso] == corso and out[i]['d'] == giorno and out[i]['c'][key_corsi][id_corsi][key_anno] == anno
                        and out[i]['c'][key_corsi][id_corsi][key_cdl] == cdl and out[i]['c'][key_corsi][id_corsi][key_tipo] == tipo
            and out[i]['c'][key_corsi][id_corsi][key_mag_tr] == mag_tr):
                        count += 1
                        if (count > 2):
                            print corso
                            # print new_out[i]['h']
                            print giorno
                            return False
    return True

# funzione che riordina l'orario output ottenuto dal modello in modo da mettere in ordine i giorni della
# setimana e le fasce orarie
# parametri:
#   - out: orario output del modello
# return:
#   - new_out: orario ordinato per giorni e fasce orarie (si ottiene prima tutt i lunedi delle 9, poi delle 10,
#  ..., poi tutti i martedi, ...)
def ordina_orario(out):
    #fasce_orarie = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00']
    #giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi']
    fasce_orarie = range(8)
    giorni = range(5)

    new_out = []
    for gg in giorni:
        for fo in fasce_orarie:
            for i in xrange(out.__len__()):
                giorno = out[i]['d']
                orario = out[i]['h']
                if (giorno == gg and orario == fo):
                    new_out.append({"h": orario, "c": out[i]['c'], "r": out[i]['r'], "d": giorno})
    #print new_out
    return new_out

# test che permette di verificare che le ore di un corso siano consecutive
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testHourConsecutiveness(out):
    #fasce_orarie = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00']
    #giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi']
    fasce_orarie = range(8)
    giorni = range(5)
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    key_cdl = 'corso_di_laurea'
    key_anno = 'anno'
    key_tipo = 'tipo'
    key_mag_tr = 'mag_tr'

    #new_out = ordina_orario(out, fasce_orarie, giorni)
    num_max_ore_cons = 3            # al massimo una lezione dura 3 ore consecutive
    for gg in giorni:
        old_corsi = []
        for j in xrange(out.__len__()): ###new_out
            giorno = out[j]['d']    ###new_out
            corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]    ###new_out
            #print corso
            #print giorno
            if (giorno == gg and corso not in old_corsi):           # in questo modo dovrei prendere solo la prima ora di uno stesso corso nello stesso giorno
                old_corsi.append(corso)
                aula = out[j]['r']  ###new_out
                orario = out[j]['h']    ###new_out
                index_orari = fasce_orarie.index(orario)            # cerco l'indice dell'ora di inizio di quel blocco di ore
                #print orario
                cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
                anno = out[j]['c'][key_corsi][id_corsi][key_anno]
                mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]
                tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]

                orari_possibili_per_corso = []
                #if (index_orari == 3):          # se fine mattinata (NOTA: il fine pomeriggio e' gia' gestito sotto)
                #    pass    #orari_possibili_per_corso.append(orario)
                if (index_orari <= 3 and index_orari+num_max_ore_cons > 3):
                    orari_possibili_per_corso = fasce_orarie[index_orari+1:num_max_ore_cons+1]      # estraggo le sole fasce orarie disponibili per quella lezione
                else:
                    orari_possibili_per_corso = fasce_orarie[index_orari + 1:index_orari + num_max_ore_cons]  # estraggo le sole fasce orarie disponibili per quella lezione
                #print orari_possibili_per_corso

                for i in range(0,j)+range(j+1, out.__len__()):          #per tutte le altre ore dell'orario     ###new_out
                    if (out[i]['h'] not in orari_possibili_per_corso and out[i]['c'][key_corsi][id_corsi][key_nome_corso]
                        == corso and out[i]['r'] == aula and out[i]['d'] == giorno and
                                out[j]['c'][key_corsi][id_corsi][key_cdl] == cdl and
                                out[j]['c'][key_corsi][id_corsi][key_anno] == anno and out[j]['c'][key_corsi][id_corsi][key_tipo] == tipo
            and out[j]['c'][key_corsi][id_corsi][key_mag_tr] == mag_tr):    ###new_out
                        # print corso
                        # print out[i]['h']  ###new_out
                        # print giorno
                        return False
    return True

# funzione che permette di trovare un corso con le stesse caratteristiche di quello corrente, ma
# nela fascia oraria indicata
# parametri:
#   - out: orario ottenuto dal modello
#   - j: corso corrente che bisogna escludere dalla ricerca
#   - orari_possibili_per_corso: fascia orario del corso da cercare
#   - corso: nome del corso attuale
#   - anno: anno del corso attuale
#   - giorno: giorno di lezione del corso attuale
#   - cdl: corso di laurea del corso attuale
#   - tipo: tipo del corso attuale (obbligatorio / consigliato)
#   - mag_tr: durata del piano di studi (LM / L2)
# return:
#   - True: trovato il corso con tali caratterisitche
#   - False: corso non trovato
def search_course_before_or_after(out, j, orari_possibili_per_corso, corso, anno, giorno, cdl, tipo, mag_tr):
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    key_anno = 'anno'
    key_cdl = 'corso_di_laurea'
    key_tipo = 'tipo'
    key_mag_tr = 'mag_tr'

    for i in range(0, j) + range(j + 1, out.__len__()):  # per tutte le altre ore dell'orario
        if (out[i]['h'] == orari_possibili_per_corso and out[i]['c'][key_corsi][id_corsi][key_nome_corso] == corso
                and out[i]['d'] == giorno and out[i]['c'][key_corsi][id_corsi][key_anno] == anno
            and out[i]['c'][key_corsi][id_corsi][key_cdl] == cdl and out[i]['c'][key_corsi][id_corsi][key_tipo] == tipo
            and out[i]['c'][key_corsi][id_corsi][key_mag_tr] == mag_tr):
                # print out[i]['c'][key_corsi][id_corsi][key_nome_corso]
                # print anno
                # print  giorno
                # print out[i]['h']
                # print out[i]['c'][key_corsi][id_corsi][key_cdl]
                # print tipo

                return True
    return False

# test che permette di verificare che non esista blocchi di singole ore
# parametri:
#   - out: orario ottenuto da modello
# return:
#   - True: test ok
#   - False: test fallito
def testSingleHour(out):
    #fasce_orarie = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00']
    #giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi']
    fasce_orarie = range(8)
    giorni = range(5)
    key_corsi = 'corsi effettivi'
    id_corsi = 0  # per evitare di guardare i corsi condivisi
    key_nome_corso = 'nome'
    key_anno = 'anno'
    key_cdl = 'corso_di_laurea'
    key_tipo = 'tipo'
    key_mag_tr = 'mag_tr'

    #for gg in giorni:
    for j in xrange(out.__len__()):
        giorno = out[j]['d']
        tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]
        if (tipo == 'obbligatorio'):
            orario = out[j]['h']
            index_orari = fasce_orarie.index(orario)  # cerco l'indice dell'ora di inizio di quel blocco di ore

            orari_possibili_per_corso = []
            # estraggo le sole fasce orarie disponibili per quella lezione (distinguendo i casi critici)
            if (index_orari == 0 or index_orari == 4):          # inizio mattina e inizio pomeriggio
                orari_possibili_per_corso.append(fasce_orarie[index_orari + 1])
            elif (index_orari == 3 or index_orari == (fasce_orarie.__len__())-1):           # fine mattina e fine pomeriggio
                orari_possibili_per_corso.append(fasce_orarie[index_orari - 1])
            else:                           # il resto
                orari_possibili_per_corso.append(fasce_orarie[index_orari - 1])
                orari_possibili_per_corso.append(fasce_orarie[index_orari + 1])

            # print index_orari
            corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
            anno = out[j]['c'][key_corsi][id_corsi][key_anno]
            cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
            mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]


            present_course_before_or_after = []
            for i in orari_possibili_per_corso:     # per ogni fascia oraria cerco se esiste un corso con caratteristiche
                                                    # simili a quelle correnti
                present_course_before_or_after.append(search_course_before_or_after(out, j, i, corso, anno, giorno, cdl, tipo, mag_tr))

            if (True not in present_course_before_or_after):           # se non sono stati trovati sia il corso precedente che il successivo

                # print '#########################################'
                # print corso
                # print giorno
                # print orari_possibili_per_corso
                # print anno
                # print orario
                # print cdl
                # print tipo
                # print '#########################################'
                return False
    return True