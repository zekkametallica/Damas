# -*- coding: utf8 -*-
try:
    import Tkinter as tk
    print("versao 2.7 do python")
except:
    import tkinter as tk
    print ("versao 3.0 do python")

import engine2 as eg
import pdb
import DamaMiniMax as ia
import thread
import cliente
import time
"Esse modulo é responsavel por inicializar as tarefas graficas"

CORES=["WHITE","GRAY","WHITE","BLACK"]
ALTURA=70
LARGURA=70
VEZ=[0,0,"BRANCA",0,"PRETA"]
VEZCOMPUTADOR=[0,0,"SUA VEZ",0,"COMPUTADOR ESTA PENSANDO"]
VITORIA=["Jogo em Progresso...",0,"EMPATOU!","VITORIA DAS BRANCA","VITORIA DAS PRETAS"]
JOGADOR=0
MAQUINA=1
ONLINE=2
DESAFIO=4
class meuJogo:
    
    def __init__(self,raiz):
        self.raiz=raiz
        self.jogo=0
        self.canvasWidth=0
        self.canvasHeight=0
        self.jogada1=[]
        self.jogada2=[]
        
        
        

    def iniciarJogo(self,tipo=eg.TAB_PADRAO,contra=MAQUINA):
        #inicializa o jogo e a enggine 
        self.contra=contra
        self.jogo=eg.tabuleiro(setup=tipo)
        self.tabuleiro=self.jogo.InformarStatus()
        self.listaWidgetsTabuleiro=[]
        self.jogo.mostrarTela()
        self.amostra=not(self.tabuleiro[0][-1]) #CorBranca 0x0


        self.quadroJogo=tk.Frame(self.raiz)
        self.quadroStatus=tk.Frame(self.raiz,width=200)
        self.quadroStatus.pack(side=tk.RIGHT)
        self.quadroJogo.pack()
        self.canvas=tk.Canvas(self.quadroJogo,height=ALTURA*len(self.tabuleiro),width=len(self.tabuleiro)*LARGURA)
        self.canvas.pack()
        
        
        self.criarMenu(self.quadroStatus)
        self.criarTabuleiro()
        if self.contra==DESAFIO:
            thread.start_new_thread( self.desafio,() )
        
            
    def desafio(self):
        while 1:
            self.computador()
        
    def criarMenu(self,raiz):
        global VEZ,VITORIA
        #cria os widgets de status ao lado
        self.stringDinamica1=tk.StringVar()
        self.stringDinamica2=tk.StringVar()
        
        
        self.indicadorVez=tk.Label(raiz,textvariable=self.stringDinamica1,width=20)
        self.indicadorVitoria=tk.Label(raiz,textvariable=self.stringDinamica2,width=40)
        
        self.indicadorVez.pack()
        self.indicadorVitoria.pack()
        
        self.stringDinamica1.set("VEZ: " + VEZ[self.jogo.mostrarVez()[0]])
        self.stringDinamica2.set("STATUS: " + VITORIA[self.jogo.ganhei])
        
    def criarTabuleiro(self):
        #poe o abuleiro na tela
        global ALTURA,LARGURA,VEZ
        amostra=self.amostra

        self.stringDinamica1.set("VEZ: " + VEZ[self.jogo.mostrarVez()[0]])
        self.stringDinamica2.set("STATUS: " + VITORIA[self.jogo.ganhei])
        
        self.tabuleiro=self.jogo.InformarStatus()
        
       
        self.canvas.delete("all")
        for linha in range(len(self.tabuleiro)):
            
            for coluna in range(len(self.tabuleiro)):
                self.canvas.create_rectangle(ALTURA*linha,
                coluna*LARGURA, ALTURA*(linha+1), (coluna+1)*LARGURA, fill=CORES[amostra],tags=("%i;%i"%(linha,coluna),"casa"))
                
                cor=self.tabuleiro[coluna][linha]
                
                if cor==eg.PECA_BRANCA:
                    self.canvas.create_oval(ALTURA*linha,
                coluna*LARGURA, ALTURA*(linha+1), (coluna+1)*LARGURA, fill="WHITE",
                tags=("%i;%i"%(linha,coluna),"peca"))
                    
                if cor==eg.PECA_PRETA:
                    self.canvas.create_oval(ALTURA*linha,
                coluna*LARGURA, ALTURA*(linha+1), (coluna+1)*LARGURA, fill="BLACK",
                tags=("%i;%i"%(linha,coluna),"peca"))

                if cor==eg.DAMA_BRANCA:
                    self.canvas.create_oval(ALTURA*linha,
                coluna*LARGURA, ALTURA*(linha+1), (coluna+1)*LARGURA, fill="#ff99ff",
                tags=("%i;%i"%(linha,coluna),"peca"))
                    
                    
                if cor==eg.DAMA_PRETA:
                    
                    self.canvas.create_oval(ALTURA*linha,
                coluna*LARGURA, ALTURA*(linha+1), (coluna+1)*LARGURA, fill="#004444",
                tags=("%i;%i"%(linha,coluna),"peca"))
                
                amostra=not(amostra)
                
            amostra=not(amostra)
        self.canvas.tag_bind("peca", '<ButtonPress-1>', self.checarJogadas)
        self.canvas.tag_bind("casa", '<ButtonPress-1>', self.checarCasaDestino)
        
        
        #self.canvasWidth=self.canvas.winfo_width()
        #self.canvasHeight=self.canvas.winfo_height()
        
        #self.canvas.bind('<Configure>', self.resize)
        
        
    def checarJogadas(self,evento):
        "captura os eventos e transforma em jogadas, alem de deixar em verde."
        "Apresenta uns bugs de deixar 2 casas em verde, mas nao compromete a jogabilidade e so ocorrem no caso do usuario clickar errado"
        
        if self.contra==MAQUINA:
            if not eg.PECA_BRANCA in self.jogo.mostrarVez() :
                return
        
        identificacao = self.canvas.find_withtag("current")
        print(identificacao)
        coordenada = self.canvas.gettags(identificacao)[0]
        posicaoClickada = [int(i) for i in coordenada.split(";")]
        casaReferente = self.canvas.find_withtag(coordenada)
        
        if "casa" in self.canvas.gettags(casaReferente[0]):
            
            self.canvas.itemconfig(casaReferente[0],fill="green")
        else:
            self.canvas.itemconfig(casaReferente[1],fill="green")

        if self.jogada1==[]:
            self.jogada1=posicaoClickada

        #print (posicaoClickada)
        
        #identificacao.configure()
    def checarCasaDestino(self,evento):
        "trasnforma evento em casa de destino"
        if self.jogada1==[]:
            return -1
        
        identificacao = self.canvas.find_withtag("current")
        
        coordenada = self.canvas.gettags(identificacao)[0]
        posicaoClickada = [int(i) for i in coordenada.split(";")]
        casaReferente = self.canvas.find_withtag(coordenada)
        
        if "casa" in self.canvas.gettags(casaReferente[0]):    
            self.canvas.itemconfig(casaReferente[0],fill="red")
        else:
            self.canvas.itemconfig(casaReferente[1],fill="red")
        if self.jogada2==[]:
            self.jogada2=posicaoClickada

        checar=self.jogo.MostrarMovimentosValidos(self.jogada1[0],self.jogada1[1])

        self.moverHumano()
        
        if self.contra==MAQUINA:
            thread.start_new_thread( self.computador,() )
        elif self.contra==ONLINE:
            thread.start_new_thread( self.online,() )
            print ("online")
            
    def computador(self):
        "faz a movimentacao do computador. Atencao , computador sao sempre as pretas, na dificuldade maxima"
        
        while True:
            if self.contra==MAQUINA and not eg.PECA_PRETA in self.jogo.mostrarVez():
                break
            
            no=ia.meuNo(jogoPadrao=self.jogo)
            resultado=no.mostrarResultado()
            move=resultado.movimentoOriginario
            self.jogo.fazerMovimento(move[0],move[1],move[2],move[3])
            self.jogada1,self.jogada2=[],[]
            
            self.criarTabuleiro()
            time.sleep(0.5)
            if self.contra==DESAFIO:
                break
        
            
            

    def online(self):
        "TODO: Implementar"
        "faz a movimentacao online. Atencao , servidor sao sempre as pretas, na dificuldade maxima"
        while eg.PECA_PRETA in self.jogo.mostrarVez():

            meuCliente=cliente.cliente()
            meuCliente.enviar(str())
            no=ia.meuNo(jogoPadrao=self.jogo)
            resultado=no.mostrarResultado()
            move=resultado.movimentoOriginario
            self.jogo.fazerMovimento(move[0],move[1],move[2],move[3])
            self.jogada1,self.jogada2=[],[]
            self.criarTabuleiro()
        
    def moverHumano(self):
        #print(self.jogada1[0],self.jogada1[1],self.jogada2[0],self.jogada2[1])
        "faz a movimentacao do player"
        self.jogo.fazerMovimento(self.jogada1[0],self.jogada1[1],self.jogada2[0],self.jogada2[1])
        
        self.jogada1,self.jogada2=[],[]
        
        self.criarTabuleiro()



if __name__=="__main__":
    #teste de modulo
    raiz=tk.Tk()
    jogo1=meuJogo(raiz)
    jogo1.iniciarJogo(contra=DESAFIO)


    raiz.mainloop()
