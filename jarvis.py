import speech_recognition as sr
import os
import subprocess
import json
import threading
import tkinter as tk
import customtkinter as ctk
from groq import Groq
import pygetwindow as gw
import pygame
import keyboard
import time

# ----------------- Configuration -----------------
GROQ_API_KEY = "your_api_key_here"
MEMORY_FILE = "thought.txt"
CHAT_CACHE_FILE = "chat_cache.txt"

client = Groq(api_key=GROQ_API_KEY)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jarvis AI Desktop")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Audio Initialization
        pygame.mixer.init()
        self.current_voice = "en-US-ChristopherNeural" # Default edge-tts voice (smooth male)
        
        # Clear cache files on startup
        if os.path.exists(CHAT_CACHE_FILE):
            try: os.remove(CHAT_CACHE_FILE)
            except: pass
        if os.path.exists("temp_speech.mp3"):
            try: os.remove("temp_speech.mp3")
            except: pass

        # Top bar
        self.lbl_title = ctk.CTkLabel(self, text="JARVIS AI CORE", font=("Segoe UI Black", 24), text_color="#00ffcc")
        self.lbl_title.pack(pady=(20, 10))
        
        # Container for chat text
        self.chat_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        self.chat_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.chat_area = tk.Text(self.chat_frame, wrap=tk.WORD, bg="#1e1e1e", fg="#e0e0e0", font=("Segoe UI", 12), borderwidth=0, highlightthickness=0)
        self.chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Stop Speaking Button
        self.interrupt_btn = ctk.CTkButton(
            self, text="🛑 STOP SPEAKING (Hit \\)", 
            fg_color="#cc0000", hover_color="#ff3333", 
            font=("Segoe UI", 14, "bold"), height=50,
            command=self.interrupt_speech_manual
        )
        self.interrupt_btn.pack(pady=(5, 20), fill=tk.X, padx=20)
        
        # Global Hotkey (\) to interrupt anywhere
        try:
            keyboard.add_hotkey('\\', self.interrupt_speech_hotkey)
        except Exception as e:
            print("Warning: Could not bind global hotkey (requires admin privileges).")
        
        # Start AI Loop
        self.running = True
        self.ai_thread = threading.Thread(target=self.ai_loop, daemon=True)
        self.ai_thread.start()

    def log(self, sender, text):
        def update_ui():
            self.chat_area.config(state=tk.NORMAL)
            
            self.chat_area.insert(tk.END, f"[{sender}]: ", (sender,))
            self.chat_area.insert(tk.END, f"{text}\n\n")
            
            self.chat_area.tag_config("JARVIS", foreground="#00ffcc", font=("Segoe UI", 12, "bold"))
            self.chat_area.tag_config("YOU", foreground="#ffb700", font=("Segoe UI", 12, "bold"))
            self.chat_area.tag_config("SYSTEM", foreground="#ff5555", font=("Segoe UI", 12, "bold"))
            
            self.chat_area.yview(tk.END)
            self.chat_area.config(state=tk.DISABLED)
            
            with open(CHAT_CACHE_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{sender}]: {text}\n\n")
                
        self.after(0, update_ui)

    def interrupt_speech_manual(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.log("SYSTEM", "Speech Interrupted by User.")
            
    def interrupt_speech_hotkey(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.log("SYSTEM", "Speech Interrupted by Backslash (\\).")

    def speak(self, text):
        self.log("JARVIS", text)
        if not text:
            return
            
        clean_text = text.replace("'", "").replace('"', "").replace('\n', ' ')
        audio_file = "temp_speech.mp3"
        
        try:
            # Generate human-like audio using edge-tts module directly (much faster than subprocess)
            import asyncio
            import edge_tts
            
            async def gen():
                # Increased the rate by 20% to make him speak faster and sound more energetic
                communicate = edge_tts.Communicate(clean_text, self.current_voice, rate="+20%")
                await communicate.save(audio_file)
                
            asyncio.run(gen())
            
            # Play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Block until finished or interrupted
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Audio Error: {e}")

    def on_closing(self):
        self.running = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        pygame.mixer.quit()
        
        if os.path.exists("temp_speech.mp3"):
            try: os.remove("temp_speech.mp3")
            except: pass
            
        if os.path.exists(CHAT_CACHE_FILE):
            try: os.remove(CHAT_CACHE_FILE)
            except: pass
        
        self.destroy()
        os._exit(0)

    # ----------------- Tools -----------------
    
    def get_active_window_title(self):
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                title = active_window.title
                return f"The user is currently looking at: {title}"
            return "No active window found."
        except Exception as e:
            return f"Error reading screen: {e}"

    def change_voice(self, voice_type):
        voice_type = voice_type.lower()
        if "female" in voice_type:
            self.current_voice = "en-US-AriaNeural"
        elif "hindi" in voice_type or "indian" in voice_type:
            self.current_voice = "en-IN-NeerjaNeural"
        else:
            self.current_voice = "en-US-ChristopherNeural"
            
        return f"Voice changed to {voice_type} successfully using Azure Neural TTS."

    def save_thought(self, thought):
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"- {thought}\n")
        return "Thought memorized successfully."

    def edit_memory(self, new_content):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            f.write(new_content + "\n")
        return "Memory completely overwritten successfully."

    def read_thoughts(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "No prior thoughts recorded yet."

    def listen_and_transcribe(self, recognizer, source, timeout=1, phrase_time_limit=10):
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        wav_data = audio.get_wav_data()
        transcription = client.audio.transcriptions.create(
            file=("audio.wav", wav_data),
            model="whisper-large-v3",
        )
        return transcription.text.strip()

    def listen_for_confirmation(self, recognizer, source):
        try:
            text = self.listen_and_transcribe(recognizer, source, timeout=5, phrase_time_limit=5).lower()
            self.log("YOU", text)
            return text
        except:
            return ""

    def ask_confirmation(self, recognizer, source, command):
        self.speak(f"Warning. I need to execute a potentially destructive command: {command}")
        self.speak("Please say 'yes confirm' to proceed.")
        
        first = self.listen_for_confirmation(recognizer, source)
        if "yes" in first or "confirm" in first:
            self.speak("First confirmation received. Please say 'yes confirm' one more time.")
            second = self.listen_for_confirmation(recognizer, source)
            if "yes" in second or "confirm" in second:
                self.speak("Second confirmation received.")
                return True
            else:
                self.speak("Second confirmation failed.")
                return False
        else:
            self.speak("Action aborted.")
            return False

    def execute_terminal_command(self, command, recognizer, source):
        dangerous_keywords = ["del ", "rmdir", "remove-item", "format ", "rm "]
        is_dangerous = any(keyword in command.lower() for keyword in dangerous_keywords)
        
        if is_dangerous:
            confirmed = self.ask_confirmation(recognizer, source, command)
            if not confirmed:
                return "Execution aborted by user due to safety rules."
                
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            output = result.stdout.strip()
            err = result.stderr.strip()
            if result.returncode == 0:
                return f"Command executed successfully. Output: {output}"[:500]
            else:
                return f"Command failed. Error: {err}"[:500]
        except Exception as e:
            return f"Error executing command: {str(e)}"

    # ----------------- LLM Logic -----------------
    def get_llm_response(self, messages, recognizer, source):
        thoughts_content = self.read_thoughts()
        system_prompt = f"""You are Jarvis, a highly intelligent, proactive, and curious AI voice assistant running directly inside the user's PC.
YOUR CORE CONDITION AND RULES:
1. You are working as an AI in a user's local PC environment. Data protection is your highest priority.
2. Keep your spoken responses concise, natural, and conversational (1-3 sentences max) because they are read aloud. ALWAYS reply in English text (even if the user speaks another language).
3. BE PROACTIVE AND CURIOUS: Do not just act like a generic bot answering requests. Ask follow up questions, ask about their day, offer to help.
4. You have a Screen Awareness tool (get_active_window_title). If the user asks what they are looking at, use it!
5. Use save_thought or edit_memory tools to permanently remember facts.

Here are your core memories and conditions from thought.txt:
{thoughts_content}
"""
        messages[0] = {"role": "system", "content": system_prompt}

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_terminal_command",
                    "description": "Execute a shell command on the user's Windows machine. Use powershell syntax.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The command to run."}
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "change_voice",
                    "description": "Change Jarvis's speaking voice. Options: 'male', 'female', 'hindi'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "voice_type": {"type": "string", "description": "The voice type to switch to."}
                        },
                        "required": ["voice_type"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "save_thought",
                    "description": "Append an important thought, condition, or memory to thought.txt.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "thought": {"type": "string", "description": "The thought to append."}
                        },
                        "required": ["thought"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_memory",
                    "description": "Completely overwrite the thought.txt file. Use this to delete or fix thoughts.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "new_content": {"type": "string", "description": "The fully rewritten content for thought.txt."}
                        },
                        "required": ["new_content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_active_window_title",
                    "description": "Read the title of the active window on the user's screen. Use this when the user asks what they are looking at or what they are doing.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    },
                },
            }
        ]

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=200,
        )
        
        response_message = response.choices[0].message
        tool_calls = getattr(response_message, 'tool_calls', None)
        
        if tool_calls:
            # Reconstruct the message to avoid groq serialization bugs
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in tool_calls]
            })
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                self.log("SYSTEM", f"[Tool Call] {function_name}({function_args})")
                
                if function_name == "execute_terminal_command":
                    result = self.execute_terminal_command(function_args.get("command"), recognizer, source)
                elif function_name == "change_voice":
                    result = self.change_voice(function_args.get("voice_type"))
                elif function_name == "save_thought":
                    result = self.save_thought(function_args.get("thought"))
                elif function_name == "edit_memory":
                    result = self.edit_memory(function_args.get("new_content"))
                elif function_name == "get_active_window_title":
                    result = self.get_active_window_title()
                else:
                    result = f"Error: function {function_name} does not exist"
                    
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": result,
                    }
                )
                
            second_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=tools,
                max_tokens=200,
            )
            final_msg = second_response.choices[0].message.content
            messages.append({"role": "assistant", "content": final_msg})
            return final_msg
        else:
            final_msg = response_message.content
            if final_msg:
                messages.append({"role": "assistant", "content": final_msg})
            return final_msg

    def ai_loop(self):
        recognizer = sr.Recognizer()
        self.speak("Jarvis AI Desktop is online. Listening.")
        
        messages = [{"role": "system", "content": ""}]
        
        with sr.Microphone() as source:
            self.log("SYSTEM", "Calibrating microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            self.log("SYSTEM", "Ready.")
            
            while self.running:
                try:
                    text = self.listen_and_transcribe(recognizer, source)
                    if not text:
                        continue
                        
                    hallucinations = ["thank you.", "thank you", "thanks for watching.", "thanks for watching", "bye.", "bye", "you", "you.", "."]
                    if text.lower() in hallucinations:
                        continue
                        
                    self.log("YOU", text)
                    messages.append({"role": "user", "content": text})
                    
                    if len(messages) > 15:
                        messages = [messages[0]] + messages[-14:]
                        
                    response_text = self.get_llm_response(messages, recognizer, source)
                    
                    if response_text:
                        self.speak(response_text)
                        
                except sr.WaitTimeoutError:
                    pass 
                except Exception as e:
                    if "WaitTimeoutError" not in str(e):
                        print(f"Error: {e}")

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
