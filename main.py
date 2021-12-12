from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog, ttk
import os
import webbrowser
import sys

window = Tk()
window.title("Image Watermarking Desktop App")
# window.iconbitmap('static/images/icon.png')
window.geometry("650x440")

frame = Frame(window)
frame.pack(fill=BOTH, expand=1)

# Define background image
bg = ImageTk.PhotoImage(file='static/images/bg2.png')
bg_label = Label(frame, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas = Canvas(frame, width=650, height=440)
canvas.pack(fill=BOTH, expand=True)
# Set img in canvas
canvas.create_image(0, 0, image=bg, anchor='nw')

BASIC_IMG_DIR = 'static/images/'
WTM_IMG_DIR = 'static/wtm_images/'


def resizer(e):
    global bg1, resized_bg, new_bg
    bg1 = Image.open('static/images/bg2.png')
    resized_bg = bg1.resize((e.width, e.height), Image.ANTIALIAS)
    # Define img again
    new_bg = ImageTk.PhotoImage(resized_bg)
    # Add it back to the canvas
    canvas.create_image(0, 0, image=new_bg, anchor='nw')


# Create New Frame with full screen ScrollBar
def second_frame_scrollbar():
    # Create a Canvas
    global canvas
    canvas = Canvas(frame)
    canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    # Add a Scrollbar to the Canvas
    scrollbar = ttk.Scrollbar(frame, orient=HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=TOP, fill=X)
    # Configure the Canvas
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    # Create Another Frame Inside the Canvas
    global second_frame
    second_frame = Frame(canvas)
    # Add that New frame to the Window in the Canvas
    canvas.create_window((0, 0), window=second_frame, anchor='nw')

    # Canvas Label
    wtm_label = Label(canvas, text="Select and Apply watermark image", font=("Arial", 17), fg='#b00f38')
    wtm_label.pack()
    remark_label = Label(canvas, text='✔ Watermarked image(s) will be saved in the "wtm_images" folder\n\n',
                         font=("Arial", 12), fg='#b00f38')
    remark_label.pack()

    # 'Apply Watermark' Button
    second_frame_btn = Menubutton(canvas, text="Apply Watermark", relief=RAISED, width=20, font=("Arial", 12),
                                  bg="#fde701", fg='#221e1f')
    menu_2 = Menu(second_frame_btn, tearoff=0, activebackground='#f9330d')
    second_frame_btn['menu'] = menu_2
    menu_2.add_checkbutton(label="Add Text Watermark", variable=StringVar, command=add_txt_wtm)
    menu_2.add_checkbutton(label="Add Logo Watermark", variable=StringVar, command=add_logo_wtm)
    second_frame_btn.pack()


# Rename and Save watermarked image(s) in the 'wtm_images' folder
def rename_and_save(img, img_location):
    img_name = img_location
    img_name = img_name.replace(BASIC_IMG_DIR, '')
    img.save(f'{WTM_IMG_DIR}/wm_{img_name}')


# Display wtm image on the desktop
def display(img):
    img_resize = img.resize((200, 150), Image.ANTIALIAS)
    img_resize = ImageTk.PhotoImage(img_resize)
    panel = Label(second_frame, image=img_resize)
    panel.image = img_resize
    panel.pack(side=LEFT, pady=(170, 10))
    window.geometry("650x400")


# Clear everything on the frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()


def clear_second_frame():
    for widget in second_frame.winfo_children():
        widget.destroy()


def restart():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


# 'ADD IMAGES' SUBMENU
def open_from_computer():
    images_folder = []
    global img_list
    img_list = images_folder

    # Create an Open dialog and return the selected filename(s) that correspond to existing filename(s)
    filepath = filedialog.askopenfilenames(title="Select File", filetypes=(("JPG", "*.jpg"),
                                                                           ("PNG", "*.png"), ("all filenames", "*.*")))
    if filepath:
        # Delete all the labels on the main screen
        clear_frame()
        # Create a full screen ScrollBar
        second_frame_scrollbar()

        # Extract filename from path
        for path in filepath:
            img = Image.open(path).convert('RGB')
            filename = os.path.basename(path)
            img_name = ''.join(filename)

            images_folder.append(img_name)

            # Save img to the 'Images' folder
            img.save(f'{BASIC_IMG_DIR}{img_name}')
            # Display image on the second_frame desktop
            display(img)


# Search for how to get drive dialog to save files ????????
def from_google_drive():
    webbrowser.register("chrome", None,
                        webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    google_drive = webbrowser.get("chrome").open_new_tab("https://drive.google.com/drive/u/0/my-drive")


def from_google_photos():
    webbrowser.register("chrome", None,
                        webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    img = webbrowser.get("chrome").open_new_tab("https://photos.google.com/?pageId=none")


# 'APPLY WATERMARK' Submenu
def add_txt_wtm():
    # Create new window
    window_2 = Toplevel(pady=20, padx=20)
    window_2.title('Text Watermark')

    # Create watermark params input fields
    enter_text = Entry(window_2, width=20)
    enter_text_lbl = Label(window_2, text='Enter Text:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_text.grid(row=0, column=1)
    enter_text_lbl.grid(row=0, column=0)

    enter_txt_color = Entry(window_2, width=20)
    enter_txt_color_lbl = Label(window_2, text='Enter Text Color:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_txt_color.grid(row=1, column=1)
    enter_txt_color_lbl.grid(row=1, column=0)

    enter_txt_size = Entry(window_2, width=20)
    enter_txt_size_lbl = Label(window_2, text='Enter Text Size (px):', font=("Arial", 10), fg='#588C73', pady=3)
    enter_txt_size.grid(row=2, column=1)
    enter_txt_size_lbl.grid(row=2, column=0)

    enter_y_position = Entry(window_2, width=20)
    enter_y_position_lbl = Label(window_2, text='Enter Y-axis Position:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_y_position.grid(row=3, column=1)
    enter_y_position_lbl.grid(row=3, column=0)

    enter_x_position = Entry(window_2, width=20)
    enter_x_position_lbl = Label(window_2, text='Enter X-axis Position:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_x_position.grid(row=4, column=1)
    enter_x_position_lbl.grid(row=4, column=0)

    # After 'Text Watermark' parameters given and 'Apply' button clicked:
    def add_txt_continue():
        # Get given parameters
        text = enter_text.get()
        txt_color = enter_txt_color.get()
        txt_size = int(enter_txt_size.get())
        y_position = int(enter_y_position.get())
        x_position = int(enter_x_position.get())

        enter_text.delete(0, END)
        enter_txt_color.delete(0, END)
        enter_txt_size.delete(0, END)
        enter_y_position.delete(0, END)
        enter_x_position.delete(0, END)

        # Delete all the base images on the second_frame desktop
        clear_second_frame()

        for img_name in img_list:
            img_location = f'{BASIC_IMG_DIR}{img_name}'
            # Get an image object
            img = Image.open(img_location)

            txt_position = (y_position, x_position)
            font = ImageFont.truetype("arial.ttf", txt_size)

            # Get a drawing context
            draw = ImageDraw.Draw(img)
            draw.text(txt_position, text=text, fill=txt_color, font=font)
            # Rename and Save watermarked image in the 'wtm_images' folder
            rename_and_save(img, img_location)
            # Display wtm image(s) on the second_frame desktop
            display(img)

    button_apply = Button(window_2, text='Apply', relief=RAISED, width=20, font=("Arial", 12), bg="#D96459",
                          fg='#F4F4F4', command=add_txt_continue)
    button_apply.grid(row=5, columnspan=2, pady=10)


def add_logo_wtm():
    # Get watermark img
    wtm_location = filedialog.askopenfilename(title="Select Watermark")
    watermark = Image.open(wtm_location)

    # Create new window
    window_3 = Toplevel(pady=20, padx=20)
    window_3.title('Logo Watermark')

    # Create watermark params input fields
    enter_wtm_size = Entry(window_3, width=20)
    enter_wtm_size_lbl = Label(window_3, text='Enter Logo Size (% of base img):', font=("Arial", 10), fg='#588C73',
                               pady=3)
    enter_wtm_size.grid(row=0, column=1)
    enter_wtm_size_lbl.grid(row=0, column=0)

    enter_y_position = Entry(window_3, width=20)
    enter_y_position_lbl = Label(window_3, text='Enter X-axis Position:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_y_position.grid(row=1, column=1)
    enter_y_position_lbl.grid(row=1, column=0)

    enter_x_position = Entry(window_3, width=20)
    enter_x_position_lbl = Label(window_3, text='Enter Y-axis Position:', font=("Arial", 10), fg='#588C73', pady=3)
    enter_x_position.grid(row=2, column=1)
    enter_x_position_lbl.grid(row=2, column=0)

    def add_logo_wtm_continue():

        # Get given parameters
        wtm_size = int(enter_wtm_size.get())
        x_position = int(enter_x_position.get())
        y_position = int(enter_y_position.get())

        enter_wtm_size.delete(0, END)
        enter_x_position.delete(0, END)
        enter_y_position.delete(0, END)

        pct = wtm_size / 100  # Convert given wtm_size to %
        wtm_position = (y_position, x_position)

        # Delete all the base images on the second_frame desktop
        clear_second_frame()

        for img_name in img_list:
            # Open base img from 'images' folder
            img_location = f'{BASIC_IMG_DIR}{img_name}'
            image = Image.open(img_location).convert('RGBA')

            # Resize watermark relative to the base image in %
            wtm_size = watermark.resize((round(image.size[0] * pct), round(image.size[1] * pct)))
            wtm_mask = wtm_size.convert('RGBA')

            # Make a blank img for the wtm, initialized to transparent wtm color. Paste img into it
            blank_img = Image.new('RGBA', image.size, (0, 0, 0, 0))
            blank_img.paste(image, (0, 0))
            blank_img.paste(wtm_mask, wtm_position, mask=wtm_mask)

            # Rename and Save watermarked image in the 'wtm_images' folder
            img = blank_img.convert('RGB')  # If leave it as RGBA it gives an ERROR msg
            rename_and_save(img, img_location)

            # Display wtm image on the desktop
            display(img)

    button_apply = Button(window_3, text='Apply', relief=RAISED, width=20, font=('Arial', 12), bg='#D96459',
                          fg='#F4F4F4', command=add_logo_wtm_continue)
    button_apply.grid(row=3, columnspan=2, pady=10)


# MAIN MENU
main_menu = Menu(window)
window.config(menu=main_menu)

# 'Close App' Menu
main_menu.add_command(label="   Close App   ", command=window.destroy)

# 'Add Images' Menu
image_menu = Menu(main_menu, activebackground='#fde701')
main_menu.add_cascade(label="   Add Images   ", menu=image_menu)
image_menu.add_command(label="From My Computer", command=open_from_computer)
image_menu.add_command(label="From Google Drive", command=from_google_drive)
image_menu.add_command(label="From Google Photos", command=from_google_photos)

# 'Apply Watermark' Menu
watermark_menu = Menu(main_menu, activebackground='#00fefe')
main_menu.add_cascade(label="   Apply Watermark   ", menu=watermark_menu)
watermark_menu.add_command(label="Add Text Watermark", command=add_txt_wtm)
watermark_menu.add_command(label="Add Logo Watermark", command=add_logo_wtm)

# 'Restart' Menu
main_menu.add_command(label="   Restart   ", command=restart)

# Frame Label-1
img_label = Label(canvas, text="Select and Open image(s)", font=("Arial", 17), fg='#b00f38', bg='#f6f6f6')
img_label.pack(pady=50)

# 'Select Images' BUTTON
frame_btn = Menubutton(canvas, text="Select Images", relief=RAISED, width=20, font=("Arial", 12), bg="#fde701",
                       fg='#221e1f')
menu_1 = Menu(frame_btn, tearoff=0, activebackground='#f9330d')
frame_btn['menu'] = menu_1
menu_1.add_checkbutton(label="From My Computer", variable=StringVar, command=open_from_computer)
menu_1.add_checkbutton(label="From Google Drive", variable=IntVar(), command=from_google_drive)
menu_1.add_checkbutton(label="From Google Photos", variable=IntVar(), command=from_google_photos)
frame_btn.pack(pady=(0, 50))

# Frame Label-2
note_label = Label(canvas, text='✔ Opened image(s) will be saved in the "images" folder ✔', font=("Arial", 12),
                   fg='#b00f38', bg='#f6f6f6')
note_label.pack()

window.bind('<Configure>', resizer)
window.mainloop()

