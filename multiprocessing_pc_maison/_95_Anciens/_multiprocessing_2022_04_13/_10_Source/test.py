from multiprocessing import Process, Queue
# import sys
import time

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
   print (data['serveur'][CON_INFO]) 
   print (f'{CONNEXION}  {CON_INFO}  {QUEUE_RECV}')
   
   #main()