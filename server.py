__author__ = 'nncsang'

import socket
import threading
import GlobalVariable
from Logger import Logger as Logger
import json

# Initialize SOCKET
try:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((GlobalVariable.HOST, GlobalVariable.PORT))
    srv.listen(GlobalVariable.BACK_LOG)
    #srv.settimeout(GlobalVariable.TIME_OUT)

    Logger.notify(Logger.INFO, 'Starting listening on %s:%s' % (GlobalVariable.HOST, GlobalVariable.PORT))

    # Initialize MUTEX
    srv_lock=threading.Lock()

    class Client(threading.Thread):
        def run(self):
            while True:
                srv_lock.acquire()
                conn, addr = srv.accept()
                srv_lock.release()

                print("Client %s : %d connected" % addr)

                while True:
                    data=conn.recv(1024)
                    if not data:
                        break

                    conn.send(data.upper())

                conn.close()
                print("Client %s : %d disconnected" % addr)




    pool=[Client() for i in range(GlobalVariable.POOL_SIZE)]
    [t.start() for t in pool]
    [t.join() for t in pool]

except socket.error:
    Logger.log(str(socket.error))
except socket.timeout:
    Logger.log(str(socket.error))




