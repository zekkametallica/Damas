# -*- coding: utf8 -*-
from Tkinter import *
import damaGrafico as dg
import engine2 as eg

class Window(Frame):

    
    def __init__(self, master=None):
        
        # Cria um novo frame. 
        Frame.__init__(self, master)   

                       
        self.master = master
        self.init_window()

    
    def init_window(self):

        # muda o titulo    
        self.master.title("Meu Jogo de Damas")

        
        self.pack(fill=BOTH, expand=1)

        # cria menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        quadro=Frame(root,width=200,height=50)
        quadro.pack()
        

        edit = Menu(menu)

        edit.add_command(label="Contra Player",command=self.comando1)
        edit.add_command(label="Contra Maquina",command=self.comando2)
        edit.add_command(label="Player 6x6",command=self.comando3)
        edit.add_command(label="Ver 2 'IA' Batalhando",command=self.comando4)

        
        menu.add_cascade(label="Jogar", menu=edit)

    #inicializa os 3 tipos de jogo
    def comando1(self):
        jogo1=dg.meuJogo(root)
        jogo1.iniciarJogo(contra=dg.JOGADOR)
        
    def comando2(self):
        jogo1=dg.meuJogo(root)
        jogo1.iniciarJogo(contra=dg.MAQUINA)
    def comando3(self):
        jogo1=dg.meuJogo(root)
        jogo1.iniciarJogo(contra=dg.JOGADOR,tipo=eg.TAB3_PADRAO)

    def comando4(self):
        jogo1=dg.meuJogo(root)
        jogo1.iniciarJogo(contra=dg.DESAFIO,tipo=eg.TAB_PADRAO)

root = Tk()
app = Window(root)

root.mainloop()  
