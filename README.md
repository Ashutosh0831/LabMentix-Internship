🧪 API Tester — Python Desktop App

A simple yet powerful Postman-like desktop application built with Python (Tkinter) to test REST APIs easily.
You can send requests (GET, POST, PUT, DELETE), view formatted JSON responses, save history, and export results — all from a clean GUI.

🚀 Features
Feature	Description
🌐 HTTP Methods	Supports GET, POST, PUT, DELETE requests
🧾 Custom Headers & Body	Add headers and request body easily
💬 JSON Pretty Print	Responses are shown in a formatted, readable JSON view
💾 Save & Export	Save responses to .json or .txt files
🕒 Persistent History	All request/response history is stored locally (JSON + SQLite)
⏱ Response Time Tracking	Displays how long each request took
🎨 Dark/Light Theme	Toggle between light and dark modes
⚙️ Executable Build	Easily convert project into .exe using PyInstaller
🧰 Project Structure
API_TESTER/
│
├── assets/
│   └── icons/                # App icons
│
├── data/
│   ├── history.db            # SQLite database for persistent history
│   └── history.json          # Optional JSON-based request log
│
├── env/                      # Virtual environment (optional)
│
├── tools/
│   └── autorun.py            # Helper script for setup tasks
│
├── ui/
│   └── main_window.py        # Tkinter UI and theme handling
│
├── main.py                   # Entry point of the application
├── README.md                 # Project documentation
└── requirements.txt           # Python dependencies

⚙️ Installation
1️⃣ Clone or Download the Repository
git clone https://github.com/yourusername/api_tester.git
cd api_tester

2️⃣ Create a Virtual Environment (Recommended)
python -m venv env

3️⃣ Activate the Environment

Windows:

env\Scripts\activate


Mac/Linux:

source env/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

🖥️ Running the Application

After installing dependencies, just run:

python main.py


✅ The GUI will open — now you can:

Enter API URL

Select HTTP method

Add headers/body (optional)

Click Send to view formatted JSON response

🔍 Example APIs to Test
Method	URL	Description
GET	https://jsonplaceholder.typicode.com/posts/1
	Fetch a sample post
POST	https://jsonplaceholder.typicode.com/posts
	Create a fake post
PUT	https://jsonplaceholder.typicode.com/posts/1
	Update a post
DELETE	https://jsonplaceholder.typicode.com/posts/1
	Delete a post
💾 Export Options

You can export response data as:

JSON file (.json)

Text file (.txt)

Saved responses can be found in your data/ folder.

🗃️ Database & History

Request/response logs are automatically stored in:

data/history.db (SQLite)

data/history.json (JSON backup)

History is persistent between sessions.

🎨 Dark & Light Theme

Switch between Dark Mode 🌙 and Light Mode ☀️ from the top menu or settings area.
Theme preference is saved locally.

⚡ Build Executable with PyInstaller

To create a standalone .exe file:

pyinstaller main.py ^
--noconsole ^
--onefile ^
--add-data "assets;assets" ^
--add-data "ui;ui" ^
--add-data "tools;tools" ^
--icon="assets/icons/api_gateway.ico" ^
--name "API Tester"


📁 The generated executable will appear in:

dist/main.exe


Then just double-click it to launch your app!


🧱 Tech Stack

Python 3.x

Tkinter (GUI)

Requests (HTTP handling)

JSON (response formatting)

SQLite3 (persistent history)

PyInstaller (for packaging)

🧑‍💻 Author

Ashutosh Pandey
💼 BCA Student | Full-Stack & Python Developer
📧 theashutoshp05@gmail.com

🪪 License

This project is licensed under the MIT License — feel free to modify and distribute.