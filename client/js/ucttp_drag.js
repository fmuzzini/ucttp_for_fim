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
    visualizza();
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