import os
import re
from shlex import quote
import struct
import subprocess
import time
import keyboard
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME , ACCESS_KEY
import sqlite3
import webbrowser
import pvporcupine
import urllib.parse
import webbrowser
# from engine.helper import *


conn=sqlite3.connect("jarvis.db")
cursor=conn.cursor()
# Playing assiatnt sound function
import pywhatkit as kit

@eel.expose
def playAssistantSound(value):
    start= "www\\assets\\audio\\init.mp3"
    voice="www\\assets\\audio\\voice.mp3"
    if value=='1':
        playsound(voice)
    else:
        playsound(start)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()  
    print("the query is"+query)
    app_name = query.strip()
    
    if app_name != "":
        try:
            cursor.execute(
                'SELECT path FROM SYS_COMMAND WHERE name = ?', (app_name,)  # Fixed: SQL syntax and parameter
            )
            results = cursor.fetchall()
            
            if len(results) != 0:
                speak("opening " + app_name)  # Fixed: added space
                os.startfile(results[0][0])
                
            else:  # Fixed: simplified condition
                cursor.execute(
                    'SELECT url FROM WEBCOMMAND WHERE name = ?', (app_name,)  # Fixed: SQL syntax and column name
                )
                results = cursor.fetchall()
            
                if len(results) != 0:
                    speak("opening " + app_name)  # Fixed: added space
                    webbrowser.open(results[0][0])
                
                else:
                    speak("opening " + app_name)  # Fixed: added space
                    try:
                        os.system('start ' + app_name)  # Fixed: added space
                    except:
                        speak('sir, no app found to open')
            
        except Exception as e:  # Better to catch specific exceptions
            speak('something went wrong')  # Fixed: typo
    else:
        speak('found nothing to open in your speech, sir')

def searchongoogle(query):
    from engine.helper import remove_words
    words_to_remove = [ASSISTANT_NAME,'make', 'a', 'an', 'google', 'search', 'for','show', 'me',
    'can', 'you', 'please' ]
    newquery = remove_words(query, words_to_remove)
    print(newquery)
    newquery1='+'.join(newquery.split())
    link='https://www.google.com/search?q='
    url=link+newquery1
    webbrowser.open_new(url)
    speak("searching"+newquery+"on google")
    

def PlayYoutube(query):
    from engine.helper import extract_yt_term
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(
             access_key=ACCESS_KEY,
            keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(e)
        
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    from engine.helper import remove_words
    mail=0
    
    if "mail"in query:
        mail=1
    words_to_remove = [ASSISTANT_NAME, 'mail','make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video','sms']
    query = remove_words(query, words_to_remove)
    

    try:
        query = query.strip().lower()
        if mail!="1":
            cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
            results = cursor.fetchall()
            print(results[0][0])
            mobile_number_str = str(results[0][0])
            mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            cursor.execute("SELECT email FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
            results = cursor.fetchall()
            print(results[0][0])
            email= str(results[0][0])
            return email, query
    
    except Exception as e:
        print(e)
        speak('the details are not available in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    try:
        # Ensure mobile_no starts with '+'
        if not mobile_no.startswith('+'):
            mobile_no = '+' + mobile_no

        if flag == 'message':
            encoded_message = quote(message)
            whatsapp_uri = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
            jarvis_message = f"Opening WhatsApp to send message to {name}."
            speak(jarvis_message)
            
            subprocess.run(f'start "" "{whatsapp_uri}"', shell=True)
            
            # Give the app a moment to load, focus, and populate the message box.
            # You might need to adjust this delay based on your system speed.
            time.sleep(5) 
            
            # Simulate pressing 'enter' to send the pre-filled message
            pyautogui.press('enter') 
            speak(f"Message sent successfully to {name}.")


        elif flag == 'call':
            whatsapp_uri = f"whatsapp://call?phone={mobile_no}"
            jarvis_message = f"Attempting to call {name} via WhatsApp."
            speak(jarvis_message)
            
            subprocess.run(f'start "" "{whatsapp_uri}"', shell=True)
            time.sleep(5) # Give the app time to initiate the call

        elif flag == 'video call':
            whatsapp_uri = f"whatsapp://videocall?phone={mobile_no}"
            jarvis_message = f"Attempting to video call {name} via WhatsApp."
            speak(jarvis_message)
            
            subprocess.run(f'start "" "{whatsapp_uri}"', shell=True)
            time.sleep(5) # Give the app time to initiate the video call

        else:
            speak("I didn't understand the WhatsApp action you requested.")

        print(f"WhatsApp action attempted for {name} with URI: {whatsapp_uri}")

    except Exception as e:
        print(f"Error in whatsApp function: {e}")
        speak("Sorry, I couldn't complete the WhatsApp action.")
def phonecall(mobile_no, name):
    mobile_no = mobile_no.replace(" ", "").replace("-", "")
    
    # Add country code if missing
    if mobile_no.startswith("+91"):
        formatted_no = mobile_no
    elif mobile_no.startswith("91"):
        formatted_no = "+" + mobile_no
    else:
        formatted_no = "+91" + mobile_no

    speak(f"Calling {name} from phone")
    os.system(f'adb shell am start -a android.intent.action.CALL -d tel:{formatted_no}')
    

def sms(mobile_no, name, message):
   # URL encode the message properly (handles all special characters)
   encoded_message = urllib.parse.quote(message)
   
   speak(f"Sending message to {name} by phone")

   # Construct ADB command
   adb_command = f'adb shell am start -a android.intent.action.VIEW -d "sms:{mobile_no}?body={encoded_message}"'
   
   # Execute command and check for errors
   result = os.system(adb_command)
   if result != 0:
       print(f"Error executing ADB command: {result}")
       return False
   
   time.sleep(2)
   
   # Tap send button
   os.system("adb shell input tap 981 2261")
   
   return True
def sendemail(name,email,subject,body):
    subject=urllib.parse.quote(subject)
    body.replace(" ", "\\ ")
    os.system(f"adb shell am start -a android.intent.action.VIEW -d mailto:{email}?subject={subject}")
    time.sleep(1)
    os.system("adb shell input tap 148 828")
    os.system(f"adb shell input text '{body}'")
    time.sleep(1) 
    # speak("mail sent to"+name)
    print("sending mail to "+name)  
    os.system("adb shell input tap 884 181") 