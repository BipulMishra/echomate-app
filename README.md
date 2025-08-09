 ## EchoMate ❤️

A Streamlit web app that creates a digital reflection of a loved one from a WhatsApp chat history, powered by Google's Gemini AI.

## Description

EchoMate allows users to upload an exported WhatsApp chat file (`.txt`) and interact with an AI chatbot that mimics the personality, tone, and conversational style of a specific person from that chat. By using the powerful few-shot prompting capabilities of the Gemini `1.5-flash` model, the app generates responses in real-time, creating a unique and personal "digital echo" of your friend, partner, or loved one.

This project is designed to be a fun, personal experience and serves as a powerful demonstration of modern Large Language Model capabilities.

-----

## Features

  * **Dynamic Persona Generation:** No pre-training needed. The AI adopts the persona on-the-fly based on the provided chat examples.
  * **WhatsApp Chat Parsing:** Intelligently parses standard `.txt` chat exports to extract messages from the target user.
  * **Interactive Chat Interface:** A clean and responsive user interface built with Streamlit.
  * **Secure & Session-Based:** Your chat data is processed only for the duration of your session and is never stored on a server.
  * **Robust Name Matching:** The app is designed to handle variations in names, including capitalization, spaces, and most special characters.

-----

## Tech Stack

  * **Frontend:** [Streamlit](https://streamlit.io/)
  * **Backend & Logic:** [Python](https://www.python.org/)
  * **AI Model:** [Google Gemini 1.5 Flash](https://ai.google.dev/)
  * **Core Libraries:** `google-generativeai`, `pandas`

-----

## Setup and Installation

To run this project locally, follow these steps:

**1. Prerequisites:**

  * Python 3.8 or higher
  * Git for cloning the repository

**2. Clone the Repository:**

```bash
git clone https://github.com/your-username/echomate-app.git
cd echomate-app
```

*(Replace `your-username` with your actual GitHub username.)*

**3. Create and Activate a Virtual Environment:**

  * **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
  * **On macOS & Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**4. Install Dependencies:**
Make sure you have a `requirements.txt` file in your project. Then run:

```bash
pip install -r requirements.txt
```

**5. Add Your Gemini API Key:**

  * Get your API key from [Google AI Studio](https://aistudio.google.com/).
  * Open the `app.py` file and paste your key into this line:
    ```python
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    ```
    *(Note: For deployment, it is critical to use Streamlit's Secrets management as shown in the final version of the code.)*

-----

## Usage

**1. Run the App:**
Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
```

Your browser will automatically open with the EchoMate application.

**2. Use the Sidebar:**

  * **Upload File:** Click the "Browse files" button to upload your WhatsApp `.txt` chat export.
  * **Enter Your Name:** Type your name exactly as it appears in the chat file.
  * **Enter Their Name:** Type the name of the person you want the AI to imitate.
  * Click the **"Create Persona"** button.

**3. Start Chatting:**
If the names and file are correct, a success message will appear, and the chat interface will be ready for you to use. Enjoy your conversation\!

-----

## Ethical Disclaimer ⚠️

This project handles personal and sensitive data. It is intended for personal, educational, and experimental purposes only.

  * **Consent is crucial.** Do not use anyone's chat history without their explicit and informed permission.
  * **Privacy:** The application is designed to be session-based, and no chat data is saved or stored permanently. However, be mindful of deploying such applications publicly.

-----

## Author

Built with ❤️ by **Bipul Mishra**.
