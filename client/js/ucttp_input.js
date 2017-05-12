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
        dataType: "text"
    });
    return false;
}

//callback alla risposta del server
function success(data) {
    data = data.split("\n");
    data.splice(0,2);
    response = data[0];
    j = JSON.parse(response);
    orari_cat = parsing(j);
    set_selezione(orari_cat);
    //init_tabella({col:["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"], row:["9", "10", "11", "12", "14", "15", "16", "17"]});
    //set_virtual_table(rooms["Aula M1.4"]);
    //disegna_tabella();
//    set_selezione(j);

}