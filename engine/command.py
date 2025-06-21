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
    
    # Show on UI
    

    # Directories and filenames
    voices_dir = "voices"
    os.makedirs(voices_dir, exist_ok=True)  # Ensure folder exists

    filename = f"{uuid.uuid4().hex}.wav"
    output_path = os.path.join(voices_dir, filename)
    
    # Piper paths
    piper_exe = "piper\\piper.exe"
    model_path = "piper\\en_US-ryan-low.onnx"
    config_path = "piper\\config.json"
    speed=1

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
            os.remove(output_path)
        except Exception as e:
            print(f"⚠️ Error playing/deleting audio: {e}")
    else:
        print("❌ Piper failed to generate audio.")



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
                speak("hello sir, how may I help you")

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
                    return
                phonecall(mobile_no, name)

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
