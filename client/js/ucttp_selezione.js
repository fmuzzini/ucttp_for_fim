/**
 * Created by Filippo Muzzini on 04/05/2017.
 */

var form_selezione;
var orari;
var lista_select = [];

function get_form_selezione(){
    form_selezione = $("#"+id_selezione);
}

function set_selezione(orari_) {
    orari = orari_
    form = form_selezione;
    var box = create_box(orari);
    form.append(box);
    form.next_sel = box;
}

function create_box(list) {
    //se sono alla fine
    ind_list = lista_select.length;
    if (list[0] !== undefined){
        var button = $("<input>").attr("type","submit").attr("value","Visualizza Orario");
        form_selezione.append(button);
        lista_select[ind_list] = {box: button, orario: list};
        return;
    }
    var box = $("<select></select>").attr("onchange","next_box("+ind_list+")");
    var blank = $("<option></option>").attr("selected","selected").attr("disabled","disabled").text("---");
    lista_select[ind_list] = {box: box, orario: list};
    box.append(blank);
    for (var s in list){
        opt = $("<option></option>").text(s).attr("value",s);
        box.append(opt);
    }

    return box;
}

function next_box(ind) {
    if (ind !== lista_select.length-1){
        remove_next(ind);
    }
    sel = lista_select[ind].box.val();
    var n_box = create_box(lista_select[ind].orario[sel]);
    form_selezione.append(n_box);
}

function remove_next(ind){
   while(lista_select.length > ind+1){
       var el = lista_select.pop();
       el.box.remove();
   }
}

function visualizza() {
    var orario = lista_select[lista_select.length-1].orario;
    init_tabella();
    set_virtual_table(orario);
    disegna_tabella();
}