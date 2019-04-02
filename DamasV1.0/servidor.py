import socket
import threading
import time

class server:
    def __init__(self):
        bind_ip = "0.0.0.0"
        portaDeConexao = 9916

        self.conectado=0
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((bind_ip,portaDeConexao))
        self.server.listen(5)
        threading.Thread(target=self.conecaoLoop,args=()).start()

    def conecaoLoop(self):
        print("conexao loop")
        while 1:
            self.client,addr = self.server.accept()
            self.conectado=1
            print("conexao com ",addr)
            client_handler = threading.Thread(target=self.handlerCliente,args=())
            client_handler.start()

    def enviar(self,mensagem="ack"):
        self.client.send(mensagem)
        self.client.close()
        self.conectado=0
    def handlerCliente(self):

        request= self.client.recv(1024)
        print("recebi: ",request)
        
        #self.client.send(mensagem)
        
        



meuServer=server()
