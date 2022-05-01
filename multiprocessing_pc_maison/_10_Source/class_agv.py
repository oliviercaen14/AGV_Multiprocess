import logging,os
from variables_globales import global_logger
import log_multi_file

# my_logger = logfile.create_logger()
# my_logger = logging.getLogger('Main')
NBR_ESP = 100
def espaces (nombre : int = NBR_ESP):
    return ' ' * nombre
# my_logger.info(f"Supervision : agv = {agv} data = {decompose_dico(133,info[DATA])}in PID {os.getpid()}")
class info_agv:
# dde_acquit : 0 
# etat_bumper : False 
# etat_presence : True 
# etat_auto : 1 
# etat_radar : 1 
# etat_au : 1 
# num_tag : 1031 
# suivi_fil : 1 
# cpt_trame : 56 
# in PID 15388

    def __init__(self,num_agv,adresse_ip,connexion,queue_log):
        self.adresse_ip = adresse_ip
        self.connexion = connexion
        self.num_agv = num_agv
        self.num_agv_txt = f'AGV_{str(num_agv).zfill(2)}'
        # self.my_logger =  logging.getLogger(self.num_agv_txt)
        global global_logger
        # log_multi_file.worker_configurer(queue_log)
        global_logger = logging.getLogger(self.num_agv_txt)
        #logging.getLogger(self.num_agv_txt)
        # global_logger.propagate = False
        
        self.liste_texte = []
        self.dde_acquit:int = 0
        self.etat_bumper:int = 0
        self.etat_presence:int = 0
        self.etat_auto:int = 0
        self.etat_radar:int = 0
        self.etat_au:int = 0
        self._num_tag:int = 0
        self._num_tag_1000:int = 0
        self.suivi_fil:int = 0
        self.cpt_trame:int = 0
        self._besoin_bumper:list = []
        self._bumper_recu:int = 0
        self.dico_fonction = {
                                'dde_acquit':self.dde_acquit_setter,
                                'etat_bumper':self.etat_bumper_setter,
                                'etat_presence':self.etat_presence_setter,
                                'etat_auto':self.etat_auto_setter,
                                'etat_radar':self.etat_radar_setter,
                                'etat_au':self.etat_au_setter,
                                'num_tag':self.num_tag_setter,
                                'suivi_fil':self.suivi_fil_setter,
                                'cpt_trame':self.cpt_trame_setter
                                }
    
    @property
    def besoin_bumper(self):
        return self._besoin_bumper

    @besoin_bumper.setter
    def besoin_bumper(self, values):
        self._besoin_bumper = [element for element in values if element >= 1000]


    @property
    def num_tag_1000(self):
        return self._num_tag_1000

    @property
    def num_tag(self):
        return self._num_tag

    def dde_acquit_setter(self, value): 
        self.liste_texte.append(f'{espaces()}dde_acquit = {value}') if value == self.dde_acquit else  self.liste_texte.append(f'{espaces()}dde_acquit = {value} ancienne valeur = {self.dde_acquit}') 
        self.dde_acquit = value
        # print (f'dde_acquit = {value}  ')
        
    def etat_bumper_setter(self, value):    
        self.liste_texte.append(f'{espaces()}etat_bumper = {value}') if value == self.etat_bumper else  self.liste_texte.append(f'{espaces()}etat_bumper = {value} ancienne valeur = {self.etat_bumper}') 
        self.etat_bumper = value        
        # print (f'etat_bumper_setter = {value}  ')
        
    def etat_presence_setter(self, value):    
        self.liste_texte.append(f'{espaces()}etat_presence = {value}') if value == self.etat_presence else  self.liste_texte.append(f'{espaces()}etat_presence = {value} ancienne valeur = {self.etat_presence}') 
        self.etat_presence = value        
        # print (f'etat_presence_setter = {value}  ')
        
    def etat_auto_setter(self, value):    
        self.liste_texte.append(f'{espaces()}etat_auto = {value}') if value == self.etat_auto else  self.liste_texte.append(f'{espaces()}etat_auto = {value} ancienne valeur = {self.etat_auto}') 
        self.etat_auto = value        
        # print (f'etat_auto_setter = {value}  ')
        
    def etat_radar_setter(self, value):    
        self.liste_texte.append(f'{espaces()}etat_radar = {value}') if value == self.etat_radar else  self.liste_texte.append(f'{espaces()}etat_radar = {value} ancienne valeur = {self.etat_radar}') 
        self.etat_radar = value        
        # print (f'etat_radar_setter = {value}  ')
        
    def etat_au_setter(self, value):    
        self.liste_texte.append(f'{espaces()}etat_au = {value}') if value == self.etat_au else  self.liste_texte.append(f'{espaces()}etat_au = {value} ancienne valeur = {self.etat_au}') 
        self.etat_au = value        
        # print (f'etat_au_setter = {value}  ')
        


    # @num_tag.setter
    def num_tag_setter(self, value):
        self.num_tag_str = value
        value = int(value)
        self.liste_texte.append(f'{espaces()}num_tag = {value}') if value == self.num_tag else  self.liste_texte.append(f'{espaces()}num_tag = {value} ancienne valeur = {self.num_tag}') 
        # print(f'num_tag = {value} ')
        if value >= 1000:
            #raise ValueError("Temperature below -273 is not possible")
            self._num_tag_1000 = value
        self._num_tag = value
        
    
    def suivi_fil_setter(self, value):    
        self.liste_texte.append(f'{espaces()}suivi_fil = {value}') if value == self.suivi_fil else  self.liste_texte.append(f'{espaces()}suivi_fil = {value} ancienne valeur = {self.suivi_fil}') 
        self.suivi_fil = value        
        # print (f'suivi_fil_setter = {value}  ')
        
    def cpt_trame_setter(self, value):    
        self.liste_texte.append(f'{espaces()}cpt_trame = {value}') if value == self.cpt_trame else  self.liste_texte.append(f'{espaces()}cpt_trame = {value} ancienne valeur = {self.cpt_trame}') 
        self.cpt_trame = value        
        # print (f'cpt_trame_setter = {value}  ')
        
        
    def mise_a_jour(self,values):
        self.liste_texte = [f'\n{espaces(NBR_ESP - 5)}AGV = {self.num_agv_txt}']
        for key, element in values.items():
            if f := self.dico_fonction.get(key):
                f(element)
            else : global_logger.warning(f"element de donnée incompatible : cle = {key} valeur = {element} in PID {os.getpid()}")
        self.liste_texte.append(espaces())
        texte = '\n'.join(self.liste_texte)        
        global_logger.info(f"{texte}in PID {os.getpid()}")
        # print(texte)
        try:
            self.connexion.send(bytearray(self.num_tag_str,'utf-8'))
        except Exception as e:
            global_logger.warning(f"Echec de l'envoi de données = {self.num_tag_str} in PID {os.getpid()}")
            print(f"Echec de l'envoi de données = {self.num_tag_str} in PID {os.getpid()}")
            

    