from constantes import *
import time
import logging,os,datetime
import class_agv,fichier_excel,log_multi_file
# from variables_globales import global_logger

# my_logger = logfile.create_logger()
global_logger = None
# - Supervision : agv = AGV_08 
#                 data = {'dde_acquit': 0,
#                         'etat_bumper': False, 
#                         'etat_presence': True, 
#                         'etat_auto': '1', 
#                         'etat_radar': '1', 
#                         'etat_au': '1', 
#                         'num_tag': '1001', 
#                         'suivi_fil': '1', 
#                         'cpt_trame': '55'} 
#                         in PID 15744

def decompose_dico (nbr_caract,dico):
    espaces = ' ' * nbr_caract
    return ''.join(f'{key} : {element} \n {espaces} ' for key, element in dico.items())
        
def new_agv(liste_agv,info,queue_log):
    agv = ADR_IP_AGV.get(info[QUI])
    if not agv:
        global_logger.warning(f"Nouvelle connexion venant d'Adresse IP inconnue =  {info[QUI]} in PID {os.getpid()}")
        return liste_agv
    if  liste_agv.get(info[QUI]):
        global_logger.info(f"nouvelle Connexion AGV = {info[QUI]} in PID {os.getpid()}")
        liste_agv[info[QUI]][CONNEXION] = info[CONNEXION]
        liste_agv[info[QUI]][CLASS_AGV].connexion = info[CONNEXION]
        
    else:
        global_logger.info(f"Connexion AGV = {info[QUI]} in PID {os.getpid()}")
        donnees = {QUI:info[QUI],
                CONNEXION:info[CONNEXION],
                AGV:agv,
                DATA:None,
                CLASS_AGV:class_agv.info_agv(agv,info[QUI],info[CONNEXION],queue_log)}
        liste_agv[info[QUI]] = donnees
        
    return liste_agv    
    
def new_data(liste_agv,info,queue_log):
    agv = ADR_IP_AGV.get(info[QUI])
    if not agv:
        global_logger.warning(f"nouvelles données venant d'une Adresse IP inconnue =  {info[QUI]} in PID {os.getpid()}")
        return liste_agv

    if  not liste_agv.get(info[QUI]):
        liste_agv = dict(new_agv(liste_agv,info,queue_log))
    liste_agv[info[QUI]][CONNEXION] = info[CONNEXION]
    liste_agv[info[QUI]][CLASS_AGV].mise_a_jour(info[DATA])

    return liste_agv    



    
        
        
def f_process(fifo_in,queue_log):
    log_multi_file.worker_configurer(queue_log)
    # global my_logger
    global global_logger
    global_logger = logging.getLogger('gestion_globale')
    heure = datetime
    cpt,flag = 0,0 #pour test
    liste_agv = {}
    fin = False
    global_logger.info(f"demarrage supervision in PID {os.getpid()}")
    fichier_excel.gest_fichier_excel(queue_log)
    info = None
    while not fin:
        while not fifo_in.empty() :
            try:
                info = fifo_in.get()
            except Exception:
                info = None
                global_logger.error(f"impossible de recevoir les info de la queue 'Supervision'  {Exception} in PID {os.getpid()}")
            if info:
                if info[TYPE] == TYPE_NEW_AGV:
                    liste_agv = dict(new_agv(liste_agv,info,queue_log))
                    print (f'liste_agv from new_agv = {liste_agv}')
                elif info[TYPE] == TYPE_NEW_DATA:  
                    liste_agv = dict(new_data(liste_agv,info,queue_log))
        time.sleep(0.001)
        #pour test des logs
        heure = datetime.datetime.now().time()
        seconde = heure.second
        if seconde == 0:
            if flag == 0:
                flag = 1
                cpt += 1
                global_logger.info(f"Supervision__ : {heure}  {cpt} pour test in PID {os.getpid()}")
                print(f"Supervision__ : {heure}  {cpt} pour test in PID {os.getpid()}")
        else: flag = 0
