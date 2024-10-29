import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
img = None
img_display = None
image_history = []  # Stack to store image states
loading_duration = 5500  # Duration for loading animation in milliseconds

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
            frame = cv2.resize(frame, (window_width, window_height))  # Use dynamic window size
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
    root.title("Dynamic Star Pattern Detection App")

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Define window dimensions relative to screen size
    global window_width, window_height
    window_width, window_height = int(screen_width * 0.7), int(screen_height * 0.7)
    root.geometry(f"{window_width}x{window_height}")

    # Load and set the background image
    background_img = Image.open("assets/background.png")
    background_img = background_img.resize((window_width, window_height), Image.LANCZOS)
    background_img_tk = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(root, image=background_img_tk)
    background_label.image = background_img_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a canvas to display the image
    global canvas
    canvas = tk.Canvas(root, width=window_width * 0.5, height=window_height * 0.6, bg="black", highlightthickness=2, highlightbackground="#8080FF")
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
    global load_btn, grayscale_btn, sharpen_btn, rotate_btn, blur_btn, find_btn, remove_filters_btn, enhance_btn

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

    remove_filters_btn = tk.Button(root, text="Remove All Filters", command=remove_all_filters, state="disabled", **button_style)
    remove_filters_btn.grid(row=6, column=1, padx=10, pady=10)

    enhance_btn = tk.Button(root, text="Enhance Image", command=enhance_image, state="disabled", **button_style)
    enhance_btn.grid(row=7, column=1, padx=10, pady=10)

    # Title Label
    title_label = tk.Label(root, text="Star Pattern Detection App", font=("Arial", 16, "bold"), bg="#1A1A40", fg="#8080FF")
    title_label.grid(row=8, column=0, columnspan=3, pady=20)

    # Configure grid weights for proper resizing
    for i in range(9):
        root.grid_rowconfigure(i, weight=1)
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
        img.thumbnail((window_width * 0.5, window_height * 0.6))  # Resize to fit canvas size
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display
        enable_buttons()
        show_graphs()  # Show graphs after loading the image

def show_graphs():
    if img is None:
        return  # No image loaded, do nothing

    # Create a new window for the graphs
    graphs_window = tk.Toplevel(root)
    graphs_window.title("Image Analysis Charts")
    graphs_window.geometry("800x600")

    # Brightness Distribution
    brightness_data = np.array(img).mean(axis=2)  # Average across color channels for brightness
    plt.figure(figsize=(10, 4))

    plt.subplot(2, 2, 1)
    plt.hist(brightness_data.ravel(), bins=256, color='gray', alpha=0.7)
    plt.title('Brightness Distribution')
    plt.xlabel('Brightness Value')
    plt.ylabel('Frequency')

    # Color Histogram
    plt.subplot(2, 2, 2)
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        histogram, bin_edges = np.histogram(np.array(img)[:, :, i], bins=256, range=(0, 255))
        plt.plot(bin_edges[0:-1], histogram, color=color)
    plt.title('Color Histogram')
    plt.xlabel('Color Value')
    plt.ylabel('Frequency')

    # Edge Detection Distribution
    img_np = np.array(img)
    edges = cv2.Canny(img_np, 100, 200)  # Basic Canny edge detection
    plt.subplot(2, 2, 3)
    plt.hist(edges.ravel(), bins=2, color='black', alpha=0.7)
    plt.title('Edge Detection Distribution')
    plt.xlabel('Edge Detected (0 or 1)')
    plt.ylabel('Frequency')

    # Frequency of Detected Patterns
    # This is a placeholder. Implement the logic to analyze and display detected patterns.
    detected_patterns = ['Auriga', 'Boötes', 'None']  # Example patterns
    pattern_counts = [5, 3, 10]  # Example frequencies

    plt.subplot(2, 2, 4)
    plt.bar(detected_patterns, pattern_counts, color='purple')
    plt.title('Frequency of Detected Patterns')
    plt.xlabel('Patterns')
    plt.ylabel('Frequency')

    plt.tight_layout()

    # Draw the matplotlib figure in the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=graphs_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def enable_buttons():
    grayscale_btn.config(state="normal")
    sharpen_btn.config(state="normal")
    rotate_btn.config(state="normal")
    blur_btn.config(state="normal")
    find_btn.config(state="normal")
    remove_filters_btn.config(state="normal")
    enhance_btn.config(state="normal")

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

        # Placeholder star pattern detection logic
        detected_pattern = "Pattern: Auriga or Boötes"
        pattern_label = tk.Label(root, text=detected_pattern, font=("Arial", 14, "bold"), bg="#1A1A40", fg="white")
        pattern_label.grid(row=9, column=0, columnspan=3, pady=10)

def remove_all_filters():
    global img, img_display
    if image_history:
        img = image_history[0]  # Reset to the first state (original)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def enhance_image():
    # Placeholder for additional enhancement logic
    pass

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

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Define window dimensions relative to screen size
window_width, window_height = int(screen_width * 0.7), int(screen_height * 0.7)
root.geometry(f"{window_width}x{window_height}")

# Start the loading animation
show_loading_video()

root.mainloop()









