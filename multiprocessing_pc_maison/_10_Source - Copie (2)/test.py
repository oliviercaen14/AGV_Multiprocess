from multiprocessing import Process, Queue
# import sys
import time
import os


CONNEXION,CON_INFO,QUEUE_RECV,QUEUE_SEND = ['connexion','con_info','queue_recv','queu_send'] 

donnees = {CONNEXION :'192.168.0.1',
           CON_INFO:2
            }

data = {'serveur':donnees}

def f(q):
    print ('entree dans le process')
    fin = False
    info = ''
    while not fin:
        while not q.empty() :
            info = q.get()
            print(info)
        print('----------')
        time.sleep(1)
        # except  :
        #     print(f'Whew!, {sys.exc_info()[0]}, occurred.')
        #     print(q.qsize())
        #     print('except') 
        #     time.sleep(5)
        if info == 'FIN':
            fin = True
        # else: time.sleep(2)
    time.sleep(5)
    print('sortie du process')
def main():
    q = Queue()
    p = Process(target = f, args = (q,))
    p.start()
    for index in range(1000):
        time.sleep(0.0001)
        q.put(index)
    q.put('FIN')
    print ('envoi FIN')
    p.join()
    print('Fin du programme principal')
    
    
    
if __name__ == '__main__':
    root = os.path.dirname(__file__)
    os.chdir(root)
    os.chdir('../')
    path_racine = os.getcwd()
    
    path_log = os.path.join(path_racine, "_20_Logs")

    # abs_path = os.path.join(root, rel_path)
    print (f'root = {path_racine}')
    print (f'path_log = {path_log} ')
    # print (f'abs_path = {abs_path}  ')
    # print (os.path.relpath())
    print(os.getcwd())

#    print (data['serveur'][CON_INFO]) 
#    print (f'{CONNEXION}  {CON_INFO}  {QUEUE_RECV}')
   
   #main()
   
#    Desktop/file.txt
# ../User/Desktop/file.txt
# ../../../User/Desktop/file.txt
# ../../Desktop/file.txt