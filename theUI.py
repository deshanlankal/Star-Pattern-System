import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np

# Global variables
img = None
img_display = None
image_history = []  # Stack to store image states

# Function to start the main application after loading animation
def start_main_app():   
    loading_label.destroy()  # Remove the loading animation when done
    create_main_ui()         # Start the main application UI

# Function to display the loading animation using a video for 3 seconds
def show_loading_video():
    video_path = "assets/loading.mp4"  # Replace with the path to your video file
    cap = cv2.VideoCapture(video_path)
    root.after(3000, lambda: (cap.release(), start_main_app()))  # Start main app after 3 seconds

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Resize frame to fit application window
            frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
            
            # Convert the frame to RGB (OpenCV uses BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame)
            frame_imgtk = ImageTk.PhotoImage(frame_pil)

            loading_label.imgtk = frame_imgtk
            loading_label.configure(image=frame_imgtk)

            # Repeat every 30 ms for a smooth frame update
            loading_label.after(30, update_frame)
        else:
            cap.release()  # Release the video file when done
            start_main_app()  # Start main application when video ends

    # Start displaying frames
    update_frame()

# Function to create the main UI
def create_main_ui():
    root.title("Star Pattern Detection App")
    root.geometry("700x500")
    root.config(bg="#1A1A40")

    # Load and set the background image
    background_img = Image.open("assets/background.png")  # Replace with your .png image path
    background_img = background_img.resize((700, 500), Image.LANCZOS)
    background_img_tk = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(root, image=background_img_tk)
    background_label.image = background_img_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a canvas to display the image
    global canvas
    canvas = tk.Canvas(root, width=400, height=300, bg="black", highlightthickness=2, highlightbackground="#8080FF")
    canvas.grid(row=0, column=0, rowspan=7, padx=20, pady=20)

    # Button styling
    button_style = {
        "font": ("Arial", 12, "bold"),
        "bg": "#34495E",
        "fg": "white",
        "relief": "raised",
        "width": 20,
        "height": 2,
        "bd": 0,
        "activebackground": "#8080FF",
        "cursor": "hand2",
    }

    # Create buttons with enhanced styling
    load_btn = tk.Button(root, text="Load Image", command=load_image, **button_style)
    load_btn.grid(row=0, column=1, padx=10, pady=10)

    grayscale_btn = tk.Button(root, text="Convert to Grayscale", command=convert_to_grayscale, **button_style)
    grayscale_btn.grid(row=1, column=1, padx=10, pady=10)

    sharpen_btn = tk.Button(root, text="Sharpen Image", command=sharpen_image, **button_style)
    sharpen_btn.grid(row=2, column=1, padx=10, pady=10)

    rotate_btn = tk.Button(root, text="Rotate 90°", command=rotate_image, **button_style)
    rotate_btn.grid(row=3, column=1, padx=10, pady=10)

    undo_btn = tk.Button(root, text="Undo", command=undo, **button_style)  # New Undo button
    undo_btn.grid(row=4, column=1, padx=10, pady=10)

    find_btn = tk.Button(root, text="Detect Star Pattern", command=find_pattern, **button_style)
    find_btn.grid(row=5, column=1, padx=10, pady=10)

    # Title Label
    title_label = tk.Label(root, text="Star Pattern Detection App", font=("Arial", 16, "bold"), bg="#1A1A40", fg="#8080FF")
    title_label.grid(row=6, column=0, columnspan=2, pady=20)

# Functionality for the buttons
def load_image():
    global img, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        push_image_state()  # Save current image state
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def convert_to_grayscale():
    global img, img_display
    if img:
        push_image_state()  # Save current image state
        img = ImageOps.grayscale(img)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def sharpen_image():
    global img, img_display
    if img:
        push_image_state()  # Save current image state
        # Define a sharpening kernel
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        img_np = np.array(img)
        img_sharpened = cv2.filter2D(img_np, -1, kernel)
        
        # Convert back to PIL Image
        img = Image.fromarray(img_sharpened)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def rotate_image():
    global img, img_display
    if img:
        push_image_state()  # Save current image state
        img = img.rotate(90, expand=True)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def find_pattern():
    # Placeholder for image pattern recognition.
    pass

def push_image_state():
    global img, image_history
    if img:
        image_history.append(img.copy())  # Save a copy of the current image state

def undo():
    global img, img_display, image_history
    if image_history:
        img = image_history.pop()  # Restore the last saved image state
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

# Create the main root window and loading label
root = tk.Tk()
root.geometry("700x500")
loading_label = tk.Label(root)
loading_label.pack(fill="both", expand=True)  # Make the loading label expand to the window size
show_loading_video()  # Display loading video

# Start the GUI loop
root.mainloop()
