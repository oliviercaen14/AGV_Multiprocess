from constantes import *
import time
import utilitaires
import logging,os,datetime
import logfile
import class_agv

# logfile.setup_logger(__name__) 
# my_logger = logging.getLogger(__name__)
my_logger = logfile.create_logger()
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
        
def new_agv(liste_agv,info):
    agv = ADR_IP_AGV.get[info[QUI]]
    if not agv:
        my_logger.warning(f'Adresse IP inconnue =  {info[QUI]} in PID {os.getpid()}')
        return liste_agv
    if  liste_agv.get(agv):
        my_logger.info(f"nouvelle Connexion AGV = {info[QUI]} in PID {os.getpid()}")
        liste_agv[agv][CONNEXION] = info[CONNEXION]
    else:
        my_logger.info(f"Connexion AGV = {info[QUI]} in PID {os.getpid()}")
        donnees = {QUI:info[QUI],
                CONNEXION:info[CONNEXION],
                AGV:agv,
                DATA:None,
                CLASS_AGV:class_agv.info_agv(agv)}
        liste_agv[info[QUI]] = donnees
    return liste_agv    
    
    
    
    
    # agv = ADR_IP_AGV.get[info[QUI]]  
    # if not agv:
    #     my_logger.warning(f'Adresse IP inconnue =  {info[QUI]} in PID {os.getpid()}')
    #     return liste_agv
    # agv_dans_liste = liste_agv.get(agv)
    # if not agv_dans_liste:
    #     donnees = {QUI:info[QUI],
    #             CONNEXION:info[CONNEXION],
    #             AGV:agv,
    #             DATA:None,
    #             CLASS_AGV:class_agv.info_agv(agv)}
    #     liste_agv[info[QUI]] = donnees
    # else:
    #     liste_agv[agv][CONNEXION] = info[CONNEXION]
    # return liste_agv
        
        
        
def f_process(fifo_in):
    heure = datetime
    cpt,flag = 0,0 #pour test
    liste_agv = {}
    fin = False
    my_logger.info(f"demarrage supervision in PID {os.getpid()}")

    while not fin:
        while not fifo_in.empty() :
            try:
                info = fifo_in.get()
            except Exception:
                my_logger.error(f"Supervision : exception =  {Exception} in PID {os.getpid()}")
			
            if info[TYPE] == TYPE_NEW_AGV:
                liste_agv = dict(new_agv(liste_agv,info))
                #connexion[QUI] = info[DATA]
                # utilitaires.log_message_info(f'supervision : Nouvel AGV = {info[QUI]}')
            elif info[TYPE] == TYPE_NEW_DATA:  
                try:
                    agv = ADR_IP_AGV[info[QUI]]
                except Exception:
                    my_logger.error(f"Supervision : exception =  {Exception} in PID {os.getpid()}")
                
                try:    
                    donnees = {QUI:info[QUI],
                            CONNEXION:info[CONNEXION],
                            AGV:agv,
                            DATA:info[DATA],
                            'class_agv':class_agv.info_agv(agv)}
                except Exception:
                    my_logger.error(f"Supervision : exception =  {Exception} in PID {os.getpid()}")
                    
                #connexion[info[QUI]] = info[CONNEXION]
                liste_agv[info[QUI]] = donnees
                
                try:
                    ma_connexion = liste_agv[info[QUI]][CONNEXION]   #connexion[info[QUI]]
                    ma_connexion.send(bytearray([1,2,3]))
                except Exception:
                    my_logger.error(f"Supervision : exception =  {Exception} in PID {os.getpid()}")
                
                # utilitaires.log_message_info(f'Supervision : {agv} {info[DATA]}')
                # my_logger.info(f"Supervision : agv = {agv} data = {info[DATA]} in PID {os.getpid()}")
                my_logger.info(f"Supervision : agv = {agv} data = {decompose_dico(133,info[DATA])}in PID {os.getpid()}")
        time.sleep(0.001)
        #pour test des logs
        heure = datetime.datetime.now().time()
        seconde = heure.second
        if seconde == 0:
            if flag == 0:
                flag = 1
                cpt += 1
                my_logger.info(f"Supervision__ : {heure}  {cpt} pour test in PID {os.getpid()}")
                print(f"Supervision__ : {heure}  {cpt} pour test in PID {os.getpid()}")
        else: flag = 0
