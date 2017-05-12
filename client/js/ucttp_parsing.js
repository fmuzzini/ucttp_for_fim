/**
 * Created by Filippo Muzzini on 04/05/2017.
 */

//variabili globali

function parsing(data){
    /*crea orari per ogni categoria e sottocategorie
    aule:
        aula1: orario
        aula2: orario
    corsi:
        lm:
            info:
                anno:
                    curr
     prof:
        prof1: orario
     */
    rooms = [];
    prof = [];
    courses = [];
    for (var o in data){
        ora = data[o];

        //inserimento nella lista delle aule
        if (rooms[ora.r] === undefined){
            rooms[ora.r] = [];
        }
        rooms[ora.r].push(ora);

        //inserimento nella lista dei prof
        if (prof[ora.c.prof] === undefined){
            prof[ora.c.prof] = [];
        }
        prof[ora.c.prof].push(ora);

        //inserimento nella lista dei corsi
        c_fs = ora.c["corsi effettivi"];
        for (var i in c_fs){
            cf = c_fs[i];
            insert_course(cf.mag_tr, cf.corso_di_laurea, cf.anno, ora);
        }
    }


    orari = {
        rooms: rooms,
        prof: prof,
        courses: courses
    };
    return orari;
}

//inserisce il corso nella giusta lista
function insert_course(mag_tr, cl, anno, ora){
    if (courses[mag_tr] === undefined){
        courses[mag_tr] = [];
    }
    if (courses[mag_tr][cl] === undefined){
        courses[mag_tr][cl] = [];
    }
    if (courses[mag_tr][cl][anno] === undefined){
        courses[mag_tr][cl][anno] = [];
    }

    courses[mag_tr][cl][anno].push(ora);
}