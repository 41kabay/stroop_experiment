# Stroop Task for Bilingual Participants

This is a cognitive psychology experiment based on the **Stroop Task**, implemented in Python using [PsychoPy](https://psychopy.org/). It is designed to assess cognitive control in **bilingual participants**, by comparing reaction times and accuracy across two language blocks: native and second language.

## 🧠 Description

Participants will see **color words** displayed in various colors. Their task is to respond:

- **Press → (Right Arrow)** if the **word meaning matches** the color of the text (**congruent**).
- **Press ← (Left Arrow)** if the **word meaning does not match** the color of the text (**incongruent**).

The experiment:
- Supports bilingual comparison (native vs. second language)
- Provides **Russian, Spanish, Turkish** as native languages (English is always the second language)
- Measures **reaction time** and **accuracy**
- Saves the results in `stroop_results.csv` (UTF-8 encoded)

---

## 🌐 Language Support

User interface is always in **English**. The experiment includes stimuli in:
- English (as second language)
- Russian
- Turkish
- Spanish

---

## ⚙️ Requirements

You must have:

- **Python 3.8+**
- [PsychoPy](https://psychopy.org/download.html) installed via pip or the standalone app

### 🧪 To install via pip:

```bash
pip install psychopy
Or using a virtual environment:

python -m venv venv
venv\Scripts\activate      # On Windows
pip install psychopy

▶️ How to Run

Clone or download the repository:

git clone https://github.com/your-username/stroop-task-bilingual.git
cd stroop-task-bilingual


Run the experiment:

python stroop_experiment.py


The task will launch in fullscreen mode. At the end, results will be saved as stroop_results.csv in the same folder.

