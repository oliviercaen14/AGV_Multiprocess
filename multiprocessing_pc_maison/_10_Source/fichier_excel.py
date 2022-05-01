import openpyxl
from dataclasses import dataclass
import time
from variables_globales import path_racine
import logging
import utilitaires ,log_multi_file
import os

# logfile.setup_logger(__name__) 
# my_logger = logging.getLogger(__name__)
# my_logger = logfile.create_logger()
my_logger = None

CAPTEURS = [None,'V1','V2-3','V4','V5','R1','R2_3','R4','R5','Pose_Essieu','Pose_Pont','Prise_Luge']

# @dataclass
# class Zone:
#     zone_debut: int = 0
#     zone_fin: int = 0
#     zone_priorite:int = 0   
#     tags:list = []



@dataclass
class Tag:
    num_tag : int = 0
    num_tag_str: str = ''
    etat_Bumper: bool = False
    capteur: str = ''
    zone_fin: str = ''
    priorite: str = '0'
    type_tag: str = ''

   
# def test(liste_tags):
#     while True:
#         print('----------passage-------------')
#         for key,values in liste_tags.items():
#         # for values in liste_tags.items():
#             for index_row,mon_tag in enumerate(values):
#                 my_logger.info(f' Onglet = {mon_tag.type_tag} Ligne = {index_row}  Tag = {mon_tag.num_tag} Bumper = {mon_tag.etat_Bumper} capteur= {mon_tag.capteur} Zone Fin = {mon_tag.zone_fin} priorite = {mon_tag.priorite}  in PID {os.getpid()}')
#         time.sleep(1)  


def split_row(mon_tag,row,onglet):
    colonne = [cell.value for cell in row]
    mon_tag.num_tag = utilitaires.convert_str_int(colonne[0])
    mon_tag.num_tag_str = str(mon_tag.num_tag)
    mon_tag.etat_Bumper = colonne[1] != None
    if colonne[2] not in CAPTEURS:
        my_logger.warning (f'---------------------- erreurs ------------ {colonne[0]} {colonne[2]} in PID {os.getpid()}')
        colonne[2] = '?'
    else:
        mon_tag.capteur = colonne[2] if colonne[2] != None else ''     
    
    mon_tag.zone_fin = utilitaires.convert_str_int(colonne[3]) if colonne[3] != None else 0 
    mon_tag.priorite = utilitaires.convert_str_int(colonne[4]) if colonne[4] != None else 0 
    mon_tag.type_tag = onglet
    return mon_tag


def cherche_zone(dico_num_tags,tag_debut,tag_fin,ligne):
    liste_tags = dico_num_tags[ligne]
    liste_retour = []
    changemeny_ligne = False
    index_debut = liste_tags.index(tag_debut) +1
    try:
        index_fin = liste_tags.index(tag_fin)
    except Exception:
        print(Exception)
        index_fin = dico_num_tags['Tag_Commun'].index(tag_fin)
        changemeny_ligne = True
             
    if index_fin > index_debut and not changemeny_ligne :
        liste_retour.extend(liste_tags[index] for index in range(index_debut , index_fin) if liste_tags[index] > 699)
    else:
        liste_retour.extend(valeur for valeur in liste_tags[index_debut:]  if valeur > 699)
        liste_tags = dico_num_tags['Tag_Commun']
        liste_retour.extend(valeur for valeur in liste_tags[:index_fin]  if valeur > 699)
        
        
        # mon_range = range(index_debut  , index_fin)
        # for index in mon_range:
        #     valeur = liste_tags[index]
        #     if valeur > 699:
        #         liste_retour.append(valeur)
    return liste_retour

def Get_racine():
    os.chdir(os.path.dirname(__file__) )
    os.chdir('../')
    global path_racine
    path_racine = os.getcwd()
    print(path_racine)
    return path_racine

def lecture_ficier(liste_tags):
    path_racine = Get_racine()
    filename = os.path.join(path_racine,'_15_donnees','config_tag.xlsx')
    workbook = openpyxl.load_workbook(filename, read_only = False, data_only = True) 
    liste_sheet = [sheet.title for sheet in workbook]
    liste_fenetre = ['Tag_Commun','Tag_Essieu','Tag_Pont']  
    list_num_tags = [] #  
    dico_num_tags = {'Tag_Commun':[],'Tag_Essieu':[],'Tag_Pont':[]}
    dico_zones = {}
    dico_zone_data = {'Occupe':'','Zone':[],'Priorite':'','zone_fin':0,'Ligne':'Tag_Commun'}
    for element in liste_fenetre:
        if element in liste_sheet:
            sheet = workbook[element]
            liste_tags[element]=[]
            my_logger.info (f'Traitement Onglet : {element} ------- in PID {os.getpid()}')
            for row in sheet.iter_rows(min_row = 2, max_row = 100, min_col = 1, max_col = 5):
                if row[0].value is None:
                    break
                montag = Tag()
                montag = split_row(montag,row,element)
                liste_tags[element].append(montag)    
                if montag.zone_fin != 0:
                    dico_zones[montag.num_tag] = dict(dico_zone_data) 
                    dico_zones[montag.num_tag]['Priorite'] = montag.priorite if montag.priorite != 0 else 0  
                    dico_zones[montag.num_tag]['zone_fin'] = montag.zone_fin   
                    dico_zones[montag.num_tag]['Ligne'] = element 
                list_num_tags.append(montag.num_tag)    
                dico_num_tags[element].append(montag.num_tag)
                montag = None
                # ligne = row[0].row
        else: my_logger.warning (f'Onglet {element} manquant in PID {os.getpid()}')
    for cle, valeur in dico_zones.items():
        # dico_zones[cle]['Zone'] = cherche_zone(list_num_tags,cle,valeur['zone_fin'],valeur['zone_fin']    )
        dico_zones[cle]['Zone'] = cherche_zone(dico_num_tags,cle,valeur['zone_fin'],valeur['Ligne']    )
    return liste_tags, list_num_tags,dico_zones,dico_num_tags
    
def gest_fichier_excel(queue_log):
    global my_logger
    log_multi_file.worker_configurer(queue_log)
    my_logger = logging.getLogger('fichier_excel')
    my_logger.info (f'Gestion fichier Excel ------- in PID {os.getpid()}')
  

    # logfilename = f'{real_path}/Logs/Serveur.log'
    # format_logging = '%(asctime)s -- %(levelname)s -- %(message)s'
    # logging.basicConfig(filename=logfilename,level=logging.DEBUG,format=format_logging)
    
    liste_tags = {}
    list_num_tags = []
    liste_tags,list_num_tags,dico_zones,dico_num_tags = lecture_ficier(liste_tags)    
    # for key,values in liste_tags.items():
    # # for values in liste_tags.items():
    #     for index_row,mon_tag in enumerate(values):
    #         my_logger.info(f' Onglet = {mon_tag.type_tag} Ligne = {index_row}  Tag = {mon_tag.num_tag} Bumper = {mon_tag.etat_Bumper} capteur= {mon_tag.capteur} Zone Fin = {mon_tag.zone_fin} priorite = {mon_tag.priorite}  in PID {os.getpid()}')
    # for element in list_num_tags:
    #      my_logger.info(f'Numéro de tag =  {element}  in PID {os.getpid()}') 
    # print(f'dico_zones = {dico_zones} ' )
    # print(f'list_num_tags = {list_num_tags}')
    # print(f'dico_num_tags = {dico_num_tags}')
    
 