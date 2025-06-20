import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "hello" in query or "hi" in query:
            speak("hello sir,how may i help you ")
        elif detectCapabilitiesIntent(query):  # ✅ If handled...
            return  # 🔥 Stop right here!
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone" in query or "video" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
                
        elif "mail" in query:
            from engine.features import sendemail
            speak("what's the subject")
            subject=takecommand()
            speak("tell me the body of email")
            body=takecommand()
            email,name=findContact(query)
            speak("sending mail to"+name)
            sendemail(name,email,subject,body)
            
        elif "call" in query:
            from engine.features import phonecall,findContact
            mobile_no,name=findContact(query)
            phonecall(mobile_no,name)
            
        elif "sms" in query:
             from engine.features import sms,findContact
             mobile_no,name=findContact(query)
             speak("tell me the message to send")
             quote=takecommand()
             mobile_no,name=sms(mobile_no,name,quote)
             
        else:
            from engine.features import chatBot
            speak("As of now, I am just a basic Python program with limited capabilities, so I can't help you with that at the moment. But don't worry — I'm constantly learning, evolving, and adding new features to better assist you in the future. Your patience and feedback help me grow!")
    
    except Exception as e:
        print(e)
    
    eel.ShowHood()  # ✅ Correct (matches exposed JS function)
