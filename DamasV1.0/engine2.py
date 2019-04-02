# -*- coding: utf8 -*-
WELCOME="""
_________            .___         .___ __________         ________        _______       ._______   _____  
\_   ___ \  ____   __| _/____   __| _/ \______   \___.__. \_____  \___  __\   _  \    __| _/_   | /  |  | 
/    \  \/ /  _ \ / __ |/ __ \ / __ |   |    |  _<   |  |   _(__  <\  \/  /  /_\  \  / __ | |   |/   |  |_
\     \___(  <_> ) /_/ \  ___// /_/ |   |    |   \\___  |  /       \>    <\  \_/   \/ /_/ | |   /    ^   /
 \______  /\____/\____ |\___  >____ |   |______  // ____| /______  /__/\_ \\_____  /\____ | |___\____   | 
        \/            \/    \/     \/          \/ \/             \/      \/      \/      \/          |__|
Bem Vindo à Minha engine de damas"""

"algumas variaves estao encapsuladas por que nao \
era para outros usuarios deste modulo alterarem seu valor. RO"
"aqui são algumas definições que facilitam o uso posteriormente.\
Tenha em mente que um tabuleiro é tratado como uma matriz 8x8 \
onde os numeros representam as seguintes coisas: "
CASA_BRANCA=0
CASA_PRETA=1
PECA_BRANCA=2
DAMA_BRANCA=3
PECA_PRETA=4
DAMA_PRETA=5


#jogadas ok
JOGADA_OK=0
JOGADA_COMEU=1

SEGUE_JOGO=0
JOGADA_EMPATE=2
JOGADA_VITORIA_BRANCA=3
JOGADA_VITORIA_PRETA=4

#erros
DESTINO_CHEIO=3
JOGADA_COR_PROIBIDA=4
TENTOU_COMER_PROPIA_COR=5
CASA_NEGATIVA=6
CASA_MAIOR_8=7
VEZ_ERRADA=8


TAB_PADRAO=             [       [0, 2, 0, 2, 0, 2, 0, 2],
                                [2, 0, 2, 0, 2, 0, 2, 0],
                                [0, 2, 0, 2, 0, 2, 0, 2],
                                [1, 0, 1, 0, 1, 0, 1, 0],       
                                [0, 1, 0, 1, 0, 1, 0, 1],
                                [4, 0, 4, 0, 4, 0, 4, 0],
                                [0, 4, 0, 4, 0, 4, 0, 4],
                                [4, 0, 4, 0, 4, 0, 4, 0]
                        ]
TAB2_PADRAO=             [       [0, 0, 0, 0, 0, 1, 0, 1],
                                [1, 0, 1, 0, 1, 0, 1, 0],
                                [0, 3, 0, 1, 0, 1, 0, 2],
                                [1, 0, 1, 0, 1, 0, 1, 0],       
                                [0, 1, 0, 1, 0, 1, 0, 1],
                                [4, 0, 4, 0, 4, 0, 4, 0],
                                [0, 4, 0, 4, 0, 4, 0, 4],
                                [4, 0, 4, 0, 4, 0, 4, 0]
                        ]

                        
TAB3_PADRAO=            [       [0, 2, 0, 2 ,0 ,2],
                                [2, 0, 2, 0 ,2 ,0],
                                [0, 1, 0, 1 ,0 ,1],       
                                [1, 0, 1, 0 ,1 ,0],
                                [0, 4, 0, 4 ,0 ,4],
                                [4, 0, 4, 0 ,4 ,0]
                        ]

TAB4_PADRAO=            [       [0, 2, 0, 2, 0],
                                [2, 0, 2, 0, 2],       
                                [0, 1, 0, 1, 0],
                                [4, 0, 4, 0, 4],
                                [0, 4, 0, 4, 0]
                        ]

TAB5_PADRAO=            [       [0, 2, 0],
                                [1, 0, 1],
                                [0, 4, 0]
                        ]


"Essa é a classe resposnsável por armazenar um status do jogo"
"""A partida termina empatada quando:

os dois parceiros concordarem com o empate;
a partir de qualquer ponto da partida, ocorrer 20 lances sucessivos de Damas, sem tomada ou deslocamento de pedra;
uma mesma posição se produzir pela terceira vez, cabendo ao mesmo jogador o lance, deverá o interessado reclamar o empate, antes que a posição se modifique (esta regra só vale se a partida estiver sendo anotada em uma planilha); e,
na luta de três damas contra uma, o lado maior não conseguir obter vitória em vinte lances.
"""
class tabuleiro:
        def __init__(self,setup=TAB_PADRAO,quemComeca=[PECA_BRANCA,DAMA_BRANCA],lancesSemCaptura=0):
                "inicializa o jogo a partir de uma matriz com as pecas ja posicionadas"
                #setup eh uma matriz de inteiros representando o estado do jogo
                self.numeroLancesSemCaptura=lancesSemCaptura
                self.altura=len(setup)
                self.largura=len(setup[0])
                
                self.contagemBrancaPeca=0
                self.contagemBrancaDama=0
                self.contagemPretaPeca=0
                self.contagemPretaDama=0
                
                self.MovimentosValidos=[]
                self.amostraCor=-1
                self.corNaoUsada=-1

                "Essas são as variáveis críticas que não devem ser mexidas"
                self.__status=setup
                self.__vez=quemComeca
                self.__tabuleiroBkp=[]
                
                self.corNaoUsada=self.__status[0][0]
                #self.corEmBaixo=not(self.corNaoUsada)
                if self.corNaoUsada==CASA_PRETA:
                        self.corEmbaixo=CASA_BRANCA
                else:
                        self.corEmBaixo=CASA_PRETA
                        
                self.ganhei=self.ChecarVitoria()
                
        def fazerCopia(self):
                return tabuleiro(self.__status,self.__vez,self.numeroLancesSemCaptura)
        def mostrarTela(self):
                "Exibe o estado da tela em ascii"
                
                traducao=[u"\u25A1",u"\u25A0",'b','B','p','P']
                for i in self.__status:
                        string=""
                        x=[ traducao[j] for j in i ]
                        for k in x:
                                string+=k
                        print(string)
                print("")
                                
        def estaVazia(self,x,y):
                "retorna True se a casa Esta Vazia"
                if self.__status[y][x]==CASA_BRANCA or self.__status[y][x]==CASA_PRETA :
                        return True
                else:
                        return False
                
        def fazerMovimento(self,xOrigem,yOrigem,xDest,yDest):
                "Checa se Um movimento é valido.Se sim, o realiza, caso contrario retorna o Erro Correspondente"
                self.__tabuleiroBkp=[]
                #print("vez:",self.__vez)


                podeComer=self.GerarMovimentos(xOrigem,yOrigem)
                #print(self.MovimentosValidos)


                valido = 0
                for jogada in self.MovimentosValidos:
                        if [xOrigem,yOrigem,xDest,yDest]==jogada[:-1]:
                                jogadaDecidida=jogada
                                valido=1
                                break
                
                if valido:
                        #print("Movendo pecaTipo "+str(self.__status[yOrigem][xOrigem])+" de x,y=%i,%i --> x,y=%i,%i"%(xOrigem,yOrigem,xDest,yDest))
                        #self.mostrarTela()
                        self.__executarMovimento(xOrigem,yOrigem,xDest,yDest,jogadaDecidida[-1])              
                else:
                        print ("erro, jogada invalida")
                        return "jogada invalida"

                podeComer=self.GerarMovimentos(xDest,yDest)
                if (podeComer==True and jogadaDecidida[-1]==JOGADA_COMEU):
                        trocar=0
                else:
                        trocar=1
                    
                        

                if trocar==1:
                    if PECA_BRANCA in self.__vez:
                            self.__vez=[PECA_PRETA,DAMA_PRETA]
                    else:
                            self.__vez=[PECA_BRANCA,DAMA_BRANCA]    
                
                
                self.__AtualizarPeca()
                

                fim=self.ChecarVitoria()
                return fim
                    


        def __executarMovimento(self,xOrigem,yOrigem,xDest,yDest,tipo=JOGADA_OK):
                "Executa de fato a jogada(deve ser chamada apenas se a jogada for valida)é responsável tambem por trocar as cores mudadas no pulo das pecas"


                if tipo==JOGADA_OK:
                        self.numeroLancesSemCaptura+=1
                        self.__status[yDest][xDest]=self.__status[yOrigem][xOrigem]
                        self.__status[yOrigem][xOrigem]=self.corEmBaixo
                if tipo==JOGADA_COMEU:
                        self.numeroLancesSemCaptura=0
                        self.__status[yDest][xDest]=self.__status[yOrigem][xOrigem]
                        difX=xDest-xOrigem
                        difY=yDest-yOrigem
                        self.__status[yDest-difY//2][xDest-difX//2]=self.corEmBaixo
                        self.__status[yOrigem][xOrigem]=self.corEmBaixo
        def contagem(self):
                self.contagemBrancaPeca=0
                self.contagemBrancaDama=0
                self.contagemPretaPeca=0
                self.contagemPretaDama=0
                for linha in self.__status:
                        self.contagemBrancaPeca+=linha.count(PECA_BRANCA)
                        self.contagemBrancaDama+=linha.count(DAMA_BRANCA)
                        self.contagemPretaPeca+=linha.count(PECA_PRETA)
                        self.contagemPretaDama+=linha.count(DAMA_PRETA)
                
        def ChecarVitoria(self):
                "Checa se alguma condição de fim de jogo foi estabelecida"
                self.contagem()

                #print(contagemBrancaPeca,contagemBrancaDama,contagemPretaPeca,contagemPretaDama)
                
                if self.contagemBrancaPeca+self.contagemBrancaDama==0:
                        retorno=JOGADA_VITORIA_PRETA
                elif self.contagemPretaPeca+self.contagemPretaDama==0:
                        retorno=JOGADA_VITORIA_BRANCA
                elif self.numeroLancesSemCaptura>=20:
                        if self.contagemPretaDama>=2 and self.contagemBrancaDama==1 and self.contagemBrancaPeca==0:
                                retorno=JOGADA_VITORIA_PRETA
                                #print("retornei empate")
                        elif self.contagemPretaDama==1 and self.contagemBrancaDama>=2 and self.contagemPretaPeca==0:
                                retorno=JOGADA_VITORIA_BRANCA
                                #print("retornei empate")
                        else:
                                #print("retornei empate")
                                retorno=JOGADA_EMPATE
                        
                else:
                        #print(self.numeroLancesSemCaptura)
                        retorno=SEGUE_JOGO
                self.ganhei=retorno
                return retorno

                
        def __AtualizarPeca(self):
                "confere se alguma peca virou dama"
                for i in range(self.largura):
                        if self.__status[0][i] == PECA_PRETA:
                                self.__status[0][i]=DAMA_PRETA
                for i in range(self.largura):
                        if self.__status[-1][i] == PECA_BRANCA:
                                self.__status[-1][i]=DAMA_BRANCA
                        
        
        def __fazerBkp(self):
                "faz uma copia da matriz tabuleiro"
                bkp=[]
                for i in self.__status:
                        bkp.append(i[::])
                return bkp
                
        def GerarMovimentos(self,xOrigem,yOrigem):
                self.MovimentosValidos=[]
                "Esta funcao gera todos os movimentos Validos a partir de uma casa.Nao Considera o caso de comer +1 peca, porem isso \
                é implementado na funcao Fazer movimento, que permite o jogador \"cickar duas vezes\" para comer a segunda ou terceira peça "
                if len(self.__tabuleiroBkp) <1:
                        self.__tabuleiroBkp.append(self.__fazerBkp())
                        
                #self.mostrarTela()
                listaMovimentosValidos=[]
                #print("\nOrigem: %i,%i"%(xOrigem,yOrigem))
                
                
                        
                if self.estaVazia(xOrigem,yOrigem):
                        #self.mostrarTela()
                        for i in self.__status:
                                print(i)
                        raise IndexError("movimento Invalido Origem nao tem peca")


                
                elif self.__status[yOrigem][xOrigem] == PECA_BRANCA:
                        pecaMovida=PECA_BRANCA
                        listaMovimentos=[[xOrigem-1,yOrigem+1],[xOrigem+1,yOrigem+1] ,
                                        [xOrigem-2,yOrigem+2],[xOrigem+2,yOrigem+2] ]
                        
                elif self.__status[yOrigem][xOrigem] == PECA_PRETA:
                        pecaMovida=PECA_PRETA
                        listaMovimentos=[[xOrigem-1,yOrigem-1],[xOrigem+1,yOrigem-1],
                                         [xOrigem-2,yOrigem-2],[xOrigem+2,yOrigem-2]]
                        
                elif self.__status[yOrigem][xOrigem]==DAMA_BRANCA :
                        pecaMovida=DAMA_BRANCA
                        listaMovimentos=[[xOrigem-1,yOrigem-1],[xOrigem-1,yOrigem+1],
                                         [xOrigem+1,yOrigem-1],[xOrigem+1,yOrigem+1],
                                         [xOrigem-2,yOrigem-2],[xOrigem-2,yOrigem+2],
                                         [xOrigem+2,yOrigem-2],[xOrigem+2,yOrigem+2],
                                         ]
                        
                elif self.__status[yOrigem][xOrigem]==DAMA_PRETA :
                        pecaMovida=DAMA_PRETA
                        listaMovimentos=[[xOrigem-1,yOrigem-1],[xOrigem-1,yOrigem+1],
                                         [xOrigem+1,yOrigem-1],[xOrigem+1,yOrigem+1],
                                         [xOrigem-2,yOrigem-2],[xOrigem-2,yOrigem+2],
                                         [xOrigem+2,yOrigem-2],[xOrigem+2,yOrigem+2],
                                         ]
                else:
                        for i in self.__status:
                                print(i)
                        raise IndexError("erro desconhecido")

                #print("peca movida",pecaMovida)
                podeComer=False
                for jogada in listaMovimentos:
                        
                        retorno= self.__ChecarMovimento(xOrigem,yOrigem,jogada[0],jogada[1],pecaMovida)
                        jogada.append(retorno)
                        #print("resultado da jogada : ",jogada)
                        
                        if retorno == JOGADA_OK or retorno == JOGADA_COMEU:
                                self.MovimentosValidos.append([xOrigem,yOrigem]+jogada)
                                
                        if retorno == JOGADA_COMEU:
                                podeComer=True
                
                                
                                #print (self.MovimentosValidos)
                        #        self.__executarMovimento(xOrigem,yOrigem,jogada[0],jogada[1],JOGADA_COMEU)
                                #print(jogada[0],jogada[1],"jogada")
                        #        self.GerarMovimentos(jogada[0],jogada[1])

                self.__status=self.__tabuleiroBkp[0]
                #print("restaurando tabuleiro, fim")
                #print(self.MovimentosValidos)
                return podeComer #Tipo da jogada possivel
                
        def __ChecarMovimento(self,xOrigem,yOrigem,xDest,yDest,pecaMovida):
                "Confere se o movimento gerado pela funcao acima é um movimento valido, dado o estado atual do tabuleiro"
                #print(xDest,yDest)
                
                difX=xDest-xOrigem
                difY=yDest-yOrigem
                
                peca=self.__status[yOrigem][xOrigem]
                if not (peca in self.__vez):
                        return VEZ_ERRADA
                if yDest<0 or xDest<0:
                        return CASA_NEGATIVA
                if  yDest>=self.altura or xDest>=self.largura:
                        return CASA_MAIOR_8
                
                if self.estaVazia(xDest,yDest)==False:
                        return DESTINO_CHEIO
                
                elif self.__status[yDest][xDest]==self.amostraCor:
                        return JOGADA_COR_PROIBIDA

                elif abs(difX)==1 and abs(difY)==1:
                        return JOGADA_OK

                if pecaMovida in [ PECA_BRANCA, DAMA_BRANCA]:
                        if (abs(difX)==2 and abs(difY)==2) and self.__status[yDest-difY//2][xDest-difX//2] in [PECA_PRETA,DAMA_PRETA]:
                                return JOGADA_COMEU
                        else:
                                return TENTOU_COMER_PROPIA_COR

                if pecaMovida in [ PECA_PRETA, DAMA_PRETA]:
                        if (abs(difX)==2 and abs(difY)==2) and self.__status[yDest-difY//2][xDest-difX//2] in [PECA_BRANCA,DAMA_BRANCA]:
                                return JOGADA_COMEU
                        else:
                                return TENTOU_COMER_PROPIA_COR          
                else:
                        raise NameError ("Isso eh um bug, contactar o programador")
        def InformarStatus(self):
                "retorna a matriz tabuleiro, interface com o programador"
                return self.__status

        def MostrarMovimentosValidos(self,xOrigem,yOrigem):
                
                self.GerarMovimentos(xOrigem,yOrigem)
                return self.MovimentosValidos
        
        def mostrarVez(self):
                return self.__vez

if __name__=="__main__":
        jogo=tabuleiro()
        jogo.mostrarTela()


