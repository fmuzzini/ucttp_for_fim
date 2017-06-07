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
        cap_aula: cap_aula,
        ora_dopo_pranzo: ora_dopo_pranzo,
        dict_preferenze_prof: dict_preferenze_prof,
        dict_map_corso_blocchi_ore: dict_map_corso_blocchi_ore
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
    $("#dialog_save").dialog("open");
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