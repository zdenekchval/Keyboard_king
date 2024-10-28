
import tkinter
import random


class App(tkinter.Tk):
    def __init__(self, titulek, sirka, vyska):
        super().__init__()
        self.sirka = sirka
        self.vyska = vyska
        self.obdelnik_je_vybrany = False
        self.running = True
        self.rychlost = 1
        self.rychlost_prepinani_obdelniku = 2000
        self.sirka_obdelniku = 40
        self.vyska_obdelniku = 20
        self.pocet_kol = 10
        self.score = 0
        self.kolo = 1
        self.title(titulek)
        self.canvas = tkinter.Canvas(self, width=sirka, height=vyska, background="white")

        self.canvas.bind("<Button-1>", self.ovladani_mysi)
        self.canvas.bind("s", self.stisknuti_klavesy)
        self.canvas.bind("d", self.stisknuti_klavesy)
        self.canvas.bind("f", self.stisknuti_klavesy)
        self.canvas.bind("j", self.stisknuti_klavesy)
        self.canvas.bind("k", self.stisknuti_klavesy)
        self.canvas.bind("l", self.stisknuti_klavesy)

        self.titulni_strana()

        self.canvas.focus_set()

    def o_hre(self):
        o_hre_okno = tkinter.Toplevel(self)
        o_hre_okno.title("O hře")
        o_hre_okno.geometry("300x200")
        label = tkinter.Label(o_hre_okno, text="Verze: 1.0\nAutor: Vaše jméno", font=("Arial", 12))
        label.pack(pady=20)

    def napoveda(self):
        napoveda_okno = tkinter.Toplevel(self)
        napoveda_okno.title("Nápověda")
        napoveda_okno.geometry("300x200")
        text = ("text")
        label = tkinter.Label(napoveda_okno, text=text, font=("Arial", 12), wraplength=250)
        label.pack(pady=20)

    def titulni_strana(self):
        self.canvas.delete("all")
        self.tlacitko_zacatek_hry = tkinter.Button(self, text="Nová hra", command=self.hra)
        self.menu = tkinter.Menu(self)
        
        self.menu = tkinter.Menu(self)
        self.config(menu=self.menu)

        file_menu = tkinter.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Nápověda", command=self.napoveda)
        file_menu.add_command(label="O hře", command=self.o_hre)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="Help", menu=file_menu)

        self.canvas.pack()
        self.tlacitko_zacatek_hry.pack()
    

    def score_napis(self):
        self.kolo_napis = self.canvas.create_text(62, 50, text=f"Kolo: {str(self.kolo)}/{str(self.pocet_kol)}", font=f"Arial 17", fill="red")
        self.dobre = self.canvas.create_text(55, 100, text=f"Score: {str(self.score)}", font=f"Arial 17", fill="red")
    
    def ovladani_mysi(self, event):
        print(event.x, event.y)

    def stisknuti_klavesy(self, event):
        if not self.obdelnik_je_vybrany:
            self.obdelnik_je_vybrany = True
            if event.keysym in "sdfjkl":
                index = "sdfjkl".index(event.keysym)
                self.canvas.itemconfig(self.obdelniky[index], fill="black")
                self.canvas.moveto(self.kruh, 40 + index * (self.sirka_obdelniku + 40), self.canvas.coords(self.kruh)[1])
                if event.keysym == self.vybrany_obdelnik:
                    self.score += 1
                    self.canvas.itemconfig(self.dobre, text=(f"Score: {str(self.score)}"))

    def hra(self):
        self.tlacitko_zacatek_hry.destroy()
        self.menu.destroy()
        self.score_napis()
        self.obdelniky = []
        for i in range(6):
            obdelnik = self.canvas.create_rectangle(
                40 + i * (self.sirka_obdelniku + 40), 
                self.vyska - 20, 
                40 + (i + 1) * self.sirka_obdelniku + i * 40, 
                self.vyska - 20 - self.vyska_obdelniku, 
                fill="white", 
                outline="black"
            )
            self.obdelniky.append(obdelnik)
        self.zvoleny_obdelnik = self.obdelniky[0]
        self.nahodny_vyber_obdelniku()
        self.vytvoreni_kruhu()
        self.tik()

    def reset_barev(self):
        for obdelnik in self.obdelniky:
            self.canvas.itemconfig(obdelnik, fill="white")
        self.running = True

    def nahodny_vyber_obdelniku(self):
        self.obdelnik_je_vybrany = False
        self.reset_barev()
        obdelnik = random.choice("sdfjkl")
        self.vybrany_obdelnik = obdelnik
        index = "sdfjkl".index(obdelnik)
        self.canvas.itemconfig(self.obdelniky[index], fill="grey")
        self.after(self.rychlost_prepinani_obdelniku, self.nahodny_vyber_obdelniku)

    def vytvoreni_kruhu(self):
        
        self.random_x1 = random.choice([40, 80+self.sirka_obdelniku, 120+2*self.sirka_obdelniku, 160+3*self.sirka_obdelniku, 200+4*self.sirka_obdelniku, 240+5*self.sirka_obdelniku,])
        self.kruh = self.canvas.create_oval(self.random_x1, 0, self.random_x1+self.sirka_obdelniku, self.sirka_obdelniku, fill="red", outline="red", tag = "kruh")

    def padani_kruhu(self):
        self.canvas.move(self.kruh, 0, self.rychlost)
        if self.canvas.coords(self.kruh)[1] > self.vyska:
            self.canvas.delete("kruh")
            self.vytvoreni_kruhu()
            print(self.rychlost)
            print(self.rychlost_prepinani_obdelniku)
            self.rychlost = (1.3*self.rychlost)**(2/3)
            self.rychlost_prepinani_obdelniku = round(2000/(self.rychlost))
            self.kolo += 1
            self.canvas.itemconfig(self.kolo_napis, text=f"Kolo: {str(self.kolo)}/{str(self.pocet_kol)}")
        if self.kolo == self.pocet_kol+1:
            self.canvas.delete("all")
            self.napis_game_over = self.canvas.create_text(250, 250, text="GAME OVER", font=f"Arial 50", fill="red")
            self.napis_dosazene_score = self.canvas.create_text(250, 300, text=f"Vaše score: {self.score}", font=f"Arial 25", fill="red")
            self.after(3000, self.reset_hra)
            self.running = False
    
    def reset_hra(self):
        self.canvas.delete("all")
        self.score = 0
        self.kolo = 1
        self.titulni_strana()


    def tik(self):
        if self.running == True:
            self.padani_kruhu()
            self.after(10, self.tik)

    def run(self):
        self.mainloop()



if __name__ == "__main__":
    app = App("keyboardking", 500, 500)
    app.run()