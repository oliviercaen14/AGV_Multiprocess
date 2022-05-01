import logging,os
from logging.handlers import TimedRotatingFileHandler
from variables_globales import path_racine

def Get_racine():
    os.chdir(os.path.dirname(__file__) )
    os.chdir('../')
    global path_racine
    path_racine = os.getcwd()
    print(path_racine)
    return path_racine

# second (s)
# minute (m)
# hour (h)
# day (d)
# w0-w6 (weekday, 0=Monday)
# midnight
def setup_logger_old(nom):
    print (f'nom setupp_logger = Serveur_{nom}')
    global path_racine
    path_racine = Get_racine()
    level = logging.DEBUG
    my_logger = logging.getLogger(nom)
    my_logger.setLevel(level)
    log_file = f'{path_racine}/_20_Logs/Serveur_{nom}'
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(filename)-30s:%(lineno)-5d - %(funcName)-22s - %(message)s')
    # ch = logging.FileHandler(log_file)
    
    handler  = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=14)
    handler.suffix = "%Y-%m-%d_%H_%M_%S.log"
    # handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_-\d{2}-\d{2}-\d{2}.log$")
    handler.setLevel(level)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler )

def create_logger():
    import multiprocessing, logging
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    # formatter = logging.Formatter('[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s -  %(processName)-12s - %(filename)-30s:%(lineno)-5d - %(funcName)-22s - %(message)s')
    global path_racine
    path_racine = Get_racine()
    log_file = f'{path_racine}/_20_Logs/Serveur.log'
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    # this bit will make sure you won't have 
    # duplicated messages in the output
    if not len(logger.handlers): 
        logger.addHandler(handler)
    return logger

def getProcessSafeLogger(logPath):
    import multiprocessing, logging
    if multiprocessing.current_process().name == "MainProcess":
        return logging.getLogger(logPath)
    else:
        return multiprocessing.get_logger(logPath) 

# def setup_logger_old():
#     global path_racine
#     path_racine = utilitaires.Get_racine()
#     # real_path = os.path.dirname(__file__)    #parametres du bloc de gestion des logs
#     # logfilename = f'{real_path}/Logs/Serveur.log'
#     # format_logging = '%(asctime)s -- %(levelname)s -- %(message)s'
# #    logging.basicConfig(filename=logfilename,level=logging.DEBUG,format=format_logging)
#     # global  my_logger
    
#     print('passage')
#     level = logging.DEBUG
#     my_logger = None
#     my_logger = logging.getLogger("app")
#     my_logger.setLevel(level)
#     log_file = f'{path_racine}/_20_Logs/Serveur.log'
#     formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(filename)-30s:%(lineno)-5d - %(funcName)-22s - %(message)s')
#     # ch = logging.FileHandler(log_file)
#     ch = TimedRotatingFileHandler(log_file,
#                                        when="m",
#                                        interval=1,
#                                        backupCount=5)
#     #ch = logging.handlers.TimedRotatingFileHandler(log_file, when='D', backupCount=2)
#     ch.setLevel(level)
#     ch.setFormatter(formatter)
#     my_logger.addHandler(ch)
#     # my_logger.info("Setup logger in PID {}".format(os.getpid()))
#     my_logger.info(f"Setup logger in PID {os.getpid()}")


