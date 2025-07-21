   # 🧠 Jarvis Desktop Assistant

   **Jarvis** is a Python-powered personal voice assistant for desktop automation and voice interactions. It uses speech recognition, offline TTS, GUI automation, and ADB integration to interact and control your system with your voice.

   ---

   ## 🚀 Features

   - 🎙️ Voice interaction using wake word detection and commands
   - 🧠 Smart responses (Wikipedia, search)
   - 🖱️ Mouse and keyboard automation
   - 🌐 Web interface (Flask + Eel)
   - 🗣️ Offline TTS via [Piper](https://github.com/rhasspy/piper)
   - 📱 ADB over Wi-Fi (automated via `.bat`)

   ---

   ## 🛠️ Tech Stack

   - **Languages**: Python 3
   - **Frontend**: HTML/CSS via Eel
   - **Backend**: Flask, Bottle
   - **Voice/Audio**: Piper, Pyttsx3, PyAudio, SpeechRecognition, pvporcupine
   - **Automation**: PyAutoGUI, keyboard
   - **Utilities**: requests, wikipedia, BeautifulSoup4

   ---

   ## 📁 Project Structure

   ```
   jarvis/
   ├── engine/
   ├── piper/
   │   ├── piper.exe
   │   ├── en_US-ryan-low.onnx
   │   └── en_US-ryan-low.onnx.json
   ├── envjarvis/
   ├── run.py
   ├── requirements.txt
   ├── start_jarvis.bat
   ├── connect_device.bat
   └── README.md
   ```

   ---

   ## 📦 Installation

   1. Clone the repo and navigate inside:
      ```bash
      git clone https://github.com/yourusername/jarvis-assistant.git
      cd jarvis-assistant
      ```

   2. Create a virtual environment:
      ```bash
      python -m venv envjarvis
      .\envjarvis\Scripts\activate
      ```

   3. Install required packages:
      ```bash
      pip install -r requirements.txt
      ```

   ---

   ## 🧾 Piper TTS Setup

   1. Download Piper binary:
      - [Piper Releases](https://github.com/rhasspy/piper/releases)
      - Extract `piper.exe` into the `piper/` folder.

   2. Download a voice model:
      - Example: `en_US-ryan-low.onnx` and `en_US-ryan-low.onnx.json`
      - Put them in the same `piper/` folder.

   3. Optional: Test Piper manually:
      ```bash
      .\piper.exe -m piper\en_US-ryan-low.onnx -f output.wav
      ```

   ---

   ## 📱 ADB Wi-Fi Connection

   1. Enable Developer Mode & USB Debugging on Android.
   2. Connect via USB at least once to trust the PC.
   3. Run the script:
      ```bash
      .\connect_device.bat
      ```

   It will:
   - Disconnect old ADB sessions
   - Switch the device to TCP/IP mode
   - Auto-detect IP and connect over Wi-Fi

   If IP detection fails, you can edit the fallback IP in the script.

   ---

   ## 📸 Future Improvements

   - ChatGPT API integration
   - Spotify/YT Music support
   - Browser automation

   ---

   ## 👤 Author

   - **Om Jumde**
   - GitHub: [@Yaro957](https://github.com/Yaro957)

   ---
