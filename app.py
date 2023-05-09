from class_relatorio import GerarRelatorio
from tkinter import (Label, Frame, Toplevel,
                     Text, END, Entry, StringVar,
                     IntVar, Button, Radiobutton,
                     Tk)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Notebook
import os


class Janela:

    def __init__(self, instancia_de_Tk):
        '''Tela inicial do app'''

        self.instancia = instancia_de_Tk

        frame1 = Frame(instancia_de_Tk)
        frame1.configure(border=5)
        frame1.pack()
        frame2 = Frame(instancia_de_Tk)
        frame2.configure(border=5)
        frame2.pack()
        frame3 = Frame(instancia_de_Tk)
        frame3.configure(border=5)
        frame3.pack()
        frame4 = Frame(instancia_de_Tk)
        frame4.configure(border=5)
        frame4.pack()
        frame5 = Frame(instancia_de_Tk)
        frame5.configure(border=5)
        frame5.pack()
        frame6 = Frame(instancia_de_Tk)
        frame6.configure(border=5)
        frame6.pack()

        label1 = Label(frame1, text="*Modulo:")
        label1.pack()
        self.modulo = Entry(frame1)
        self.modulo.pack()
        label2 = Label(frame2, text="*Ano:")
        label2.pack()
        self.anos = Entry(frame2)
        self.anos.pack()
        self.itens = StringVar()
        self.itens.set('')
        label_item = Label(frame4, textvariable=self.itens)
        label_item.pack()
        itens = Label(frame3, text='Item:')
        itens.pack()
        options = ['rodada', 'analito']
        self.options_choice = StringVar(value='aa')
        for opt in options:
            self.r = Radiobutton(frame5,
                                 text=opt,
                                 value=opt,
                                 variable=self.options_choice,
                                 state='normal')
            self.r.pack(padx='10', side='left')
        self.itens_filtro = Entry(frame3)
        self.itens_filtro.pack()
        button2 = Button(frame6, text="Ver itens",
                         command=self.ver_itens)
        button2.pack(padx='10', side='left')
        button1 = Button(frame6, text="Salvar relatorios",
                         command=self.gerar_relatorios)
        button1.pack(padx='10', side='left')
        btn3 = Button(frame6, text='Informações Gráficas',
                      command=self.segunda_tela)
        btn3.pack(padx='10', side='left')
        btn4 = Button(frame6, text='Ver tabelas', command=self.tela_tabela)
        btn4.pack(padx='10', side='left')

    def gerar_relatorios(self):
        '''Função para pegar os dados da API e gerar 
        arquivos .csv dentro da pasta dist/'''
        gerar = GerarRelatorio(self.anos.get().split(','), self.modulo.get())
        try:
            os.mkdir(f'modulo {self.modulo.get()}')
        except:
            pass
        gerar.salvar_relatorio(fr'modulo {self.modulo.get()}\{self.options_choice.get()} - anos {self.anos.get()}.csv',
                               item=self.itens_filtro.get().split(','), relatorio=self.options_choice.get())

    def ver_itens(self):
        '''Função para chamar os nomes dos itens do dataframe
        Caso alguém esqueca'''
        itens = GerarRelatorio(self.anos.get().split(','),
                               self.modulo.get()).gerar_nomes_items()
        self.itens.set(itens)

    def gerar_grafico(self, n=5):
        '''Função para gerar uma figura de um barplot.
        Tem que ser melhorado o visual'''
        itens = self.itens_filtro.get().split(',')
        itens = [i.strip() for i in itens]
        df = GerarRelatorio(self.anos.get().split(','),
                            self.modulo.get()).relatorio_por_analito(itens)
        fig = plt.figure(figsize=(10, 10))
        fig.clf() #Limpa a tela
        axi = fig.subplots()
        df = df.tail(n)
        axi.clear()
        axi.bar(df.ANALITO, df['média'])
        axi.set_title(f'{n} com menos reportes')
        axi.set_ylabel('Part. por Rodada')
        for i, v in enumerate(df['média'].values):
            axi.text(i, v+1, str(v), ha='center')
        return fig

    def segunda_tela(self):
        '''Chamar a tela do gráfico'''
        win = Toplevel(self.instancia)
        win.title('Gráfico')
        win.geometry('900x840')
        frame1 = Frame(win)
        frame1.pack()
        frame2 = Frame(win)
        frame2.pack()
        frame3 = Frame(win)
        frame3.pack()
        label = Label(frame1, text='Os N mais baixos:')
        label.pack()
        n_mais_baixos = IntVar(value=5)
        entry1 = Entry(frame1, textvariable=n_mais_baixos)
        entry1.pack()

        self.canvas = None

        def plotar_grafico():
            n = n_mais_baixos.get()
            figure = self.gerar_grafico(n)

            # Destrói o objeto canvas existente (se houver)
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # Cria o novo objeto canvas
            self.canvas = FigureCanvasTkAgg(figure, master=frame3)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

        btn = Button(frame2, text='gerar graficos', command=plotar_grafico)
        btn.pack(pady='10')

    def tela_tabela(self):
        '''Cria a visualização da tabela em forma de str num bloco de texto'''
        win = Toplevel(self.instancia)
        win.title('Tabela')
        win.geometry('900x480')
        notebook = Notebook(win)
        notebook.pack(pady='10', expand=True)
        frame1 = Frame(notebook)
        frame1.pack(fill='both', expand=True)
        frame2 = Frame(notebook)
        frame2.pack(fill='both', expand=True)
        analito_text = Text(frame1)
        analito_text.pack()
        rodada_text = Text(frame2)
        rodada_text.pack()
        itens = self.itens_filtro.get().split(',')
        itens = [i.strip() for i in itens]
        if '' not in itens:
            analito = GerarRelatorio(self.anos.get().split(','),
                                     self.modulo.get())
            analito = analito.relatorio_por_analito(itens)
            rodada = GerarRelatorio(self.anos.get().split(','),
                                    self.modulo.get())
            rodada = rodada.relatorio_por_rodada(itens)
        else:
            analito = GerarRelatorio(self.anos.get().split(','),
                                     self.modulo.get()).relatorio_por_analito()
            rodada = GerarRelatorio(self.anos.get().split(','),
                                    self.modulo.get()).relatorio_por_rodada()
        analito_text.insert(END, analito.to_string(index=False))
        rodada.sort_values(['ANALITO', 'data'],
                           ascending=[True, True], inplace=True)
        rodada_text.insert(END, rodada.to_string(index=False))
        notebook.add(frame1, text='Rodada')
        notebook.add(frame2, text='Analito')


root = Tk()
root.geometry('500x300')
root.title('Agrupamento - Participantes')
Janela(root)
root.mainloop()
