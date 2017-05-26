/**
 * Created by Filippo Muzzini on 04/05/2017.
 */


var URL = "cgi-bin/ucttp.py";   // URL della pagina del risolutore
var input_file = ['piani', 'manifesto', 'insegnamenti', 'aule', 'pesi', 'indisponibilita', 'parametri', 'blocchi', 'edifici'];    //nomi dei file necessari come l'input

var id_table = "tab_output";    //id della tabella di output
var id_selezione = "selezione";  //id del form di selezione

function init() {
    init_input();
    get_table();
    get_form_selezione();
}

