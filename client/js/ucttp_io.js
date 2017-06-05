/**
 * Created by pippo on 01/06/2017.
 */

function save(file) {
    var item_to_save = {
        orario : orario,
        meta: meta
    };
    item_to_save = JSON.stringify(item_to_save);

    var item_back = {
        orario : orario,
        meta: meta,
        dict_aule: dict_aule,
        disp: disp_prof,
        map_corsi: map_corsi,
        num_stud: num_stud,
        map_aule: map_aule,
        cap_aula: cap_aula
    };
    item_back = JSON.stringify(item_back);

    var form = $("<form>").attr("action", url_save).attr("method", "post");

    if(file){
        var hidden_file = $("<input>").attr("type", "hidden").attr("name", "file").attr("value", true);
        form.append(hidden_file);
    }

    var hidden_back = $("<input>").attr("type", "hidden").attr("name", "item_back").attr("value", item_back);
    var hidden_save = $("<input>").attr("type", "hidden").attr("name", "item_to_save").attr("value", item_to_save);
    form.append(hidden_back);
    form.append(hidden_save);
    $("body").append(form);

    form.submit();
}

function salvataggio(file) {
    $("#dialog_save").dialog({
        autoOpen: true,
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
    });
}

function carica() {
    var input = $("#input_orario").get(0).files[0];
    var reader = new FileReader();
    
    reader.onload = function (event) {
        var data = event.target.result;
        table.text("");
        form_selezione.text("");
        elabora_response(data);
    };

    reader.readAsText(input);

    return false;
}