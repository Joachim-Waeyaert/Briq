# screens/quiz_game.py

# Importeer de benodigde libraries
import tkinter as tk  # Voor het maken van de grafische gebruikersinterface (GUI)
from gtts import gTTS  # Voor tekst-naar-spraak (Google Text-to-Speech)
from io import BytesIO  # Voor het werken met in-memory bestanden (zoals audio)
import pygame  # Voor het afspelen van audio
import random  # Voor het willekeurig kiezen van vragen en uitdagingen
import speech_recognition as sr  # Voor spraakherkenning (microfooninput omzetten naar tekst)
from sentence_transformers import SentenceTransformer, util  # Voor semantische vergelijking van antwoorden
import sys  # Voor het volledig afsluiten van het programma

# Definieer de categorieën en bijbehorende vragen als een dictionary
categorie_vragen = {
    "Geschiedenis": [
        # Elke tuple bevat een vraag en het juiste antwoord
        ("In welk jaar werd België onafhankelijk?", "1830"),
        ("Wie was de eerste koning van België?", "Leopold I"),
        ("Wanneer eindigde de Tweede Wereldoorlog?", "1945"),
        ("Welke Belgische stad werd zwaar gebombardeerd tijdens WOII?", "Luik"),
        ("Wat is de naam van de Belgische kolonie tot 1960?", "Congo"),
        ("Wie was premier van België in de jaren 80?", "Wilfried Martens"),
        ("Wat gebeurde er op 21 juli in België?", "Nationale feestdag"),
        ("Wie was de Belgische koning tijdens WOI?", "Albert I"),
        ("Wat was het Marshallplan?", "Economisch hulpprogramma"),
        ("Welke muur viel in 1989?", "Berlijnse Muur")
    ],
    "Kunst": [
        ("Wie schilderde de Mona Lisa?", "Leonardo da Vinci"),
        ("Wie was Vincent van Gogh?", "Schilder"),
        ("Welke Belgische schilder is bekend van surrealistische kunst?", "René Magritte"),
        ("Wie schilderde De Nachtwacht?", "Rembrandt"),
        ("Wat is art nouveau?", "Architectuurstijl"),
        ("Welke Belgische stad is beroemd om stripmuren?", "Brussel"),
        ("Wie creëerde Suske en Wiske?", "Willy Vandersteen"),
        ("Wat is het Louvre?", "Museum in Parijs"),
        ("Wie schreef 'Het verdriet van België'?", "Hugo Claus"),
        ("Wat is impressionisme?", "Schilderstijl")
    ],
    "Wetenschap": [
        ("Wie formuleerde de relativiteitstheorie?", "Albert Einstein"),
        ("Wat is zwaartekracht?", "Aantrekkingskracht"),
        ("Wat doet een telescoop?", "Kijkt naar sterren"),
        ("Wat is penicilline?", "Antibioticum"),
        ("Wat is een atoom?", "Kleinste deeltje"),
        ("Wat meet een thermometer?", "Temperatuur"),
        ("Wat is DNA?", "Erfelijk materiaal"),
        ("Wat doet een microscoop?", "Vergroot kleine dingen"),
        ("Wie ontdekte de zwaartekracht?", "Isaac Newton"),
        ("Wat is fotosynthese?", "Proces in planten")
    ]
}

# Lijst met uitdagingen die gegeven worden bij een fout antwoord
uitdagingen = [
    "Wissel van kant met je dubbelpartner",
    "Speel met je niet-dominante hand",
    "Speel een punt waarbij je alleen met je backhand mag serveren.",
    "Geef je racket achter je rug door totdat je terug bij je dominante hand komt.",
    "Geef met je racket een tik op de grond."
]

# Laad het taalmodel voor semantische vergelijking van antwoorden
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Initialiseer de audio-engine van pygame
pygame.mixer.init()
pygame.display.init()
pygame.display.set_mode((1, 1))  # Nodig voor sommige systemen om audio te laten werken

def speel_audio(tekst, root):
    """
    Zet tekst om naar spraak en speel deze af via de speakers.
    """
    mp3_fp = BytesIO()  # In-memory bestand voor audio
    tts = gTTS(tekst, lang='nl')  # Maak een TTS-object aan voor Nederlandse tekst
    tts.write_to_fp(mp3_fp)  # Schrijf de audio naar het in-memory bestand
    mp3_fp.seek(0)  # Zet de pointer aan het begin
    pygame.mixer.music.load(mp3_fp, 'mp3')  # Laad de audio in pygame
    pygame.mixer.music.play()  # Speel de audio af
    while pygame.mixer.music.get_busy():
        root.update()  # Houd de GUI actief tijdens het afspelen
        pygame.time.wait(10)

def luister_naar_antwoord(root):
    """
    Luister naar het antwoord van de gebruiker via de microfoon en zet dit om naar tekst.
    Geeft een foutmelding als er geen spraak wordt gehoord of als de spraak niet wordt herkend.
    """
    recognizer = sr.Recognizer()  # Maak een spraakherkenner aan
    with sr.Microphone() as source:
        print("Microfoon aanpassen aan omgevingsgeluid...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Kalibreer op achtergrondgeluid

        try:
            print("Luisteren naar antwoord...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Neem audio op
            antwoord = recognizer.recognize_google(audio, language='nl-NL')  # Herken de spraak
            print(f"Herkenning voltooid: {antwoord}")
            return antwoord.strip().lower()  # Geef het antwoord terug in kleine letters
        except sr.WaitTimeoutError:
            print("Er werd geen spraak gedetecteerd binnen de tijdslimiet.")
            speel_audio("Ik heb je niet verstaan. Probeer het opnieuw.", root)  # Geef melding bij geen spraak
            return luister_naar_antwoord(root)  # Probeer opnieuw
        except sr.UnknownValueError:
            print("Kon de spraak niet begrijpen.")
            speel_audio("Ik kon je niet verstaan. Probeer het opnieuw.", root)  # Geef melding bij onherkenbare spraak
            return luister_naar_antwoord(root)  # Probeer opnieuw
        except sr.RequestError as e:
            print(f"Probleem met de spraakherkenning: {e}")
            speel_audio("Er is een probleem met de spraakherkenning.", root)  # Geef melding bij fout
            return None

def toon_canvas_tekst(canvas, tekst, kleur="white", achtergrond="black"):
    """
    Toon tekst gecentreerd op het canvas met opgegeven kleuren.
    """
    canvas.delete("all")  # Wis het canvas
    canvas.config(bg=achtergrond)  # Stel achtergrondkleur in
    canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2,
        text=tekst,
        fill=kleur,
        font=("Arial", 24),
        anchor="center",
        width=canvas.winfo_width() - 100
    )

def toon_eindscherm(root, canvas, punten_team1, punten_team2):
    """
    Toon het eindscherm met de scores van beide teams.
    """
    canvas.delete("all")  # Wis het canvas
    canvas.config(bg="black")  # Zet achtergrond op zwart
    eindtekst = f"Einde van de quiz!\n\nTeam 1: {punten_team1} punten\nTeam 2: {punten_team2} punten"
    canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2,
        text=eindtekst,
        fill="white",
        font=("Arial", 28),
        anchor="center"
    )
    speel_audio(f"Einde van de quiz. Team 1 heeft {punten_team1} punten. Team 2 heeft {punten_team2} punten.", root)
    # Voeg een knop toe om het programma af te sluiten
    btn = tk.Button(root, text="Afsluiten", font=("Arial", 16), command=root.destroy)
    btn.place(relx=0.5, rely=0.8, anchor="center")

def run_quiz(root, category, canvas):
    """
    Start de quiz voor een bepaalde categorie.
    Wisselt beurten tussen team 1 en team 2, houdt punten bij, en stopt als 'stop' wordt gezegd.
    """
    root.update()  # Update het venster
    vragen = categorie_vragen[category]  # Haal de vragen op
    random.shuffle(vragen)  # Schud de volgorde
    punten_team1 = 0  # Puntentelling team 1
    punten_team2 = 0  # Puntentelling team 2
    beurt_team1 = True  # True = team 1, False = team 2

    for i, (vraag, juist_antwoord) in enumerate(vragen):
        huidig_team = "Team 1" if beurt_team1 else "Team 2"  # Bepaal welk team aan de beurt is
        while True:
            toon_canvas_tekst(canvas, f"{huidig_team}:\n{vraag}", kleur="white", achtergrond="black")  # Toon de vraag
            root.update()
            speel_audio(f"{huidig_team}: {vraag}", root)  # Lees de vraag voor
            antwoord = luister_naar_antwoord(root)  # Luister naar het antwoord
            if antwoord is None:
                print("Geen antwoord ontvangen. Probeer opnieuw.")
                continue  # Vraag opnieuw om een antwoord
            if antwoord.strip().lower() == "stop":  # Stop de quiz als 'stop' wordt gezegd
                toon_eindscherm(root, canvas, punten_team1, punten_team2)
                return

            print(f"Herkenning: '{antwoord}', Correct antwoord: '{juist_antwoord}'")

            # Vergelijk het antwoord semantisch met het juiste antwoord
            embeddings = model.encode([antwoord, juist_antwoord.lower()])
            similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

            if similarity > 0.6:  # Drempelwaarde voor overeenstemming
                toon_canvas_tekst(canvas, "Juist!", kleur="white", achtergrond="green")
                root.update()
                speel_audio("Juist!", root)
                if beurt_team1:
                    punten_team1 += 1  # Punt voor team 1
                else:
                    punten_team2 += 1  # Punt voor team 2
                break
            else:
                toon_canvas_tekst(canvas, f"Fout!\nHet juiste antwoord is: {juist_antwoord}", kleur="white", achtergrond="red")
                root.update()
                speel_audio(f"Fout! Het juiste antwoord is: {juist_antwoord}", root)

                uitdaging = random.choice(uitdagingen)  # Kies een willekeurige uitdaging
                toon_canvas_tekst(canvas, f"Uitdaging:\n{uitdaging}", kleur="white", achtergrond="orange")
                root.update()
                speel_audio(f"Je krijgt een uitdaging: {uitdaging}", root)
                break

        beurt_team1 = not beurt_team1  # Wissel van team na elke vraag
        pygame.time.wait(2000)  # Wacht 2 seconden voor de volgende vraag

    toon_eindscherm(root, canvas, punten_team1, punten_team2)  # Toon eindscherm als quiz klaar is

def stop_program(event=None):
    """
    Sluit het programma volledig af.
    """
    print("Programma wordt afgesloten...")
    root.destroy()  # Sluit het Tkinter-venster
    sys.exit()  # Beëindig het programma volledig

if __name__ == "__main__":
    # Startpunt van het programma
    root = tk.Tk()  # Maak het hoofdvenster aan
    root.bind("<Control-q>", stop_program)  # Ctrl+Q sluit het programma af

    # Maak een canvas voor de quiz
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Start de quiz met de categorie 'Geschiedenis'
    run_quiz(root, "Geschiedenis", canvas)

    root.mainloop()  # Start de Tkinter event loop