/**
 * Created by Filippo Muzzini on 04/05/2017.
 */

//variabili globali
var table;
var virtual_table;
var cell_table;
var color;

//trova la tabella
function get_table(){
    table = $("#"+id_table);
    return table;
}

//inizializza la struttura della tabella
function init_tabella(){
    table.text("");
    col = meta.giorni;
    row = meta.ore;

    cell_table = new matrix(row.length, col.length);

    //prima riga = header colonne
    f_row = $("<tr></tr>");
    f_row.append($("<td></td>"));
    for (i=0; i<col.length; i++){
        f_row.append($("<td></td>").text(col[i]).attr("class", "header_giorno"));
    }
    table.append(f_row);

    //ogni riga ha come primo elemento l'header di quella riga
    for (i=0; i<row.length; i++){
        o_row = $("<tr></tr>");
        header = $("<td></td>").text(row[i]).attr("class", "header_ora");
        o_row.append(header);

        //le altre celle della riga hanno attributi sulla posizione
        for (var j=0; j<col.length; j++){
            cell = $("<td></td>").attr("h", i).attr("d", j).attr("ondragover", "allowDrop(event)").attr("ondrop", "drop(event)");
            o_row.append(cell);
            cell_table.set(i,j,cell);
        }

        table.append(o_row);
    }

    init_virtual_table(row.length, col.length);
}

//inizializza la tabella virtuale
function init_virtual_table(n_r, n_c){
    color = [];
    virtual_table = new matrix(n_r, n_c);
    for (i=0; i<n_r; i++){
        for (var j=0; j<n_c; j++){
            w = new widget_ora(i,j);
            virtual_table.set(i,j,w);
        }
    }
}

//associa le ore ad ogni cella della tabella virtuale
function set_virtual_table(orario){
    for (i in orario){
        ora = orario[i];
        h = ora.h;
        d = ora.d;
        ora.id = get_id(ora);
        virtual_table.get(h,d).add(ora);
    }
}

function get_id(ora) {
    return ora.n;
}

function disegna_tabella(){
    v = virtual_table;
    for (var i=0; i<v.x; i++){
        for (var j=0; j<v.y; j++){
            v.get(i,j).display();
        }
    }
}

//oggetto che rappresenta la visualizzazione grafica di una cella
function widget_ora(h,d){
    this.h = h;
    this.d = d;
    this.ore = [];

    this.add = function(ora){
        this.ore.push(ora);
    };

    this.display = function() {
        var r = $("<div></div>").attr("class", "widget");
        for (var i=0; i<this.ore.length; i++){
            var id = this.ore[i].id;
            var text = get_nome(this.ore[i].c);
            //var h3 = $("<h3>").text(text);
            var p = $("<p>").attr("draggable", "true").attr("class", "corso").attr("ondragstart", "drag(event)");
            var prof = $("<p>").attr("class", "prof").text(this.ore[i].c.prof);
            var aula = $("<p>").attr("class", "aula").attr("ondblclick","scegli_aula(event, this)").text(this.ore[i].r);
            p.attr("id", id);
            p.text(text);
            p.append(prof);
            p.append(aula);

            //r.append(h3);
            r.append(p);
        }

        // $( function() {
        //     r.accordion({
        //         header: "h3",
        //         collapsible: true,
        //         active: false
        //     });
        // } );

        cell_table.get(this.h, this.d).append(r);
    }

}

function get_nome(corso_) {
    var corsi = corso_['corsi effettivi'];
    if (form_selezione.next_sel.value !== 'courses'){
        return corsi[0].nome;
    }

    var corso = form_selezione.next_sel;
    var mag_tr = corso.next_sel;
    var anno = mag_tr.next_sel;
    for(var i=0; i<corsi.length; i++){
        var ef = corsi[i];
        if (ef['mag_tr'] === mag_tr && ef['anno'] === anno && ef['corso'] === corso){
            return ef['nome']
        }
    }
}

function matrix(x,y){
    this.x = x;
    this.y = y;
    this.item = [];
    for (var i=0; i<x; i++){
        var row = [];
        for (var j=0; j<y; j++){
            row.push(0);
        }
        this.item.push(row);
    }

    this.set = function(x,y,o){
        this.item[x][y] = o;
    };

    this.get = function(x,y){
        return this.item[x][y];
    };

    this.reset = function(){
        for (var i=0; i<this.x; i++){
            for (var j=0; j<this.y; j++){
                this.set(x,y, 0);
            }
        }
    }
}
