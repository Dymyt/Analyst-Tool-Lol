from tkinter import *
from tkinter.ttk import *


#Primera ventana
class Win1:
    def __init__(self, master):
        self.master = master
        self.master.geometry("520x650")
        self.master.resizable(0, 0)
        self.master.title("LoL Analysis Tool by Llota")
        self.frameArriba = Frame(self.master)
        self.frameArriba.pack()
        self.imagenTitulo = PhotoImage(file = r"C:\LolTool\IntGraphicImages\title.png")
        self.titulo = Label(self.frameArriba, image = self.imagenTitulo).grid(row = 0, column = 0, columnspan = 2)
        #self.texto1 = Label(self.frameArriba, text = "Herramienta análisis enfrentamiento: ").grid(sticky = "W", row = 1, column = 0, padx = 10, pady = 20)
        #self.texto2 = Label(self.frameArriba, text = "Herramienta análisis equipo: ").grid(sticky = "W", row = 2, column = 0, padx = 10)
        #self.butnew("IR", "2", 1, Win2)
        #self.butnew("IR", "3", 2, Win3)
        self.frameAbajo = Frame(self.master)
        self.frameAbajo.pack()
        self.frameBotones = Frame(self.master)
        self.frameBotones.pack()

        self.imagenSeparacion = PhotoImage(file = r"C:\LolTool\IntGraphicImages\separacion.png")
        self.separacion = Label(self.frameAbajo, image = self.imagenSeparacion).grid(row = 0 , column = 0, columnspan = 3)
        self.aliadoTop = Label(self.frameAbajo, text = "Introduce nombre del campeón a analizar: ").grid(sticky = "W", row = 1, column =0, padx = 10, pady = 5)
        self.entradaAliadoTop = Entry (self.frameAbajo)
        self.entradaAliadoTop.grid(sticky = "W", row = 1, column =1)

        self.aaLAbel = Label(self.frameAbajo, text = "Introduce fecha de inicio: ").grid(sticky = "W", row = 2, column =0, padx = 10, pady = 5)
        self.aa = Entry (self.frameAbajo)
        self.aa.grid(sticky = "W", row = 2, column =1)

        self.botonCargarSonido = Button (self.frameAbajo, text = "GENERAR EXCEL JUGADOR", command = lambda: self.ponerSonidoMinimapa())
        self.botonCargarSonido.grid(row = 3, column = 1, pady= 20)

        self.imagenSeparacionSimple = PhotoImage(file = r"C:\LolTool\IntGraphicImages\separacionsimple.png")
        self.separacionSimple = Label(self.frameAbajo, image = self.imagenSeparacionSimple).grid(row = 6 , column = 0, columnspan = 3)
        self.enemigoTop = Label(self.frameAbajo, text = " Introduce nombre documento .txt: ").grid(sticky = "W", row = 7, column =0, padx = 10, pady = 5)
        self.entradaEnemigoTop = Entry (self.frameAbajo)
        self.entradaEnemigoTop.grid(sticky = "W", row = 7, column =1)

        self.enemigoNombre = Label(self.frameAbajo, text = "Introduce cómo quieres que se llame el documento .xlsx: ").grid(sticky = "W", row = 13, column =0, padx = 10, pady = 5)
        self.entradaEnemigoNombre = Entry (self.frameAbajo)
        self.entradaEnemigoNombre.grid(sticky = "W", row = 13, column =1)
        self.botonCargarDatos = Button(self.frameAbajo, text = "GENERAR EXCEL PARTIDAS").grid(row = 14, column =1, pady= 20 )

        self.separacionSimple2 = Label(self.frameAbajo, image = self.imagenSeparacionSimple).grid(row = 15 , column = 0, columnspan = 3)

        self.entradaCAJA = Entry(self.frameAbajo)
        self.entradaCAJA.grid(row=16,
               column=0,
               ipadx=150, ipady =90, columnspan =3)

    def butnew(self, text, number, fila, _class):
        Button(self.frameArriba, text = text, command = lambda: self.new_window(number, _class)).grid(sticky = "W", row = fila, column = 1)

    def new_window(self,number, _class):
        self.new = Toplevel(self.master)
        _class(self.new, number)

root = Tk()
app = Win1(root)
root.mainloop()