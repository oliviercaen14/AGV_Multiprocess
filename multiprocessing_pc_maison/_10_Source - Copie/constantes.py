#from dataclasses import dataclass
from enum import Enum
from dataclasses import dataclass

DDE_ACQUIT,ETAT_BUMPER,ETAT_PRESENCE,ETAT_AUTO,ETAT_RADAR,ETAT_AU,NUM_TAG,SUIVI_FIL,CPT_TRAME = ['dde_acquit','etat_bumper','etat_presence','etat_auto','etat_radar','etat_au','num_tag','suivi_fil','cpt_trame'] 


INFO_AGV = {DDE_ACQUIT:0,
            ETAT_BUMPER:0,
            ETAT_PRESENCE:0,
            ETAT_AUTO:0,
            ETAT_RADAR:0,
            ETAT_AU:0,
            NUM_TAG:0,
            SUIVI_FIL:0,
            CPT_TRAME:0
            }
RESTE_TRAME,INFO_TRAME = ['reste_trame','info_trame']
RETOUR_INFO_TRAME = {RESTE_TRAME:[],
                     INFO_TRAME:[]
                    }
MY_TRAME = [16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 53  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 49 , 48 , 49 , 48 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117,
            3,6,8,16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 54  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 53 , 48 , 48 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117,
            4,5,7,16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 55  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 51 , 48 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117,
            2,6,7,16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 56  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 48 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117
            ]

CONNEXION,CON_INFO,QUEUE_RECV,QUEUE_SEND,QUEUE_SUPERVISION,PROCESS,SUPERVISION = ['connexion','con_info','queue_recv','queue_send','queue_supervision','process','supervision'] 

DONNEES = {CONNEXION:None,
           CON_INFO:'',
           QUEUE_RECV:None,
           QUEUE_SEND:None,
           QUEUE_SUPERVISION:None,
           PROCESS:None,
           SUPERVISION:None
            }

TYPE,QUI,DATA,TYPE_NEW_AGV,TYPE_NEW_DATA,TYPE_INFO,AGV = ['type','qui','data','type_new_agv','type_new_data','type_info','agv']

DICO_SUPERVISION = {TYPE:'',
                    QUI:'',
                    CONNEXION:None,
                    DATA:None
                    }
TAG,BUMPER,ZONE,CAPTEUR = ['tag','bumper','zone','capteur']
DICO_MISSION = {TAG:None,
                BUMPER:None,
                ZONE:None,
                CAPTEUR:None
                }

ADR_IP_AGV = {'172.19.171.71':1, # 'AGV_01',
              '172.19.171.72':2, #'AGV_02',
              '172.19.171.73':3, # 'AGV_03',
              '172.19.171.74':4, # 'AGV_04',
              '172.19.171.75':5, # 'AGV_05',
              '172.19.171.76':6, # 'AGV_06',
              '172.19.171.77':7, # 'AGV_07',
              '127.0.0.1':8, # 'AGV_08',
              '172.19.171.79':9, # 'AGV_09',
              '172.19.171.80':10, # 'AGV_10',
              '172.19.171.81':11, # 'AGV_11'
                }

import class_agv

if __name__ == '__main__':
    Agv_1 = class_agv.info_agv()
    Agv_1.num_tag = 12
    Agv_1.num_tag = 1012
    Agv_1.besoin_bumper = [1000,1012,3,1014]
    print(Agv_1.besoin_bumper)
    Agv_1.besoin_bumper = [1000,1012,3,1014]
    
    Animal = Enum('Animal', 'ant bee cat dog')
    print (Animal)
    Animal = 'bee'
    print (Animal)
    