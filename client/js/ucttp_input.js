/**
 * Created by Filippo Muzzini on 02/05/2017.
 */

//variabili globali
var file_form;

//crea il form per l'inserimento dei file
function init_input() {
    file_form = $("#files");
    file_form.submit = function(f){return false;};
    input_elem = create_input_element(input_file);
    for (var index in input_elem){
        i = input_elem[index];
        file_form.append(i.label);
        file_form.append(i.input);
		file_form.append("<br/>")
    }
    sub = $("<input>").attr("type", "submit").attr("value", "OK");
    file_form.append(sub);
    file_form.submit(invia);
}

//creare gli elementi per l'input
function create_input_element(input_file) {
    res = [];
    for (var index in input_file){
        var i = input_file[index];
        label = $("<label>").text(i).attr("for", i);
        input = $("<input>").attr("type", "file").attr("id", i).attr("name", i);
        elem = {
            label: label,
            input: input
        };
        res.push(elem);
    }

    return res;
}

//gestisce l'invio dei file in modo asincrono
function invia(f) {
    table.text("");
    form_selezione.text("");
    fm = f;
    data = new FormData();
    for(var index in input_elem){
        var reader = new FileReader();
        i = input_elem[index].input;


        data.append(i.attr("name"), i.get(0).files[0])

    }

    $.ajax({
        type: "POST",
        url: URL,
        processData: false,
        contentType: false,
        headers: {"Content-Transfer-Encoding": "base64"},
        data: data,
        success: success,
        error: error,
        beforeSend: attesa,
        dataType: "text"
    });
    return false;
}

//callback alla risposta del server
function success(data) {
    data = data.split("\n");
    data.splice(0,2);
    response = data[0];

    elabora_response(response);
}

function elabora_response(response) {
    j = JSON.parse(response);
    orario = j.orario;
    orario_iniziale = JSON.parse(JSON.stringify(orario));
    orari_cat = parsing(orario);
    meta = j.meta;
    set_selezione(orari_cat);

    dict_aule = j.dict_aule;
    disp_prof = j.disp;
    map_corsi = j.map_corsi;
    num_stud = j.num_stud;
    map_aule = j.map_aule;
    cap_aula = j.cap_aula;
    dict_preferenze_prof = j.dict_preferenze_prof;
    ora_dopo_pranzo = j.ora_dopo_pranzo;
    dict_map_corso_blocchi_ore = j.dict_map_corso_blocchi_ore;

    pop_aule_is_loaded = false;

    $("#dialog").dialog("close");
    $("body").accordion("option", "active", 1);

    controllo_orario();
}

function attesa(){
    $("#dialog").dialog("open");
}

function error() {
    $("#dialog").dialog("close");
    $("#error").dialog("open");
}