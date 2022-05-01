import logging,os
def convert_str_int(value):
    try:  #conversion du numero de tag en Integer
        retour = int(value)
        if retour < 0:
            log_message_warning(f' {value} devrait être >= 0')
            retour = -2
    except ValueError:
        # logging.debug(f"Agv = {self.numero} --  anomalie à la lecture du numéro de tag - numéro lu = {numero_tag}")
        retour = '-1'
        log_message_warning(f' {value} n''est pas une valeur entiere ... ')
 
    return retour

def log_message_debug(message):
    logging.debug(message)
    print(message)

def log_message_info(message):
    logging.info(message)
    print(message) 

def log_message_warning(message):
    logging.warning(message)
    print(message) 

def log_message_error(message):
    logging.error(message)
    print(message) 

def log_message_critical(message):
    logging.critical(message)
    print(message) 

def test():
    test1 = [1,2,3]
    test2 = {'Essai': 12}
    return test1,test2


def setup_logger():
    real_path = os.path.dirname(__file__)    #parametres du bloc de gestion des logs
    # logfilename = f'{real_path}/Logs/Serveur.log'
    # format_logging = '%(asctime)s -- %(levelname)s -- %(message)s'
#    logging.basicConfig(filename=logfilename,level=logging.DEBUG,format=format_logging)
    print('passage')
    level = logging.DEBUG
    logger = logging.getLogger("app")
    logger.setLevel(level)
    log_file = f'{real_path}/Serveur.log'
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(filename)-20s:%(lineno)-5d - %(funcName)-22s - %(message)s')
    ch = logging.FileHandler(log_file)
    #ch = logging.handlers.TimedRotatingFileHandler(log_file, when='D', backupCount=2)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    #logger.info("Setup logger in PID {}".format(os.getpid()))
    logger.info(f"Setup logger in PID {os.getpid()}")

setup_logger()