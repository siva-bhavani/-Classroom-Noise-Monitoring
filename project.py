import sounddevice as sd
import numpy as np
import pygame
import time
import tkinter as tk
from threading import Thread

# Set parameters
DURATION = 1  # Duration to sample in seconds
THRESHOLD = 60  # Decibels threshold for sound alert
SAMPLERATE = 44100  # Standard sample rate (44.1 kHz)

# Initialize pygame for sound alert
pygame.mixer.init()
alert_sound = pygame.mixer.Sound("alert.mp3")  # Replace with your alert sound file path
alert_playing = False  # To track whether the alert sound is playing

# Function to create a flashing window as visual alert
def show_visual_alert():
    root = tk.Tk()
    root.geometry("200x100")
    root.title("Alert!")
    label = tk.Label(root, text="Noise Level Exceeded!", font=("Arial", 16), fg="red")
    label.pack(pady=30)
    
    # Flash the window
    for _ in range(5):  # Flash 5 times
        root.config(bg="yellow")
        root.update()
        time.sleep(0.5)
        root.config(bg="white")
        root.update()
        time.sleep(0.5)
    
    root.quit()

# Function to get the noise level
def get_noise_level():
    # Record audio data
    audio_data = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='float32')
    sd.wait()

    # Calculate amplitude and convert to decibels
    amplitude = np.abs(audio_data)
    volume = 20 * np.log10(np.mean(amplitude) + 1e-6) + 100  # Convert to dB
    return volume

# Monitor noise levels continuously
while True:
    noise_level = get_noise_level()
    print(f"Current Noise Level: {noise_level:.2f} dB")

    if noise_level > THRESHOLD:
        if not alert_playing:  # If the alert sound is not already playing
            print("⚠️ Noise Level Exceeded!")
            alert_sound.play()  # Play alert sound
            alert_playing = True  # Mark that the alert is playing

            # Show visual alert (flashing window)
            Thread(target=show_visual_alert).start()
    else:
        if alert_playing:  # If the noise level is below the threshold and sound is playing
            print("🔇 Noise level back to normal.")
            pygame.mixer.stop()  # Stop the sound alert
            alert_playing = False  # Mark that the alert is not playing

    time.sleep(2)  # Check every 2 seconds
