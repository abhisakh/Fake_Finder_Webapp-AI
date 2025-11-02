# 🕵️‍♂️ Fake Finder Challenge
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 14 54 38" src="https://github.com/user-attachments/assets/d412cf39-267a-4a0c-b18d-3d05f98d2238" />

## 💡 Overview

The Fake Finder Challenge is an engaging web-based "True or False" style game built to test a user's 
ability to distinguish fact from fiction.

The application leverages the Gemini API with Google Search grounding to dynamically generate a 
set of facts (including exactly one fabricated "fake" statement) based on a topic and difficulty 
level provided by the user. The game's goal is to identify that single false statement 
among the list of truths.

The project features a Python (Flask) backend for API handling and a sleek, high-contrast dark-themed 
frontend built with standard HTML, CSS, and vanilla JavaScript.

---

## 🚀 Gameplay Screenshots

Get a quick look at the Fake Finder Challenge in action!
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 14 54 38" src="https://github.com/user-attachments/assets/a6211bca-e57b-4783-bb0b-4db0ba062fc7" />

### Configuration Screen

This is where you set your topic and desired difficulty level.

<img width="1023" height="867" alt="Screenshot 2025-11-02 at 14 58 31" src="https://github.com/user-attachments/assets/690dee9a-ca5a-49f2-b14b-dd8230f1bd8a" />


### Loading Facts

The app retrieves information and challenges the AI to generate facts.

<img width="1023" height="867" alt="Screenshot 2025-11-02 at 14 59 05" src="https://github.com/user-attachments/assets/b6d6650d-c92e-42ba-aad4-358047b768d4" />

### The Challenge

Choose which of the four statements is the fake one.
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 14 59 55" src="https://github.com/user-attachments/assets/fd045a42-5bad-4024-9a16-35928f70556c" />
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 15 01 24" src="https://github.com/user-attachments/assets/8356bde6-d934-4a65-b03d-9c4632d53e51" />

### Incorrect Guess

Better luck next time! The correct fake statement is revealed.
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 15 02 09" src="https://github.com/user-attachments/assets/835a28fc-4515-4aa9-b62d-8e528245b20d" />

### Correct Guess

Success! You've identified the fake.
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 15 03 45" src="https://github.com/user-attachments/assets/873cb1b4-2e5e-4565-b729-9d3ec8fcc840" />
<img width="1023" height="867" alt="Screenshot 2025-11-02 at 15 04 10" src="https://github.com/user-attachments/assets/a4d4633b-4fd9-4fcb-8d07-5ae9493f7fe0" />



---

## ✨ Features

- Dynamic Content: Uses the Gemini API to search for and generate facts about any user-defined topic.
- AI-Generated Lie: Guarantees one fabricated "fake" statement is included for a genuine challenge.
- Difficulty Scaling: Adjusts the complexity and subtlety of the facts based on the selected difficulty (Easy, Medium, Hard).
- Advanced Dark Theme: A polished, high-contrast user interface using the Inter font and smooth micro-interactions.
- Real-time Interaction: Frontend logic handles fact selection, submission, and immediate visual feedback.

---

## 🛠️ Installation and Setup

- Prerequisites
- Python 3.8+
- A Gemini API Key: You can get your key from Google AI Studio.

### Step 1: Clone the Repository
```Bash
git clone https://github.com/abhisakh/Fake_Finder_WebAI_app.git
cd Fake_Finder_WebAI_app
```

### Step 2: Set Up Environment and Dependencies
Create and activate a Python virtual environment:
```Bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Install the required Python packages:
```Bash
pip install -r requirements.txt
```

### Step 3: Configure Your API Key
Create a file named .env in the root directory and add your Gemini API Key. 
The backend is explicitly configured to load this key for client initialization.
```Bash
# .env file
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

### Step 4: Run the Application

Start the Flask development server:
```Bash
python backend/app.py
```
---

The application will typically be available at http://127.0.0.1:5000/.

---

## 📂 Project Structure
```Bash
.
├── .env                  # Environment variables (API Key)
├── .gitignore            # Files ignored by Git
├── LICENSE               # Project license (e.g., MIT)
├── requirements.txt      # Python dependencies
├── backend/              # Python Flask application and AI logic
│   ├── ai_engine.py      # Handles all calls to the Gemini API
│   ├── app.py            # Main Flask routes and application logic
│   ├── game_logic.py     # Core game helpers (shuffling, validation)
│   └── utils.py          # Environment loading utility
├── static/               # Frontend assets
│   ├── scripts.js        # Core game interaction logic (selection, submission)
│   └── style.css         # Advanced dark theme styling
└── templates/
    └── index.html        # Main and only HTML template
```
---

## Core Backend Component Diagrams

### backend/app.py (The Orchestrator)

This is the main entry point, handling HTTP requests and coordinating the flow of data.
```Bash
       [USER INPUT]
        (Topic, Level)
              |
              V
    +-------------------+
    |   backend/app.py  |
    | (Flask Routing)   |
    +---------+---------+
              |
      /---------------\
      V               V
+-------------+  +-------------+
| ai_engine.py|  |game_logic.py|
| (Generate)  |  | (Process)   |
+-------------+  +-------------+
              |
              V
    +-------------------+
    | JSON Response     |
    | (Facts, Index)    |
    +-------------------+
```

### backend/ai_engine.py (The Intelligence Layer)

Handles external data retrieval (Wikipedia) and AI generation (Gemini).
```Bash
[Topic] -> Wikipedia -> [Article Content]
               |
               V
   +---------------------------+
   |   backend/ai_engine.py    |
   | (Gemini API Call)         |
   +------------+--------------+
                |
                V
[Gemini Output String: "(fake @ False)|(fact @ True)..."]
```

### backend/game_logic.py (The Game Processor)

Takes the raw AI output and prepares it for the frontend game state.
```Bash
    [Raw Gemini String]
            |
            V
+-----------------------+
| backend/game_logic.py |
| (Parse, Shuffle)      |
+-----------+-----------+
            |
            V
[List of Tuples: [("Fact A", True), ("Fact B", False), ...]]
```

---

## 🙋‍♂️ Authors (Hackathon 2025, MasterSchool, Berlin)
 **Abhisakh Sarma**
GitHub: [https://github.com/abhisakh](https://github.com/abhisakh)


The old Hackathon project [link](https://github.com/abhisakh/Fake_Finder)


_Contributions and feedback are always welcome!_

🌐 GitHub Profile
