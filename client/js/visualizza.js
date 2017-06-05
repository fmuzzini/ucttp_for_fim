/**
 * Created by pippo on 05/06/2017.
 */

function get_orario() {
    $.get(url_get_orario, function (j) {
        get_table();
        get_form_selezione();

        orario = j.orario;
        orari_cat = parsing(orario);
        meta = j.meta;
        set_selezione(orari_cat);
    })
}