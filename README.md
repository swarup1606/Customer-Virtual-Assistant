# Customer Virtual Assistant (CVA) 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview 🌟

Welcome to **Customer Virtual Assistant (CVA)**, an innovative Python-based assistant designed to provide seamless interactions through both voice and text. With a sleek graphical interface and robust functionalities—including speech recognition, text-to-speech, image processing, and multimedia integration—this project is perfect for delivering outstanding customer support.

---

![Screenshot 2025-02-19 134737](https://github.com/user-attachments/assets/111285f4-e4ad-4435-95c5-334e0a0155b3)

## Table of Contents 📑

- [Features](#features-)
- [Installation](#installation-)
- [Usage](#usage-)
- [Modules and Libraries](#modules-and-libraries-)
- [Project Structure](#project-structure-)
- [License](#license-)
- [Contact](#contact-)

---

## Features ✨

- **Interactive GUI:** Built with `tkinter` for an intuitive and user-friendly experience.
- **Voice Recognition:** Leverages `speech_recognition` to convert your voice into text.
- **Text-to-Speech:** Utilizes `pyttsx3` and `gTTS` for dynamic audio feedback.
- **Image & Multimedia Integration:** Powered by `Pillow` and `pygame` to enrich interactions.
- **Smooth Performance:** Uses `threading` to ensure a responsive, non-blocking interface.
- **Modular Design:** Easily extendable to suit various customer support needs.

---

## Installation 🔧

### Prerequisites

- **Python 3.8 or later** (use the latest one)
- **pip** (Python package installer)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/swarup1606/customer-Virtual-Assistant.git
   cd Customer-Virtual-Assistant
   
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
- Note: Modules like tkinter, json, os, tempfile, random, and time are part of the Python Standard Library and require no additional installation.
  
### Usage 🚀

To launch the virtual assistant, simply run:
```bash
python main.py
```
A GUI window will appear, allowing you to interact with the assistant via both voice commands and text input. Enjoy the seamless experience!
   
### Modules and Libraries 🛠

This project utilizes several powerful Python libraries:

- tkinter: For building the interactive GUI.
- Pillow (PIL): For image processing and manipulation.
- pyttsx3: For offline text-to-speech conversion.
- speech_recognition: To capture and interpret voice commands.
- gTTS: For text-to-speech conversion using Google Text-to-Speech.
- pygame: For advanced audio playback and multimedia features.
- requests: For making HTTP requests (if needed).
- threading: To ensure smooth UI performance by handling background tasks.
- Standard Libraries: Including json, os, tempfile, random, and time.

### Project Structure 📁

Here’s a suggested directory layout for clarity and maintainability:
```bash
customer-Virtual-Assistant
├── .venv                    # Virutal Environment
├── mic_icon                 # Mic icon image
├── Asst.py                  # Main application file
├── requirements.txt         # List of project dependencies
└── README.md                # Project documentation (this file)
```
### requirements.txt
```bash
Pillow
pyttsx3
SpeechRecognition
gTTS
pygame
requests
```

### License 📄
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact 📫
For questions, feedback, or suggestions, please reach out:

- Swarup Satish Kakade
- swarupkakade1810@gmail.com
- https://github.com/swarup1606
- https://www.linkedin.com/in/swarup1109/

### DEMO VIDEO
https://www.loom.com/share/ddc1363e5eb04decbf006fc22491eef4?sid=13b5d2dd-bfaf-4021-bd9d-9877664db942

### Made with ❤️ and Python 🐍

