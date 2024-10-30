# Zdeněk Chval, Ondřej Buchar
# hra keyboard king

import tkinter
import random


class App(tkinter.Tk):
    def __init__(self, titulek, sirka, vyska):
        super().__init__()
        self.sirka = sirka  # šířka okna
        self.vyska = vyska  # výška okna
        self.obdelnik_je_vybrany = False  # Proměnná určující jestli je nějaký obdélník vybraný
        self.running = True  # Proměnná určující jestli je hra spuštěná
        self.zvoleny_obdelnik = ""  # Proměnná určující který obdélník je rozsvícený
        self.rychlost = 1  # Počáteční rychlost padání kruhu
        self.rychlost_prepinani_obdelniku = 2000  # Počáteční rychlost přepínání obdelníků
        self.sirka_obdelniku = 40  # Šířka obdélníku
        self.vyska_obdelniku = 20  # Výška obdélníku
        self.pocet_kol = 10  # Počet kol
        self.score = 0  # Scóre
        self.kolo = 1  # Kolo
        self.title(titulek)  # Titulek
        self.canvas = tkinter.Canvas(self, width=sirka, height=vyska, background="white")
        self.obr = tkinter.PhotoImage(file="pozadi.png")  # Obrázek na pozadí

        # Ovládání
        self.canvas.bind("s", self.stisknuti_klavesy)
        self.canvas.bind("d", self.stisknuti_klavesy)
        self.canvas.bind("f", self.stisknuti_klavesy)
        self.canvas.bind("j", self.stisknuti_klavesy)
        self.canvas.bind("k", self.stisknuti_klavesy)
        self.canvas.bind("l", self.stisknuti_klavesy)

        self.titulni_strana() # Zobrazení titulní strany

        self.canvas.focus_set()

    def o_hre(self):
        """
        Otevření okna "O hře" s obrázkem avatara charakterizujícího, jmény autorů a verzí hry
        """
        o_hre_okno = tkinter.Toplevel(self)
        o_hre_okno.title("O hře")
        o_hre_okno.geometry("500x500")
        self.obr2 = tkinter.PhotoImage(file="avatar.png")
        label = tkinter.Label(o_hre_okno, text="Zdeněk Chval, Ondřej Buchar\nVersion 1.0.0", font=("Arial", 12))
        self.avatar = tkinter.Label(o_hre_okno, image=self.obr2)
        self.avatar.pack()
        label.pack(pady=20)

    def napoveda(self):
        """
        Otevření okna "Nápověda" s popisem hry
        """
        napoveda_okno = tkinter.Toplevel(self)
        napoveda_okno.title("Nápověda")
        napoveda_okno.geometry("500x500")
        label = tkinter.Label(napoveda_okno, text="Cílem hry je stisknout správnou klávesu odpovídající označenému obdélníku ve chvíli, kdy na něj dopadne červený kruh, a získat tak body. Ovládejte obdélníky pomocí kláves „s“, „d“, „f“ (pro levé obdélníky) a „j“, „k“, „l“ (pro pravé obdélníky). S každým kolem se rychlost padání kruhu zvyšuje; hra končí po 10 kolech a zobrazí vaše skóre", font=("Arial", 12), wraplength=250)
        label.pack(pady=20)

    def titulni_strana(self):
        """
        Titulní strana
        """
        self.canvas.delete("all")  # smazání všech objektů z plátna (nápis "GAME OVER" a score po skončení hry)
        self.pozadi = self.canvas.create_image(250, 250, anchor='center', image=self.obr)  # pozadí
        self.tlacitko_zacatek_hry = tkinter.Button(self, text="Nová hra", command=self.hra)  # tlačítko pro zahájení hry

        # Menubar s rozbalovacím menu
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
        """
        Nápis score a aktuálního kola
        """
        self.kolo_napis = self.canvas.create_text(62, 50, text=f"Kolo: {str(self.kolo)}/{str(self.pocet_kol)}", font=f"Arial 17", fill="black")
        self.dobre = self.canvas.create_text(55, 100, text=f"Score: {str(self.score)}", font=f"Arial 17", fill="black")

    def stisknuti_klavesy(self, event):
        """
        Zvolení příslušného obdélníku podle stisknuté klávesy
        """
        # Uživatel může zvolit obdélník jen jednou za kolo (od rozsvícení jednoho obdélníku do jeho zhasnutí)
        if not self.obdelnik_je_vybrany:
            self.obdelnik_je_vybrany = True
            if event.keysym in "sdfjkl":
                index = "sdfjkl".index(event.keysym)
                self.canvas.itemconfig(self.obdelniky[index], fill="black")  # Změna barvy vybraného obdélníku
                self.canvas.moveto(self.kruh, 40 + index * (self.sirka_obdelniku + 40), self.canvas.coords(self.kruh)[1])  # Přesun kruhu nad vybraný obdélník

                # Pokud se zvolený obdélník shoduje s rozsvíceným obdélníkem score se zvýší o 1
                if event.keysym == self.vybrany_obdelnik:
                    self.score += 1
                    self.canvas.itemconfig(self.dobre, text=(f"Score: {str(self.score)}"))

    def hra(self):
        """
        Začátek hry po stisknutí tlačítka "Nová hra"
        """
        self.tlacitko_zacatek_hry.destroy()  # Skrytí tlačítka pro spuštění hry
        self.menu.destroy()  # Skrytí menu 
        self.score_napis()  # Zobrazení score a aktuálního kola
        self.obdelniky = []  # List s obdélníků

        # Vytvoření obdélníků
        for i in range(6):
            obdelnik = self.canvas.create_rectangle(
                40 + i * (self.sirka_obdelniku + 40), 
                self.vyska - 20, 
                40 + (i + 1) * self.sirka_obdelniku + i * 40, 
                self.vyska - 20 - self.vyska_obdelniku, 
                fill="white", 
                outline="black"
            )
            self.obdelniky.append(obdelnik)  # Přidání obdélníku do listu
        self.nahodny_vyber_obdelniku()  # nahodně rozsvítí jeden z obdélníků
        self.vytvoreni_kruhu()  # vytvoření kruhu
        self.tik()

    def reset_barev(self):
        """
        Změna barvy všech obdélníků na bílou
        """
        for obdelnik in self.obdelniky:
            self.canvas.itemconfig(obdelnik, fill="white")

    def nahodny_vyber_obdelniku(self):
        """
        Náhodně rozsvítí jeden obdélník
        """
        # resetování barev všech obdélníků na bílou
        self.obdelnik_je_vybrany = False
        self.reset_barev()

        # zvolení náhodného obdélníku a změna jeho barvy na šedou
        obdelnik = random.choice("sdfjkl")
        self.vybrany_obdelnik = obdelnik
        index = "sdfjkl".index(obdelnik)
        self.canvas.itemconfig(self.obdelniky[index], fill="grey")

        self.after(self.rychlost_prepinani_obdelniku, self.nahodny_vyber_obdelniku) # Rozsvícení jiného obdélníku po určité době

    def vytvoreni_kruhu(self):
        """
        Vytvoření kruhu který indikuje jak dlouhé je každé kolo
        """
        self.random_x1 = random.choice([40, 80+self.sirka_obdelniku, 120+2*self.sirka_obdelniku, 160+3*self.sirka_obdelniku, 200+4*self.sirka_obdelniku, 240+5*self.sirka_obdelniku,])
        self.kruh = self.canvas.create_oval(self.random_x1, 0, self.random_x1+self.sirka_obdelniku, self.sirka_obdelniku, fill="red", outline="red", tag = "kruh")

    def padani_kruhu(self):
        """
        Pohyb kruhu směrem dolů
        """
        self.canvas.move(self.kruh, 0, self.rychlost)

        # Když kruh "spadne dolů", číslo kola se zvýší o 1, zvýšíse rychlost přepínání obdélníků a rychlost padání kruhu a vytvoří se nový kruh v horní části okna
        if self.canvas.coords(self.kruh)[1] > self.vyska:
            self.canvas.delete("kruh")
            self.vytvoreni_kruhu()
            self.rychlost = self.rychlost * (2 ** (1 / self.pocet_kol))
            self.rychlost_prepinani_obdelniku = round(2000/(self.rychlost))
            self.kolo += 1
            self.canvas.itemconfig(self.kolo_napis, text=f"Kolo: {str(self.kolo)}/{str(self.pocet_kol)}")

        # Na konci posledního kola se zobrazí nápis "GAME OVER" a dosažené score
        if self.kolo == self.pocet_kol+1:
            self.canvas.delete("all")
            self.napis_game_over = self.canvas.create_text(250, 250, text="GAME OVER", font=f"Arial 50", fill="black")
            self.napis_dosazene_score = self.canvas.create_text(250, 300, text=f"Vaše score: {self.score}", font=f"Arial 25", fill="black")
            self.after(3000, self.reset_hra)  # po 3 sekundách se zobrazí zpět úvodní obrazovka
            self.running = False
    
    def reset_hra(self):
        """
        Resetuje score, číslo kola, smaže vše z plátna a zobrazí úvodní stránku
        """
        self.canvas.delete("all")
        self.score = 0
        self.kolo = 1
        self.titulni_strana()


    def tik(self):
        """
        Animace padání kruhu
        """
        if self.running == True:
            self.padani_kruhu()
            self.after(10, self.tik)

    def run(self):
        """
        Spuštění aplikace
        """
        self.mainloop()


# Hlavní program
if __name__ == "__main__":
    app = App("keyboardking", 500, 500)  # Vytvoření instance aplikace
    app.run()  # Spuštění aplikace
