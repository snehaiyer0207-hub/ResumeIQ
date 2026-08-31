# ResumeIQ

ResumeIQ is a web-based resume analysis system built using Python and Flask.

## Features

- PDF resume analysis
- Multiple job roles
- Skill detection
- Job-specific keyword matching
- Missing keyword detection
- ATS score calculation
- Resume section detection
- Personalized recommendations

## Technologies Used

- Python
- Flask
- pdfplumber
- HTML
- CSS
- JavaScript

## How It Works

1. Upload a resume in PDF format.
2. Select a job role.
3. ResumeIQ extracts the resume text.
4. The system analyzes skills, sections and keywords.
5. An ATS score is calculated.
6. Missing keywords and recommendations are displayed.

## Project Structure

```text
ResumeIQ/
├── app.py
├── analyzer.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
└── .gitignore

## Author

Sneha Iyer