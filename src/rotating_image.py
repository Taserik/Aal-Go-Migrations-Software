import tkinter as tk
from PIL import Image, ImageTk

class RotatingImage:
    
    def __init__(self, canvas, button, image_path):
        self.angle = 0
        self.image = Image.open(image_path).convert('RGBA')
        self.image_width, self.image_height = self.image.size
        
        self.canvas = canvas
        self.button = button
        self.tk_image = ImageTk.PhotoImage(self.image.rotate(self.angle, expand=True))
        self.button.config(image=self.tk_image)
        
        self.after_id = None
        
    def rotate_image(self):
        self.angle += 10
        rotated_image = self.image.rotate(self.angle, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)
        self.button.config(image=self.tk_image)
        self.after_id = self.button.after(50, self.rotate_image)
        
    def start_rotation(self):
        self.show_label()
        self.rotate_image()

    def stop_rotation(self):
        if self.after_id:
            self.button.after_cancel(self.after_id)
            self.after_id = None
            
    def show_label(self):
        self.label = tk.Label(self.canvas, text="Eeling in process!", font=('Helvetica', 10))
        self.label.grid(row=3, column=3)
        self.blink_label()
         
    def blink_label(self):
        self.label.grid(row=3, column=3)
        self.label.config(bg='red', fg='white')
        self.canvas.after(500, lambda: self.label.config(bg='white', fg='red'))
        self.canvas.after(1000, self.blink_label)
