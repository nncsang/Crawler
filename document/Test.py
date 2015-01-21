__author__ = 'nncsang'

import socket
import GlobalVariable
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((GlobalVariable.TABLE_URL , 80))
s.sendall("GET http://"+ GlobalVariable.TABLE_URL + " HTTP/1.0\n\n")

html = ""
response = [s.recv(2048)]
i = 0;
while response[-1]:
    response.append(s.recv(2048))



print ''.join(response)
