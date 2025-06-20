import re


def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    if not input_string:
        return ""
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string
def detectCapabilitiesIntent(query):
    from engine.command import speak  # Adjust this based on your file structure

    capability_phrases = [
        "what can you do",
        "your features",
        "list your abilities",
        "what are your skills",
        "show me what you can do",
        "tell me your commands",
        "how can you help me",
        "jarvis commands",
        "help menu",
        "what can jarvis do",
        "list of features",
        "what are you",
        "why are you",
        "what are your capablitites"
    ]

    query = query.lower()

    if any(phrase in query for phrase in capability_phrases):
        speak(
speak(
    "Hello, I am Jarvis — your personal AI assistant, inspired by the fictional AI from Iron Man. "
    "I can perform a variety of tasks to assist you. "
    "Here's what I can do: "
    "Play sounds, open apps and websites, play YouTube videos, detect hotwords, manage your contacts, "
    "send WhatsApp messages or make calls, initiate phone calls, send SMS, and even draft and send emails. "
    "I'm always learning and evolving to serve you better, just like my namesake."
)

        )
        return True  # ✅ Tell caller: I handled it!
    return False

