# CASCA

**CASCA (Cognitive Autonomous System for Contextual Assistance)** is an offline-first AI assistant designed to provide contextual conversations, memory-based personalization, and voice interaction while keeping user data local.

## Features

* Offline AI assistant
* Local LLM integration using Ollama
* Context-aware memory system
* Voice input and speech output
* Emotion-aware response generation
* Modern desktop GUI
* Privacy-focused local storage
* Personalized interactions through memory recall

## System Architecture

User Input (Text / Voice)
↓
CASCA UI
↓
Speech Processing
↓
Memory Retrieval
↓
Prompt Generation
↓
Local LLM (Llama 3.2 via Ollama)
↓
Response Generation
↓
Text-to-Speech Output

## Technologies Used

* Python
* Ollama
* Llama 3.2
* CustomTkinter
* SpeechRecognition
* pyttsx3
* JSON
* Requests

## Project Structure

```text
CASCA/
│
├── main.py
├── brain.py
├── memory.py
├── voice.py
├── stt.py
├── ui.py
│
├── memory/
├── assets/
└── README.md
```

## Requirements

* Windows 10 / 11
* Python 3.11+
* Ollama
* Llama 3.2 model
* Microphone
* Speakers or headphones

## Installation

1. Install Python.
2. Install Ollama.
3. Pull the model:

```bash
ollama pull llama3.2
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run CASCA:

```bash
python ui.py
```

## Vision

CASCA aims to provide a personal AI experience that remains private, responsive, and accessible without relying on cloud services.

## Future Improvements

* Semantic memory retrieval
* Improved emotion recognition
* Image understanding
* Multimodal interaction
* Mobile version
* Smart device integration

## Author

**Tousif Sheikh**

Master of Computer Applications (MCA)
Assam Don Bosco University
