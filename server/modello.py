import xpress as xp
import numpy as np
import os


def solve_model(C, D, H, R, CIC, P, CLO, CL, HI, PROF_OUT, CAP_AULA, ATT, LIST_ATT, CORSI_ATT, E, EDI, CORSI_EDI, NUM_STUD, TAB_PESI, coef):
    n_C = len(C)		# numero ore del corso (1 2 3 4 5 6 7 8 9)
    n_D = len(D)		# giorni (1..5)
    n_H = len(H)		# ore (1..8)
    n_R = len(R)		# aule (1..n)

    n_CL = len(CL)

    #se gli insiemi sono vuoti il problema non si puo' risolvere
    if (n_C == 0 or n_D == 0 or n_H == 0 or n_R == 0 or len(CIC) == 0 or len(P) == 0 or len(CLO) == 0 or len(CAP_AULA) != n_R or len(NUM_STUD) != n_C):
        raise Exception("Mancanza dati")

    #l'insieme CIC_union e' l'insieme di tutti i CI
    CIC_union = set([item for CI in CIC for item in CI])

    n_CIC = len(CIC_union)

    C_minus_CI = C - CIC_union

    #Instanziamento problema
    mp = xp.problem (name = "Gestione Aule")
    mp.setlogfile(os.devnull)
    #mp.setlogfile("log")

    #set controls
    controls = {
        'cutstrategy': 3,
        'gomcuts': 20,
        'cutfreq': 1,
        'cutdepth': 1000,
        'nodeselection': 5
    }
    mp.setControl(controls)

    #Variabili decisionali x
    x = np.array([xp.var(vartype=xp.binary) for i in xrange(n_C*n_D*n_H*n_R)]).reshape((n_C,n_D,n_H,n_R))

    #variabili decisionali xi_cap
    csi_cap = np.array([xp.var(vartype=xp.continuous) for i in xrange(n_C*n_D*n_H*n_R)]).reshape((n_C,n_D,n_H,n_R))

    #variabili decisionali xi_att
    csi_att = np.array([xp.var(vartype=xp.continuous) for i in xrange(n_C * n_D * n_H * n_R)]).reshape((n_C, n_D, n_H, n_R))

    #variabili decisionali xi_edi
    csi_edi = np.array([xp.var(vartype=xp.continuous) for i in xrange(n_C * n_D * n_H * n_R)]).reshape((n_C, n_D, n_H, n_R))

    #variabili decisionali s
    s = np.array([xp.var(vartype=xp.continuous) for i in xrange(n_CL*n_D*n_H)]).reshape((n_CL, n_D, n_H))

    #variabili decisionali g
    #g = np.array([xp.var(vartype=xp.binary) for i in xrange(n_CL*n_D)]).reshape((n_CL,n_D))

    #vincolo di uno solo corso nella stessa stanza in un certo momento
    ocir = (xp.Sum([x[c,d,h,r] for c in C]) <= 1 for r in R for h in H for d in D)

    #vincolo di non sovrapposizione corsi dello stesso prof
    nsp = (xp.Sum([x[c,d,h,r] for c in p for r in R]) <= 1 for p in P for h in H for d in D)

    #vincolo di non sovrapposizione corsi obbligatori
    nsco = (xp.Sum([x[c,d,h,r] for c in CO for r in R]) <= 1 for CO in CLO for h in H for d in D)

    #vincolo tutte le ore di lezione devono essere in orario
    toio = (xp.Sum([x[c,d,h,r] for d in D for h in H for r in R]) == 1 for c in C)

    #vincolo capienza aula
    ca = (x[c,d,h,r]*NUM_STUD[c] - csi_cap[c,d,h,r] <= CAP_AULA[r] for c in CIC_union for r in R for h in H for d in D)

    #vincolo uno solo blocco di lezioni della stessa materia in un giorno
    sbg = (xp.Sum([x[c,d,h,r] for c in CI for h in H for r in R]) <= 1 for d in D for CI in CIC)

    #vincolo continuita' ore
    co = (x[c,d,h,r] - x[c-1,d,h-1,r] == 0 for c in C_minus_CI for h in H for d in D for r in R)

    #vincoli per evitare ore a cavallo pausa pranzo e circolarita'
    #l'ora iniziale deve essere sempre presente per evitare circolarita'
    if (len(HI) == 0):
        HI = [0]
    br = (x[c,d,h,r] == 0 for c in C_minus_CI for h in HI for d in D for r in R)

    vincoli_agg = []
    funz_agg = []
    #vincolo indisponibilita' prof
    if (len(PROF_OUT) != 0):
        ip = (x[c,d,h,r] == 0 for r in R for (c,d,h) in PROF_OUT)
        vincoli_agg.append(ip)

    #vincolo attrezzature aula
    if (len(CORSI_ATT) != 0) and (len(LIST_ATT) != 0):
        att = (CORSI_ATT[c,t] * x[c,d,h,r] - LIST_ATT[r,t] - csi_att[c,d,h,r] <= 0 for d in D for h in H for c in CIC_union for r in R for t in ATT)
        vincoli_agg.append(att)
        # funzione obbiettivo sulle attrezzature delle aule
        obj_att = (coef['att'] / float(n_CIC) * xp.Sum([csi_att[c, d, h, r] for c in CIC_union for d in D for h in H for r in R]))
        funz_agg.append(obj_att)

    #vincolo edifici
    if (len(CORSI_EDI) != 0 and len(EDI) != 0):
        edi = (CORSI_EDI[c,e] * x[c,d,h,r] - EDI[r,e] - csi_edi[c,d,h,r] <= 0 for e in E for c in CIC_union for h in H for d in D for r in R)
        vincoli_agg.append(edi)
        # funzione obbiettivo sugli edifici
        obj_e = (coef['cap'] / float(n_CIC) * xp.Sum([csi_edi[c, d, h, r] for c in CIC_union for d in D for h in H for r in R]))
        funz_agg.append(obj_e)

    #vincolo sovrapposizione corsi facoltativi
    cf = (xp.Sum([x[c,d,h,r] for r in R for c in cl]) <= s[index,d,h] for d in D for h in H for (index,cl) in enumerate(CL))

    #funzione obbiettivo base (solo capacita' aule)
    obj_cap = (coef['cap'] / float(n_CIC*(np.max(NUM_STUD)-np.min(CAP_AULA))) * xp.Sum([csi_cap[c,d,h,r] for c in CIC_union for d in D for h in H for r in R]))

    #funzione obiettivo per compattare orario
    if len(TAB_PESI) != 0:
        max_pesi = float(n_C * np.max(TAB_PESI))
        min_pesi = float(n_C * np.min(TAB_PESI))
        obj_comp = (coef['comp'] / (max_pesi - min_pesi) * (-min_pesi + xp.Sum([x[c,d,h,r]*TAB_PESI[d,h] for c in C for d in D for h in H for r in R]) ))
        funz_agg.append(obj_comp)

    #vincoli giorni
    #ng = (xp.Sum([x[c,d,h,r] for c in cl for r in R for h in H]) <= g[index,d] * len(H) * len(cl) for (index,cl) in enumerate(CL) for d in [0, 4])
    #obj_ng = (coef['comp'] / float(n_CL*2*2) * xp.Sum([g[cl,d] for cl in xrange(n_CL) for d in [0, 4]]))

    #funzione obbiettivo corsi facoltativi
    obj_fac = (coef['sov'] / float(n_C) * xp.Sum([s[cl,d,h] for cl in xrange(n_CL) for d in D for h in H]))

    #funzione obbiettivo completa
    obj = obj_cap + obj_fac #+ obj_ng
    for f in funz_agg:
        obj = obj + f

    #Aggiunta variabili decisionali al problema
    mp.addVariable(x)
    mp.addVariable(csi_cap)
    mp.addVariable(csi_att)
    mp.addVariable(csi_edi)
    mp.addVariable(s)
    #mp.addVariable(g)

    #Aggiunta vincoli al problema
    mp.addConstraint(ocir)
    mp.addConstraint(nsp)
    mp.addConstraint(nsco)
    mp.addConstraint(toio)
    mp.addConstraint(sbg)
    mp.addConstraint(ca)
    mp.addConstraint(co)
    mp.addConstraint(br)
    mp.addConstraint(cf)
    #mp.addConstraint(ng)
    for v in vincoli_agg:
        mp.addConstraint(v)

    #Inserimento funzione obbiettivo nel problema
    mp.setObjective(obj, sense=xp.minimize)

    #mp.write("modello.lp", "lps")

    #risoluzione
    mp.solve()

    status_string = mp.getProbStatusString()
    if "infeas" in status_string:
        raise Exception("Problem is infeasible")

    #rimappamento variabili soluzione
    sol_x = mp.getSolution(x)
    sol_x = np.array(sol_x).reshape((n_C,n_D,n_H,n_R))

    sol_csi = mp.getSolution(csi_cap)
    sol_csi = np.array(sol_csi).reshape((n_C,n_D,n_H,n_R))
    sol_s = mp.getSolution(s)
    sol_s = np.array(sol_s).reshape((n_CL, n_D, n_H))
    sol_att = mp.getSolution(csi_att)
    sol_att = np.array(sol_att).reshape((n_C,n_D,n_H,n_R))
    sol_edi = mp.getSolution(csi_edi)
    sol_edi = np.array(sol_edi).reshape((n_C,n_D,n_H,n_R))

    #valore funzione obbiettivo
    obj_val = mp.getObjVal()

    sol = ModelSolution(sol_x, sol_csi, obj_val)

    return sol


class ModelSolution:
    def __init__(self, x, csi, obj_val):
        self.x = x
        self.csi = csi
        self.obj_val = obj_val
