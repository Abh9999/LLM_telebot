# Local AI Assistant Prototype 🤖

A Secure, and locally hosted AI chatbot interface built with Python.

## 🎯 Project Overview
This project demonstrates a **Full-Stack AI implementation** integrating a Large Language Model (LLM) with a user-friendly interface (Telegram). The goal was to create an AI assistant that runs **locally on consumer hardware**, ensuring data privacy and zero cloud dependency.

**Key Features:**
* **Local Inference:** Uses `TinyLlama-1.1B` running offline for maximum data privacy.
* **Latency Management:** Implements asynchronous `chat_action` updates to manage user expectations during inference time.
* **Secure Deployment:** Utilizes `.env` environment variables to strictly separate secrets from the codebase.

## 🛠 Tech Stack
* **Language:** Python 3.9+
* **Model:** TinyLlama 1.1B (via Hugging Face Transformers)
* **Interface:** Python-Telegram-Bot API
* **Optimization:** `torch.bfloat16` for memory efficiency

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Abh9999/LLM_telebot](https://github.com/Abh9999/LLM_telebot)
   cd Local-LLM-Assistant
