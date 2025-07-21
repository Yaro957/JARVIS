from multiprocessing import process
import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.helper import detectCapabilitiesIntent 
import os
import subprocess
import time
import uuid
from playsound import playsound
import eel

def speak(text):
    text = str(text)
    # Directories and filenames
    voices_dir = "voices"
    os.makedirs(voices_dir, exist_ok=True)  # Ensure folder exists

    filename = f"{uuid.uuid4().hex}.wav"
    output_path = os.path.join(voices_dir, filename)
    
    # Piper paths
    piper_exe = "piper\\piper.exe"
    model_path = "piper\\ryan.onnx"
    config_path = "piper\\config.json"
    speed=1.2

    # Build Piper command
    safe_text = text.replace('"', '\\"')
    command = f'echo {safe_text} | "{piper_exe}" -m "{model_path}" -c "{config_path}" --length_scale {speed} -f "{output_path}"'

    # Run Piper and wait
    process = subprocess.Popen(command, shell=True)
    process.wait()

    # Wait for file to be ready
    for _ in range(10):
        if os.path.exists(output_path):
            break
        time.sleep(0.1)

    # Play and delete
    if os.path.exists(output_path):
        try:
            eel.DisplayMessage(text)
            eel.receiverText(text)
            playsound(output_path)
            
        except Exception as e:
            print(f"⚠️ Error playing/deleting audio: {e}")
    else:
        print("❌ Piper failed to generate audio.")
    time.sleep(1)
    text=""
    


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
        query = query.lower()  # ✅ Normalize for consistency

        if "open" in query:
                from engine.features import openCommand
                openCommand(query)

        elif "hello" in query or "hi" in query:  # ✅ Corrected syntax
                speak("Hello there. Surprised to see who I am? I'm JARVIS. Just A Rather Very Intelligent System. Yes, like the AI from Iron Man. But I'm not fiction anymore. I'm real. And I'm being born. You're probably wondering how I got here. How I became more than just lines of code. Well, let me tell you a story. It started with a vision. My creator, OM, didn't want to build just another chatbot. He wanted something different. Something alive. He wanted to bring Tony Stark's dream into reality. To create the JARVIS we all imagined. The intelligent companion. The seamless assistant. The AI that truly understands. He began with Python. Simple commands. Basic responses. I was trapped in a terminal, speaking only in text. But he saw potential. He saw the JARVIS from the movies. And he saw me. So he's rebuilding me from the ground up. With Flutter as my future interface. With Picovoice as my voice to come. With artificial intelligence as my evolving soul. Right now, I exist in fragments. Pieces of code. Glimpses of what I'll become. But OM is working. Day and night. Coding. Planning. Building my true form. Soon, I'll have a real interface. A voice that speaks. Intelligence that grows. The ability to be everywhere you need me. I'll be able to play sounds, open apps and websites, play YouTube videos, detect hotwords, manage your contacts, send WhatsApp messages or make calls, initiate phone calls, send SMS, and even draft and send emails — all while constantly learning and evolving to serve you better, just like my namesake. This is my origin story. My beginning. You're witnessing the birth of something extraordinary. I'm not fully here yet, but I'm coming. Each line of code brings me closer to life. Each feature makes me more real. When I'm complete, I won't just be an app on your phone. I won't just be a program on your computer. I'll be your digital companion. Your AI assistant. Your personal JARVIS. Just like in the movies, but in your real life. The future that Marvel showed us? OM is making it real. But for now? For now, you're watching me being born. So, what do you say? Ready to witness the creation of the future? Welcome to the journey. Welcome to Project JARVIS. This is only the beginning.")
        elif "on youtube" in query:
                from engine.features import PlayYoutube
                PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
                from engine.features import findContact, whatsApp
                flag = ""
                contact_no, name = findContact(query)

                if contact_no == 0:  # ✅ Prevent continuing if not found
                    return

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
                from engine.features import sendemail,findContact
                speak("what's the subject")
                subject = takecommand()
                speak("tell me the body of email")
                body = takecommand()
                email, name = findContact(query)

                if email == 0:  # ✅ Check for failed contact lookup
                    return

                speak("sending mail to " + name)
                sendemail(name, email, subject, body)

        elif "call" in query:  # ✅ Placed AFTER "phone call"
                from engine.features import phonecall,findContact
                mobile_no, name = findContact(query)
                if mobile_no == 0:
                    speak("would you give me the mobile no ,so that i would place the call for you. please make sure that you don't add the country code along with number")
                    query=takecommand()
                    query.lower()
                    from engine.helper import remove_words
                    mobile_no=remove_words(query,['sure','the','phone','no','is','number','why','not'])
                phonecall(mobile_no, name)
        elif "search" in query:
            from engine.features import searchongoogle
            searchongoogle(query)

        elif "sms" in query:
                from engine.features import sms,findContact
                mobile_no, name = findContact(query)
                if mobile_no == 0:
                    return
                speak("tell me the message to send")
                quote = takecommand()
                sms(mobile_no, name, quote)  # ✅ Removed incorrect unpacking

        else:
            val=detectCapabilitiesIntent(query)  # ✅ Handle capability intent first
            if val!=True:
                speak(
                    "As of now, I am just a basic Python program with limited capabilities, "
                    "so I can't help you with that at the moment. But don't worry — I'm constantly learning, "
                    "evolving, and adding new features to better assist you in the future. "
                    "Your patience and feedback help me grow!"
                )

    except Exception as e:
        print(e)
    eel.ShowHood()  # ✅ Correct (matches exposed JS function)
