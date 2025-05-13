import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
import datetime
import os
from uuid import uuid4

# Initialize OpenAI API (replace with your API key)
openai.api_key = "your-openai-api-key-here"

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to a male voice (adjust index for preference)
engine.setProperty('rate', 150)  # Speed of speech

# Initialize speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for audio input and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Please repeat.")
            return None
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return None

def get_openai_response(prompt):
    """Get a response from OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if available
            messages=[
                {"role": "system", "content": "You are J.A.R.V.I.S., a witty and helpful AI assistant inspired by Iron Man. Respond conversationally and assist with tasks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

def open_website(url):
    """Open a website in the default browser."""
    webbrowser.open(url)
    speak("Opening the website for you.")

def process_command(command):
    """Process the user's command and perform actions."""
    if not command:
        return

    # Greetings and basic commands
    if "hello" in command or "hi" in command:
        speak("Hello! How can I assist you today?")
        return
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        return
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}.")
        return
    elif "open google" in command:
        open_website("https://www.google.com")
        return
    elif "open youtube" in command:
        open_website("https://www.youtube.com")
        return
    elif "open facebook" in command:
        open_website("https://www.facebook.com")
        return
    elif "stop" in command or "exit" in command:
        speak("Goodbye, sir.")
        exit()

    # Use OpenAI for general queries
    response = get_openai_response(command)
    speak(response)

def main():
    """Main function to run J.A.R.V.I.S."""
    speak("Initializing J.A.R.V.I.S. How may I serve you, sir?")
    while True:
        command = listen()
        process_command(command)

if __name__ == "__main__":
    main()