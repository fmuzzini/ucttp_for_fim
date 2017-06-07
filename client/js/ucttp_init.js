/**
 * Created by Filippo Muzzini on 04/05/2017.
 */


var URL = "cgi-bin/ucttp.py";   // URL della pagina del risolutore
var url_save = "cgi-bin/save.py"; //URL pagina salvataggio
var url_get_orario = "cgi-bin/get_orario.py";
var input_file = ['piani', 'manifesto', 'insegnamenti', 'aule', 'pesi', 'indisponibilita', 'parametri', 'blocchi', 'edifici'];    //nomi dei file necessari come l'input

var id_table = "tab_output";    //id della tabella di output
var id_selezione = "selezione";  //id del form di selezione

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
            maxHeigth: 200,
            position: {
                my: "right top",
                at: "right center"
            },
            classes: {
                "ui-dialog": "ui-dialog-vincoli"
            }
        })
    });

    $( function() {
        $( "#conf_rip" ).dialog({
            resizable: false,
            autoOpen: false,
            modal: true,
            buttons: {
                "Confermo": function () {
                    rip_orario();
                    $( this ).dialog( "close" );
                },
                "Annulla": function() {
                    $( this ).dialog( "close" );
                }
            }
        });
     } );

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
    });

    $( function () {
        $("#dialog_save").dialog({
            autoOpen: false,
            modal: true,
            buttons: {
                "Salva solo sul server": function () {
                    save(false);
                    $( this ).dialog( "close" );
                },
                "Salva anche su file": function () {
                    save(true);
                    $( this ).dialog( "close" );
                },
                "Annulla operazione": function() {
                  $( this ).dialog( "close" );
                }
            }
        })
    });
}

function show_vincoli() {
        $("#vincoli").dialog("open");
}


function controllo_orario() {
    var res = check_constraints_model(orario, disp_prof, meta, dict_aule, dict_preferenze_prof, map_corsi, num_stud, map_aule, cap_aula, ora_dopo_pranzo, dict_map_corso_blocchi_ore);
    $("#vincoli").html(res);
}

