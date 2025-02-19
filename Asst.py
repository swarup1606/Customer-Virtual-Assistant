import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import requests
import json
import threading
from gtts import gTTS
import os
import tempfile
import pygame
import random
import time  # Needed for delaying deletion of the temp file

try:
    from playsound import playsound
except ImportError:
    playsound = None

WIT_ACCESS_TOKEN = "XZF3P3IDPPTU2YG5O6FUIU36E6654G77"  # Replace with your Wit.ai token

class VirtualAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Virtual Assistant")
        self.root.geometry("680x800")
        self.root.configure(bg="#f7f7f7")
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        self.current_language = "en"
        self.language_codes = {"en": "en-US", "hi": "hi-IN"}
        
        # General messages for status and responses
        self.messages = {
            "welcome": {
                "en": "Welcome to our Virtual Assistant. How may I assist you today?",
                "hi": "हमारे वर्चुअल असिस्टेंट में आपका स्वागत है। मैं आपकी कैसे सहायता कर सकता हूँ?"
            },
            "listening": {
                "en": "Listening...",
                "hi": "सुन रहा है..."
            },
            "transcribing": {
                "en": "Transcribing...",
                "hi": "लिख रहा है..."
            },
            "you_said": {
                "en": "You said: ",
                "hi": "आपने कहा: "
            },
            "recognized_intent": {
                "en": "Recognized Intent: ",
                "hi": "पहचाना गया इरादा: "
            },
            "assistant": {
                "en": "Assistant: ",
                "hi": "सहायक: "
            },
            "unknown_request": {
                "en": "Sorry, I couldn't understand your request.",
                "hi": "क्षमा करें, मैं आपकी अनुरोध समझ नहीं पाया।"
            },
            "saving_conv": {
                "en": "Conversation saved to",
                "hi": "वार्तालाप सहेजा गया:"
            },
            "goodbye": {
                "en": "Thank you for using our service. Have a great day!",
                "hi": "हमारी सेवा का उपयोग करने के लिए धन्यवाद। आपका दिन शुभ हो!"
            },
            "error": {
                "en": "An error occurred. Please try again.",
                "hi": "एक त्रुटि हुई है। कृपया पुनः प्रयास करें।"
            },
            "troubleshooting": {
                "en": ("Here are some troubleshooting suggestions: Please restart your device, check all connections, update your software, "
                       "try unplugging and replugging any external devices, and ensure your drivers are up to date. "
                       "If the problem persists, a technician visit may be required."),
                "hi": ("यहाँ कुछ ट्रबलशूटिंग सुझाव हैं: कृपया अपने डिवाइस को पुनः प्रारंभ करें, सभी कनेक्शन की जांच करें, अपने सॉफ़्टवेयर को अपडेट करें, "
                       "किसी भी बाहरी उपकरण को अनप्लग करके फिर से प्लग करें, और सुनिश्चित करें कि आपके ड्राइवर अद्यतित हैं। "
                       "यदि समस्या बनी रहती है, तो तकनीशियन की यात्रा आवश्यक हो सकती है।")
            },
            "warranty_response": {
                "en": ("Thank you. Your warranty claim has been recorded. Please check your email for further instructions regarding your warranty claim. "
                       "Also, please ensure that you have your purchase receipt ready."),
                "hi": ("धन्यवाद। आपका वारंटी दावा रिकॉर्ड कर लिया गया है। कृपया आगे के निर्देशों के लिए अपना ईमेल चेक करें। "
                       "साथ ही, कृपया सुनिश्चित करें कि आपके पास खरीद रसीद उपलब्ध है।")
            }
        }
        
        # Prompts for gathering user details and confirmations
        self.prompts = {
            "full_name": {
                "en": "Please provide your full name.",
                "hi": "कृपया अपना पूरा नाम बताएं।"
            },
            "contact_info": {
                "en": "Please provide your contact number.",
                "hi": "कृपया अपना संपर्क नंबर बताएं।"
            },
            "contact_info_valid": {
                "en": "Please provide a valid 10-digit phone number.",
                "hi": "कृपया एक मान्य 10-अंकीय फोन नंबर बताएं।"
            },
            "address": {
                "en": "Please provide your address.",
                "hi": "कृपया अपना पता बताएं।"
            },
            "issue_details": {
                "en": "Please describe the technical issue in detail.",
                "hi": "कृपया तकनीकी समस्या का विस्तृत विवरण बताएं।"
            },
            "preferred_time": {
                "en": "What is your preferred date and time for a technician visit?",
                "hi": "तकनीशियन की यात्रा के लिए आपका पसंदीदा दिन और समय क्या है?"
            },
            "confirmation": {
                "en": "Is the above information correct? Please say 'yes' or 'no'.",
                "hi": "क्या उपरोक्त जानकारी सही है? कृपया 'हां' या 'नहीं' कहें।"
            },
            "thanks": {
                "en": "Thank you. Your information has been recorded.",
                "hi": "धन्यवाद। आपकी जानकारी दर्ज कर ली गई है।"
            },
            "troubleshooting_prompt": {
                "en": "We will now provide some troubleshooting suggestions.",
                "hi": "अब हम कुछ ट्रबलशूटिंग सुझाव देंगे।"
            },
            "followup_troubleshooting": {
                "en": "Did those steps help? Please say 'yes' or 'no'.",
                "hi": "क्या ये कदम मददगार रहे? कृपया 'हां' या 'नहीं' कहें।"
            },
            "fun_fact_prompt": {
                "en": "Would you like to hear a fun fact? Please say 'yes' or 'no'.",
                "hi": "क्या आप एक रोचक तथ्य सुनना चाहेंगे? कृपया 'हां' या 'नहीं' कहें।"
            }
        }
        
        pygame.mixer.init()
        self.setup_style()
        self.setup_menu()
        self.setup_ui()
        self.speak(self.messages["welcome"][self.current_language])
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f7f7f7")
        style.configure("TLabel", background="#f7f7f7", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#f7f7f7", foreground="#333333")
        style.configure("TButton", font=("Helvetica", 10), background="#e0e0e0")
        style.configure("TEntry", font=("Helvetica", 10))
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Conversation", command=self.save_conversation)
        file_menu.add_command(label="Clear Conversation", command=self.clear_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About",
            "Customer Virtual Assistant\nEnhanced with Voice & Text Input\nSupports English & Hindi\nNow with self-help troubleshooting and warranty claim prompts!"))
        menubar.add_cascade(label="Help", menu=about_menu)
        self.root.config(menu=menubar)
    
    def setup_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.columnconfigure(0, weight=1)
        header_label = ttk.Label(top_frame, text="Customer Virtual Assistant", style="Header.TLabel")
        header_label.pack(side=tk.LEFT, padx=(0, 20))
        lang_label = ttk.Label(top_frame, text="Language:")
        lang_label.pack(side=tk.LEFT, padx=(10, 2))
        self.lang_var = tk.StringVar(value="English")
        lang_options = ttk.Combobox(top_frame, textvariable=self.lang_var, values=["English", "Hindi"], state="readonly", width=10)
        lang_options.pack(side=tk.LEFT, padx=5)
        lang_options.bind("<<ComboboxSelected>>", self.on_language_change)
        
        mid_frame = ttk.Frame(self.root)
        mid_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        instruction_label = ttk.Label(mid_frame, text="Click the mic to start and speak after listening.", font=("Arial", 13, "bold"))
        instruction_label.pack(pady=(5, 2))
        self.conversation = scrolledtext.ScrolledText(mid_frame, wrap=tk.WORD, height=20, font=("Arial", 11),
                                                       bg="#ffffff", relief=tk.SUNKEN, bd=2)
        self.conversation.pack(fill=tk.BOTH, expand=True)
        self.conversation.configure(state="disabled")
        
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        bottom_frame.columnconfigure(1, weight=1)
        try:
            mic_img_path = "mic_icon.png"  # Adjust path if needed
            mic_image = Image.open(mic_img_path)
            mic_image = mic_image.resize((50, 50))
            self.mic_photo = ImageTk.PhotoImage(mic_image)
            voice_button = ttk.Button(bottom_frame, image=self.mic_photo, command=self.process_voice_request)
        except Exception:
            voice_button = ttk.Button(bottom_frame, text="Voice", command=self.process_voice_request)
        voice_button.grid(row=0, column=0, padx=5, pady=5)
        self.text_entry = ttk.Entry(bottom_frame, width=40)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.text_entry.bind("<Return>", lambda event: self.process_text_request())
        text_button = ttk.Button(bottom_frame, text="Submit Query", command=self.process_text_request)
        text_button.grid(row=0, column=2, padx=5, pady=5)
        clear_button = ttk.Button(bottom_frame, text="Clear Conversation", command=self.clear_conversation)
        clear_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=1)
        save_button = ttk.Button(bottom_frame, text="Save Conversation", command=self.save_conversation)
        save_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
        funfact_button = ttk.Button(bottom_frame, text="Fun Fact", command=self.tell_fun_fact)
        funfact_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=3)
    
    def add_to_conversation(self, speaker, text):
        self.conversation.configure(state="normal")
        self.conversation.insert(tk.END, f"{speaker} {text}\n")
        self.conversation.see(tk.END)
        self.conversation.configure(state="disabled")
    
    def on_language_change(self, event):
        selection = self.lang_var.get()
        self.current_language = "hi" if selection == "Hindi" else "en"
        self.speak(self.messages["welcome"][self.current_language])
    
    def speak(self, text):
        # Add text to conversation window
        self.add_to_conversation(self.messages["assistant"][self.current_language], text)
        
        # For Hindi, use gTTS with a temporary file
        if self.current_language == "hi":
            try:
                tts = gTTS(text=text, lang="hi")
                # Create a temporary file that is not automatically deleted
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                tts.save(temp_path)
                if playsound:
                    playsound(temp_path)
                    # Wait a bit to ensure the file is released
                    time.sleep(1)
                else:
                    pygame.mixer.music.load(temp_path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                # Attempt to delete the temporary file safely.
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            except Exception as e:
                self.add_to_conversation("Error:", f"TTS Error: {str(e)}")
        else:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.add_to_conversation("Error:", f"TTS Error: {str(e)}")
    
    def speech_to_text(self):
        try:
            with sr.Microphone() as source:
                self.add_to_conversation("", self.messages["listening"][self.current_language])
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source)
            self.add_to_conversation("", self.messages["transcribing"][self.current_language])
            lang_code = self.language_codes.get(self.current_language, "en-US")
            # Check if 'recognize_google' method exists
            if not hasattr(self.recognizer, 'recognize_google'):
                self.add_to_conversation("", "Error: 'recognize_google' not found. Please check your SpeechRecognition installation.")
                return ""
            text = self.recognizer.recognize_google(audio, language=lang_code)
            self.add_to_conversation("", self.messages["you_said"][self.current_language] + text)
            return text
        except sr.UnknownValueError:
            self.add_to_conversation("", "Sorry, I couldn't understand what you said.")
            return ""
        except sr.RequestError as e:
            self.add_to_conversation("", f"Speech recognition error: {e}")
            return ""
    
    def is_affirmative(self, response):
        if self.current_language == "en":
            valid_yes = ["yes", "yeah", "yep", "correct"]
            return any(word in response.lower() for word in valid_yes)
        else:
            valid_yes = ["हां", "हाँ", "जी हां"]
            return any(word in response for word in valid_yes)
    
    def get_valid_response(self, prompt_key):
        while True:
            self.speak(self.prompts[prompt_key][self.current_language])
            response = self.speech_to_text()
            if response.strip():
                return response
            else:
                self.speak(self.messages["error"][self.current_language])
    
    def get_valid_phone_number(self):
        while True:
            response = self.get_valid_response("contact_info")
            phone = ''.join(filter(str.isdigit, response))
            if len(phone) == 10:
                return phone
            else:
                self.speak(self.prompts["contact_info_valid"][self.current_language])
    
    def analyze_intent(self, text):
        # For Hindi, use simple keyword matching
        if self.current_language == "hi":
            text_lower = text.lower()
            if "तकनीकी" in text_lower or "समस्या" in text_lower or "मुद्दा" in text_lower:
                return "technical_issue"
            elif "वारंटी" in text_lower or "दावा" in text_lower:
                return "warranty_claim"
            elif "तथ्य" in text_lower or "मज़ेदार" in text_lower or "रोचक" in text_lower:
                return "fun_fact"
            else:
                return "Unknown"
        else:
            headers = {"Authorization": f"Bearer {WIT_ACCESS_TOKEN}"}
            params = {"q": text}
            try:
                response = requests.get("https://api.wit.ai/message", headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('intents'):
                        return data['intents'][0]['name']
                return "Unknown"
            except Exception as e:
                self.add_to_conversation("", f"Intent analysis error: {str(e)}")
                return "Unknown"
    
    def extract_information(self, intent):
        if intent in ["warranty_claim", "technical_issue"]:
            full_name = self.get_valid_response("full_name")
            contact_info = self.get_valid_phone_number()
            try:
                contact_info = int(contact_info)
            except:
                pass
            address = self.get_valid_response("address")
            issue_details = self.get_valid_response("issue_details")
            preferred_time = self.get_valid_response("preferred_time")
            
            confirmation = self.get_valid_response("confirmation")
            if not self.is_affirmative(confirmation):
                self.speak("Let's try again. " + self.messages["error"][self.current_language])
                return self.extract_information(intent)
            return full_name, contact_info, address, issue_details, preferred_time
        else:
            return "", "", "", "", ""
    
    def handle_troubleshooting(self, query):
        self.speak(self.messages["troubleshooting"][self.current_language])
    
    def tell_fun_fact(self):
        fun_facts = [
            "Did you know the first computer bug was an actual moth found in a computer?",
            "A single Google query uses 1,000 computers in 0.2 seconds to retrieve an answer.",
            "The first computer programmer was Ada Lovelace in the 1800s.",
            "Did you know that more people own a mobile phone than a toothbrush?",
            "The world's first website is still online. It was created by Tim Berners-Lee in 1991.",
            "A standard computer keyboard has over 100 keys, each with its own history.",
            "Some calculators were once used in space missions!",
            "The word 'robot' comes from a Czech word meaning 'forced labor'."
        ]
        fact = random.choice(fun_facts)
        self.speak(fact)
    
    def save_to_json(self, full_name, contact_info, address, issue_details, preferred_time):
        data = {
            "Full Name": full_name,
            "Contact Information": contact_info,
            "Address": address,
            "Issue Details": issue_details,
            "Preferred Time": preferred_time
        }
        try:
            with open("user_data.json", "a", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                file.write("\n")
        except Exception as e:
            self.add_to_conversation("", f"Error saving data: {str(e)}")
    
    def process_voice_request(self):
        threading.Thread(target=self._process_request, args=(None,), daemon=True).start()
    
    def process_text_request(self):
        text = self.text_entry.get().strip()
        if text:
            self.text_entry.delete(0, tk.END)
            threading.Thread(target=self._process_request, args=(text,), daemon=True).start()
    
    def _process_request(self, text_input):
        # Use language-appropriate prompt if no text is provided
        if not text_input:
            if self.current_language == "hi":
                self.add_to_conversation("", "कृपया तकनीकी समस्या या वारंटी दावा कहें।")
            else:
                self.add_to_conversation("", "SAY TECHNICAL ISSUE OR WARRANTY CLAIM")
            audio_text = self.speech_to_text()
        else:
            audio_text = text_input
        
        if audio_text:
            intent = self.analyze_intent(audio_text)
            self.add_to_conversation(self.messages["recognized_intent"][self.current_language], intent)
            
            if intent == "technical_issue":
                # For technical issues, first gather user information.
                full_name, contact_info, address, issue_details, preferred_time = self.extract_information(intent)
                # Provide troubleshooting suggestions.
                self.speak(self.prompts["troubleshooting_prompt"][self.current_language])
                self.handle_troubleshooting(audio_text)
                # Ask if the suggestions helped.
                self.speak(self.prompts["followup_troubleshooting"][self.current_language])
                followup = self.speech_to_text()
                if self.is_affirmative(followup):
                    if self.current_language == "hi":
                        self.speak("बहुत अच्छा! मुझे खुशी है कि मैं आपकी सहायता कर सका।")
                    else:
                        self.speak("Great! Glad I could help.")
                else:
                    if self.current_language == "hi":
                        self.speak("ठीक है, मैं एक तकनीशियन की यात्रा निर्धारित करूंगा।")
                    else:
                        self.speak("Alright, I will schedule a technician visit.")
                    self.save_to_json(full_name, contact_info, address, issue_details, preferred_time)
                    if self.current_language == "hi":
                        self.speak("आपकी जानकारी रिकॉर्ड कर ली गई है। तकनीशियन जल्द ही आपसे संपर्क करेंगे।")
                    else:
                        self.speak("Your details have been recorded. A technician will visit you soon.")
            
            elif intent == "warranty_claim":
                # For warranty claims, gather user information and then provide warranty-specific prompts.
                full_name, contact_info, address, issue_details, preferred_time = self.extract_information(intent)
                self.save_to_json(full_name, contact_info, address, issue_details, preferred_time)
                self.speak(self.messages["warranty_response"][self.current_language])
            
            elif intent == "fun_fact":
                self.tell_fun_fact()
            
            else:
                self.speak(self.messages["unknown_request"][self.current_language])
    
    def save_conversation(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(self.conversation.get(1.0, tk.END))
                self.add_to_conversation("", f"{self.messages['saving_conv'][self.current_language]} {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save conversation: {str(e)}")
    
    def clear_conversation(self):
        self.conversation.configure(state="normal")
        self.conversation.delete(1.0, tk.END)
        self.conversation.configure(state="disabled")
        self.add_to_conversation("", "Conversation cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualAssistantApp(root)
    root.mainloop()
