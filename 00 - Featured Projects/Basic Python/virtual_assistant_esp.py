import pyttsx3
import speech_recognition as sr
import pyjokes
import yfinance as yf
import pywhatkit
import webbrowser
import datetime
import wikipedia

#Opciones de voz / idioma
id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

#Escuchar microfono y devolver el audio como texto
def transformar_audio_en_texto():

    #Almacenar el recognizer en una variable
    r = sr.Recognizer()

    #Configurar microfono
    with sr.Microphone() as origen:

        #Tiempo de espera
        r.pause_threshold = 0.8

        #Informar que comenzo la grabacion
        print("ya puedes hablar")

        #Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            #Buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language = "es-es")

            #prueba de que pudo ingresar
            print("Dijiste: "+pedido)

            #Devolver a pedido
            return pedido

        #si no comprende el audio
        except sr.UnknownValueError:

            #prueba de que no comprendio el audio
            print("Ups, no entendi")

            #devolver error

            return "sigo esperando"

        #no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("Ups, no entendi")

            # devolver error

            return "sigo esperando"

        #error inesperado

        except:
            # prueba de que no comprendio el audio
            print("Ups, algo salio mal")

            # devolver error

            return "sigo esperando"

#funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id2)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#informar del dia de la semana
def pedir_dia():

    #variable datos de hoy
    dia = datetime.date.today()
    print(dia)

    #variable dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario nombre dias
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    #decir dia semana
    hablar(f"Hoy es {calendario[dia_semana]}")

#informar de la hora
def pedir_hora():

    #variable hora
    hora = datetime.datetime.now()
    hora = f"Son las {hora.hour} {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    #decir la hora
    hablar(hora)

#saludo inicial
def saludo():

    #variable datos hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        m = "Buenas noches"

    elif 6 <= hora.hour < 13:
        m = "Buen día"

    else:
        m = "Buenas tardes"

    #decir saludo
    hablar(f"{m}, soy Helena, tu asistente personal. Por favor, dime en que puedo ayudarte")

#control de pedidos: funcion central del asistente
def centro_operaciones():

    #saludo inicial
    saludo()

    #loop que se repite
    comenzar = True

    while comenzar:

        #activar micro y guardar pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("De acuerdo. Abriendo youtube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir navegador" in pedido:
            hablar("Vamos a ello.")
            webbrowser.open("https://www.google.com")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "buscar en wikipedia" in pedido:
            hablar("Buscando en wikipedia")
            pedido = pedido.replace("wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente: ")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Estoy con ello")
            pedido = pedido.replace("busca es internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Buena idea, ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple" : "APPL",
                       "amazon" : "AMZN",
                       "google" : "GOOGL"}
            try:
                accion = cartera[accion]
                accion = yf.Ticker(accion)
                precio_actual = accion.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de la accion es {precio_actual}")
                continue
            except:
                hablar("Perdón, pero no la he encontrado en la base de datos")

        elif "adiós" in pedido:
            hablar("Hasta luego. Cualquier cosa que necesites me avisas")
            break

centro_operaciones()

