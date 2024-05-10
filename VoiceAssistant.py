import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import threading

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Global variable to keep track of the conversation state
conversation_active = False

# Function to convert text to speech
def speak(text):
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 0.8)
    engine.say(text)
    engine.runAndWait()

# Function to recognize user speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error recognizing your speech. Please try again later.")
        return ""

# Function to handle user commands
def handle_command(query):
    conversation_text.insert(tk.END, "You: " + query + "\n")
    if "hello" in query:
        response = "Hello! How can I assist you today?"
        conversation_text.insert(tk.END, "Assistant: " + response + "\n")
        speak(response)
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        conversation_text.insert(tk.END, "Assistant: " + response + "\n")
        speak(response)
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response = f"Today's date is {current_date}"
        conversation_text.insert(tk.END, "Assistant: " + response + "\n")
        speak(response)
    elif "search on google" in query:
        response = "What would you like to search for?"
        conversation_text.insert(tk.END, "Assistant: " + response + "\n")
        speak(response)
        search_query = recognize_speech()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
    elif "quit" in query or "stop" in query:
        response = "Goodbye"
        conversation_text.insert(tk.END, "Assistant: " + response + "\n")
        speak(response)
        sys.exit()

def update_style():
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 14), padding=10)
    style.configure('TLabel', font=('Helvetica', 16), padding=8, background='#424242', foreground='white')

# GUI Setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("450x500")
root.configure(bg='#424242')  # Set background color to dark grey
update_style()

# Main Display Area
info_frame = tk.Frame(root, bg="#424242")  # Set frame background color to dark grey
info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Status Display (changes based on listening state)
status_label = ttk.Label(root, text="Listening...", font=('Arial', 14, 'bold'), background='#424242', foreground='white')
status_label.pack(pady=15)

# Load microphone images
mic_img_active = tk.PhotoImage(file="microphone.png")  # Microphone image for active conversation
mic_img_inactive = tk.PhotoImage(file="img.png")  # Microphone image for inactive conversation

mic_button = tk.Button(root, image=mic_img_inactive, bd=0, bg='#424242', activebackground='#424242')
mic_button.pack(pady=(0, 10))

# Conversation Display
conversation_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15, font=("Helvetica", 12), bg='#f0f0f0', fg='black')
conversation_text.pack(expand=True, fill="both", padx=20, pady=(0, 10))

# Function to handle microphone button click
def toggle_conversation():
    global conversation_active
    if conversation_active:
        status_label.config(text="Conversation paused")
        conversation_active = False
        mic_button.config(image=mic_img_inactive)
    else:
        status_label.config(text="Listening...")
        conversation_active = True
        mic_button.config(image=mic_img_active)
        threading.Thread(target=start_listening).start()

mic_button.config(command=toggle_conversation)

# Function to handle speech recognition
def start_listening():
    global conversation_active
    while conversation_active:
        query = recognize_speech()
        if query:
            handle_command(query)

root.mainloop()
