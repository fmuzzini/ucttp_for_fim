/**
 * Created by pippo on 25/05/2017.
 */

function drag(ev){
    ev.dataTransfer.setData("el", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("el");
    var target = ev.target;

    if (target.nodeName === "P")
        target = target.parentNode;
    else if (target.nodeName === "TD")
        target = target.childNodes[0];
    else if (target.nodeName !== "DIV")
        return false;

    var td = target.parentNode;
    var g = td.getAttribute("d");
    var h = td.getAttribute("h");

    muovi(data, g, h);

    target.appendChild(document.getElementById(data));
    //visualizza()
    
    controllo_orario();
}

function scegli_aula(ev, el){
    ev.preventDefault();
    var el = $(el);

    mostra_popup(el);
}

function mostra_popup(el) {
    var id = el.parent().attr("id");
    var room = el.text();
    var pop = $("#aule_pop");
    var tend = $("#tendina_pop_aule");
    tend.attr("id_ora", id);

    loading_pop_aule();
    //var sel = $("#pop_"+get_room_name(room));
    var sel = $("option:contains('"+room+"')");

    sel.prop("selected", true);

    pop.dialog("open");
}

function loading_pop_aule() {
    if(pop_aule_is_loaded)
        return;

    var tendina = $("#tendina_pop_aule");
    tendina.html("");
    for (r in rooms){
        var opt = $("<option>").attr("id", "pop_"+get_room_name(r)).text(r);
        tendina.append(opt);
    }
    pop_aule_is_loaded = true;
}

function get_room_name(r) {
    return r.replace(/\s+/g, '').replace(/\(.*\)/g, '');
}

function allowDrop(ev) {
    ev.preventDefault();
}

function muovi(id, g, h) {
    var ora = get_ora(parseInt(id));
    ora.d = parseInt(g);
    ora.h = parseInt(h);
}

function get_ora(id) {
    for (i in orario){
        var ora = orario[i];
        if (ora.id === id)
            return ora;
    }
}


function cambio_aula(id, aula){
    var ora = get_ora(parseInt(id));
    ora.r = aula;
}

function aula_cambiata(el) {
    var id = $(el).attr("id_ora");
    var aula = $(el.selectedOptions).text();
    var ora = get_ora(parseInt(id));
    var v_aula = ora.r;
    cambio_aula(id, aula);

    //cambia array aula
    var index = rooms[v_aula].indexOf(ora);
    rooms[v_aula] = rooms[v_aula].splice(index, 1);
    rooms[aula].push(ora);
    visualizza();

    controllo_orario();

    var pop = $("#aule_pop");
    pop.dialog("close");
}

function ripristino() {
    $( "#conf_rip" ).dialog("open");
}

function rip_orario() {
    orario = JSON.parse(JSON.stringify(orario_iniziale));
    table.text("");
    form_selezione.text("");
    orari_cat = parsing(orario);
    set_selezione(orari_cat);
    controllo_orario();
}