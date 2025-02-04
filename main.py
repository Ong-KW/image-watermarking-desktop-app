from tkinter import *
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont
import glob, os

# Get all true type fonts
my_dict = {ImageFont.truetype(font=fn).getname()[0] : fn for fn in glob.glob('/Windows/Fonts/*.ttf') if ImageFont.truetype(font=fn).getname()[1] == "Regular"}
font_dict = {key : value.replace("/Windows/Fonts\\","") for key,value in my_dict.items()}

font_list = [key for key,value in font_dict.items()]


def add_text():
    # Get the user input text
    msg = text_input.get()

    # Get the user selected font
    font_name = font_cb.get()
    font_ttf = font_dict[font_name]

    # Get the font size selected by the user
    font_size = round(float(size_scale.get()) * 12)

    # Get the opacity (0 to 100%) selected by the user
    opacity = round(int(opacity_scale.get()) * (255/100))

    for infile in glob.glob("/Image_to_Watermark/*.jpg"):
        file, ext = os.path.splitext(infile)

        # Open image
        with Image.open(infile).convert("RGBA") as base:
            # Get the width and height of base image
            W, H = base.size

            # Make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", (W, H), (255, 255, 255, 0))

            font = ImageFont.truetype(font=font_ttf, size=font_size)

            # Call draw Method to add 2D graphics in an image
            d = ImageDraw.Draw(txt)

            # Get the width and height of the text
            _, _, w, h = d.textbbox((0, 0), text=msg, font=font)

            # Draw text, half opacity
            d.text((W - w - 10, H - h - 10), text=msg, font=font, fill=(255, 255, 255, opacity))

            # Composite the text over the base image
            result = Image.alpha_composite(base, txt)

            # Show the image
            result.show()

            # Convert the result image to "RGB" and save as new "JPEG" file
            out = result.convert("RGB")
            out.save(file + "_watermarked.jpg", "JPEG")

    # Close the window
    window.destroy()

window = Tk()
window.title("Image Watermarking Desktop App")
window.minsize(width=400, height=250)
window.config(padx=20, pady=20)

text_label = Label(text="Text")
text_label.grid(row=0 ,column=0)
text_label.config(padx=5, pady=5)

text_input = Entry(width=30)
text_input.grid(row=0 ,column=1)

font_label = Label(text="Font")
font_label.grid(row=1, column=0)
font_label.config(padx=5, pady=10)

selected_font = StringVar()
font_cb = ttk.Combobox(window, width = 27, textvariable = selected_font)

font_cb['values'] = [value for value in font_list]
font_cb['state'] = 'readonly'
font_cb.grid(row=1, column=1)

size_label = Label(text="Size")
size_label.grid(row=2, column=0)
size_label.config(padx=5, pady=10)

v1 = DoubleVar()

size_scale = Scale(window, variable = v1,
           from_ = 0.2, to = 20,
           orient = HORIZONTAL, length=200, sliderlength=15)
size_scale.grid(row=2, column=1)

opacity_label = Label(text="Opacity")
opacity_label.grid(row=3, column=0)
opacity_label.config(padx=5, pady=20)

v2 = DoubleVar()

opacity_scale = Scale(window, variable = v2,
           from_ = 0, to = 100,
           orient = HORIZONTAL, length=200, sliderlength=15)
opacity_scale.grid(row=3, column=1)

add_button = Button(text="Add Text", command=add_text)
add_button.grid(row=4, column=0)
add_button.config(padx=5, pady=5)

window.mainloop()


