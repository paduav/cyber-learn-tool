# Cybersecurity Learning Tool

## Overview

This is a tool designed to help middle school educators generate interactive cybersecurity classroom activities for students. Instead of a traditional search tool, this application creates cybersecurity scenarios and pairs them with relevant activities stored in the tool's database.

The system also uses AI to customize and tailor activities based on classroom constraints such as grade level, and time.


## Features

* Scenario-Based Activity Generation
* AI-Assisted Activity Customization
* Activity Database
* User Interface 


## Workflow design

1. Frontend/Activity Input - Teacher inputs parameters for activity
2. Backend Processing (Python, app.py) - The python backend would process the request and prepare to send it to the database and AI
3. Database Ranking (SQLite3, models.py) - A database function ranks activities based on the initial input
4. Format for AI (formatter.py) - Ranked activities are then formatted into an input that the AI can easily understand and work with
5. AI Customization (Gemini API) - The AI tailors the activities to the teacher’s input parameters and prepares a final lesson plan
4. Final Activity Output - The final lesson plan is outputted and displayed on the frontend



## Tech Stack

* Backend: Python, Flask
* Database: SQLite
* Frontend: HTML, CSS, Javascript
* AI Integration: Gemini API


## Team

* Database Developer: Virgil Padua
* Backend Developer: Uday Annavarapu
* Frontend Developer: Shaina Silawan

