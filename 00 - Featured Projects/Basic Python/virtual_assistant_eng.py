import pyttsx3
import speech_recognition as sr
import pyjokes
import yfinance as yf
import pywhatkit
import webbrowser
import datetime
import wikipedia

# Voice / language options
id_en = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id_es = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Listen to microphone and return audio as text
def audio_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("You can speak now...")
        audio = r.listen(source)

        try:
            command = r.recognize_google(audio, language="en-us")
            print("You said: " + command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            return "waiting"
        except sr.RequestError:
            print("Sorry, there was a connection issue.")
            return "waiting"
        except:
            print("Oops, something went wrong.")
            return "waiting"

# Make the assistant speak
def speak(message):
    engine = pyttsx3.init()
    engine.setProperty("voice", id_en)
    engine.say(message)
    engine.runAndWait()

# Tell the day of the week
def tell_day():
    today = datetime.date.today()
    print(today)

    day_of_week = today.weekday()
    print(day_of_week)

    calendar = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    speak(f"Today is {calendar[day_of_week]}")

# Tell the current time
def tell_time():
    now = datetime.datetime.now()
    time_str = f"It is {now.hour} hours, {now.minute} minutes, and {now.second} seconds."
    print(time_str)
    speak(time_str)

# Initial greeting
def greeting():
    now = datetime.datetime.now()
    if now.hour < 6 or now.hour > 20:
        m = "Good evening"
    elif 6 <= now.hour < 13:
        m = "Good morning"
    else:
        m = "Good afternoon"

    speak(f"{m}, I am Helena, your personal assistant. Please tell me how I can help you.")

# Main control center for commands
def control_center():
    greeting()
    start = True

    while start:
        command = audio_to_text().lower()

        if "open youtube" in command:
            speak("Okay. Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "open browser" in command:
            speak("Alright. Opening browser.")
            webbrowser.open("https://www.google.com")
            continue
        elif "what day is it" in command:
            tell_day()
            continue
        elif "what time is it" in command:
            tell_time()
            continue
        elif "search on wikipedia" in command:
            speak("Searching on Wikipedia.")
            command = command.replace("wikipedia", "")
            wikipedia.set_lang("en")
            result = wikipedia.summary(command, sentences=1)
            speak("According to Wikipedia: ")
            speak(result)
            continue
        elif "search the internet" in command:
            speak("I'm on it.")
            command = command.replace("search the internet", "")
            pywhatkit.search(command)
            speak("Here is what I found.")
            continue
        elif "play" in command:
            speak("Good idea, playing it now.")
            pywhatkit.playonyt(command)
            continue
        elif "joke" in command:
            speak(pyjokes.get_joke("en"))
            continue
        elif "stock price" in command:
            stock = command.split("of")[-1].strip()
            portfolio = {
                "apple": "AAPL",
                "amazon": "AMZN",
                "google": "GOOGL"
            }
            try:
                stock = portfolio[stock]
                stock_data = yf.Ticker(stock)
                current_price = stock_data.info["regularMarketPrice"]
                speak(f"I found it, the current stock price is {current_price}")
                continue
            except:
                speak("Sorry, I couldn't find it in the database.")
        elif "goodbye" in command or "bye" in command:
            speak("Goodbye. Let me know if you need anything else.")
            break

control_center()
