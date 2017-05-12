import xpress as xp
import numpy as np
import os


def solve_model(C, D, H, R, CIC, P, CLO, HI, CAP_AULA, NUM_STUD):
    n_C = len(C)		# numero ore del corso (1 2 3 4 5 6 7 8 9)
    n_D = len(D)		# giorni (1..5)
    n_H = len(H)		# ore (1..8)
    n_R = len(R)		# aule (1..n)

    #l'insieme CIC_union e' l'insieme di tutti i CI
    CIC_union = set([item for CI in CIC for item in CI])
    #n_CIC = len(CIC_union)

    C_minus_CI = C - CIC_union
    #CI -> indici iniziali ore (1, 4)
    #CIC -> ([1, 4], [5, 7]) indici iniziali di ogni corso divisi
    #CAP_AULA -> (33, 44, 64 ...)
    #CO -> corsi obbligatori -> indici saltando quelli opzionali (1,3,4,5, ...)
    #CLO -> insieme dei C0 -> [(1..150), [], []]
    #P -> insieme degli insiemi dei corsi di un prof  -> [[],[],[]]
    #p -> insieme dei corsi di un prof -> []
    #NUM_STUD -> (21, 44, ...)

    #Instanziamento problema
    mp = xp.problem (name = "Gestione Aule")
    mp.setlogfile(os.devnull)

    #Variabili decisionali x
    x = np.array([xp.var(vartype = xp.binary) for i in xrange(n_C*n_D*n_H*n_R)]).reshape((n_C,n_D,n_H,n_R))

    #variabili decisionali xi
    csi = np.array([xp.var(vartype = xp.continuous) for i in xrange(n_C*n_D*n_H*n_R)]).reshape((n_C,n_D,n_H,n_R))

    #vincolo di uno solo corso nella stessa stanza in un certo momento
    ocir = (xp.Sum([x[c,d,h,r] for c in C]) <= 1 for r in R for h in H for d in D)

    #vincolo di non sovrapposizione corsi dello stesso prof
    nsp = (xp.Sum([x[c,d,h,r] for c in p for r in R]) <= 1 for p in P for h in H for d in D)

    #vincolo di non sovrapposizione corsi obbligatori
    nsco = (xp.Sum([x[c,d,h,r] for c in CO for r in R]) <= 1 for CO in CLO for h in H for d in D)

    #vincolo tutte le ore di lezione devono essere in orario
    toio = (xp.Sum([x[c,d,h,r] for d in D for h in H for r in R]) == 1 for c in C)

    #vincolo capienza aula
    ca = (x[c,d,h,r]*NUM_STUD[c] - csi[c,d,h,r] <= CAP_AULA[r] for c in CIC_union for r in R for h in H for d in D)

    #vincolo uno solo blocco di lezioni della stessa materia in un giorno
    sbg = (xp.Sum([x[c,d,h,r] for c in CI for h in H for r in R]) <= 1 for d in D for CI in CIC)

    #vincolo continuita' ore
    co = (x[c,d,h,r] - x[c-1,d,h-1,r] == 0 for c in C_minus_CI for h in H for d in D for r in R)

    #vincoli per evitare ore a cavallo pausa pranzo e circolarita'
    br = (x[c,d,h,r] == 0 for c in C_minus_CI for h in HI for d in D for r in R)

    #funzione obbiettivo
    obj = (xp.Sum([csi[c,d,h,r] for c in CIC_union for d in D for h in H for r in R]))

    #Aggiunta variabili decisionali al problema
    mp.addVariable(x)
    mp.addVariable(csi)

    #Aggiunta vincoli al problema
    mp.addConstraint(ocir)
    mp.addConstraint(nsp)
    mp.addConstraint(nsco)
    mp.addConstraint(toio)
    mp.addConstraint(sbg)
    mp.addConstraint(ca)
    mp.addConstraint(co)
    mp.addConstraint(br)

    #Inserimento funzione obbiettivo nel problema
    mp.setObjective(obj, sense=xp.minimize)

    #risoluzione
    mp.solve()

    status_string = mp.getProbStatusString()
    if "infeas" in status_string:
        raise Exception("Problem is infeasible")

    #rimappamento variabili soluzione
    sol_x = mp.getSolution(x)
    sol_x = np.array(sol_x).reshape((n_C,n_D,n_H,n_R))

    sol_csi = mp.getSolution(csi)
    sol_csi = np.array(sol_csi).reshape((n_C,n_D,n_H,n_R))

    #valore funzione obbiettivo
    obj_val = mp.getObjVal()

    sol = ModelSolution(sol_x, sol_csi, obj_val)

    return sol


class ModelSolution:
    def __init__(self, x, csi, obj_val):
        self.x = x
        self.csi = csi
        self.obj_val = obj_val
