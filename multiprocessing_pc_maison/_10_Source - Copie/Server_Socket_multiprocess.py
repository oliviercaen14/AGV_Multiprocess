import time,os
import logging
import socket
from multiprocessing import Process, Queue
from constantes import *
# from variables_globales import path_racine,logger
import variables_globales as var_glob
from Gestion_Process import f_process
import traite_trame,logfile

import fichier_excel
 
# lineno = lambda: inspect.currentframe().f_back.f_lineno
# logfile.setup_logger(__name__) 
# my_logger = logging.getLogger(__name__)
my_logger = logfile.create_logger()

def f_agv(donnees):
    adr_ip,port =  donnees[CON_INFO] 
    my_logger.info(f"entree dans le process : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")
    my_logger.info(f"donnees[CON_INFO] in PID {os.getpid()}")
    tableau_donnees = []
    dico_supervision = DICO_SUPERVISION
    dico_supervision[TYPE]=TYPE_NEW_AGV
    dico_supervision[QUI]=donnees[CON_INFO][0]
    dico_supervision[CONNEXION]= donnees[CONNEXION]
    donnees[QUEUE_SUPERVISION].put(dico_supervision)
    fin = False
    while not fin:

        try:
            data = donnees[CONNEXION].recv(1024)
#            dico_supervision = DICO_SUPERVISION
            dico_supervision[TYPE]=TYPE_NEW_DATA
#            dico_supervision[QUI]=donnees[CON_INFO][0]
#            dico_supervision[CONNEXION]= donnees[CONNEXION]
            tableau_donnees.extend(data)
            dico_supervision[DATA]=tableau_donnees
            tableau_donnees = traite_trame.decompose_trame(dico_supervision,donnees[QUEUE_SUPERVISION])
            time.sleep(0.05)
        except socket.error as e: 
            my_logger.info(f"erreur de socket : {e} in PID {os.getpid()}")
            data = None
        if not data:
            #For laddr use mySocket.getsockname() and for raddr use mySocket.getpeername()
            my_logger.info(f"suppression de la connexion : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")
            donnees[CONNEXION].close()
            fin = True
    
    my_logger.info(f"sortie du process : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")


def main():
    my_logger.info(f'démarrage application in PID {os.getpid()}')
    print('suite')
    # Créer un socket TCP / IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Liez le socket au port
    server.bind(('', 11000))
    # Écoutez les connexions entrantes
    server.listen(5)
    # liste des connexions
    msg = {}
    queue_supervision = Queue()
    supervision = Process(target = f_process, args = (queue_supervision,))
    supervision.start()
    while True:
        # Attendez qu'au moins une des sockets soit prête pour le traitement
        # Un socket serveur "readable" est prêt à accepter une connexion
        # utilitaires.log_message_info('Attente de connexion')  
        my_logger.info(f'Attente de connexion in PID {os.getpid()}')
        connection, client_address = server.accept()
        # utilitaires.log_message_info(f'connexion  {client_address} accepté')  
        my_logger.info(f'connexion  {client_address} accepté in PID {os.getpid()}')
        # Donner à la connexion une file d'attente pour les données que nous voulons envoyer
        msg[connection] = DONNEES
        msg[connection][CONNEXION] = connection
        msg[connection][CON_INFO] = client_address
        msg[connection][QUEUE_RECV] = Queue()
        msg[connection][QUEUE_SEND] = Queue()
        msg[connection][QUEUE_SUPERVISION] = queue_supervision
        msg[connection][PROCESS] = Process(target = f_agv, args = (msg[connection],))
        msg[connection][PROCESS].start()
 

       

                
if __name__ == '__main__':
    my_logger.info(f'démarrage __main__ in PID {os.getpid()}')
    fichier_excel.gest_fichier_excel()
    main()
