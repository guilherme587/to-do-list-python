import tkinter.ttk as ttk
import tkinter as tk
from tkinter import font
from tkinter.messagebox import showerror, showwarning, showinfo

class Tarefa:
    def __init__(self, tarefa):
        self.tarefa = tarefa

    def __str__(self):
        return self.tarefa

class Lista_deTarefas(Tarefa):
    def __init__(self):
        self.lista_detarefas = []
    
    def add_tarefa(self, task):
        self.lista_detarefas.append(task)

    def remove_tarefa(self, pos):
        self.lista_detarefas.pop(pos)

    def atualiza_tarefa(self, pos, task):
        self.lista_detarefas.insert(pos, task)

    @staticmethod
    def campo(task):
        if task != '':
            return True
        Lista_deTarefas.erro('campo')
        return False
    
    @staticmethod
    def linha_select(select):
        if len(select) != 0:
            return True
        Lista_deTarefas.erro('selct')
        return False

    @staticmethod
    def select(par):
        return par

    @staticmethod
    def erro(erro):
        if erro == 'campo':
            showerror('Erro',\
            'Todos os Campos Devem Estar Preenchidos!')

        if erro == 'selct':
            showerror('Erro',\
            'Uma linha deve ser selecionada para essa ação!')
        
    def __str__(self):
        s = 'Lis To Do:\n'
        for j, i in enumerate(self.lista_detarefas):
            s += f'{i}\n'
        return s
    
    def converte_para_lista(self):
        s = []
        for f in self.lista_detarefas:
            s.append(str(f))
        return s

class View:
    def __init__(self, tela):
        self.tela = tela
        self.botao = {}
        self.frame = {}
        self.label = {}
        self.labelframe = {}
        self.entry = {}
        self.r_button = {}
        self.lb_v = tk.StringVar()
        self.listbox = {}
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=12, weight=font.BOLD) 
        self.desenha()
    
    def desenha(self):
        #label
        self.tela.title('To Do List')

        #frame
        self.frame['f1'] = tk.Frame(self.tela, bg = 'red')
        self.frame['f1'].grid(row = 0, column = 0)

        #lf
        # self.labelframe['lf1'] = tk.LabelFrame(self.tela, text = 'Tarefa:')
        # self.labelframe['lf1'].grid(row = 7, column = 0)
        # esc = tk.StringVar()
        # self.r_button[1] = tk.Radiobutton(self.labelframe['lf1'], text='Opc 2Opc 2Opc 2Opc 2Opc 2Op', value=22, variable=esc, bg = 'red', borderwidth = 0)
        # self.r_button[1].pack()
        # self.lb_v.set(self.labelframe['lf1'])

        #listbox
        self.listbox['lb1'] = tk.Listbox(self.frame['f1'], listvariable = self.lb_v, height = 20, width = 40, bg = '#EB5E55', fg = '#FDF0D5', borderwidth = 0)
        self.listbox['lb1'].grid(row = 0, column = 1, sticky = 'nwes')
        
        #scrollbar
        sb_y = ttk.Scrollbar(self.frame['f1'], orient = tk.VERTICAL, command = self.listbox['lb1'].yview) # command é o yview da tabela
        self.listbox['lb1'].configure(yscroll = sb_y.set)
        sb_x = ttk.Scrollbar(self.frame['f1'], orient = tk.HORIZONTAL, command = self.listbox['lb1'].xview) # command é o yview da tabela
        self.listbox['lb1'].configure(xscroll = sb_x.set)
        sb_y.grid(row = 0, column = 2, sticky = 'ns')
        sb_x.grid(row = 1, columnspan = 3, sticky = 'we')

        #entry
        self.entry['task'] = tk.Entry(self.tela)
        self.entry['task'].grid(row = 2, columnspan = 1, padx = 2, pady = 10, ipadx = 70)
        
        sb_x_entry = ttk.Scrollbar(self.tela, orient = tk.HORIZONTAL, command = self.entry['task'].xview) # command é o yview da tabela
        self.entry['task'].configure(xscroll = sb_x_entry.set)
        sb_x_entry.grid(row = 3, column = 0, sticky = 'we')

        #button
        self.botao['b_add'] = tk.Button(self.tela, text = 'Adiciona', bg = '#FDF0D5', borderwidth = 0)
        self.botao['b_add'].grid(row = 4, columnspan = 1, sticky = 'we')

        self.botao['b_insere'] = tk.Button(self.tela, text = 'Insere', bg = '#FDF0D5', borderwidth = 0)
        self.botao['b_insere'].grid(row = 5, columnspan = 1, sticky = 'we')

        self.botao['b_remove'] = tk.Button(self.tela, text = 'Remove', bg = '#C6D8D3', borderwidth = 0)
        self.botao['b_remove'].grid(row = 6, columnspan = 3, sticky = 'we')   

class Control:
    def __init__(self):
        self.tela = tk.Tk()
        #self.tela.geometry('400x400+500+100')

    def inicializa(self, view, model):
        self.view = view
        self.model = model
        self.controlador()

    def controlador(self):
        self.view.botao['b_add']['command'] = lambda: self.processa_entrada('add')
        self.view.botao['b_insere']['command'] = lambda: self.processa_entrada('insere')
        self.view.botao['b_remove']['command'] = lambda: self.processa_entrada('remove')

    def processa_entrada(self, par):
        #pega a linha selecionada no formato de uma tupla
        row_select = self.model.select(self.view.listbox['lb1'].curselection())

        if par == 'add':
            if self.model.campo(self.view.entry['task'].get()):
                self.model.add_tarefa(self.view.entry['task'].get())
                self.view.lb_v.set(self.model.converte_para_lista())
        
        if par == 'insere':
            if self.model.campo(self.view.entry['task'].get()) and self.model.linha_select(row_select):
                self.model.atualiza_tarefa(row_select[0], self.view.entry['task'].get())
                self.view.lb_v.set(self.model.converte_para_lista())

        if par == 'remove':
            
            if self.model.linha_select(row_select):
                self.model.remove_tarefa(row_select[0])
                self.view.lb_v.set(self.model.converte_para_lista())
        

    def executa(self):
        tk.mainloop()

def main():
    #GIU
    to_doList = Lista_deTarefas()
    to_doList.converte_para_lista()
    control = Control()
    view = View(control.tela)
    control.inicializa(view, to_doList)
    control.executa() 

if __name__ == '__main__':
    main()