# screens/category_select.py
import tkinter as tk  # Voor het maken van de GUI
from quiz_game import run_quiz  # Importeer de quiz-logica

def show_category_select_screen(root):
    # Verwijder alle widgets van het vorige scherm (maakt het venster leeg)
    for widget in root.winfo_children():
        widget.destroy()

    # Maak het venster fullscreen zonder titelbalk en randen
    root.overrideredirect(True)  # Geen standaard vensterbalk
    root.geometry("800x480+0+0")  # Zet positie en grootte
    root.configure(bg="black")  # Achtergrondkleur zwart

    # Voeg een toetsencombinatie toe om het programma te sluiten (Ctrl+Q)
    root.bind("<Control-q>", lambda event: root.destroy())

    # Titel bovenaan het scherm
    label = tk.Label(root, text="Kies een categorie", font=("Arial", 24), fg="white", bg="black")
    label.pack(pady=30)

    # Functie om de quiz te starten voor de gekozen categorie
    def start_quiz(category):
        print(f"Start quiz voor categorie: {category}")  # Debugprint
        for widget in root.winfo_children():
            widget.destroy()  # Maak het venster leeg voor de quiz
        root.update()  # Ververs het venster

        # Maak een canvas aan voor de quizvragen
        canvas = tk.Canvas(root, width=800, height=480, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Start de quiz met de gekozen categorie
        run_quiz(root, category, canvas)

    # Lijst van categorieën waaruit gekozen kan worden
    categories = ["Geschiedenis", "Kunst", "Wetenschap"]

    # Maak een knop voor elke categorie
    for cat in categories:
        btn = tk.Button(
            root,
            text=cat,
            font=("Arial", 16),
            width=20,
            command=lambda c=cat: start_quiz(c)  # Start quiz met gekozen categorie
        )
        btn.pack(pady=10)

    # Voeg een knop toe om het programma af te sluiten
    quit_button = tk.Button(
        root,
        text="Afsluiten",
        font=("Arial", 16),
        width=20,
        command=root.destroy  # Sluit het venster
    )
    quit_button.pack(pady=20)
