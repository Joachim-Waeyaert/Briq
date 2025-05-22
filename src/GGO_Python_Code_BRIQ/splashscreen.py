import tkinter as tk  # Voor het maken van de GUI (grafische gebruikersinterface)
from PIL import Image, ImageTk, ImageEnhance  # Voor het laden, tonen en aanpassen van afbeeldingen

class SplashScreen:
    def __init__(self, root, on_finish):
        self.root = root  # Hoofdvenster van Tkinter
        self.on_finish = on_finish  # Functie die wordt aangeroepen als het splashscreen klaar is

        # Maak het venster zonder titelbalk en zet het op 800x480 pixels
        self.root.overrideredirect(True)  # Geen standaard vensterbalk
        self.root.geometry("800x480+0+0")  # Zet positie en grootte

        # Voeg toetsencombinatie toe om het programma te sluiten (Ctrl+Q)
        self.root.bind("<Control-q>", lambda event: self.root.destroy())

        # Maak een canvas aan om de afbeelding op te tonen
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Probeer de afbeelding te laden
        try:
            self.original_image = Image.open(r"/home/rgm/Documents/ggo-healthy-aging/assets/briq.png").convert("RGBA")
            # Schaal de afbeelding naar 800x480 pixels
            self.original_image = self.original_image.resize((800, 480))
            self.alpha = 0.0  # Start met volledig transparant
            self.tk_image = None  # Houdt de PhotoImage referentie bij
            self.image_id = None  # Houdt het canvas image object bij
            # Start het fade-in effect
            self.fade_in()
        except FileNotFoundError:
            print("Afbeelding niet gevonden. Toon zwart scherm met 'logo'.")
            self.canvas.create_rectangle(0, 0, 800, 480, fill="black", outline="black")
            self.canvas.create_text(
                400, 240, text="logo", fill="white", font=("Arial", 48), anchor=tk.CENTER
            )
            self.root.after(2000, self.finish)  # Toon 2 seconden, dan verder

    def fade_in(self):
        # Laat de afbeelding langzaam verschijnen door de helderheid te verhogen
        if self.alpha < 1.0:
            self.alpha += 0.05  # Verhoog de helderheid
            self.update_image()  # Update de afbeelding op het canvas
            self.root.after(50, self.fade_in)  # Wacht 50 ms en ga verder
        else:
            self.root.after(2000, self.fade_out)  # Na 2 seconden start fade-out

    def fade_out(self):
        # Laat de afbeelding langzaam verdwijnen door de helderheid te verlagen
        if self.alpha > 0.0:
            self.alpha -= 0.05  # Verlaag de helderheid
            self.update_image()  # Update de afbeelding op het canvas
            self.root.after(50, self.fade_out)  # Wacht 50 ms en ga verder
        else:
            self.finish()  # Ga verder naar het volgende scherm

    def update_image(self):
        # Pas de helderheid van de afbeelding aan volgens self.alpha
        enhancer = ImageEnhance.Brightness(self.original_image)
        faded = enhancer.enhance(self.alpha)
        self.tk_image = ImageTk.PhotoImage(faded)  # Zet om naar een PhotoImage voor Tkinter

        if self.image_id:
            self.canvas.delete(self.image_id)  # Verwijder vorige afbeelding

        # Plaats de afbeelding gecentreerd op het canvas
        self.image_id = self.canvas.create_image(400, 240, image=self.tk_image, anchor=tk.CENTER)

    def finish(self):
        self.root.destroy()
        self.on_finish()

def main():
    root = tk.Tk()  # Maak het hoofdvenster aan
    SplashScreen(root, on_finish=lambda: print("klaar"))  # Start het splashscreen, print "klaar" als het klaar is
    root.mainloop()  # Start de Tkinter event loop

if __name__ == "__main__":
    main()  # Start het programma als dit bestand direct wordt uitgevoerd