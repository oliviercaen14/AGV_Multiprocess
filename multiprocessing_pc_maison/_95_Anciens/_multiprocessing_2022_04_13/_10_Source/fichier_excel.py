import openpyxl
from dataclasses import dataclass
import time
#from variables_globales import liste_sheet,liste_tags
from multiprocessing import Process, Manager
import logging
import utilitaires 
import os

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

   
def test(liste_tags):
    while True:
        print('----------passage-------------')
        for key,values in liste_tags.items():
        # for values in liste_tags.items():
            for index_row,mon_tag in enumerate(values):
                utilitaires.log_message_info(f' Onglet = {mon_tag.type_tag} Ligne = {index_row}  Tag = {mon_tag.num_tag} Bumper = {mon_tag.etat_Bumper} capteur= {mon_tag.capteur} Zone Fin = {mon_tag.zone_fin} priorite = {mon_tag.priorite} ')
        time.sleep(1)  


def split_row(mon_tag,row,onglet):
    colonne = [cell.value for cell in row]
    mon_tag.num_tag = utilitaires.convert_str_int(colonne[0])
    mon_tag.num_tag_str = str(mon_tag.num_tag)
    mon_tag.etat_Bumper = colonne[1] != None
    if colonne[2] not in CAPTEURS:
        utilitaires.log_message_warning (f'---------------------- erreurs ------------ {colonne[0]} {colonne[2]}')
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

def lecture_ficier(liste_tags):
    workbook = openpyxl.load_workbook('config_tag.xlsx', read_only = False, data_only = True) 
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
            utilitaires.log_message_info (f'Traitement Onglet : {element} -------')
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
        else: utilitaires.log_message_warning (f'Onglet {element} manquant')
    for cle, valeur in dico_zones.items():
        # dico_zones[cle]['Zone'] = cherche_zone(list_num_tags,cle,valeur['zone_fin'],valeur['zone_fin']    )
        dico_zones[cle]['Zone'] = cherche_zone(dico_num_tags,cle,valeur['zone_fin'],valeur['Ligne']    )
    return liste_tags, list_num_tags,dico_zones,dico_num_tags
    
def main():
    liste_tags = {}
    list_num_tags = []
    liste_tags,list_num_tags,dico_zones,dico_num_tags = lecture_ficier(liste_tags)    
    for key,values in liste_tags.items():
    # for values in liste_tags.items():
        for index_row,mon_tag in enumerate(values):
            utilitaires.log_message_info(f' Onglet = {mon_tag.type_tag} Ligne = {index_row}  Tag = {mon_tag.num_tag} Bumper = {mon_tag.etat_Bumper} capteur= {mon_tag.capteur} Zone Fin = {mon_tag.zone_fin} priorite = {mon_tag.priorite} ')
    for element in list_num_tags:
         utilitaires.log_message_info(f'Numéro de tag =  {element} ') 
    print(dico_zones)
    print(list_num_tags)
    print(dico_num_tags)
    
    
if __name__ == '__main__':
#    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    #directory du projet
    real_path = os.path.dirname(__file__)    #parametres du bloc de gestion des logs
    logfilename = f'{real_path}/Logs/Serveur.log'
    format_logging = '%(asctime)s -- %(levelname)s -- %(message)s'
    logging.basicConfig(filename=logfilename,level=logging.DEBUG,format=format_logging)


    utilitaires.log_message_info('démarrage application')   
    main()
    utilitaires.log_message_info('sortie de l''application')   
    # with Manager() as manager:
    #     liste_tags = manager.dict()
    #     mon_test = Process(target = test, args = (liste_tags,))
    #     mon_test.start()
    #     time.sleep(2)
    #     main(liste_tags)
    # for key,values in liste_tags.items():
    # # for values in liste_tags.items():
    #     for index_row,mon_tag in enumerate(values):
    #         print(f' Onglet = {mon_tag.type_tag} Ligne = {index_row}  Tag = {mon_tag.num_tag} Bumper = {mon_tag.etat_Bumper} capteur= {mon_tag.capteur} Zone Fin = {mon_tag.zone_fin} priorite = {mon_tag.priorite} ')
