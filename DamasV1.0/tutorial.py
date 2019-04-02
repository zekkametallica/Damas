import engine2
import DamaMiniMax as ia
"tabuleiro padrao de damas, você pode inicializar qualquer jogo a partir daqui"
"ISSO EH UM TUTORIAL PARA DESENVOLVEDORES"
"""
aqui são algumas definições que facilitam o uso posteriormente.
Tenha em mente que um tabuleiro é tratado como uma matriz 8x8 
onde os numeros representam as seguintes coisas:
"""
CASA_BRANCA=0
CASA_PRETA=1
PECA_BRANCA=2
DAMA_BRANCA=3
PECA_PRETA=4
DAMA_PRETA=5


#jogadas ok
JOGADA_OK=0
JOGADA_COMEU=1


#retornos de vitória:
JOGADA_VITORIA_BRANCA=3
JOGADA_VITORIA_PRETA=4
JOGADA_EMPATE=2



"obs : Voces devem usar os metodos fazer movimento e "


"        Eixo x  0  1  2  3  4  5  6   7      "  """eixo y
                                                    0
                                                    1
                                                    ...
                                                    7"""
tab=    [       [2, 0, 2, 0, 2, 0, 2, 0],
                [0, 2, 0, 2, 0, 2, 0, 2],
                [2, 0, 2, 0, 2, 0, 2, 0],
                [0, 1, 0, 1, 0, 1, 0, 1],       
                [1, 0, 1, 0, 1, 0, 1, 0],
                [0, 4, 0, 4, 0, 4, 0, 4],
                [4, 0, 4, 0, 4, 0, 4, 0],
                [0, 4, 0, 4, 0, 1, 0, 4]
        ]


jogo1=engine2.tabuleiro() # inicializou
jogo1.mostrarTela()  # mostrou tela

#jogo1.fazerMovimento(0,2,1,3) #moveu Primeira Branca
#jogo1.mostrarTela()

while jogo1.ganhei==engine2.SEGUE_JOGO:
    no1=ia.meuNo(jogoPadrao=jogo1)
    resultado=no1.mostrarResultado()
    move=resultado.movimentoOriginario


    jogo1.fazerMovimento(move[0],move[1],move[2],move[3]) #moveu Primeira Preta
    jogo1.mostrarTela()


#jogo1.fazerMovimento(1,3,3,5) #moveu a branca 
#jogo1.mostrarTela()

#jogo1.fazerMovimento(3,5,5,7) # moveu outra preça branca (comeu 2 vezes entao pode jogar repetido)
#jogo1.mostrarTela() # mostrou de novo

#acabou=jogo1.fazerMovimento(1,5,0,4) #moveu Preta
#jogo1.mostrarTela()

#print("Se o que  metodo fazerMovimento for igual a JOGADA_OK(0) o jogo continua:",acabou==JOGADA_OK,
#      acabou!=JOGADA_VITORIA_BRANCA,acabou!=JOGADA_VITORIA_PRETA,acabou!=JOGADA_EMPATE)

#meuJogo=jogo1.InformarStatus() # devolve o valor da matriz para que vcs possam usar na interface tkinter
#print(meuJogo) #isso printa a matriz semelhante ao tab, porem com o conteudo atual do jogo
