import socket



class cliente:
    def __init__(self,target="127.0.0.1",port=9990):
        self.recebi=0
        print("rodando Cliente")
        self.resposta=""
        self.target=target
        self.porta= 9916
        self.conectar()
        
    def conectar(self):
        self.cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cliente.connect((self.target,self.porta))
        
    def enviar(self,mensagem="ola"):
        self.recebi=0
        self.cliente.send(mensagem)
        self.resposta=self.cliente.recv(4096)
        self.recebi=1
        print(self.resposta)

meuCliente=cliente()
