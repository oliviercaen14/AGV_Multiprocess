from constantes import * #DDE_ACQUIT,ETAT_BUMPER,ETAT_PRESENCE,ETAT_AUTO,ETAT_RADAR,ETAT_AU,NUM_TAG,SUIVI_FIL,CPT_TRAME,INFO_AGV,RESTE_TRAME,INFO_TRAME,RETOUR_INFO_TRAME #MY_TRAME
import utilitaires
import os,logfile
my_logger = logfile.create_logger()

#mise en forme des données au format d'une trame compléte = 0x10/0x02/ ..... /0x10/0x03/Crc
def decompose_trame(dico_supervision,fifo):
    table_reception = dico_supervision[DATA]
    nbr_16_list = [idx for idx,e in enumerate(table_reception) if e == 16 ]
    fin_trt = False
    while (len(nbr_16_list) >= 2) and not fin_trt:
        if table_reception[nbr_16_list[0]+1] == 2:
            if table_reception[nbr_16_list[1]+1] == 3:
                if len(table_reception) > nbr_16_list[1]+3:
                    trame_a_traiter = table_reception[nbr_16_list[0]:nbr_16_list[1]+4]
                    gestion_trame(trame_a_traiter,dico_supervision,fifo) # Traitement d'une trame complète
                    for _ in range(nbr_16_list[1]+2):
                        del table_reception[0]
                else:
                    fin_trt = True
            else:
                for _ in range(nbr_16_list[1]):
                        del table_reception[0]
        else:
            for _ in range(nbr_16_list[0]+1):
                del table_reception[0]
        nbr_16_list = [idx for idx,e in enumerate(table_reception) if e == 16 ]
    table_reception.pop()
    return table_reception

#traitement du contenu de chaque trame
def gestion_trame(ma_trame,dico_supervision,fifo):
    trame_agv = ma_trame
    info_agv = INFO_AGV
    if ((trame_agv[0] == 0x10) and (trame_agv[1] == 0x02)):
        if trame_agv[12] == 63: #réponse à la demande d'acquittement du message AGV
            info_agv[DDE_ACQUIT] = 1
            trame_agv.pop(12) #on supprime le mot de demande d'acquitement de la trame pour ne pas avoir à gérer le décalage induit dans le reste de la trame

        info_agv[ETAT_BUMPER] = ((trame_agv[23] - 48) & 4) == 4 
        info_agv[ETAT_PRESENCE] = ((trame_agv[23] - 48) & 1) == 1
        info_agv[CPT_TRAME] = ''.join(chr(c) for c in trame_agv[10:12])
        info_agv[NUM_TAG] = lecture_numero_tag(trame_agv)   
        info_agv[SUIVI_FIL] = lecture_suivi_fil(trame_agv)   
        info_agv[ETAT_AUTO] = lecture_Manu(trame_agv)   
        info_agv[ETAT_RADAR] = lecture_Radar(trame_agv)   
        info_agv[ETAT_AU] = lecture_AU(trame_agv)   
        dico_supervision[DATA]=info_agv
        fifo.put(dico_supervision) 
        ligne_ascii = '10 02 '
        for decimal in ma_trame:
            ligne_ascii += chr(decimal) if decimal >= 48 else str(decimal)
        # logging.debug(f"Agv = {self.numero} --  {','.join(str(e) for e in ma_trame)}")
        # logging.info(f" Agv = {self.numero} -- numero trame = {num_trame_agv} , numero tag = {self.numero_tag_int} , numero tag Annexe = {self.numero_tag_int_annexe} , valeur 23 = {valeur_23} Bumper = {val_Bumper} nombre de fois = {self.bumper_nombre_fois}")
        # utilitaires.log_message_info (ligne_ascii)
        my_logger.info(f'{ligne_ascii} in PID {os.getpid()}')
        # print(info_agv)

def position_chr(value,cherche,index):
    try:
        position = value.index(cherche,index)
    except ValueError:
        return -1
    return position
    
def lecture_numero_tag(trame_agv):
    pos_p =  position_chr(trame_agv,ord('p'),30)  # trame_agv.index(ord('p'),30)
    pos_Y = position_chr(trame_agv,ord('Y'),30)   #trame_agv.index(ord('Y'),pos_p)
    if pos_p > 0 and pos_Y > 0 and pos_Y > pos_p:
        numero_tag_list = trame_agv[pos_p+1:pos_Y]
        numero_tag = ''.join(chr(c) for c in numero_tag_list)
    else:
        #utilitaires.log_message_info(f"Agv = {self.numero} --  identifiant de tag non trouvé")
        numero_tag = '?'

    try:  #conversion du numero de tag en Integer
        num_tag_int = int(numero_tag)
    except ValueError:
        # logging.debug(f"Agv = {self.numero} --  anomalie à la lecture du numéro de tag - numéro lu = {numero_tag}")
        numero_tag = '?'
    return numero_tag

def lecture_Manu(trame_agv):
    try:
        pos_p = trame_agv.index(ord('p'),30)
    except ValueError:
        return '?'
    return '0' if chr(trame_agv[pos_p-1]) == 'R'  else '1'

def lecture_Radar(trame_agv):
    try:
        pos_E = trame_agv.index(ord('E'),30)
    except ValueError:
        return '?'
    return '0' if chr(trame_agv[pos_E+1]) == '4'  else '1'

def lecture_AU(trame_agv):
    try:
        pos_E = trame_agv.index(ord('E'),30)
    except ValueError:
        return '?'
    return '0' if chr(trame_agv[pos_E+1]) == '3'  else '1'



def lecture_suivi_fil(trame_agv):
    try:
        pos_Y = trame_agv.index(ord('Y'),30)
    except ValueError:
        return '?'
    return chr(trame_agv[pos_Y+1]) if pos_Y > 0 else '?'


# if __name__ == '__main__':
#     decompose_trame(MY_TRAME,None)
#     print(ord('R'))