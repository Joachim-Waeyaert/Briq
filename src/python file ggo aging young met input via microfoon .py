from gtts import gTTS
from io import BytesIO
import pygame
import random
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util

# Vragenlijst en antwoorden
vragen = [
    ("In welk jaar werd België onafhankelijk?", "1830"),
    ("Wie was de eerste koning van België?", "Leopold I"),
    ("Wat is de hoofdstad van België?", "Brussel"),
    ("Wie schreef 'De Leeuw van Vlaanderen'?", "Hendrik Conscience"),
    ("Welke bekende surrealistische schilder komt uit België?", "René Magritte"),
    ("Wat is de bekendste diamantstad in België?", "Antwerpen"),
    ("Wat is de traditionele Belgische saus die vaak bij frieten wordt gegeten?", "Mayonaise"),
    ("Welk bekend abdijbier uit België wordt in een Trappistenabdij gebrouwen en is internationaal geliefd?", "Chimay"),
    ("Wat is de naam van de clown die jarenlang de hoofdrol speelde in het populaire kinderprogramma 'Pipo'?", "Pipo de Clown"),
    ("Welke Belgische wielrenner, ook wel 'De Kannibaal' genoemd, won meerdere edities van de Ronde van Vlaanderen?", "Eddy Merckx"),
    ("Welke Europese instelling, die een centrale rol speelt in het wetgevingsproces, heeft haar hoofdkantoor in Brussel?", "Europese Commissie"),
    ("Wat is de naam van de rivier die historisch door Brussel stroomt?", "Zenne"),
    ("Welke Belgische stad, bekend om haar pittoreske grachten en middeleeuwse gebouwen, wordt vaak 'het Venetië van het Noorden' genoemd?", "Brugge"),
    ("Wie was de bekende Belgische premier in de jaren '80, beroemd om zijn rol in de federale hervormingen?", "Wilfried Martens"),
    ("Wanneer is de nationale feestdag van België?", "21 juli"),
    ("Welke Belgische stripfiguur werd gecreëerd door Hergé?", "Kuifje (Tintin)"),
    ("Welk bekend Belgisch chocolademerk staat internationaal bekend om zijn luxe chocolade?", "Godiva"),
    ("Welke Belgische zanger verwierf in de jaren '60 internationale faam met zijn Franstalige chansons?", "Jacques Brel"),
    ("Welke Belgische popgroep scoorde grote hits in de jaren '80 met Nederlandstalige nummers?", "Clouseau"),
    ("Wat is de traditionele Belgische maaltijd die bestaat uit stoofvlees met bier en vaak wordt geserveerd met frieten?", "Carbonnade flamande"),
    ("Welke Belgische stad organiseert de bekende Gentse Floraliën, een grote bloemen- en plantenexpositie?", "Gent"),
    ("Wie was de ingenieur die het Atomium in Brussel ontwierp?", "André Waterkeyn"),
    ("Wat is de naam van de heuvelachtige streek in het zuiden van België, beroemd om zijn natuur en recreatiemogelijkheden?", "De Ardennen"),
    ("Hoe noemt men de beroemde Belgische lekkernij die vaak met slagroom of chocolade wordt gegeten?", "Belgische wafel"),
    ("Wie was de beroemde Vlaamse barokschilder, bekend van werken als 'De Aanbidding der Koningen'?", "Peter Paul Rubens"),
    ("In welk jaar vond de Slag bij Waterloo plaats?", "1815"),
    ("Welke Belgische universiteit, opgericht in 1425, is een van de oudste in Europa?", "KU Leuven"),
    ("Welke rivier is van groot economisch belang voor de haven van Antwerpen?", "Schelde"),
    ("Welke Belgische stripreeks, gecreëerd door Edgar P. Jacobs, draait om de avonturen van een detective en zijn vriend?", "Blake en Mortimer"),
    ("Welke Belgische stad is beroemd om het jaarlijkse carnaval met de traditionele Gilles?", "Binche"),
    ("In welk jaar werd België bevrijd van de Duitse bezetting tijdens de Tweede Wereldoorlog?", "1944"),
    ("Wie was de Belgische koning tijdens de Eerste Wereldoorlog?", "Albert I"),
    ("Welke rivier stroomt door de stad Luik?", "Maas"),
    ("In welke Belgische stad vind je het Stoclet Palace, een icoon van art nouveau architectuur?", "Brussel"),
    ("Welke Belgische chocolatier wordt beschouwd als de uitvinder van de praline?", "Neuhaus"),
    ("Welke Belgische stad werd in het begin van de 20e eeuw wel eens 'het kleine Parijs' genoemd?", "Antwerpen"),
    ("Welke bekende Belgische stripreeks, gecreëerd door Willy Vandersteen, vertelt over de avonturen van Suske en Wiske?", "Suske en Wiske"),
    ("Hoe noemt men het klassieke Belgische gerecht dat bestaat uit mosselen en frieten?", "Moules-frites"),
    ("Wat is de naam van het populaire Belgische spelprogramma waarin spelers proberen zoveel mogelijk punten te scoren door woorden te vormen?", "Lingo"),
    ("Welke Belgische koningin, echtgenote van Koning Baudouin, werd zeer geliefd door het volk?", "Koningin Fabiola"),
    ("Welke Belgische stad staat bekend om de beroemde Meir, een van de drukste winkelstraten van België?", "Antwerpen"),
    ("Hoe heet de hoogste professionele voetbalcompetitie in België?", "Jupiler Pro League"),
    ("Welke bekende Belgische acteur speelde een hoofdrol in de film 'De Zaak Alzheimer'?", "Koen De Bouw"),
    ("Wat is de hoofdstad van de Belgische provincie Limburg?", "Hasselt"),
    ("Hoe heette de Belgische publieke omroep die in de jaren '70 en '80 bekend was om haar televisieprogramma's?", "BRT"),
    ("Welke bekende Belgische komiek en acteur speelde in de film 'Koko Flanel'?", "Urbanus"),
    ("Wat is de naam van het volkslied dat vaak als symbool van Vlaanderen wordt beschouwd?", "De Vlaamse Leeuw"),
    ("Welke beroemde Belgische architect wordt beschouwd als een pionier van de art nouveau-beweging?", "Victor Horta"),
    ("Welke Belgische schrijver is bekend van het boek 'Het verdriet van België'?", "Hugo Claus")
]
def SpeechToText():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("Luisteren...")
        r.pause_threshold = 1
        audio = r.listen(source)
    print("Recognizing...")
    antwoord = r.recognize_google(audio, language='nl-NL')
    print(f"Je zei: {antwoord}")
    return antwoord
# Lijst van uitdagingen
uitdagingen = [
    "Wissel van kant met je dubbelpartner",
    "Speel met je niet-dominante hand",
    "Speel een punt waarbij je alleen met je backhand mag serveren.",
    "Geef je racket achter je rug door totdat je terug bij je dominante hand komt.",
    "Geef met je racket een tik op de grond."
]

# Initialiseer pygame mixer en display
pygame.mixer.init()
pygame.display.init()
pygame.display.set_mode((1, 1))

# Schud de lijst met vragen
random.shuffle(vragen)
# Functie om audio af te spelen
def speel_audio(tekst):
    mp3_fp = BytesIO()
    tts = gTTS(tekst, lang='nl')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

# Functie om invoer te controleren
def luister_naar_antwoord():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Spreek nu...")
        speel_audio("Spreek nu je antwoord uit")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            antwoord = recognizer.recognize_google(audio, language='nl-NL')
            print("Je zei:", antwoord)
            return antwoord.strip().lower()
        except sr.UnknownValueError:
            print("Ik kon je niet verstaan. Probeer het opnieuw.")
            speel_audio("Ik kon je niet verstaan. Probeer het opnieuw.")
            return luister_naar_antwoord()
        except sr.RequestError:
            print("Er is een probleem met de spraakherkenning.")
            speel_audio("Er is een probleem met de spraakherkenning.")
            return None
        
# Start de quiz
def start_quiz(vragen):
    for vraag, juist_antwoord in vragen:
        while True:
            print(vraag)
            speel_audio(vraag)

            print("Aan het luisteren")
            print(f"Juist antwoord: {juist_antwoord}")
            antwoord = wacht_op_gebruikersinput(juist_antwoord)

            if antwoord == "HERHAAL":
                continue  # Vraag opnieuw afspelen
            break  # Ga naar de volgende vraag

        # Wacht op spatiebalk om door te gaan
        print("Druk op spatie om door te gaan naar de volgende vraag...")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                break
# Initialiseer SBERT-model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Functie om invoer te controleren
def wacht_op_gebruikersinput(juist_antwoord):
    antwoord = luister_naar_antwoord()
    if antwoord is None:
        return "HERHAAL"
    
    # Bereken de gelijkenis tussen het antwoord en het juiste antwoord
    embeddings = model.encode([antwoord, juist_antwoord.lower()])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    
    if similarity > 0.6:  # Drempelwaarde voor overeenstemming
        print("Juist!")
        speel_audio("Juist!")
        return True
    else:
        print(f"Fout! Het juiste antwoord is: {juist_antwoord}")
        speel_audio(f"Fout! Het juiste antwoord is: {juist_antwoord}")

        # Kies een willekeurige uitdaging
        uitdaging = random.choice(uitdagingen)
        print(f"Uitdaging: {uitdaging}")
        speel_audio(f"Je krijgt een uitdaging! {uitdaging}")

        return False
# Start de quiz
start_quiz(vragen)