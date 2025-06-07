import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    print("NANI:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You:", command)
        return command
    except:
        return ""

def get_weather(city):
    api_key = 'your_openweathermap_api_key'  # Replace with your API key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] != '404':
        main = data['main']
        temp = main['temp']
        desc = data['weather'][0]['description']
        weather_info = f'The temperature in {city} is {temp}°C with {desc}.'
        talk(weather_info)
    else:
        talk("Sorry, I couldn't find the weather for that city.")

def run_nani(command):
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'search' in command:
        query = command.replace('search', '')
        talk('Searching for ' + query)
        pywhatkit.search(query)

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'weather in' in command:
        city = command.replace('weather in', '').strip()
        get_weather(city)

    elif 'flip a coin' in command:
        result = random.choice(['heads', 'tails'])
        talk('It is ' + result)

    elif 'roll a dice' in command:
        dice = random.randint(1, 6)
        talk(f'You rolled a {dice}')

    elif 'remind me to' in command:
        task = command.replace('remind me to', '')
        talk('Reminder set for: ' + task)
        with open('reminders.txt', 'a') as f:
            f.write(task + '\n')

    elif 'date' in command:
        talk('Sorry, I have a headache')

    elif 'are you single' in command:
        talk('I am in a relationship with Nithyanand')

    else:
        talk('Please say the command again')

# Wake word loop
while True:
    wake_command = take_command()
    if 'hey nani' in wake_command:
        talk("Hah vintunna cheppu ...")
        command = take_command()
        run_nani(command)

