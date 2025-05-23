# splashscreen.py
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import threading

class SplashScreen:
    def __init__(self, root, on_finish):
        self.root = root
        self.on_finish = on_finish

        self.root.overrideredirect(True)
        self.root.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.original_image = Image.open("assets/logo.png").convert("RGBA")
        self.alpha = 0.0
        self.image_id = None
        self.fade_in()

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05
            self.update_image()
            self.root.after(50, self.fade_in)
        else:
            self.root.after(2000, self.fade_out)

    def fade_out(self):
        if self.alpha > 0.0:
            self.alpha -= 0.05
            self.update_image()
            self.root.after(50, self.fade_out)
        else:
            self.on_finish()

    def update_image(self):
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(self.original_image)
        faded = enhancer.enhance(self.alpha)
        self.tk_image = ImageTk.PhotoImage(faded)

        if self.image_id:
            self.canvas.delete(self.image_id)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width // 2
        y = screen_height // 2
        self.image_id = self.canvas.create_image(x, y, image=self.tk_image)

