# Car Expert AI Chatbot

A Flask-based chatbot project focused on automobile questions, powered by Google Gemini.

This is a personal project that I built on my own to practice AI integration, backend APIs, and frontend chat UI development.

## Features

- Car-focused AI assistant (filters non-car questions)
- Gemini model integration for natural responses
- Structured response format for car information:
  - Car Name
  - Manufacturer
  - Engine
  - Top Speed
  - Horsepower
  - Torque
  - Mileage / Range
  - Fuel Type
  - Transmission
  - Price Range
  - Key Features
- Chat history saved in JSON
- Responsive frontend UI with chat history sidebar

## Tech Stack

- Python
- Flask
- Google Generative AI SDK
- HTML, CSS, JavaScript

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- chat_history.json
`-- templates/
    `-- index.html
```

## Prerequisites

- Python 3.10+
- A Google Gemini API key

## Setup and Run

1. Clone the repository:

```bash
git clone <your-repo-url>
cd gemini-chatbot
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your API key:

- Open `app.py`.
- Replace the existing key in `genai.configure(api_key="...")` with your own Gemini API key.

5. Run the app:

```bash
python app.py
```

6. Open in browser:

- http://127.0.0.1:5000/

## Important Security Note

- Do not push your real API key to GitHub.
- Always use your own key.
- Before pushing code, remove hardcoded secrets and prefer environment variables.

Example (recommended approach):

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

Then set it in PowerShell before running:

```powershell
$env:GEMINI_API_KEY="your_actual_key_here"
python app.py
```

## API Endpoints

- `GET /` -> Chat UI
- `POST /chat` -> Send user message and get bot reply
- `GET /history` -> Load chat history

## Notes

- The chatbot is intentionally limited to car-related questions.
- Chat history is stored locally in `chat_history.json`.

## Future Improvements

- Move API key handling fully to environment variables
- Add unit tests
- Add chat clear/delete endpoint
- Add deployment config (Render, Railway, or Docker)

## License

This project is for learning and personal portfolio use.
