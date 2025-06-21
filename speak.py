import os
from playsound import playsound
def speak(text):
    # 🌐 Display on frontend via Eel
    eel.DisplayMessage(text)
    eel.receiverText(text)

    # Paths
    piper_dir = "piper"
    piper_path = os.path.join(piper_dir, "piper.exe")
    model_path = os.path.join(piper_dir, "en_US-ryan-low.onnx")
    config_path = os.path.join(piper_dir, "config.json")
    output_file = os.path.join(piper_dir, "output.wav")

    # 🧹 Cleanup previous output
    if os.path.exists(output_file):
        os.remove(output_file)

    # 🔐 Escape double quotes in text
    safe_text = text.replace('"', '\\"')

    # 🔧 Run Piper to generate speech
    command = f'echo {safe_text} | "{piper_path}" -m "{model_path}" -c "{config_path}" -f "{output_file}"'
    os.system(command)

    # 🔊 Play the generated audio
    if os.path.exists(output_file):
        playsound(output_file)
        os.remove(output_file)  # 🧼 Optional: Clean after play
    else:
        print("❌ Failed to generate output.wav")
