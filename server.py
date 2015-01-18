__author__ = 'nncsang'

import socket
import threading
import GlobalVariable

from Logger import Logger
from DataStructures.Buffer import Buffer
from DataStructures.Message import Message
from JSONDatabase import JSONDatabase
import json

# Initialize SOCKET
Logger.notify(Logger.INFO, 'Starting listening on %s:%s' % (GlobalVariable.HOST, GlobalVariable.PORT))
try:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((GlobalVariable.HOST, GlobalVariable.PORT))
    srv.listen(GlobalVariable.BACK_LOG)
    #srv.settimeout(GlobalVariable.TIME_OUT)

except socket.error, e:
    Logger.notify(Logger.ERROR, 'Error when initializing SOCKET: ' + str(e))
    Logger.notify(Logger.INFO, 'Program exited')
    Logger.log('Error when initializing SOCKET: ' + str(e))
    exit();

# Initialize MUTEX
srv_lock=threading.Lock()
buffer = Buffer()
db = JSONDatabase()

class ClientSocket(threading.Thread):

    def __init__(self,sock,addrinfo):
        threading.Thread.__init__(self)
        self.conn = sock
        self.addr = addrinfo
        self.daemon = True

    def run(self):
        Logger.notify(Logger.INFO, "Client %s : %d connected" % addr)

        try:
            while True:
                try:
                    data = conn.recv(1024)
                    buffer.updateBuffer(data)

                    message = buffer.parse()

                    if (message == None):
                        pass
                    else:
                        if (message.type == "UPDATE"):
                            Logger.notify(Logger.INFO, "Client %s:%d sent UPDATE request" % addr)
                            Logger.notify(Logger.INFO, "Processing UPDATE request of client %s:%d" % addr)

                            srv_lock.acquire()
                            db.write(message.payload)
                            srv_lock.release()

                            Logger.notify(Logger.INFO, "Finished storing UPDATE request of client %s:%d" % addr)

                            response = Message("RESPONSE", [], "OK")
                            conn.send(str(response))
                            continue

                        if (message.type == "CLOSE"):
                            Logger.notify(Logger.INFO, "Client %s:%d sent CLOSE request" % addr)
                            Logger.notify(Logger.INFO, "Sending OK for closing request to client %s:%d" % addr)
                            response = Message("RESPONSE", [], "OK")
                            conn.send(str(response))
                            break

                except socket.timeout:
                    Logger.notify(Logger.INFO, "Connection to client %s : %d is closed due to timeout" % addr)
                    break
        except socket.error, e:
            Logger.notify(Logger.ERROR, "Error: " + str(e))
            Logger.log("Error: " + str(e))

        conn.close()
        Logger.notify(Logger.INFO, "Client %s : %d disconnected" % addr)

while True:
    conn, addr = srv.accept()
    ClientSocket(conn,addr).start()


# class Client(threading.Thread):
#     def run(self):
#         while True:
#
#             srv_lock.acquire()
#             conn, addr = srv.accept()
#             srv_lock.release()
#
#             Logger.notify(Logger.INFO, "Client %s : %d connected" % addr)
#
#             while True:
#                 try:
#                     data = conn.recv(1024)
#                 except socket.timeout:
#                     Logger.notify(Logger.INFO, "Connection to client %s : %d is closed due to timeout" % addr)
#                     break
#                 if not data:
#                    break
#                 conn.send(data.upper())
#
#             conn.close()
#             Logger.notify(Logger.INFO, "Client %s : %d disconnected" % addr)

# pool=[Client() for i in range(GlobalVariable.POOL_SIZE)]
# [t.start() for t in pool]
# [t.join() for t in pool]






