import select
import time
import socket
from multiprocessing import Process, Queue

CONNEXION,CON_INFO,QUEUE_RECV,QUEUE_SEND,PROCESS = ['connexion','con_info','queue_recv','queu_send','process'] 

DONNEES = {CON_INFO :'',
           QUEUE_RECV:None,
           QUEUE_SEND:None,
           PROCESS:None
            }

def f_agv(donnees):
    adr_ip,port =  donnees[CON_INFO] 
    print (f'entree dans le process : adr_ip = {adr_ip}  port = {port}')
    print(donnees[CON_INFO])
    fin = False
    info = ''
    
    while not fin:
        while not donnees[QUEUE_RECV].empty() :
            info = donnees[QUEUE_RECV].get()
            if info == 'FIN':
                fin = True
            else:
                print (f'donnees recues : {info}')
                donnees[QUEUE_SEND].put(info)
        time.sleep(0.5)
    print(f'sortie du process : adr_ip = {adr_ip}  port = {port}')

def main():
    # Créer un socket TCP / IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    # Liez le socket au port
    server.bind(('localhost', 11000))
    # Écoutez les connexions entrantes
    server.listen(5)
    # Sockets à partir desquels nous nous attendons à lire
    inputs = [server]
    # Sockets dans lesquels nous nous attendons à écrire
    outputs = []
    # Files d'attente de messages sortants
    msg = {}
    while inputs:
        # Attendez qu'au moins une des sockets soit prête pour le traitement
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
    # Gérer les entrées
        for s in readable:
            if s is server:
                # Un socket serveur "readable" est prêt à accepter une connexion
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                # Donner à la connexion une file d'attente pour les données que nous voulons envoyer
                msg[connection] = DONNEES
                msg[connection][CON_INFO] = client_address
                msg[connection][QUEUE_RECV] = Queue()
                msg[connection][QUEUE_SEND] = Queue()
                msg[connection][PROCESS] = Process(target = f_agv, args = (msg[connection],))
                msg[connection][PROCESS].start()
                # msg[connection][QUEUE_RECV] = queue.Queue()
                # msg[connection][QUEUE_SEND] = queue.Queue()
                
                print(f'connexion de  {client_address} et connexion = {connection}')
            else:
                try:
                    data = s.recv(1024)
                    time.sleep(0.5)
                except: 
                    data = None
                # Un socket client "readable" contient des données
                if data:
                    
                    msg[s][QUEUE_RECV].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    #For laddr use mySocket.getsockname() and for raddr use mySocket.getpeername()
                    print(f'suppression de la connexion : {s.getpeername()}')
                    msg[s][QUEUE_RECV].put('FIN')
                    # Interpréter le résultat vide comme une connexion fermée
                    if s in outputs:
                        outputs.remove(s)
                    # if s in writable:
                    #     writable.remove(s)    
                    inputs.remove(s)
                    s.close()
                    del msg[s]
                    
        # Gérer les sorties
        for s in writable:
            message = msg.get(s)
            if message:
                if not message[QUEUE_SEND].empty():
                    next_msg = message[QUEUE_SEND].get_nowait()
                    print(f'send message = {next_msg}')
                    s.send(next_msg)

                    
        #Gérer les exceptions
        for s in exceptional:
            # Arrêtez d'écouter les entrées sur la connexion
            print(f'passage {s}')
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del msg[s]
    
if __name__ == '__main__':
   main()