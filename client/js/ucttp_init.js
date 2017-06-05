/**
 * Created by Filippo Muzzini on 04/05/2017.
 */


var URL = "cgi-bin/ucttp.py";   // URL della pagina del risolutore
var url_save = "cgi-bin/save.py"; //URL pagina salvataggio
var url_get_orario = "cgi-bin/get_orario.py";
var input_file = ['piani', 'manifesto', 'insegnamenti', 'aule', 'pesi', 'indisponibilita', 'parametri', 'blocchi', 'edifici'];    //nomi dei file necessari come l'input

var id_table = "tab_output";    //id della tabella di output
var id_selezione = "selezione";  //id del form di selezione

var pop_aule_is_loaded = false;

function init() {
    init_input();
    get_table();
    get_form_selezione();

    $( function() {
            $("body").accordion({
                header: "h2",
                heightStyle: "content"
            });
        } );

    $( function () {
        $("#dialog").dialog({
            classes: {
                "ui-dialog-titlebar-close": "ui-dialog-titlebar-no-close"
            },
            autoOpen: false,
            closeOnEscape: false,
            modal: true
        })
    });

    $( function () {
        $("#vincoli").dialog({
            autoOpen: false,
            position: {
                my: "right center",
                at: "right center"
            }
        })
    });

    $( function () {
        $("#aule_pop").dialog({
            autoOpen: false,
            modal: true
        })
    });

    $( function () {
        $("#error").dialog({
            autoOpen: false,
            modal: true
        })
    })
}

function show_vincoli() {
    $("#vincoli").dialog("open");
}


function controllo_orario() {
    var res = check_constraints_model(orario, disp_prof);
    $("#vincoli").html(res);
}

