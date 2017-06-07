/**
 * Created by Davide Paganelli on 23/05/2017.
 */


/* funzione che permette di chiamare tutti i test (controllo la bonta' della soluzione ottenuta dal modello)
 * parametri:
 *   - out: orario ottenuto da modello
 *   - obj_pref_prof: indisponibilita' prof
 *   - meta: metadati dei giorni e delle fasce orarie di lezione
 *   - dict_aule: dizionario delle aule a disposizione
 *   - obj_pref_attr_corso: oggetto che indica le preferenze di attrezzature e di sedi dei corsi
 *   - map_corsi: oggetto che memorizza i corsi a disposizione
 *   - NUM_STUD: numero di studenti iscritti ai corsi disponibili
 *   - map_aule: oggetto che memorizza le aule con il rispettivo id
 *   - CAP_AULA: capienza delle aule a disposizione
 *   - ora_dopo_pranzo: indice dell'ora di lezione appena dopo pranzo
 * return:
 *   - response: risposta html dei test fatti
 */
function check_constraints_model(out, obj_pref_prof, meta, dict_aule, obj_pref_attr_corso, map_corsi, NUM_STUD, map_aule, CAP_AULA, ora_dopo_pranzo, obj_map_corso_blocchi_ore) {
    
    //console.log(meta)

    var resultsTest_hard = new Array()
    var string_test_hard = new Array()
    var resultsTest_soft = new Array()
    var string_test_soft = new Array()
    var ris_test = {}
    var key_ris_test_risultato = 'risultato'
    var key_ris_test_msg = 'messaggio'
    var orari = meta['ore']
    var days = meta['giorni']

    // ordino l'orario
    out = ordina_orario(out, orari, days)

    // test 1 -> vincolo unicita' quadrupla c,d,h,r
    ris_test = testUniqueQuadrupla(out, orari, days)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // test 2 -> vincolo prof di un corso in un ora, non puo' avere un altro corso nella stessa ora dello stesso giorno
    ris_test = testNotUbiquityProf(out, orari, days)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // vincolo di non sovrapposizione corsi obbligatori
    ris_test = testNotOverlapMandatoryCourse(out, orari, days)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // test 4 -> vincolo tutte le ore di lezione devono essere nell'orario
    ris_test = testAllCoursesPresent(out, map_corsi)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // test 5 -> vincolo capienza aula
    /*var lista_tol = */ris_test = testRespectRoomCapacity(out, map_corsi, NUM_STUD, map_aule, CAP_AULA)
    resultsTest_soft.push(ris_test[key_ris_test_risultato])
    string_test_soft.push(ris_test[key_ris_test_msg])

    // test 6 -> vincolo un solo blocco di lezioni della stessa materia in un giorno (max 3 ore)
    ris_test = testSingleBlockCoursePerDay(out, orari, days, obj_pref_attr_corso, obj_map_corso_blocchi_ore)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // test 7 -> vincolo consecutivita' ore (guarda che non ci siano buchi nelle ore)
    /*ris_test = testHourConsecutiveness(out, orari, days)
    resultsTest.push(ris_test[key_ris_test_risultato])
    string_test.push(ris_test[key_ris_test_msg])*/

    // test 8 -> vincolo blocco di singola ora
    ris_test = testSingleHour(out, orari, days)
    resultsTest_hard.push(ris_test[key_ris_test_risultato])
    string_test_hard.push(ris_test[key_ris_test_msg])

    // test 9 -> controllo corretta gestione preferenze dei prof
    //var obj_pref_prof = {'Mauro Leoncini': [{0:[0,1]},{5:[6,7]}], 'Marina Cocchi': [{5:[1,2]}]}
    ris_test = testPrefProf(out, obj_pref_prof, orari, days)
    resultsTest_soft.push(ris_test[key_ris_test_risultato])
    string_test_soft.push(ris_test[key_ris_test_msg])

    // test 10 -> controllo corretta gestione preferenze delle attrezzature dei corsi
    ris_test = testAttrezCourse(out, dict_aule, obj_pref_attr_corso)
    resultsTest_soft.push(ris_test[key_ris_test_risultato])
    string_test_soft.push(ris_test[key_ris_test_msg])

    // test 11 -> controllo corretta gestione preferenze delle sedi dei corsi
    ris_test = testEdiCourse(out, dict_aule, obj_pref_attr_corso)
    resultsTest_soft.push(ris_test[key_ris_test_risultato])
    string_test_soft.push(ris_test[key_ris_test_msg])

    // controllo finale dei test
    /*console.log(resultsTest_hard)
    console.log(string_test_hard)
    console.log(resultsTest_soft)
    console.log(string_test_soft)*/

    // lambda expression che restituisce vero se tutti i test sono passati
    check_test = function (results) {
		for(var r = 0; r < results.length; r++){
            if (results[r] !== true) {
                return false
			}
        }
        return true
    }
	
	
	//var string_test = ["mancata unicita' (corso, giorno, ora, aula) ", "sovrapposizione ore stesso prof stessa ora", "sovrapposizione corsi obbligatori", "unico blocco ore corso in un giorno", "troppe ore corso", "singola ora corso", "indisponibilita' prof nelle ore indicate"]
	var response = '<b> Vincoli rispettati! </b>'
	
	// funzione che crea la risposta in caso di violazione dei vincoli
	return_response = function(results_hard, results_soft, response, string_test_hard, string_test_soft) {

        // funzione che dice se tutti gli elementi di una lista sono veri
        var isTrue = function(element) {
            return element === true
        }

		//response = '<b> Vincoli violati: </b>'

        //response = '<div id="dialog-vincoli">'
        response = '<div id="accordion-vincoli">'
        /*response += '<div id="tabs-vincoli"> ' +
                        '<ul> ' +
                            '<li><a href="#tab-hard">hard</a></li>' +
                            '<li><a href="#tab-soft">soft</a></li>' +
                        '<ul>'*/

        // se ci sono dei vincoli violati per quelli hard
        if (! results_hard.every(isTrue)) {
            //response += '<li> <b> hard: </b> </li> <ul>'

            response += '<h3>hard</h3> <div class="div-vincoli"><ul>';
            //response += '<div id="tab-hard"> '
            for (var r = 0; r < results_hard.length; r++) {
                if (results_hard[r] !== true) {
                    var tmp_string = '<li>';
                    tmp_string += string_test_hard[r];
                    tmp_string += '</li>';

                    response += tmp_string
                }

            }
            response += '</ul></div>'
        }

        // se ci sono dei vincoli violati per quelli soft
        if (! results_soft.every(isTrue)) {
            //response += '<li> <b> soft: </b> </li> <ul>'

            response += '<h3>soft</h3> <div class="div-vincoli"><ul>';
            //response += '<div id="tab-soft">'
            for (var r = 0; r < results_soft.length; r++) {
                if (results_soft[r] !== true) {
                    var tmp_string = '<li>';
                    tmp_string += string_test_soft[r];
                    tmp_string += '</li>';

                    response += tmp_string
                }

            }
            response += '</ul></div>'
        }
        response += '</div>'
        //response += '</ul>'
        //console.log(response)
        return response
	}

    var resultsTest = resultsTest_hard.concat(resultsTest_soft)
    if (! check_test(resultsTest)) {
        //console.log('Test non superati')
		response = return_response(resultsTest_hard, resultsTest_soft, response, string_test_hard, string_test_soft)
    }	
	return response
}

/* funzione che riordina l'orario output ottenuto dal modello in modo da mettere in ordine i giorni della
 * setimana e le fasce orarie
 * parametri:
 *   - out: orario output del modello
 *   - orari: fasce orarie in cui sia ha lezione
 *   - days: giorni in cui si ha lezione
 * return:
 *   - new_out: orario ordinato per giorni e fasce orarie (si ottiene prima tutt i lunedi delle 9, poi delle 10,
 *  ..., poi tutti i martedi, ...)
 */
function ordina_orario(out, orari, days) {

    var fasce_orarie = []
    for (var or = 0; or < orari.length; or++) {
        fasce_orarie.push(or)
    }
    var giorni = []
    for (var day = 0; day < days.length; day++) {
        giorni.push(day)
    }

    var new_out = []
    for(var gg in giorni){
        for (var fo in fasce_orarie) {
            for (var i = 0; i < out.length; i++) {
                var giorno = out[i]['d']
                var orario = out[i]['h']
                if (giorno === giorni[gg] && orario === fasce_orarie[fo])
                    new_out.push({"h": orario, "c": out[i]['c'], "r": out[i]['r'], "d": giorno})
            }
        }
    }

    //console.log(new_out)
    return new_out
}

/* funzione che ottiene tutte le ore dell'orario eccetto index
 * parametri:
 *      - ore: orario ottenuto dal modello
 *      - index: indice in cui escludere la ricerca
 * return:
 *      - list_hour: array delle ore escluso index
 */
function create_list_other_hour(ore, index) {
            var list_hour = []
            for(var i = 0; i < ore.length; i++){
                if (i != index)
                    list_hour.push(i)
            }
            return list_hour
        }

/*
 * funzione che costruisce l'oggetto che restituisce i risultati di ogni test
 * argomenti:
 *      - bool: esito test
 *      - msg: messaggio del test
 * return:
 *      - oggetto che unifica i 2 risultati dei test
 */
function create_test_response(bool, msg){
    return {'risultato': bool, 'messaggio': msg}
}

/* test che permette di verificare che la quadrupla (corso, ora, giorno, fascia_oraria) sia unica
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie in cui fare lezione
 *   - days: giorni in cui si ha lezione
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testUniqueQuadrupla(out, orari, days) {
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0  // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var ris = {}
    var stringa = ''

    for (var j = 0; j < out.length; j++){
        var orario = out[j]['h']
        var corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
        var aula = out[j]['r']
        var giorno = out[j]['d']

        var list_other_hour = create_list_other_hour(out, j)

        for (var i in list_other_hour) {          //per tutte le altre ore dell'orario
            var index_hour = list_other_hour[i]
            if (out[index_hour]['h'] === orario && out[index_hour]['c'][key_corsi][id_corsi][key_nome_corso] === corso && out[index_hour]['r'] === aula && out[index_hour]['d'] === giorno) {
                stringa = "mancata unicita' (corso, giorno, ora, aula) per (" + corso + "," + days[giorno] + "," + orari[orario] + "," + aula + ")"
                ris = create_test_response(false, stringa)
                return ris
            }
        }
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* funzione che cerca i corsi di uno stesso prof
 * parametri:
 *   - out: orario ottenuto dal modello
 *   - prof: nome del prof
 * return:
 *   - corsi: lista dei corsi che il prof insegna
 */
function search_courses_prof(out, prof) {
    var key_corsi = 'corsi effettivi'
    var key_prof = 'prof'
    var id_corsi = 0        // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'

    // cerco altri corsi del prof
    var corsi = []
    for (var j = 0; j < out.length; j++) {
        var new_prof = out[j]['c'][key_prof]
        var new_corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
        if (new_prof === prof)
            if (!corsi.includes(new_corso))
                corsi.push(new_corso)
    }
    return corsi
}

/* test che permette di verificare che un prof faccia una sola lezione in una data ora di un dato giorno
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie per fare lezione
 *   - days: giorni in cui si ha lezione
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testNotUbiquityProf(out, orari, days) {
    var stringa = ''
    var corsi = []
    var index_corsi = 0
    var key_corsi = 'corsi effettivi'
    var key_prof = 'prof'
    var key_nome_corso = 'nome'
    var ris = {}

    for (var j = 0; j < out.length; j++) {
        var orario = out[j]['h']
        var corso = out[j]['c'][key_corsi][index_corsi][key_nome_corso]
        var giorno = out[j]['d']
        //if (! corsi.includes(corso)) {
         //   corsi.push(corso)

            var prof = out[j]['c'][key_prof]
            var altri_corsi_prof = search_courses_prof(out, prof)
            var list_other_hour = create_list_other_hour(out, j)

            for (var i in list_other_hour) {          //per tutte le altre ore dell'orario
                var index_hour = list_other_hour[i]
                if (out[index_hour]['h'] === orario && altri_corsi_prof.includes(out[index_hour]['c'][key_corsi][index_corsi][key_nome_corso])  && out[index_hour]['d'] === giorno) {
                    /*console.log('###############################')
                    console.log(corso)
                    console.log(prof)
                    console.log(altri_corsi_prof)
                    console.log(orario)
                    console.log(giorno)
                    console.log(out[i]['c'][key_corsi][index_corsi][key_nome_corso])
                    console.log('###############################')*/
                    stringa = "sovrapposizione corsi (di cui uno e' " + corso + ")" + " dello stesso prof " + prof + " nel giorno " + days[giorno] + " all'ora " + orari[orario]
                    ris = create_test_response(false, stringa)
                    return ris
                }
            }
        //}
    }
    ris = create_test_response(true, stringa)
    return ris

}

/* test che permette di verificare la non sovrapposizione di corsi obbligatori
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie per fare lezione
 *   - days: giorni in cui si ha lezione
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testNotOverlapMandatoryCourse(out, orari, days) {
    var corso_obb = 'obbligatorio'
    var index_corsi = 0
    var key_corsi = 'corsi effettivi'
    var key_nome_corso = 'nome'
    var key_tipo = 'tipo'
    var key_anno = 'anno'
    var key_cdl = 'corso_di_laurea'
    var key_mag_tr = 'mag_tr'
    var stringa = ''
    var ris = {}

    for (var j = 0; j < out.length; j++) {
        var corso = out[j]['c'][key_corsi][index_corsi][key_nome_corso]

        if (out[j]['c'][key_corsi][index_corsi][key_tipo] === corso_obb) {
            // console.log('###########################')
            // console.log(corso)
            var orario = out[j]['h']
            var giorno = out[j]['d']
            var anno = out[j]['c'][key_corsi][index_corsi][key_anno]
            var cdl = out[j]['c'][key_corsi][index_corsi][key_cdl]
            var mag_tr = out[j]['c'][key_corsi][index_corsi][key_mag_tr]
            var list_other_hour = create_list_other_hour(out, j)
            for (var i in list_other_hour) {          // per tutte le altre ore dell'orario
                var index_hour = list_other_hour[i]
                for (var k = 0; k < out[index_hour]['c'][key_corsi].length; k++) {       // per tutta la lista dei corsi condivisi tra i cdl
                    var new_corso = out[index_hour]['c'][key_corsi][index_corsi][key_nome_corso]
                    if (out[index_hour]['c'][key_corsi][k][key_tipo] === corso_obb &&
                        out[index_hour]['h'] === orario && out[index_hour]['d'] === giorno &&
                        out[index_hour]['c'][key_corsi][k][key_cdl] === cdl &&
                        out[index_hour]['c'][key_corsi][k][key_mag_tr] === mag_tr &&
                        out[index_hour]['c'][key_corsi][k][key_anno] === anno) {
                        // console.log(new_corso)
                        // console.log(orario)
                        // console.log(giorno)
                        // console.log(cdl)
                        // console.log(mag_tr)
                        // console.log(anno)
                        // console.log(out[i]['d'])
                        // console.log('###########################')
                        stringa = "sovrapposizione corsi obbligatori: " + corso + " (cdl " + cdl + ", anno " + anno + "," + mag_tr + ") e " + new_corso + " (cdl " + out[index_hour]['c'][key_corsi][k][key_cdl] + ", anno " + out[index_hour]['c'][key_corsi][k][key_anno] + "," + out[index_hour]['c'][key_corsi][k][key_mag_tr] + "), nel giorno " + days[giorno] + " all'ora " + orari[orario]
                        ris = create_test_response(false, stringa)
                        return ris
                    }
                }
            }
        }
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* test che permette di verificare che tutti i corsi siano presentanti
 * parametri:
 *   - out: orario ottenuto da modello
 *   - map_corsi: dizionario di mapping tra ore e corsi
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testAllCoursesPresent(out, map_corsi) {
    var lista_corsi_orario_modello = []
    var lista_corsi_orario_reali = []
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0                // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var stringa = ''
    var ris = {}

    for (var i in out) {
        var out_i = out[i]
        // console.log(i)
        lista_corsi_orario_modello.push(out_i['c'][key_corsi][id_corsi][key_nome_corso])
    }
    lista_corsi_orario_modello.sort()
    for (var key in map_corsi) {                        //////////////////////////////////
        lista_corsi_orario_reali.push(map_corsi[key][key_corsi][id_corsi][key_nome_corso])
    }
    lista_corsi_orario_reali.sort()
    //console.log(lista_corsi_orario_reali)
    //console.log(lista_corsi_orario_modello)
    for (var i = 0; i < lista_corsi_orario_modello.length; i++) {
         if (lista_corsi_orario_modello[i] !== lista_corsi_orario_reali[i]) {
             //console.log(i)
             //console.log(lista_corsi_orario_modello[i])
             //console.log(lista_corsi_orario_reali[i])
         }
    }
    for (var k = 0; k < lista_corsi_orario_modello.length; k++) {
        if (lista_corsi_orario_modello[k] === lista_corsi_orario_reali[k]) {
            ris = create_test_response(true, stringa)
            return ris
        }
    }
    stringa = "Il modello non ha considerato tutte le ore per ogni corso"
    ris = create_test_response(false, stringa)
    return ris
}

/* funzione che permette di cercare un corso e di restituirne l'id
 * parametri:
 *   - corso: nome aula da cercare
 *   - map_corsi: dizionario di mapping tra ore e corsi
 * return:
 *   - key: identificativo del corso
 *   - -1: in caso in cui non venga trovato
 */
function search_ora_corso(corso, map_corsi) {
    var key_corsi = 'corsi effettivi'
    var key_corso = 0
    var key_nome_corso = 'nome'

    for (var key in map_corsi) {                ///////////////////////////////////
        if (map_corsi[key][key_corsi][key_corso][key_nome_corso] === corso) {
            return key
        }
    }
    return -1
}

/* funzione che permette di cercare un'aula e di restituirne l'id
 * parametri:
 *   - aula: nome aula da cercare
 *   - map_aule: dizionario di mapping tra id e aule
 * return:
 *   - key: identificativo dell'aula
 *   - -1: in caso in cui non venga trovata
 */
function search_cap_aula(aula, map_aule) {
    for (var key in map_aule) {
        if (map_aule[key] == aula) {
            return key
        }
    }
    return -1
}

/* test che permette di verificare che la capacita' delle aule sia rispettata
 * parametri:
 *   - out: orario ottenuto da modello
 *   - map_corsi: dizionario di mapping tra ore e corsi
 *   - NUM_STUD: dizionario del numero di studenti per ogni ora
 *   - map_aule: dizionario di mapping tra id e aule
 *   - CAP_AULA: dizionario di capienza delle aule
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testRespectRoomCapacity(out, map_corsi, NUM_STUD, map_aule, CAP_AULA) {
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0                    // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var stringa = ''
    var ris = {}

    var lista_tol = []      // lista dei valori in cui si e' sforato la capacita' delle aule
    var old_corsi = []
    var lista_aule_err = []
    var lista_corsi_err = []
    for (var i = 0; i < out.length; i++) {
        var corso = out[i]['c'][key_corsi][id_corsi][key_nome_corso]
        if (!old_corsi.includes(corso)) {
            old_corsi.push(corso)
            var aula = out[i]['r']
            // console.log(aula)
            // console.log(corso)

            // cerco l'ora del corso
            var ora = search_ora_corso(corso, map_corsi)
            // cerco l'id dell'aula
            var id_aula = search_cap_aula(aula, map_aule)

            // console.log(map_corsi)
            // console.log(ora)
            // console.log(corso)
            // console.log(map_aule)
            // console.log(id_aula)

            if (ora === -1 || id_aula === -1) {
                console.log('errore test')
                return
            }
            // se non c'e' stato l'errore e se gli studenti eccedono la capienza
            if (NUM_STUD[ora] > CAP_AULA[id_aula]) {
                lista_tol.push(NUM_STUD[ora] - CAP_AULA[id_aula])
                lista_aule_err.push(aula)
                lista_corsi_err.push(corso)
                // console.log(out[i])
                // console.log(id_aula)
                // console.log(corso)
                // console.log(aula)
                // console.log(NUM_STUD[ora])
                // console.log(CAP_AULA[id_aula])
            }
        }
    }

    if (lista_tol) {      // se la lista e' piena
        // console.log(lista_tol)
        stringa = "Le seguenti aule non hanno una capienza sufficiente per i rispettivi corsi: (" + lista_aule_err + ") -> (" + lista_corsi_err + "), con eccesso della rispettiva quantita' di studenti: (" + lista_tol + ")"
        ris = create_test_response(false, stringa)
        return ris
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* funzione che restituisce il massimo delle ore di un corso di cui sono state indicate delle preferenze, altrimenti il suo blocco di ore di default)
 * argomenti:
 *      - obj_pref_attr_corso: oggetto delle preferenze relative ad alcuni corsi
 *      - key_corso: chiave del corso di cui cercare le ore massime
 *      - obj_map_corso_blocchi_ore: oggetto che memorizza il mapping tra codice corso e ore di default dei propri blocchi di lezione
 * return:
 *      - default_ore: per problemi o se non sono state specificate preferenze per quel corso
 *      - num_max_ore: ore massime preferenziali per quel corso
 */
function search_max_ore_corso(obj_pref_attr_corso, key_corso, obj_map_corso_blocchi_ore) {
    var num_max_ore = 0
    var key_ore = 'ore'
    var default_ore = 1

    // controllo che ci siano delle preferenze per tale corso
    if (obj_pref_attr_corso.hasOwnProperty(key_corso)) {
        // cerco le ore massime
        for (var pref = 0; pref < obj_pref_attr_corso[key_corso].length; pref++) {
            var ore_pref = obj_pref_attr_corso[key_corso][pref][key_ore]
            if (ore_pref > num_max_ore) {
                num_max_ore = ore_pref
            }
        }
    }
    else {      // non sono presenti preferenze per il corso, restituisco blocchi di default
        if (obj_map_corso_blocchi_ore.hasOwnProperty(key_corso)) {          // se e' presente tale corso nell'oggetto
            return obj_map_corso_blocchi_ore[key_corso] - 1
        }
        return default_ore
    }

    if (num_max_ore === 0) {            // per eventuali problemi
        return default_ore
    }

    return num_max_ore - 1
}

/* test che permette di verificare che ci sia un singolo blocco di ore di un corso in uno stesso giorno
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie per fare lezione
 *   - days: giorni in cui si ha lezione
 *   - obj_pref_attr_corso: oggetto che raccoglie le preferenze dei corsi
 *   - obj_pref_attr_corso: oggetto che raccoglie le preferenze dei corsi
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testSingleBlockCoursePerDay(out, orari, days, obj_pref_attr_corso, obj_map_corso_blocchi_ore) {
    var giorni = []
    for (var day = 0; day < days.length; day++) {
        giorni.push(day)
    }
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0        // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_anno = 'anno'
    var key_cdl = 'corso_di_laurea'
    var key_tipo = 'tipo'
    var key_mag_tr = 'mag_tr'
    var key_chiave = 'chiave'
    var stringa = ''
    var ris = {}

    for (var gg in giorni) {
        var old_corsi = []
        for (var j = 0; j < out.length; j++) {
            var giorno = out[j]['d']
            var corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
            var anno = out[j]['c'][key_corsi][id_corsi][key_anno]
            var cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
            var mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]
            var tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]
            // console.log(corso)
            //////////////console.log(giorno)
            if (giorno === giorni[gg] && !old_corsi.includes(corso)) {  // in questo modo dovrei prendere solo la prima ora di uno stesso corso nello stesso giorno
                old_corsi.push(corso)
                var count = 0
                var list_other_hour = create_list_other_hour(out, j)
                for (var i in list_other_hour) {                // per tutte le altre ore dell'orario
                    var index_hour = list_other_hour[i]
                    var key_corso = out[index_hour]['c'][key_corsi][id_corsi][key_chiave]
                    if (out[index_hour]['c'][key_corsi][id_corsi][key_nome_corso] === corso && out[index_hour]['d'] === giorno && out[index_hour]['c'][key_corsi][id_corsi][key_anno] === anno
                        && out[index_hour]['c'][key_corsi][id_corsi][key_cdl] === cdl && out[index_hour]['c'][key_corsi][id_corsi][key_tipo] === tipo
                        && out[index_hour]['c'][key_corsi][id_corsi][key_mag_tr] === mag_tr) {
                        count += 1
                        var max_ore_corso = search_max_ore_corso(obj_pref_attr_corso, key_corso, obj_map_corso_blocchi_ore)
                        /*if (corso === 'Programmazione 1 - GR 2') {
                            console.log(max_ore_corso)
                            console.log(count)
                        }*/
                        if (count > max_ore_corso) {
                            //////////console.log(corso)
                            // console.log(new_out[i]['h'])
                            //////////console.log(giorno)
                            stringa = "Molteplici blocchi di ore dello stesso corso " + corso + " (cdl " + cdl + ", anno " + anno + "," + mag_tr + ") all'ora " + orari[out[index_hour]['h']] + " nello stesso giorno " + days[giorno]
                            ris = create_test_response(false, stringa)
                            return ris
                        }
                    }
                }
            }
        }
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* test che permette di verificare che le ore di un corso siano consecutive
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie in cui sia ha lezione
 *   - days: giorni in cui si ha lezione
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testHourConsecutiveness(out, orari, days) {
    var fasce_orarie = []
    for (var or = 0; or < orari.length; or++) {
        fasce_orarie.push(or)
    }
    var giorni = []
    for (var day = 0; day < days.length; day++) {
        giorni.push(day)
    }
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0            // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_cdl = 'corso_di_laurea'
    var key_anno = 'anno'
    var key_tipo = 'tipo'
    var key_mag_tr = 'mag_tr'
    var stringa = ''
    var ris = {}

    var num_max_ore_cons = 3            // al massimo una lezione dura 3 ore consecutive
    var ora_prima_pranzo = fasce_orarie[(fasce_orarie.length/2)-1]      // l'ora prima del pranzo e' la fascia oraria centrale
    for (var gg in giorni) {
        var old_corsi = []
        for (var j = 0; j < out.length; j++) {
            var giorno = out[j]['d']
            var corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
            // console.log(corso)
            // console.log(giorno)
            if (giorno === giorni[gg] && !old_corsi.includes(corso)) {           // in questo modo dovrei prendere solo la prima ora di uno stesso corso nello stesso giorno
                old_corsi.push(corso)
                var aula = out[j]['r']
                var orario = out[j]['h']
                //console.log(fasce_orarie)
                //console.log(orario)
                fun = function (orario){
                    return function(element) {
                        return element === orario;
                    }
                };
                var index_orari = fasce_orarie.findIndex(fun(orario))          // cerco l'indice dell'ora di inizio di quel blocco di ore
                //console.log(index_orari)
                var cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
                var anno = out[j]['c'][key_corsi][id_corsi][key_anno]
                var mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]
                var tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]

                var orari_possibili_per_corso = []
                /*console.log('########################')
                console.log(index_orari)
                console.log(fasce_orarie)
                console.log(num_max_ore_cons)*/
                if (index_orari <= ora_prima_pranzo && index_orari + num_max_ore_cons > ora_prima_pranzo) {
                    orari_possibili_per_corso = fasce_orarie.slice(index_orari+1, ora_prima_pranzo+1)      // estraggo le sole fasce orarie disponibili per quella lezione ///////////////////////////////
                }
                else {
                    orari_possibili_per_corso = fasce_orarie.slice(index_orari + 1, index_orari + num_max_ore_cons)  // estraggo le sole fasce orarie disponibili per quella lezione ///////////////////////////////
                }
                //console.log(orari_possibili_per_corso)

                var list_other_hour = create_list_other_hour(out, j)
                for (var i in list_other_hour) {          //per tutte le altre ore dell'orario
                    var index_hour = list_other_hour[i]
                    if (!orari_possibili_per_corso.includes(out[index_hour]['h']) && out[index_hour]['c'][key_corsi][id_corsi][key_nome_corso]
                        === corso && out[index_hour]['r'] === aula && out[index_hour]['d'] === giorno &&
                        out[index_hour]['c'][key_corsi][id_corsi][key_cdl] === cdl &&
                        out[index_hour]['c'][key_corsi][id_corsi][key_anno] === anno && out[index_hour]['c'][key_corsi][id_corsi][key_tipo] === tipo
                        && out[index_hour]['c'][key_corsi][id_corsi][key_mag_tr] === mag_tr) {
                        /*console.log(orari_possibili_per_corso)
                        console.log(corso)
                        console.log(out[index_hour]['h'])
                        console.log(giorno)
                        console.log(cdl)
                        console.log(anno)
                        console.log(tipo)
                        console.log(mag_tr)
                        console.log('########################')*/
                        stringa = "mancata consecutivita' ore del corso " + corso + " (cdl " + cdl + ", anno " + anno + "," + mag_tr + ") del giorno " + days[giorno]
                        ris = create_test_response(false, stringa)
                        return ris
                    }
                }
            }
        }
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* funzione che permette di trovare un corso con le stesse caratteristiche di quello corrente, ma
 * nela fascia oraria indicata
 * parametri:
 *   - out: orario ottenuto dal modello
 *   - j: corso corrente che bisogna escludere dalla ricerca
 *   - orari_possibili_per_corso: fascia orario del corso da cercare
 *   - corso: nome del corso attuale
 *   - anno: anno del corso attuale
 *   - giorno: giorno di lezione del corso attuale
 *   - cdl: corso di laurea del corso attuale
 *   - tipo: tipo del corso attuale (obbligatorio / consigliato)
 *   - mag_tr: durata del piano di studi (LM / L2)
 * return:
 *   - True: trovato il corso con tali caratterisitche
 *   - False: corso non trovato
 */
function search_course_before_or_after(out, j, orari_possibili_per_corso, corso, anno, giorno, cdl, tipo, mag_tr) {
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0            // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_anno = 'anno'
    var key_cdl = 'corso_di_laurea'
    var key_tipo = 'tipo'
    var key_mag_tr = 'mag_tr'

    var list_other_hour = create_list_other_hour(out, j)
    for (var i in list_other_hour) {      // per tutte le altre ore dell'orario
        var index_hour = list_other_hour[i]
        if (out[index_hour]['h'] === orari_possibili_per_corso && out[index_hour]['c'][key_corsi][id_corsi][key_nome_corso] === corso
            && out[index_hour]['d'] === giorno && out[index_hour]['c'][key_corsi][id_corsi][key_anno] === anno
            && out[index_hour]['c'][key_corsi][id_corsi][key_cdl] === cdl && out[index_hour]['c'][key_corsi][id_corsi][key_tipo] === tipo
            && out[index_hour]['c'][key_corsi][id_corsi][key_mag_tr] === mag_tr) {
            // console.log(out[i]['c'][key_corsi][id_corsi][key_nome_corso])
            // console.log(anno)
            // console.log(giorno)
            // console.log(out[i]['h'])
            // console.log(out[i]['c'][key_corsi][id_corsi][key_cdl])
            // console.log(tipo)

            return true
        }
    }
    return false
}

/* test che permette di verificare che non esista blocchi di singole ore
 * parametri:
 *   - out: orario ottenuto da modello
 *   - orari: fasce orarie in cui sia ha lezione
 *   - days: giorni in cui si ha lezione
 *   - ora_dopo_pranzo: indice dell'ora di lezione che inizia appenda dopo pranzo
 * return:
 *   - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testSingleHour(out, orari, days, ora_dopo_pranzo) {
    var fasce_orarie = []
    for (var or = 0; or < orari.length; or++) {
        fasce_orarie.push(or)
    }
    var giorni = []
    for (var day = 0; day < days.length; day++) {
        giorni.push(day)
    }
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0                // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_anno = 'anno'
    var key_cdl = 'corso_di_laurea'
    var key_tipo = 'tipo'
    var key_mag_tr = 'mag_tr'
    var ora_prima_pranzo = ora_dopo_pranzo -2 //!!!!!!!!!!!!!!!!!!!!!!!!!!!fasce_orarie[(fasce_orarie.length/2)-1]
    var stringa = ''
    var ris = {}

    for (var j = 0; j < out.length; j++) {
        var giorno = out[j]['d']
        var tipo = out[j]['c'][key_corsi][id_corsi][key_tipo]
        //if (tipo === 'obbligatorio') {
            var orario = out[j]['h']
            //console.log(orario)

            fun = function (orario){
                return function(element) {
                    return element === orario;
                }
            };
            var index_orari = fasce_orarie.findIndex(fun(orario))        // cerco l'indice dell'ora di inizio di quel blocco di ore ///////////////////////////////////

            var orari_possibili_per_corso = []
            // estraggo le sole fasce orarie disponibili per quella lezione (distinguendo i casi critici)
            if (index_orari === 0 || index_orari === ora_prima_pranzo+1) {          // inizio mattina e inizio pomeriggio
                orari_possibili_per_corso.push(fasce_orarie[index_orari + 1])
            }
            else if (index_orari === ora_prima_pranzo || index_orari === (fasce_orarie.length) - 1) {           // fine mattina e fine pomeriggio
                orari_possibili_per_corso.push(fasce_orarie[index_orari - 1])
            }
            else {                           // il resto
                orari_possibili_per_corso.push(fasce_orarie[index_orari - 1])
                orari_possibili_per_corso.push(fasce_orarie[index_orari + 1])
            }

            // console.log(index_orari)
            var corso = out[j]['c'][key_corsi][id_corsi][key_nome_corso]
            var anno = out[j]['c'][key_corsi][id_corsi][key_anno]
            var cdl = out[j]['c'][key_corsi][id_corsi][key_cdl]
            var mag_tr = out[j]['c'][key_corsi][id_corsi][key_mag_tr]


            var present_course_before_or_after = []
            for (var i in orari_possibili_per_corso) {        // per ogni fascia oraria cerco se esiste un corso con caratteristiche simili a quelle correnti
                present_course_before_or_after.push(search_course_before_or_after(out, j, orari_possibili_per_corso[i], corso, anno, giorno, cdl, tipo, mag_tr))
            }

            if (!present_course_before_or_after.includes(true)) {           // se non sono stati trovati sia il corso precedente che il successivo

                /*console.log('#########################################')
                console.log(corso)
                console.log(giorno)
                console.log(orari_possibili_per_corso)
                console.log(anno)
                console.log(orario)
                console.log(cdl)
                console.log(tipo)
                console.log('#########################################')*/
                stringa = "singola ora per il corso " + corso + " (cdl " + cdl + ", anno " + anno + "," + mag_tr + ") nel giorno " + days[giorno] + " all'ora " + orari[orario]
                ris = create_test_response(false, stringa)
                return ris
            }
        //}
    }
    ris = create_test_response(true, stringa)
    return ris
}

/* test che permette di controllare se le preferenze del prof (orari) vengano rispettate
 * parametri:
 *      - out: orario ottenuto dal modello
 *      - obj_pref_prof: oggetto che memorizza le preferenze dei prof
 *      - orari: fasce orarie per fare lezione
 *      - days: giorni in cui si ha lezione
 * return:
 *      - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */
function testPrefProf(out, obj_pref_prof, orari, days){
    var key_prof = 'prof'
    var stringa = ''
    var ris = {}

    //var obj_pref_prof = {'Mauro Leoncini': [{0:[0,1]},{5:[6,7]}], 'Marina Cocchi': [{5:[1,2]}]}

    for (var prof in obj_pref_prof){                            // per tutti i prof
        var giorni_pref_prof = obj_pref_prof[prof]

        for (var k = 0; k < giorni_pref_prof.length; k++) {
            for (var giorno in giorni_pref_prof[k]) {           // per tutti i giorni
                //console.log(giorno)
                var pref_prof = giorni_pref_prof[k][giorno]     // ottengo fasce orarie di indisponibilita' per quel dato giorno
                //console.log(pref_prof)

                for (var j = 0; j < out.length; j++) {
                    var orario = out[j]['h']
                    //console.log(orario)
                    var professore = out[j]['c'][key_prof]
                    var gg = out[j]['d']

                    /*if (professore.includes('Leoncini')) {
                        console.log('############################')
                        console.log(gg)
                        console.log(giorno)
                        console.log(orario)
                        console.log(pref_prof)
                        console.log(prof)
                        console.log('############################')
                    }*/

                    if (pref_prof.includes(orario) && prof == professore && giorno == gg) {
                        stringa = "indisponibilita' prof " + prof + " nelle ore indicate (" + orari[orario] + ") del giorno " + days[giorno]
                        ris = create_test_response(false, stringa)
                        return ris
                    }
                }
            }
        }

    }
    ris = create_test_response(true, stringa)
    return ris
}

/*
 * funzione che restituisce la lista delle attrezzature di una particolare aula
 * parametri:
 *      - dict_aule: oggetto che memorizza le caratteristiche delle aule
 *      - aula: nome aula di cui cercare la lista di attrezzature
 * return:
 *      - se trovata, oggetto delle attrezzature
 *      - se non trovata, -1
 */
function search_list_attrez_aula(dict_aule, aula) {
    var list = []
    for (var sede in dict_aule) {
        for (var a in dict_aule[sede]) {
            if (a === aula) {
                /*console.log('####################')
                console.log(aula)
                console.log(dict_aule[sede][a].
                console.log('####################')*/
                list = dict_aule[sede][a].slice()
                return list
            }
        }
    }

    return -1

}

/* funzione che cerca e rimuove una cofigurazione di attrezzatura
 * argomenti:
 *      - lista: lista sia di attrezzature vere delle aule che di sedi
 *      - stringa: configurazione di attrezzature preferenziale da cercare o sede preferenziale da cercare
 * return:
 *      - true, se trovata
 *      - false, se non trovata
 */
function search_remove_item(lista, stringa) {
    /*for (var i in obj_map_cod_lista_att) {
        for (var j = 0; j < obj_map_cod_lista_att[i].length; j++) {*/
    for (var i = 0; i < lista.length; i++) {
        if (lista[i].includes(stringa)) {
            /*console.log('########################')
            console.log(stringa)
            console.log(lista)
            console.log(lista[i])
            console.log('########################')*/
            lista.splice(i, 1)
            return true
        }
    }
    return false
}

/* funzione che resituisce i nomi (distinti e no ripetuti) dei corsi che non hanno rispettato la capienza delle aule assegnate
 * argomenti:
 *      - lista_result: lista di vero o falso che indica l'aver o meno soddisfatto le capienza / le sedi delle aule richieste
 *      - lista_corsi: nomi dei corsi anche ripetuti, la cui aula e' stata testata per verificarne la corretta capacita' / il corretto assegnamento all'aula della sede giusta
 * return:
 *      - corsi_err: lista dei nomi dei corsi che non rispettano la capacita' dell'aula assegnata

 */
function search_false_item(lista_result, lista_corsi) {
    var corsi_err = []
    var old_corsi_err = []
    for (var i = 0; i < lista_result.length; i++) {
        if (lista_result[i] === false) {
            // se nuovo corso, lo appendo
            var val = lista_corsi[i]
            if (! old_corsi_err.includes(val)) {
                old_corsi_err.push(val)
                corsi_err.push(val)
            }
        }
    }

    return corsi_err
}

/*
 * test che permette di verificare che le attrezzature disponibili per un corso siano rispettate
 * parametri:
 *      - out: orario ottenuto dal modello
 *      - dict_aule: oggetto che memorizza le caratteristiche delle aule
 *      - obj_pref_attr_corso: oggetto che memorizza le preferenze di un prof sulle attrezzature
 * return:
 *      - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */

function testAttrezCourse(out, dict_aule, obj_pref_attr_corso) {
    var key_nome = 'nome'
    var index_ore_corso = 0         // mi interessa solo il primo elemento della lista (tanto gli altri elementi hanno il nome uguale)
    var stringa = ''
    var ris = {}
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0                // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_attr = 'att'
    var key_ore = 'ore'
    var obj_map_cod_lista_att = {}

    /* creo un oggetto del tipo:
     * 'codice_corso_con_pref1': [[lista_att_stringhizzate], [lista_att_stringhizzate], ... per tutte le ore di un corso],
     * 'codice_corso_con_pref2': uguale
     */
    for (var cod in obj_pref_attr_corso) {          // cod e' il codice del corso
        obj_map_cod_lista_att[cod] = []
    }

    //console.log(obj_pref_attr_corso)
    var lista_att_vere = []
    for (var cod in obj_pref_attr_corso) {          // cod e' il codice del corso

        // ottengo il nome del corso
        var course = obj_pref_attr_corso[cod][index_ore_corso][key_nome]

        // cerco tutte le ore di tale corso
        for (var i = 0; i < out.length; i++){
            if (out[i]['c'][key_corsi][id_corsi][key_nome_corso] === course) {
                // ottengo l'aula assegnata
                var aula = out[i]['r']

                // cerco la lista delle attrezzature dell'aula
                var lista_att_aula = search_list_attrez_aula(dict_aule, aula)
                //console.log(lista_att_aula)
                lista_att_aula.splice(0, 1)

                lista_att_vere.push(lista_att_aula.join().toLowerCase())
                obj_map_cod_lista_att[cod].push(lista_att_aula.join().toLowerCase())
            }
        }
    }
    //console.log("lista_att_vere")
    //console.log(lista_att_vere)
    var lista_corsi = []
    var lista_att_result = []
    for (var cod in obj_map_cod_lista_att) {          // cod e' il codice del corso
        for (var cc in obj_pref_attr_corso) {
            if (cod === cc) {
                var course = obj_pref_attr_corso[cc][index_ore_corso][key_nome]

                for (var i = 0; i < obj_pref_attr_corso[cc].length; i++) {         // per tutti i dizionari nella lista di tale corso
                    // ottengo la lista delle attrezzature preferenziali richieste per un corso
                    var lista_att = obj_pref_attr_corso[cc][i][key_attr].slice()
                    lista_att.splice(0, 1)
                    //console.log(lista_att + "!!!!!!!!!!!!!")
                    var string_att = lista_att.join().toLowerCase()       // per confrontarlo meglio
                    //console.log('string_att :' + string_att)

                    var ore = obj_pref_attr_corso[cc][i][key_ore]

                    for (var k = 0; k < ore; k++) {
                        lista_att_result.push(search_remove_item(lista_att_vere, string_att))        //obj_map_cod_lista_att
                        lista_corsi.push(course)
                    }
                }

            }
        }

    }

    /*console.log(lista_corsi)
    console.log('results: ' + lista_att_result)*/

    var isTrue = function(element) {
        return element === true
    }
    // se sono state trovate tutte le configurazioni di attrezzature richieste
    if (lista_att_result.every(isTrue)) {
        ris = create_test_response(true, stringa)
        return ris
    }
    else {
        var lista_corsi_err = search_false_item(lista_att_result, lista_corsi)
        stringa = 'Non rispettate le preferenze relative alle attrezzature dei seguenti corsi: (' + lista_corsi_err + ")"
        ris = create_test_response(false, stringa)
        return ris
    }
}

/*
 * funzione che permette di restituire la sede di una particolare aula
 * parametri:
 *      - dict_aule: oggetto che memorizza le informazioni sulle aule
 *      - aula: in nome dell'aula da cercare
 * return:
 *      - se trovata, la sede
 *      - se non trovata, -1
 */
function search_sede_aula(dict_aule, aula) {
    for (var sede in dict_aule){
        for (var a in dict_aule[sede]){
            if (a === aula) {
                return sede.toLowerCase()
            }
        }
    }

    return -1

}

/*
 * test che permette di verificare che i corsi siano assegnati ad aule di edifici indicati nelle preferenze
 * parametri:
 *      - out: orario ottenuto dal modello
 *      - dict_aule: oggetto che memorizza le caratteristiche delle aule
 *      - obj_pref_attr_corso: oggetto che memorizza le preferenze di un prof sulle attrezzature
 * return:
 *      - ris: oggetto composto dall'esito del test (true o false) e dal suo relativo eventuale messaggio di fallimento
 */

function testEdiCourse(out, dict_aule, obj_pref_attr_corso) {
    var key_nome = 'nome'
    var index_ore_corso = 0         // mi interessa solo il primo elemento della lista (tanto gli altri elementi hanno il nome uguale)
    var stringa = ''
    var ris = {}
    var key_corsi = 'corsi effettivi'
    var id_corsi = 0                // per evitare di guardare i corsi condivisi
    var key_nome_corso = 'nome'
    var key_attr = 'att'
    var key_ore = 'ore'
    var old_aule = []
    var first_index_list = 0            // indice in cui c'e' la sede preferenziale

    //console.log(obj_pref_attr_corso)

    // prendo le sedi preferenziali
    var sede_pref = []
    var sede_corsi = []
    for (var cod in obj_pref_attr_corso) {
        // ottengo il nome del corso
        var course = obj_pref_attr_corso[cod][index_ore_corso][key_nome]

        for (var index = 0; index < obj_pref_attr_corso[cod].length; index++) {
            for (var ora = 0; ora < obj_pref_attr_corso[cod][index][key_ore]; ora++) {
                var tmp_sede_pref = obj_pref_attr_corso[cod][index][key_attr][first_index_list]
                sede_pref.push(tmp_sede_pref.toLowerCase())
                sede_corsi.push(course)
            }
        }
    }

    var sede_reali = []
    for (var cod in obj_pref_attr_corso) {          // cod e' il codice del corso

        // ottengo il nome del corso
        var course = obj_pref_attr_corso[cod][index_ore_corso][key_nome]

        // cerco tutte le ore di tale corso (mi interessano solo le aule diverse dello stesso corso)
        var sede = ''
        for (var i = 0; i < out.length; i++) {

            if (out[i]['c'][key_corsi][id_corsi][key_nome_corso] === course) {
                var aula = out[i]['r']

                // se aula nuova
                if (! old_aule.includes(aula)) {
                    // ottengo la sede reale
                    sede = search_sede_aula(dict_aule, aula)
                    if (sede === -1) {
                        console.log("sede dell'aula non trovata")
                        return
                    }
                }

                sede_reali.push(sede)

            }
        }
    }

    /*console.log(sede_pref)
    console.log(sede_reali)
    console.log('sede corsi')
    console.log(sede_corsi)*/

    // controllo se sono rispettate le preferenze
    var lista_sede_result = []
    for (var k = 0; k < sede_pref.length; k++) {
        lista_sede_result.push(search_remove_item(sede_reali, sede_pref[k]))
    }

    //console.log(lista_sede_result)

    var isTrue = function(element) {
        return element === true
    }
    // se sono state trovate tutte le configurazioni di attrezzature richieste
    if (lista_sede_result.every(isTrue)) {
        ris = create_test_response(true, stringa)
        return ris
    }
    else {
        var lista_sedi_corsi_err = search_false_item(lista_sede_result, sede_corsi)
        stringa = "Non rispettate le preferenze relative alle sed dei seguenti corsi: (" + lista_sedi_corsi_err + ")"
        ris = create_test_response(false, stringa)
        return ris
    }
}