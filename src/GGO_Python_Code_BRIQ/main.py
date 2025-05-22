# Dit bestand dient als startpunt van de applicatie en zorgt ervoor dat de andere modules worden opgestart.

import tkinter as tk  # Voor het maken van het hoofdvenster (GUI)
from splashscreen import SplashScreen  # Importeer het splashscreen (opstartscherm)
from screens.ear_connection import start_ear_connection_screen  # Importeer het eerste echte scherm na de splash

def stop_program(event=None):
    """
    Sluit het programma af door het hoofdvenster te vernietigen.
    """
    root.destroy()  # Sluit het hoofdvenster van Tkinter

def main():
    global root
    root = tk.Tk()  # Maak het hoofdvenster aan

    # Voeg een toetsencombinatie toe om het programma te stoppen (Ctrl+Q)
    root.bind("<Control-q>", stop_program)

    # Start de splashscreen en ga daarna naar het ear connection-scherm
    SplashScreen(root, on_finish=start_ear_connection_screen)
    root.mainloop()  # Start de Tkinter event loop (zorgt dat het venster actief blijft)

if __name__ == "__main__":
    main()  # Start het programma als dit bestand direct wordt uitgevoerd