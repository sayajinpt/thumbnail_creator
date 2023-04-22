import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class LogoApp:
    def __init__(self, master):
        self.master = master
        master.title("Logo App")

        # Add label widget
        self.info_label = tk.Label(master, text="After selecting the background and logo, u can set the logo position by X and Y or by just simply click on the image and a result image will be saved")
        self.info_label.pack()

        self.background_image_path = None
        self.logo_image_path = None
        self.logo_position = None

        # Create widgets
        self.background_button = tk.Button(master, text="Select Background Image", command=self.select_background_image)
        self.logo_button = tk.Button(master, text="Select Logo Image", command=self.select_logo_image)
        self.x_label = tk.Label(master, text="X:")
        self.x_entry = tk.Entry(master)
        self.y_label = tk.Label(master, text="Y:")
        self.y_entry = tk.Entry(master)
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)

        # Pack widgets
        self.background_button.pack()
        self.logo_button.pack()
        self.x_label.pack()
        self.x_entry.pack()
        self.y_label.pack()
        self.y_entry.pack()
        self.submit_button.pack()

        self.preview_label = tk.Label(master)
        self.preview_label.pack()

        self.preview_label.bind('<Button-1>', self.on_preview_click)

    def select_background_image(self):
        self.background_image_path = filedialog.askopenfilename()
        if self.background_image_path:
            self.show_preview()

    def select_logo_image(self):
        self.logo_image_path = filedialog.askopenfilename()

    def show_preview(self):
        background_image = Image.open(self.background_image_path)
        preview_image = ImageTk.PhotoImage(background_image)
        self.preview_label.config(image=preview_image)
        self.preview_label.image = preview_image

    def on_preview_click(self, event):
        if self.logo_image_path is None:
            return
        x, y = event.x, event.y
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, x)
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, y)
        self.submit()

    def submit(self):
        if self.background_image_path is None or self.logo_image_path is None:
            return

        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
        except ValueError:
            return

        background_image = Image.open(self.background_image_path)
        logo_image = Image.open(self.logo_image_path)
        logo_image = logo_image.convert("RGB")
        logo_max_size = tuple(dim * 0.25 for dim in background_image.size)
        logo_image.thumbnail(logo_max_size)

        margin = 0
        self.logo_position = (x, y)

        background_image_copy = background_image.copy()
        background_image_copy.paste(logo_image, self.logo_position)

        result_image = ImageTk.PhotoImage(background_image_copy)

        # Save the result image to file
        filename = f"result_{x}_{y}.jpg"
        background_image_copy.save(filename)

if __name__ == '__main__':
    root = tk.Tk()
    app = LogoApp(root)
    root.mainloop()