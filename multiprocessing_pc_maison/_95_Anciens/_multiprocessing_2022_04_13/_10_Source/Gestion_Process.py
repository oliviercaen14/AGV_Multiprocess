from constantes import *
import time
import utilitaires
import logging,os

def f_process(fifo_in):
    logger = logging.getLogger("app") 
    #connexion = {}
    liste_agv = {}
    fin = False
    # utilitaires.log_message_info ('demarrage supervision')
    logger.info(f"demarrage supervision in PID {os.getpid()}")
    while not fin:
        while not fifo_in.empty() :
            info = fifo_in.get()
            if info[TYPE] == TYPE_NEW_AGV:
                #connexion[QUI] = info[DATA]
                # utilitaires.log_message_info(f'supervision : Nouvel AGV = {info[QUI]}')
                logger.info(f"supervision : Nouvel AGV = {info[QUI]} in PID {os.getpid()}")
            elif info[TYPE] == TYPE_NEW_DATA:  
                agv = ADR_IP_AGV[info[QUI]]
                donnees = {QUI:info[QUI],
                           CONNEXION:info[CONNEXION],
                           AGV:agv,
                           DATA:info[DATA]}
                #connexion[info[QUI]] = info[CONNEXION]
                liste_agv[info[QUI]] = donnees
                
                ma_connexion = liste_agv[info[QUI]][CONNEXION]   #connexion[info[QUI]]
                ma_connexion.send(bytearray([1,2,3]))
                # utilitaires.log_message_info(f'Supervision : {agv} {info[DATA]}')
                logger.info(f"Supervision : {agv} {info[DATA]} in PID {os.getpid()}")
        time.sleep(0.05)
