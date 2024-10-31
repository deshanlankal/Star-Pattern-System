import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

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

    # Set loading window to fullscreen
    root.attributes('-fullscreen', True)  # Make the window fullscreen

    # Get screen dimensions for resizing the video
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    def update_frame(start_time):
        current_time = cv2.getTickCount() / cv2.getTickFrequency() * 1000
        elapsed_time = current_time - start_time
        ret, frame = cap.read()

        if ret and elapsed_time < loading_duration:
            # Resize frame to fit fullscreen
            frame = cv2.resize(frame, (screen_width, screen_height))  # Resize to screen size
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
            root.attributes('-fullscreen', False)  # Exit fullscreen when loading is done
            start_main_app()  # Start main application when video ends

    # Start displaying frames
    start_time = cv2.getTickCount() / cv2.getTickFrequency() * 1000
    update_frame(start_time)

######### main UI Function ###############
def create_main_ui():
    global match_ratio_label 
    
    root.title("Dynamic Star Pattern Detection App")
################## Full Screen Thing ################################
    root.attributes('-fullscreen', True)
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Define window dimensions relative to screen size
    global window_width, window_height
    window_width, window_height = screen_width, screen_height 
    root.geometry(f"{window_width}x{window_height}")

    # Load and set the background image
    background_img = Image.open("assets/background.png")
    background_img = background_img.resize((window_width, window_height), Image.LANCZOS)
    background_img_tk = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(root, image=background_img_tk)
    background_label.image = background_img_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a canvas to display the image
    # Create a canvas to display the image
    global canvas
    canvas = tk.Canvas(root, width=window_width * 0.5, height=window_height * 0.6, bg="black", highlightthickness=2, highlightbackground="#8080FF")
    canvas.grid(row=0, column=0, rowspan=8, padx=20, pady=20)

    # Label to show the result message, positioned right below the canvas
    global result_label
    result_label = tk.Label(root, text="", font=("Arial", 12), bg="#1A1A40", fg="#FFFFFF")
    result_label.grid(row=8, column=0, padx=20, pady=5)  # Adjust row and column for desired positioning


    ######## Button styling ##################
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
    global load_btn, grayscale_btn, sharpen_btn, rotate_btn, blur_btn, remove_filters_btn, enhance_btn, remove_sault_and_pepper_btn,btn_brightness_distribution, btn_brightness_heatmap, btn_star_density_plot, btn_color_temperature_map, find_btn

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

    remove_filters_btn = tk.Button(root, text="Remove All Filters", command=reset_filters, state="disabled", **button_style)
    remove_filters_btn.grid(row=5, column=1, padx=10, pady=10)

    enhance_btn = tk.Button(root, text="Enhance Image", command=enhance_image, state="disabled", **button_style)
    enhance_btn.grid(row=6, column=1, padx=10, pady=10)

    remove_sault_and_pepper_btn = tk.Button(root, text="Remove Salt & Pepper", command=remove_salt_pepper, state="disabled", **button_style)
    remove_sault_and_pepper_btn.grid(row=7, column=1, padx=10, pady=10)

    btn_brightness_distribution = tk.Button(root, text="Brightness Distribution", command=show_brightness_distribution, state="disabled", **button_style)
    btn_brightness_distribution.grid(row=1, column=2, padx=10, pady=10)

    btn_brightness_heatmap = tk.Button(root, text="Brightness Heatmap", command=show_brightness_heatmap, state="disabled", **button_style)
    btn_brightness_heatmap.grid(row=2, column=2, padx=10, pady=10)

    btn_star_density_plot = tk.Button(root, text="Star Density Plot", command=show_star_density_plot, state="disabled", **button_style)
    btn_star_density_plot.grid(row=3, column=2, padx=10, pady=10)

    btn_color_temperature_map = tk.Button(root, text="Color Temperature Map", command=show_color_temperature_map, state="disabled", **button_style)
    btn_color_temperature_map.grid(row=4, column=2, padx=10, pady=10)

    find_btn = tk.Button(root, text="Detect Star Pattern", command=find_pattern, state="disabled", **button_style)
    find_btn.grid(row=8, column=1, padx=10, pady=10)

########################################################################################################
################# Enable & Desable btn thing ######################################################### 
    # Function to enable all processing buttons
def enable_buttons():
    grayscale_btn.config(state="normal")
    sharpen_btn.config(state="normal")
    rotate_btn.config(state="normal")
    blur_btn.config(state="normal")
    find_btn.config(state="normal")
    remove_filters_btn.config(state="normal")
    enhance_btn.config(state="normal")##
    btn_brightness_distribution.config(state="normal")
    btn_brightness_heatmap.config(state="normal")
    btn_star_density_plot.config(state="normal")
    btn_color_temperature_map.config(state="normal")
    
    # Function to disable all processing buttons
def disable_buttons():
    grayscale_btn.config(state="disabled")
    sharpen_btn.config(state="disabled")
    rotate_btn.config(state="disabled")
    blur_btn.config(state="disabled")
    find_btn.config(state="disabled")
    remove_filters_btn.config(state="disabled")
    enhance_btn.config(state="disabled")##
    btn_brightness_distribution.config(state="disabled")
    btn_brightness_heatmap.config(state="disabled")
    btn_star_density_plot.config(state="disabled")
    btn_color_temperature_map.config(state="disabled")
#####################################################################################################
#####################################################################################################
####################################################################################################


    # Configure grid weights for proper resizing
    for i in range(9):
        root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
##################33 Feguring Out The image is a night SKY *** ################################
def is_night_sky(image):
    """Check if the image is a night sky by assessing brightness and detecting star-like features."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Step 1: Brightness Check
    brightness = np.mean(img_cv)
    if brightness > 70:
        return False
    
    # Step 2: Detect Star-like Features
    _, thresh_img = cv2.threshold(img_cv, 200, 255, cv2.THRESH_BINARY)
    white_pixels = cv2.countNonZero(thresh_img)
    if white_pixels < 50:
        return False
    
    return True
###################################################################################################
def load_image():
    global img, original_img, result_label
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            original_img = Image.open(file_path)
            original_img = original_img.resize((600, 600))  # Resize to 600x600
            img = original_img.copy()

            if is_night_sky(img):
                result_label.config(text="Night sky detected!")
                update_canvas(img)
                enable_buttons()
                show_graphs()
                # Show informational message box
                messagebox.showinfo("Image Analysis", "Night sky detected!")
            else:
                result_label.config(text="Not a night sky image. Please upload a night sky image.")
                disable_buttons()
                # Show warning message box
                messagebox.showwarning("Image Analysis", "Not a night sky image. Please upload a night sky image.")
        except Exception as e:
            result_label.config(text=f"Error loading image: {e}")
            # Optional: Show error message box
            messagebox.showerror("Error", f"Error loading image: {e}")


##################///The Graphs ////################################################
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

def update_canvas(image):
    global img_display
    img_display = ImageTk.PhotoImage(image)
    canvas.config(width=600, height=600)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    canvas.image = img_display

##################### The Star Patterns Config ########################################################
def load_patterns():
    pattern_dir = "patterns/"
    for filename in os.listdir(pattern_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            pattern_img = cv2.imread(os.path.join(pattern_dir, filename), 0)
            patterns.append((pattern_img, filename.split('.')[0]))

########################################################################################################
##################  The main Function of the Program that detect the pattern ###########################
def find_pattern():
    global img
    if img:
        img_cv = np.array(img.convert('L'))
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img_cv, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        best_match_name = None
        best_match_score = float('inf')
        best_match_ratio = 0.0

        for pattern_img, pattern_name in patterns:
            kp2, des2 = orb.detectAndCompute(pattern_img, None)
            if des2 is not None:
                matches = bf.match(des1, des2)
                matches = sorted(matches, key=lambda x: x.distance)
                match_score = sum([match.distance for match in matches[:10]])
                match_ratio = len(matches) / len(kp2) if kp2 else 0.0

                if match_score < best_match_score:
                    best_match_score = match_score
                    best_match_name = pattern_name
                    best_match_ratio = match_ratio

        if best_match_name:
            result_label.config(text=f"Best Match: {best_match_name}")
            match_ratio_label.config(text=f"Matching Ratio: {best_match_ratio:.2f}")  # Ensure this line is present
        else:
            result_label.config(text="No match found")
            match_ratio_label.config(text="Matching Ratio: N/A")  # Ensure this line is present
#######################################################################################################
########### Independent Charts ########################################################################
########################################################################################################
def show_brightness_distribution():
    if img is None:
        return  # No image loaded, do nothing
    brightness_data = np.array(img.convert('L')).ravel()  # Convert to grayscale and flatten
    fig, ax = plt.subplots()
    ax.hist(brightness_data, bins=256, color='gray', alpha=0.7)
    ax.set_title('Brightness Distribution')
    ax.set_xlabel('Brightness Value')
    ax.set_ylabel('Frequency')
    show_chart(fig)

def show_brightness_heatmap():
    if img is None:
        return  # No image loaded, do nothing
    img_gray = np.array(img.convert('L'))  # Convert to grayscale
    fig, ax = plt.subplots()
    ax.imshow(img_gray, cmap='hot', interpolation='nearest')
    ax.set_title('Brightness Heatmap')
    ax.axis('off')  # Hide axes
    show_chart(fig)

def show_star_density_plot():
    if img is None:
        return  # No image loaded, do nothing
    img_gray = np.array(img.convert('L'))  # Convert to grayscale
    grid_size = 10
    star_density = np.zeros((grid_size, grid_size))
    height, width = img_gray.shape
    for x in range(grid_size):
        for y in range(grid_size):
            # Define the grid region
            grid_x = int(width * x / grid_size)
            grid_y = int(height * y / grid_size)
            grid_region = img_gray[grid_y:grid_y + height // grid_size, grid_x:grid_x + width // grid_size]
            star_density[y, x] = np.sum(grid_region > 200)  # Count bright pixels
    fig, ax = plt.subplots()
    ax.imshow(star_density, cmap='viridis', interpolation='nearest')
    ax.set_title('Star Density Plot')
    ax.set_xlabel('X Region')
    ax.set_ylabel('Y Region')
    show_chart(fig)

def show_color_temperature_map():
    if img is None:
        return  # No image loaded, do nothing
    img_np = np.array(img)  # Convert to NumPy array for processing
    hsv_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)  # Convert to HSV color space
    color_temp = hsv_img[:, :, 0]  # Extract hue channel
    fig, ax = plt.subplots()
    ax.imshow(color_temp, cmap='coolwarm', interpolation='nearest')
    ax.set_title('Color Temperature Map')
    ax.axis('off')  # Hide axes
    show_chart(fig)

def show_chart(fig):
    chart_window = tk.Toplevel(root)
    chart_window.title("Chart")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
########################################################################################################
########################################################################################################
def convert_to_grayscale():
    global img, img_display
    if img:
        push_image_state()  # Save current image state
        img = ImageOps.grayscale(img)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.image = img_display

def remove_salt_pepper():
    global img
    if img:
        img_cv = np.array(img.convert('L'))  # Convert to grayscale for processing
        img_cv = cv2.medianBlur(img_cv, 3)    # Apply median blur
        img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB))  # Convert back to RGB
        update_canvas(img)  # Update the canvas with the processed image


def reset_filters():
    global img
    if original_img:
        img = original_img.copy()
        update_canvas(img)

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

root.bind('<Escape>', lambda e: root.quit())

# Start the loading animation
show_loading_video()

root.mainloop();