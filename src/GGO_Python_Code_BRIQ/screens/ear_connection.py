import tkinter as tk  # Voor het maken van de GUI
import subprocess  # Om systeemcommando's uit te voeren (bluetoothctl)
from screens.category_select import show_category_select_screen  # Importeer het volgende scherm

# MAC-adressen van de koptelefoons (vervang door de juiste adressen)
team_1_mac_address = "F0:A9:68:19:27:24"  # Team 1 koptelefoon
team_2_mac_address = "84:D3:52:F3:C9:76"  # Team 2 koptelefoon

# Functie om verbinding te maken met een Bluetooth-apparaat
def connect_bluetooth_device(mac_address, team_name, canvas):
    try:
        if not mac_address:
            toon_canvas_tekst(canvas, f"MAC-adres voor {team_name} ontbreekt", kleur="red")
            return
        
        # Voer het bluetoothctl commando uit om verbinding te maken
        result = subprocess.run(["bluetoothctl", "connect", mac_address], capture_output=True, text=True)
        
        if "Connection successful" in result.stdout:
            toon_canvas_tekst(canvas, f"Verbonden met {team_name}: {mac_address}", kleur="green")
        else:
            toon_canvas_tekst(canvas, f"Verbinding mislukt met {team_name}: {mac_address}", kleur="red")
    except Exception as e:
        toon_canvas_tekst(canvas, f"Fout bij {team_name}: {str(e)}", kleur="red")

# Functie om naar het volgende scherm te gaan (categorie kiezen)
def volgende_script():
    try:
        show_category_select_screen(root)  # Ga naar het category select-scherm
    except Exception as e:
        toon_canvas_tekst(canvas, f"Fout bij openen volgend scherm: {str(e)}", kleur="red")

# Functie om tekst op het canvas weer te geven
def toon_canvas_tekst(canvas, tekst, kleur="white", achtergrond="black"):
    canvas.delete("all")  # Wis het canvas
    canvas.config(bg=achtergrond)  # Stel achtergrondkleur in
    canvas.create_text(
        canvas.winfo_width() // 2,  # Horizontaal midden
        canvas.winfo_height() // 2,  # Verticaal midden
        text=tekst,
        fill=kleur,
        font=("Arial", 24),
        anchor="center"  # Zorg dat de tekst gecentreerd wordt
    )

# Functie om de statusindicator (bolletje) te updaten
def update_status_indicator(team_status, connected):
    color = "green" if connected else "red"  # Groen als verbonden, rood als niet verbonden
    team_status.itemconfig(1, fill=color, outline=color)  # Pas de kleur aan

def start_ear_connection_screen():
    """
    Start het ear connection-scherm.
    Dit scherm laat de gebruiker verbinding maken met twee Bluetooth-koptelefoons.
    """
    global root, canvas, team_1_status, team_2_status
    root = tk.Tk()  # Maak een nieuw Tkinter-venster
    root.title("Bluetooth Verbinding")

    # Maak het venster fullscreen zonder titelbalk
    root.overrideredirect(True)
    root.geometry("800x480+0+0")

    # Voeg een toetsencombinatie toe om het programma te sluiten (Ctrl+Q)
    root.bind("<Control-q>", lambda event: root.destroy())

    # Stel de achtergrondkleur in
    root.configure(bg="black")

    # Titel bovenaan
    title_label = tk.Label(root, text="Maak een verbinding", font=("Arial", 24), fg="white", bg="black")
    title_label.pack(pady=20)

    # Maak een Frame voor de knoppen en statusindicatoren
    frame = tk.Frame(root, bg="black")
    frame.pack(pady=20)

    # Maak een canvas voor meldingen
    canvas = tk.Canvas(root, width=800, height=100, bg="black", highlightthickness=0)
    canvas.pack(pady=10)

    # Statusindicator en knop voor Team 1
    team_1_status = tk.Canvas(frame, width=20, height=20, bg="black", highlightthickness=0)
    team_1_status.create_oval(0, 0, 20, 20, fill="red", outline="red")
    team_1_status.grid(row=0, column=0, padx=10)

    team_1_button = tk.Button(frame, text="Verbind Team 1", font=("Arial", 14), width=30,
                               command=lambda: connect_and_update_status(team_1_mac_address, "Team 1", team_1_status, canvas))
    team_1_button.grid(row=0, column=1, padx=10, pady=5)

    # Statusindicator en knop voor Team 2
    team_2_status = tk.Canvas(frame, width=20, height=20, bg="black", highlightthickness=0)
    team_2_status.create_oval(0, 0, 20, 20, fill="red", outline="red")
    team_2_status.grid(row=1, column=0, padx=10)

    team_2_button = tk.Button(frame, text="Verbind Team 2", font=("Arial", 14), width=30,
                               command=lambda: connect_and_update_status(team_2_mac_address, "Team 2", team_2_status, canvas))
    team_2_button.grid(row=1, column=1, padx=10, pady=5)

    # Voeg een knop toe om naar het volgende scherm te gaan
    volgende_button = tk.Button(root, text="Verder", font=("Arial", 14), command=volgende_script)
    volgende_button.pack(pady=20)

    # Start de Tkinter-eventloop
    root.mainloop()

def connect_and_update_status(mac_address, team_name, status_indicator, canvas):
    """
    Verbind met een Bluetooth-apparaat en update de statusindicator.
    """
    try:
        connect_bluetooth_device(mac_address, team_name, canvas)  # Geef canvas door
        # Controleer of de verbinding succesvol was en update de statusindicator
        result = subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True)
        if "Connected: yes" in result.stdout:
            update_status_indicator(status_indicator, connected=True)
        else:
            update_status_indicator(status_indicator, connected=False)
    except Exception as e:
        toon_canvas_tekst(canvas, f"Fout bij {team_name}: {str(e)}", kleur="red")