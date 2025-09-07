import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import pygame
import os
from gtts import gTTS
from openai import OpenAI
from gtts import gTTS

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "API"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()   

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play MP3
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    print("Speaking...")

    # Wait until playback finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()   
    
    os.remove("temp.mp3")


def aiProcess(command):
    
    client = OpenAI(
        api_key=""
    )
    completions = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a virtual assistant Jarvis."},
            {"role": "user", "content": command}
        ]
    )
    return completions.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif c.lower(c).startswith("play"):
        songs = c.lower().split(" ")[1]
        link = musicLibrary.music[songs]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=pk&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles',[])

            for article in articles:
                speak(article['title'])


    else:
        # Let openAI handel the request
        output = aiProcess(c)
        speak(output)

    
if __name__ == "__main__":
    speak("Initializing JARVIS......")
    
    while True:
        r = sr.Recognizer()

        print("Recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening.......")
                audio = r.listen(source, timeout=2, phrase_time_limit=1) 
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yea")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
 