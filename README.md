# Stroop Task for Bilingual Participants

This is a cognitive psychology experiment (Stroop Task) implemented in Python using PsychoPy. It is designed to test bilingual participants in two blocks — one in their native language and one in their second language.

## 🧠 Description

Participants see color words displayed in different colors. Their task is to press:

- → if the **word meaning** matches the **text color** (congruent)
- ← if it **does not match** (incongruent)

The experiment automatically:
- Supports multiple languages (English, Russian, Spanish, Turkish)
- Measures reaction times and accuracy
- Saves results to a `.csv` file for later analysis
https://psychopy.org/download.html
---

## ⚙️ Requirements

You must have **Python 3.8+** installed.

Install required libraries with:

```bash
pip install psychopy
Or, if you're using a virtual environment:

bash
python -m venv venv
venv\Scripts\activate     # On Windows
pip install psychopy
▶️ How to Run
Download or clone this repository:

bash
git clone https://github.com/your-username/stroop-task-bilingual.git
cd stroop-task-bilingual
python stroop_experiment.py
The experiment will launch in fullscreen. Results will be saved in the same folder as stroop_results.csv
