import pyttsx3
import speech_recognition as sr
import pyautogui
import subprocess
import os
import ctypes
import pyaudio
import webbrowser
import openai

Shutdown = False
openai.api_key = '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'


def generate_openai_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        # Extract and return the generated content
        generated_content = completion['choices'][0]['message']['content']
        return generated_content
    except Exception as e:
        return f"Error generating response: {e}"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def set_brightness(percentage):
    try:
        # For Windows
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
        brightness_value = max(0, min(int((percentage / 100) * 100), 100))
        os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {brightness_value})")
        print(f"Brightness set to {brightness_value}%.")
    except Exception as e:
        print(f"Error setting brightness: {e}")

def brightness(percentage):
    try:
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        set_brightness(percentage)
        print("Brightness increased.")
    except Exception as e:
        print(f"Error increasing brightness: {e}")

def open_app(app_name):
    try:
        if app_name.lower() == "chrome":
            subprocess.Popen(["start", "chrome"], shell=True)
        else:
            subprocess.Popen([app_name + ".exe"])
        print(f"{app_name.capitalize()} opened.")
    except Exception as e:
        print(f"Error opening app: {e}")

def open_website(website_name):
    try:
        url = f"https://www.{website_name}"
        webbrowser.open(url)
        print(f"Opening {url}")
    except Exception as e:
        print(f"Error opening website: {e}")

def search_question(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        print(f"Searching for: {query}")
    except Exception as e:
        print(f"Error searching: {e}")

def extract_percentage(command):
    words = command.split()
    for i, word in enumerate(words):
        if "%" in word:
            return int(word.replace("%", ""))
        elif word == "to" and i < len(words) - 1 and words[i + 1].isdigit():
            return int(words[i + 1])
    return 0

def is_question(command):
    question_words = ["what", "when", "where", "who", "whom", "which", "whose", "why", "how"]
    return any(word in command for word in question_words)

def jarvis_command(command):
    global Shutdown

    if "open" in command:
        # Extract app or website name from the command
        open_keyword_index = command.find("open") + len("open")
        app_or_website_name = command[open_keyword_index:].strip()

        # Check if the input is a website or an app
        if "." in app_or_website_name:
            open_website(app_or_website_name)
        else:
            open_app(app_or_website_name)
    elif is_question(command):
        search_question(command)
        # response = generate_openai_response(command)
        # print(f"Response from GPT-3: {response}")
        # speak(response)
    elif "increase volume" in command:
        pyautogui.press("volumeup")
    elif "decrease volume" in command:
        pyautogui.press("volumedown")
    elif "increase brightness" or "decrease brightness" or "set brightness" in command:
        percentage = extract_percentage(command)
        brightness(percentage)
    elif "close" in command:
        # Close any app mentioned after "close" command
        close_keyword_index = command.find("close") + len("close")
        app_name = command[close_keyword_index:].strip()
        os.system(f"taskkill /f /im {app_name}.exe")
        print(f"{app_name.capitalize()} closed.")
    else:
        print("Command not recognized.")

def listen_for_activation():
    global Shutdown

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while not Shutdown:
        print("Listening for activation...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            activation_phrase = recognizer.recognize_google(audio).lower()
            if "hello jarvis" in activation_phrase:
                print("Jarvis activated. Listening for commands...")
                listen_for_commands()
            elif "shutdown" in activation_phrase:
                print("Shutdown command detected. Shutting down...")
                Shutdown = True
                return
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def listen_for_commands():
    global Shutdown

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while not Shutdown:
        print("Listening for commands...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")
            if "goodbye jarvis" in command:
                print("Jarvis deactivated.")
                break
            elif "shutdown" in command:
                print("Shutdown command detected. Shutting down...")
                Shutdown = True
                return
            else:
                jarvis_command(command)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    listen_for_activation()

