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
function init_tabella(meta){
    table.text("");
    col = meta.col;
    row = meta.row;

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
            cell = $("<td></td>").attr("h", i).attr("d", j);
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
        virtual_table.get(h,d).add(ora);
    }
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
        r = $("<div></div>").attr("class", "widget");
        testo = "";
        for (var i=0; i<this.ore.length; i++){
            testo += this.ore[i].c["corsi effettivi"][0].nome;
        }

        r.text(testo);

        cell_table.get(this.h, this.d).append(r);
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
