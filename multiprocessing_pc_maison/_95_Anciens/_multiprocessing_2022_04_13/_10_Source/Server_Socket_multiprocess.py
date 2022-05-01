import time,os
import logging
import socket
from multiprocessing import Process, Queue
from constantes import *
from Gestion_Process import f_process
import traite_trame
import utilitaires
import inspect
 
lineno = lambda: inspect.currentframe().f_back.f_lineno

def f_supervision(fifo_in):
    logger = logging.getLogger("sup") 
    print('------------------')
    test = lineno()
    print (test) 
    # print(lineno(), 'foo')
    print('-------------------')
    #connexion = {}
    liste_agv = {}
    fin = False
    # utilitaires.log_message_info ('demarrage supervision')
    logger.info(f'demarrage supervision in PID {os.getpid()}')
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
                
                # ma_connexion = liste_agv[info[QUI]][CONNEXION]   #connexion[info[QUI]]
                # ma_connexion.send(bytearray([1,2,3]))
                # utilitaires.log_message_info(f'Supervision : {agv} {info[DATA]}')
                logger.info(f"Supervision : {agv} {info[DATA]} in PID {os.getpid()}")
        time.sleep(0.001)


def f_agv(donnees):
    logger = logging.getLogger("app") 
    adr_ip,port =  donnees[CON_INFO] 
    # utilitaires.log_message_info (f'entree dans le process : adr_ip = {adr_ip}  port = {port}')
    logger.info(f"entree dans le process : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")
    # utilitaires.log_message_info(donnees[CON_INFO])
    logger.info(f"donnees[CON_INFO] in PID {os.getpid()}")
    tableau_donnees = []
    fin = False
    while not fin:

        try:
            data = donnees[CONNEXION].recv(1024)
            dico_supervision = DICO_SUPERVISION
            dico_supervision[TYPE]=TYPE_NEW_DATA
            dico_supervision[QUI]=donnees[CON_INFO][0]
            dico_supervision[CONNEXION]= donnees[CONNEXION]
            tableau_donnees.extend(data)
            dico_supervision[DATA]=tableau_donnees
            tableau_donnees = traite_trame.decompose_trame(dico_supervision,donnees[QUEUE_SUPERVISION])
            time.sleep(0.05)
        except socket.error as e: 
            # utilitaires.log_message_info (f'erreur de socket : {e}')
            logger.info(f"erreur de socket : {e} in PID {os.getpid()}")
            data = None
        # if data:
        #     pass #print (data)
        # else:
        if not data:
            #For laddr use mySocket.getsockname() and for raddr use mySocket.getpeername()
            # utilitaires.log_message_info(f'suppression de la connexion : adr_ip = {adr_ip}  port = {port}')
            logger.info(f"suppression de la connexion : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")
            donnees[CONNEXION].close()
            fin = True
    
    # utilitaires.log_message_info(f'sortie du process : adr_ip = {adr_ip}  port = {port}')
    logger.info(f"sortie du process : adr_ip = {adr_ip}  port = {port} in PID {os.getpid()}")


def main():
    logger = logging.getLogger("app") 
    # real_path = os.path.dirname(__file__)    #parametres du bloc de gestion des logs
    # logfilename = f'{real_path}/Logs/Serveur.log'
    # format_logging = '%(asctime)s -- %(levelname)s -- %(message)s'
    # logging.basicConfig(filename=logfilename,level=logging.DEBUG,format=format_logging)
    print (logging)
    # utilitaires.log_message_info('démarrage application')  
    logger.info(f'démarrage application in PID {os.getpid()}')
    # Créer un socket TCP / IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Liez le socket au port
    server.bind(('', 11000))
    # server.bind(('localhost', 11000))
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
        logger.info(f"'Attente de connexion in PID {os.getpid()}")
        connection, client_address = server.accept()
        # utilitaires.log_message_info(f'connexion  {client_address} accepté')  
        logger.info(f'connexion  {client_address} accepté in PID {os.getpid()}')
        # Donner à la connexion une file d'attente pour les données que nous voulons envoyer
        msg[connection] = DONNEES
        msg[connection][CONNEXION] = connection
        msg[connection][CON_INFO] = client_address
        msg[connection][QUEUE_RECV] = Queue()
        msg[connection][QUEUE_SEND] = Queue()
        msg[connection][QUEUE_SUPERVISION] = queue_supervision
        msg[connection][PROCESS] = Process(target = f_agv, args = (msg[connection],))
        msg[connection][PROCESS].start()
 
       
utilitaires.setup_logger()  
                
if __name__ == '__main__':
    # logger = logging.getLogger("app") 
    main()
    # logger.info(f'Sortie de l''application in PID {os.getpid()}')
