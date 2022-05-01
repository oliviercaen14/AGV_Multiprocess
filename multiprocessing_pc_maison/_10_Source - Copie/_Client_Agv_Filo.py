import socket
import itertools 
import time

def main():

    host = '127.0.0.1'
    port = 11000

    ClientMultiSocket = socket.socket()

    print('Attente de connexion')
    try:
        ClientMultiSocket.connect((host, port))
        print('connexion établie')
    except socket.error as e:
        print(e)

    time.sleep(1)
    cpt = 0
    my_tags = [1001,1002,500,1003,1004,1005,1006,501,1007,1008,1009,1010,1011,1012,1013,1051,1014,1015,1016,1047,1017,1018,1048,1019,1020,1022,1023,1024,1025,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1026,1027,1028,1052,1029,1054,1030,1031,1049,1032,1034,1061,1062,1037,1038,1039,1040]
    #my_tags = [1001,1002,500,1003]
    my_trame = [16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 53  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 49 , 48 , 49 , 57 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117]


    for _, t in itertools.product(range(10), my_tags):
        trame = my_trame
        t_str = str(t)
        while len(t_str) < 4:
            t_str = f'0{t_str}'
        trame[34] = ord(t_str[0])
        trame[35] = ord(t_str[1])
        trame[36] = ord(t_str[2])
        trame[37] = ord(t_str[3])
        trame[11] = cpt+48
        ClientMultiSocket.send(bytearray(trame))
        cpt += 1
        if cpt > 9: cpt = 0
        print(cpt)
        time.sleep(0.5)
        # data = ClientMultiSocket.recv(1024)
        # print(data)


    # for _ in range(10):
    #     for t in my_tags:
    #         trame = my_trame
    #         t_str = str(t)
    #         while len(t_str) < 4:
    #             t_str = '0'+t_str 
    #         trame[34] = ord(t_str[0])
    #         trame[35] = ord(t_str[1])
    #         trame[36] = ord(t_str[2])
    #         trame[37] = ord(t_str[3])
    #         trame[11] = cpt+48
    #         ClientMultiSocket.send(bytearray(trame))
    #         cpt += 1
    #         if cpt > 9: cpt = 0
    #         print(cpt)
    #         time.sleep(0.05)
    #         data = ClientMultiSocket.recv(1024)
    #         print(data)
    #         #time.sleep(0.1)


    ClientMultiSocket.close()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(2)
