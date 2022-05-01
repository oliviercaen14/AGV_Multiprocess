import socket
import configparser
import time


host = '127.0.0.1'
port = 11000

ClientMultiSocket = socket.socket()

print('Attente de connexion')
try:
    ClientMultiSocket.connect((host, port))
    print('connexion établie')
except socket.error as e:
    print(str(e))

time.sleep(5)

my_tags = [1001,1002,500,1003,1004,1005,1006,501,1007,1008,1009,1010,1011,1012,1013,1051,1014,1015,1016,1047,1017,1018,1048,1019,1020,1022,1023,1024,1025,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1026,1027,1028,1052,1029,1054,1030,1031,1049,1032,1034,1061,1062,1037,1038,1039,1040]
my_trame = [16 , 2 , 48 , 55 , 51 , 65 , 67 , 83 , 70 , 68 , 53 , 53  , 83 , 56 , 49 , 49 , 48 , 52 , 49,48 , 48 , 48 , 48 , 51 , 48 , 48 , 48 , 48 , 48 , 48 , 102 , 49 , 48 , 112 , 49 , 48 , 49 , 57 , 89 , 49 , 69 , 48,70 , 49 , 52 , 16 , 3 , 252 , 117]
while True:
    for t in my_tags:
        trame = my_trame
        t_str = str(t)
        while len(t_str) < 4:
            t_str = '0'+t_str 
        trame[34] = ord(t_str[0])
        trame[35] = ord(t_str[1])
        trame[36] = ord(t_str[2])
        trame[37] = ord(t_str[3])
        ClientMultiSocket.send(bytearray(trame))
        time.sleep(5)

ClientMultiSocket.close()
