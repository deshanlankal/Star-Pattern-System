import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np

# Global variables
img = None
img_display = None
image_history = []  # Stack to store image states
loading_duration = 3000  # Duration for loading animation in milliseconds

# Function to start the main application after loading animation
def start_main_app():
    loading_label.destroy()  # Remove the loading animation when done
    create_main_ui()         # Start the main application UI

# Function to display the loading animation using a video for a specified duration
def show_loading_video():
    video_path = "assets/loading.mp4"  # Replace with the path to your video file
    cap = cv2.VideoCapture(video_path)

    def update_frame(start_time):
        current_time = cv2.getTickCount() / cv2.getTickFrequency() * 1000
        elapsed_time = current_time - start_time
        ret, frame = cap.read()

        if ret and elapsed_time < loading_duration:
            # Resize frame to fit application window
            frame = cv2.resize(frame, (700, 500))  # Fixed size
            # Convert the frame to RGB (OpenCV uses BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame)
            frame_imgtk = ImageTk.PhotoImage(frame_pil)

            loading_label.imgtk = frame_imgtk
            loading_label.configure(image=frame_imgtk)

            # Repeat every 30 ms for a smooth frame update
            loading_label.after(1, update_frame, start_time)
        else:
            cap.release()  # Release the video file when done
            start_main_app()  # Start main application when video ends

    # Start displaying frames
    start_time = cv2.getTickCount() / cv2.getTickFrequency() * 1000
    update_frame(start_time)

# Function to create the main UI
def create_main_ui():
    root.title("Star Pattern Detection App")
    root.geometry("700x500")
    root.config(bg="#1A1A40")

    # Load and set the background image
    background_img = Image.open("assets/background.png")
    background_img = background_img.resize((700, 500), Image.LANCZOS)
    background_img_tk = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(root, image=background_img_tk)
    background_label.image = background_img_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a canvas to display the image
    global canvas
    canvas = tk.Canvas(root, width=400, height=300, bg="black", highlightthickness=2, highlightbackground="#8080FF")
    canvas.grid(row=0, column=0, rowspan=8, padx=20, pady=20)

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
    global load_btn, grayscale_btn, sharpen_btn, rotate_btn, blur_btn, find_btn

    load_btn = tk.Button(root, text="Load Image", command=load_image, **button_style)
    load_btn.grid(row=0, column=1, padx=10, pady=10)

    grayscale_btn = tk.Button(root, text="Convert to Grayscale", command=convert_to_grayscale, state="disabled", **button_style)
    grayscale_btn.grid(row=1, column=1, padx=10, pady=10)

    sharpen_btn = tk.Button(root, text="Sharpen Image", command=sharpen_image, state="disabled", **button_style)
    sharpen_btn.grid(row=2, column=1, padx=10, pady=10)

    rotate_btn = tk.Button(root, text="Rotate 90°", command=rotate_image, state="disabled", **button_style)
    rotate_btn.grid(row=3, column=1, padx=10, pady=10)

    blur_btn = tk.Button(root, text="Apply Gaussian Blur", command=apply_gaussian_blur, state="disabled", **button_style)
    blur_btn.grid(row=4, column=1, padx=10, pady=10)

    find_btn = tk.Button(root, text="Detect Star Pattern", command=detect_star_pattern, state="disabled", **button_style)
    find_btn.grid(row=5, column=1, padx=10, pady=10)

    # Title Label
    title_label = tk.Label(root, text="Star Pattern Detection App", font=("Arial", 16, "bold"), bg="#1A1A40", fg="#8080FF")
    title_label.grid(row=6, column=0, columnspan=3, pady=20)

    # Configure grid weights for proper resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

# Functionality for the buttons
def load_image():
    global img, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        push_image_state()  # Save current image state
        img = Image.open(file_path)
        img.thumbnail((400, 300))  # Resize to fit canvas size
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display
        enable_buttons()

def enable_buttons():
    grayscale_btn.config(state="normal")
    sharpen_btn.config(state="normal")
    rotate_btn.config(state="normal")
    blur_btn.config(state="normal")
    find_btn.config(state="normal")

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
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        img_np = np.array(img)
        img_sharpened = cv2.filter2D(img_np, -1, kernel)
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

def apply_gaussian_blur():
    global img, img_display
    if img:
        push_image_state()  # Save current image state
        img_np = np.array(img)
        blurred_img = cv2.GaussianBlur(img_np, (15, 15), 0)
        img = Image.fromarray(blurred_img)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def detect_star_pattern():
    global img, img_display
    if img:
        push_image_state()  # Save the current state of the image

        # Apply grayscale conversion
        img = ImageOps.grayscale(img)

        # Apply sharpening
        img_np = np.array(img)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        img_sharpened = cv2.filter2D(img_np, -1, kernel)
        img = Image.fromarray(img_sharpened)

        # Rotate the image
        img = img.rotate(90, expand=True)

        # Apply Gaussian blur
        img_np = np.array(img)
        blurred_img = cv2.GaussianBlur(img_np, (15, 15), 0)
        img = Image.fromarray(blurred_img)

        # Display the processed image
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

        # Here, add the code for detecting the star pattern
        # For now, this is a placeholder. Replace this with the actual detection logic
        detected_pattern = "Pattern: Auriga or Boötes"  # Example output
        pattern_label = tk.Label(root, text=detected_pattern, font=("Arial", 14, "bold"), bg="#1A1A40", fg="white")
        pattern_label.grid(row=6, column=0, columnspan=3, pady=10)

        # Update the Detect Star Pattern button to call this function
        find_btn = tk.Button(root, text="Detect Star Pattern", command=detect_star_pattern, **button_style)

    

def push_image_state():
    global img, image_history
    if img:
        image_history.append(img.copy())  # Save a copy of the current image state

# Application Setup
root = tk.Tk()
root.title("Loading...")

# Display the loading label
loading_label = tk.Label(root)
loading_label.pack()

# Start the loading animation
show_loading_video()

root.mainloop()
