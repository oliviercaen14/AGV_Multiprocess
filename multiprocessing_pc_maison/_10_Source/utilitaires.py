import os
from variables_globales import path_racine

def Get_racine():
    os.chdir(os.path.dirname(__file__) )
    os.chdir('../')
    global path_racine
    path_racine = os.getcwd()
    print(path_racine)
    return path_racine
    
def convert_str_int(value):
    try:  #conversion du numero de tag en Integer
        retour = int(value)
        if retour < 0:
            # my_logger.warning(f' {value} devrait être >= 0')
            retour = -2
    except ValueError:
        # logging.debug(f"Agv = {self.numero} --  anomalie à la lecture du numéro de tag - numéro lu = {numero_tag}")
        retour = '-1'
        # my_logger.warning(f' {value} n''est pas une valeur entiere ... ')
 
    return retour



