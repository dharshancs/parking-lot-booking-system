# Flask Web App Project

This is a simple web application built using Flask, Jinja2, HTML, CSS, and Python. It supports basic functionalities like user registration, data submission, and displaying stored data through templates. I built this as part of the final project for the IITM BS Data Science program.

## 🔧 Features

- User registration and login
- Form-based data input
- Display of stored data using Jinja templates
- API routes to fetch and post data
- Clean and responsive frontend using HTML/CSS

## 📁 Project Structure
/project-root
│
├── app.py # Main Flask app with all route definitions
├── templates/ # Contains HTML files (Jinja2 templates)
├── static/ # CSS and static assets
├── db.sqlite3 # SQLite database file (if using SQLite)
├── requirements.txt # Python package requirements
└── README.md # This file


## 🛠 Technologies Used

- Flask
- Jinja2
- HTML/CSS
- Python
- SQLite (or any DB you’re using)

## 🚀 How to Run the App

1. Clone this repo and navigate to the folder:
   ```bash
   git clone <repo-url>
   cd <project-folder>
Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Run the app:

python app.py
