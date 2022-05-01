import time,os
import logging
from logging.handlers import TimedRotatingFileHandler
import socket
from multiprocessing import Process, Queue
from constantes import *
from variables_globales import path_racine

from Gestion_Process import f_process
import traite_trame
import log_multi_file
import gzip


 
# lineno = lambda: inspect.currentframe().f_back.f_lineno
# logfile.setup_logger(__name__) 
# my_logger = logging.getLogger(__name__)
# my_logger = logfile.create_logger()

def f_agv(donnees,queue_log):
    log_multi_file.worker_configurer(queue_log)
    my_logger = logging.getLogger('AGV_08')
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
            dico_supervision[TYPE]=TYPE_NEW_DATA
            tableau_donnees.extend(data)
            dico_supervision[DATA]=tableau_donnees
            tableau_donnees = traite_trame.decompose_trame(dico_supervision,donnees[QUEUE_SUPERVISION],queue_log)
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


def main(queue_log):
    global_logger = logging.getLogger('Main_1')
    # my_logger = logging.getLogger('Main')
    global_logger.info(f'démarrage application in PID {os.getpid()}')
    queue_supervision = Queue()
    supervision = Process(target = f_process, args = (queue_supervision,queue_log, ))
    supervision.start()
    print('suite')
    # Créer un socket TCP / IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Liez le socket au port
    server.bind(('', 11000))
    # Écoutez les connexions entrantes
    server.listen(5)
    # liste des connexions
    msg = {}
    while True:
        # Attendez qu'au moins une des sockets soit prête pour le traitement
        # Un socket serveur "readable" est prêt à accepter une connexion
        # utilitaires.log_message_info('Attente de connexion')  
        global_logger.info(f'Attente de connexion in PID {os.getpid()}')
        connection, client_address = server.accept()
        # utilitaires.log_message_info(f'connexion  {client_address} accepté')  
        global_logger.info(f'connexion  {client_address} accepté in PID {os.getpid()}')
        # Donner à la connexion une file d'attente pour les données que nous voulons envoyer
        msg[connection] = DONNEES
        msg[connection][CONNEXION] = connection
        msg[connection][CON_INFO] = client_address
        msg[connection][QUEUE_RECV] = Queue()
        msg[connection][QUEUE_SEND] = Queue()
        msg[connection][QUEUE_SUPERVISION] = queue_supervision
        msg[connection][PROCESS] = Process(target = f_agv, args = (msg[connection],queue_log,))
        msg[connection][PROCESS].start()
 
def Get_racine():
    os.chdir(os.path.dirname(__file__) )
    os.chdir('../')
    global path_racine
    path_racine = os.getcwd()
    print(path_racine)
    return path_racine

# https://stackoverflow.com/questions/338450/timedrotatingfilehandler-changing-file-name
def my_namer(default_name):
    # This will be called when doing the log rotation
    # default_name is the default filename that would be assigned, e.g. Rotate_Test.txt.YYYY-MM-DD
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}_{date}.{ext}"

#https://medium.com/@rahulraghu94/overriding-pythons-timedrotatingfilehandler-to-compress-your-log-files-iot-c766a4ace240
#https://he-arc.github.io/livre-python/super/index.html
class Ma_TimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename="", when="midnight", interval=1,
                 backup_count=14, compression = None):
        super().__init__(
            filename=filename,
            when=when,
            interval=int(interval),
            backupCount=int(backup_count)
        )
        self.compression = compression
    def doRollover(self):
        import shutil
        super().doRollover()
        if self.compression is None : return
        log_dir = os.path.dirname(self.baseFilename)
        print(log_dir)
        print(os.path.basename(os.path.splitext(self.baseFilename)[0]))
        to_compress = [
            os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.startswith(
                f'{os.path.basename(os.path.splitext(self.baseFilename)[0])}_'
            ) and f.endswith((".log"))
        ]
        if self.compression == 'zip':
            self.compress_zip(to_compress)
        elif self.compression == 'gz':
            self.compress_gz(to_compress)
        
    def compress_gz(self,to_compress):
        import shutil
        print(to_compress)
        for f in to_compress:
            if os.path.exists(f):
                with open(f, "rb") as _old, gzip.open(f'{f}.gz', "wb") as _new:    
                    shutil.copyfileobj(_old, _new)
                os.remove(f)

    def compress_zip(self,to_compress):
        import zipfile
        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED

        modes = { zipfile.ZIP_DEFLATED: 'deflated',
                zipfile.ZIP_STORED:   'stored',
                }
        print(to_compress)
        # os.path.splitext(os.path.basename(onePath))[0]

        for f in to_compress:
            if os.path.exists(f): #open(f, "rb") as _old,
                with  zipfile.ZipFile(f'{f}.zip', mode='w') as new:
                    # my_arcname = os.path.splitext(os.path.basename(f))[0]
                    my_arcname = os.path.basename(f)
                    new.write(filename = f,arcname  = my_arcname, compress_type=compression)
                #gzip.open(f'{f}.gz', "wb") as _new:    
                    # shutil.copyfileobj(_old, _new)
                os.remove(f)


def listener_configurer():
    root = logging.getLogger()
    global path_racine
    path_racine = Get_racine()
    log_file = f'{path_racine}/_20_Logs/Serveur_Agv.log'
    print(f'listener config - fichier = {log_file}')
    # h = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=14)
    # h = Ma_TimedRotatingFileHandler(log_file, when='midnight', backupCount=14)
    h = Ma_TimedRotatingFileHandler(log_file,when='midnight', interval=1, backup_count=14 , compression = 'zip')
    h.namer = my_namer
    # h.suffix = "%Y-%m-%d"
    h.suffix = "%Y-%m-%d_%H_%M_%S"
    # f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    f = logging.Formatter('%(asctime)s - %(levelname)-8s -  %(processName)-12s %(name)s - %(filename)-30s:%(lineno)-5d - %(funcName)-22s - %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
def listener_process(queue, configurer):
    configurer()
    old_record_message = ''
    while True:
        try:
            # print ('listener : attente info')
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                # print ('listener : sortie')
                break
            if record.message != old_record_message:
                # print (f'listener : {record.name}  {record.lineno} {record.funcName} {record.message} ')

                logger = logging.getLogger(record.name)
                # logger.propagate = False
                logger.handle(record)  # No level or filter logic applied - just do it!
                old_record_message = str(record.message)
                # print(f' id de variable = {map( id, [ record.message,old_record_message] )}')
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
       

                
if __name__ == '__main__':
    queue = Queue(-1)
    listener = Process(target=listener_process,args=(queue, listener_configurer))
    listener.start()
    log_multi_file.worker_configurer(queue)
    my_main_logger = logging.getLogger('Main')
    # traite_trame.gest_log(queue)
    
    my_main_logger.info(f'démarrage __main__ in PID {os.getpid()}')
    main(queue)
    queue.put_nowait(None)
    listener.join()
    

