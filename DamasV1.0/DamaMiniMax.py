# -*- coding: utf8 -*-
import engine2
import pdb

"""
Este módulo é responsável por cuidar da 'inteligencia artificial' do jogo contra maquina.
Algumas considerações. incrementar a variavel camada Maxima consome MUUUUUITA memoria. Tempo de processamento não é problema.
Talvez fosse mais adequado liberar a memoria das listas de nos após obter o resultado.



Para projeto futuro: Consertar o memory management desse modulo.

Esse modulo nao leva em consideração o status de vitoria na decisao, pois diferente do xadrez, onde é possivel ganhar com pecas inimigas no tabuleiro,
Aqui comer Pecas = Vitoria.

Para o uso: a arvore é remontada toda vez que for chamada. Não leva a grandes problemas de desempenho , já que a ultima camada é sempre a mais espaçosa

Por questoes de memoria, na implementacao deste módulo, recomenda-se esperar o jogador tomar sua decisão do que 'prever'
qual sera seu movimento, fazendo um thread para cada possivel jogada

para camada de tamanho 6, consome cerca de 1gb de ram.

"""

TAXA=0.8

EMPATE=0
VITORIA=0
DERROTA=0
CAMADA_MAXIMA=4
class meuNo:
    def __init__(self,jogoPadrao=engine2.tabuleiro(),camada=0,movimentoOriginario=[],pai=0):
        
        global CONTADOR,VITORIA,DERROTA,EMPATE
        self.pai=pai
        self.numeroVitorias=0
        self.numeroDerrotas=0
        self.numeroEmpates=0
        self.tuplaResultado=(0,0,0,0)
        self.camada=camada
        self.jogo=jogoPadrao
        #self.tabuleiro=self.jogo.InformarStatus()
        self.listaJogadas=[]
        self.listaNosAbaixo=[]
        self.movimentoOriginario=movimentoOriginario
        self.meuStatus=self.jogo.ganhei
        if self.camada <CAMADA_MAXIMA:
            #print (self.camada)
            if self.meuStatus==engine2.SEGUE_JOGO:          
                self.fazerFork()
                
            elif self.meuStatus==engine2.JOGADA_EMPATE:
                #print("EMPATEI")
                EMPATE+=1

            elif self.meuStatus==engine2.JOGADA_VITORIA_BRANCA:
                VITORIA+=1
                #print("BRANCA GANHOU")

            elif self.meuStatus==engine2.JOGADA_VITORIA_PRETA:
                DERROTA+=1
                #print("PRETA GANHOU")

        #else: fim do ramo
            
    def GerarTodosMovimentos(self):
        for linha in range(self.jogo.altura):
            for coluna in range(self.jogo.largura):
                if self.jogo.estaVazia(linha,coluna)==False:
                    jogada=self.jogo.MostrarMovimentosValidos(linha,coluna)
                    if jogada!=[]:
                        self.listaJogadas+=jogada
        
        #print(str(self.listaJogadas)+'%i \n'%self.camada)
    def fazerFork(self):

        
        self.GerarTodosMovimentos()
        tamanho=len(self.listaJogadas)
        
        #print((self.listaJogadas))
        #if tamanho!=0:
        #    selecionados=rd.sample(self.listaJogadas,int(tamanho*TAXA**self.camada)) # possivel implementacao para arvores parciais

        for jogada in self.listaJogadas:
            novojogo=self.jogo.fazerCopia()
            novojogo.fazerMovimento(jogada[0],jogada[1],jogada[2],jogada[3])
            self.listaNosAbaixo.append(meuNo(novojogo,self.camada+1,movimentoOriginario=jogada,pai=self))
        
    def fazerContagem(self):
        

        #print("contagem referente a lista de movimentos=",self.movimentoOriginario)
        #pdb.set_trace()


        if self.listaNosAbaixo==[]:
            #pdb.set_trace()
            return (self.jogo.contagemBrancaPeca,self.jogo.contagemBrancaDama,
                    self.jogo.contagemPretaPeca,self.jogo.contagemPretaDama)
        else:
            #pdb.set_trace()      
            for cadaNo in self.listaNosAbaixo:

                #pdb.set_trace()
                self.tuplaResultado=somaTupla(self.tuplaResultado,cadaNo.fazerContagem())
            return self.tuplaResultado

    def mostrarResultado(self):
        self.fazerContagem()
        scoreJogadas=[]
        for elemento in self.listaNosAbaixo:
            scoreJogadas.append(pontuacao(elemento.tuplaResultado))
        print("taxa branca.vs preta:",scoreJogadas)
        #melhorJogada

        if engine2.PECA_BRANCA in self.jogo.mostrarVez():
            return self.listaNosAbaixo[scoreJogadas.index(max(scoreJogadas))] # melhor jogada para as brancas
        else:
            return self.listaNosAbaixo[scoreJogadas.index(min(scoreJogadas))] # melhor jogada para as pretas
    #def prosseguir(self):
    #    resultado=self.mostrarResultado()
    #    resultado.movimentoOriginario
        
        
def pontuacao(elemento):
    
    score=0
    score+=elemento[0]-elemento[2] #diferenca de pcas comuns em cada no


    score+=(elemento[1]-elemento[3])*3 #Estou considerando que uma dama vale 3x uma peca normal.
    #Isto carece de fontes sérias e baseia-se na intuição do programador

    return score
    
        

    
        
def somaTupla(tupla1,tupla2):
    
    somaTupla= (tupla1[0]+tupla2[0],tupla1[1]+tupla2[1],
            tupla1[2]+tupla2[2],tupla1[3]+tupla2[3])
    return somaTupla

if __name__=="__main__":
    
    #pdb.set_trace()
    no1=meuNo()

    
    #pdb.set_trace()
    resultado=no1.mostrarResultado()
    print(resultado.movimentoOriginario)
    no1=resultado


