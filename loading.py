import cv2
from PIL import Image, ImageTk

def show_loading_video(root, loading_label, callback):
    video_path = "loading.mp4"  # Replace with the path to your video file
    cap = cv2.VideoCapture(video_path)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Resize frame to fit application window
            frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame)
            frame_imgtk = ImageTk.PhotoImage(frame_pil)

            loading_label.imgtk = frame_imgtk
            loading_label.configure(image=frame_imgtk)

            # Repeat every 30 ms for a smooth frame update
            loading_label.after(30, update_frame)
        else:
            cap.release()  # Release the video file when done
            callback()  # Start main application when video ends

    # Start displaying frames
    update_frame()
