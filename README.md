<div align="center">

# 🤖 Jarvis AI Core

**A powerful, proactive AI desktop assistant that runs locally on Windows.**

Jarvis listens, understands, speaks with natural voices, remembers your preferences, and can safely execute terminal commands — all from a sleek desktop UI.

<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
<img src="https://img.shields.io/badge/Groq-Powered-orange?style=for-the-badge" alt="Groq API" />
<img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Platform" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />

</div>

---

## ✨ Features

| | |
|---|---|
| 🎙️ **Voice Recognition** | Ultra-fast transcription powered by Whisper Large-v3 via Groq |
| 🗣️ **Natural TTS** | Smooth, human-like voice synthesis using Azure Edge TTS |
| 👀 **Screen Awareness** | Knows which window you're actively looking at |
| 💻 **Terminal Control** | Executes PowerShell commands securely with voice confirmation |
| 🧠 **Persistent Memory** | Remembers important thoughts and preferences across sessions |
| 🎨 **Modern UI** | Sleek, dark-mode desktop interface built with CustomTkinter |

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Getting Your Groq API Key](#-getting-your-groq-api-key)
- [Installation](#-installation)
- [Running Jarvis](#-running-jarvis)
- [Usage Tips](#️-usage-tips)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧰 Prerequisites

- **Python 3.12** — [Download here]([https://www.python.org/downloads/](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe))
  > ⚠️ Be sure to check **"Add Python to PATH"** during installation.
- **Microphone & speakers** — required for Jarvis to hear you and talk back.

---

## 🔑 Getting Your Groq API Key

Jarvis uses [Groq](https://console.groq.com/) for lightning-fast AI reasoning and voice transcription.

1. Go to the [Groq Console](https://console.groq.com/) and create an account (or log in).
2. Navigate to **API Keys**.
3. Click **Create API Key** and copy the generated key.
4. Open `main.py` and set your key near the top of the file:

   ```python
   GROQ_API_KEY = "your_api_key_here"
   ```

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/jarvis-ai-core.git
cd jarvis-ai-core

# 2. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running Jarvis

```bash
python jarvis.py
```

Jarvis will launch its UI, calibrate your microphone, and announce that he's online and ready to assist. 🎉

---

## 🛠️ Usage Tips

- **⛔ Interrupt Jarvis:** Press `\` (backslash) anywhere on your PC to instantly stop him from speaking.
- **⚡ Run commands:** Ask Jarvis to execute terminal commands for you. Dangerous actions (like deleting files) require a double verbal confirmation — just say **"yes confirm."**
- **🎭 Change his voice:** Simply ask Jarvis to switch voices at any time.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://alite.webuilt.dev) or open a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made By Alite for anyone who's always wanted their own JARVIS.

</div>
