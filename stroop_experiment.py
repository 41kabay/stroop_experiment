# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui
import csv, os

# Participant info dialog for name and language selection
lang_options = ["Русский", "Türkçe", "Español"]
lang_map = {"Русский": "Russian", "Türkçe": "Turkish", "Español": "Spanish"}

startDlg = gui.Dlg(title="Stroop Task")
startDlg.addField("Participant code:", "")
startDlg.addField("Native Language:", choices=lang_options)
startDlg.show()
if not startDlg.OK:
    core.quit()
participant_name = startDlg.data[0].strip()
if participant_name == "":
    participant_name = "Participant"
lang_choice = startDlg.data[1]
if lang_choice is None or lang_choice not in lang_map:
    core.quit()

native_lang = lang_map[lang_choice]
second_lang = "English"
ui_lang = "English"  # интерфейс эксперимента — на английском

# Translation of language names for inserting into instructions (in UI language)
language_names = {
    'English': {'English': 'English', 'Russian': 'Russian', 'Spanish': 'Spanish', 'Turkish': 'Turkish'},
    'Russian': {'English': 'английском', 'Russian': 'русском', 'Spanish': 'испанском', 'Turkish': 'турецком'},
    'Spanish': {'English': 'inglés', 'Russian': 'ruso', 'Spanish': 'español', 'Turkish': 'turco'},
    'Turkish': {'English': 'İngilizce', 'Russian': 'Rusça', 'Spanish': 'İspanyolca', 'Turkish': 'Türkçe'}
}

# Instruction text templates in each language (UI language)
texts = {
    'English': {
        'intro': "Instructions:\nYou will see color words in different languages. If the meaning of the word matches its display color, press the RIGHT arrow (→). If it does not match, press the LEFT arrow (←). Try to respond as quickly and accurately as possible.\nThe experiment has two blocks: one in your native language ({native}) and one in your second language ({second}).\nPress any key to begin.",
        'end_block1': "End of the first block. Now get ready for the second block (in {second})...",
        'end_block2': "End of the second block.",
        'thanks': "Experiment completed. Thank you for participating!"
    },
    'Russian': {
        'intro': "Инструкция:\nВы будете видеть названия цветов на разных языках. Если значение слова соответствует его цвету, нажмите стрелку вправо (→). Если не соответствует, нажмите стрелку влево (←). Старайтесь отвечать как можно быстрее и точнее.\nЭксперимент состоит из двух блоков: один на вашем родном языке ({native}), другой на втором языке ({second}).\nНажмите любую клавишу, чтобы начать.",
        'end_block1': "Конец первого блока. Сейчас начнется второй блок (на {second})...",
        'end_block2': "Конец второго блока.",
        'thanks': "Эксперимент завершён. Спасибо за участие!"
    },
    'Spanish': {
        'intro': "Instrucciones:\nVerá nombres de colores en diferentes idiomas. Si el significado de la palabra coincide con el color en que está escrita, presione la tecla de flecha derecha (→). Si no coincide, presione la tecla de flecha izquierda (←). Procure responder lo más rápido y preciso posible.\nEl experimento tiene dos bloques: uno en su idioma nativo ({native}) y otro en su segundo idioma ({second}).\nPresione cualquier tecla para comenzar.",
        'end_block1': "Fin del primer bloque. Ahora comenzará el segundo bloque (en {second})...",
        'end_block2': "Fin del segundo bloque.",
        'thanks': "El experimento ha terminado. ¡Gracias por participar!"
    },
    'Turkish': {
        'intro': "Talimatlar:\nFarklı dillerde renk isimleri göreceksiniz. Kelimenin anlamı yazı rengiyle aynıysa sağ ok tuşuna (→) basın. Değilse sol ok tuşuna (←) basın. Lütfen mümkün olduğunca hızlı ve doğru cevap vermeye çalışın.\nDeney iki bloktan oluşur: biri ana dilinizde ({native}), diğeri ikinci dilinizde ({second}).\nBaşlamak için herhangi bir tuşa basın.",
        'end_block1': "Birinci blok bitti. Şimdi ikinci blok ({second}) başlayacak...",
        'end_block2': "İkinci blok bitti.",
        'thanks': "Deney tamamlandı. Katılımınız için teşekkürler!"
    }
}

# Format the instruction strings with chosen language names
intro_text = texts[ui_lang]['intro'].format(native=language_names[ui_lang][native_lang],
                                           second=language_names[ui_lang][second_lang])
end_block1_text = texts[ui_lang]['end_block1'].format(second=language_names[ui_lang][second_lang])
end_block2_text = texts[ui_lang]['end_block2']
thanks_text = texts[ui_lang]['thanks']

# Set up PsychoPy window and stimuli (using Arial font for broad character support)
win = visual.Window(fullscr=True, color="white", units="height")  # Use fullscr=True for experiment
font_name = "Arial"

# Text stimuli for instructions, fixation, and words
instruction_stim = visual.TextStim(win, text=intro_text, font=font_name, pos=(0,0), height=0.03, color="black", wrapWidth=1.2)
fixation = visual.TextStim(win, text="+", font=font_name, pos=(0,0), height=0.05, color="black")
word_stim = visual.TextStim(win, text="", font=font_name, pos=(0,0), height=0.08, color="black")

# Progress bar setup (outline and fill rectangles)
outline_width = 0.8 * (win.size[0] / win.size[1])  # 80% of screen width in "height" units
outline_height = 0.02  # 2% of screen height
left_edge = -outline_width / 2
progress_outline = visual.Rect(win, width=outline_width, height=outline_height,
                               pos=(0, -0.45), lineColor="black", fillColor=None)
progress_fill = visual.Rect(win, width=0.0, height=outline_height,
                            pos=(left_edge, -0.45), fillColor=[0.5,0.5,0.5], lineColor=None)

# Define color word stimuli for each language
colors = ["red", "blue", "green", "yellow", "black"]  # base color names (for setting ink color)
color_words = {
    "English": ["RED", "BLUE", "GREEN", "YELLOW", "BLACK"],
    "Russian": ["КРАСНЫЙ", "СИНИЙ", "ЗЕЛЁНЫЙ", "ЖЁЛТЫЙ", "ЧЁРНЫЙ"],
    "Spanish": ["ROJO", "AZUL", "VERDE", "AMARILLO", "NEGRO"],
    "Turkish": ["KIRMIZI", "MAVİ", "YEŞİL", "SARI", "SİYAH"]
}

# Helper function to generate a balanced list of Stroop trials for a given language
import random
def generate_stroop_trials(lang):
    n = len(colors)  # number of color categories (5)
    trials = []
    # Add one congruent trial per color
    for i in range(n):
        trials.append({"word": color_words[lang][i], "color": colors[i], "congruent": "Congruent"})
    # Add two incongruent trials per color (using a shifted scheme for balance)
    for i in range(n):
        trials.append({"word": color_words[lang][(i+1) % n], "color": colors[i], "congruent": "Incongruent"})
        trials.append({"word": color_words[lang][(i+2) % n], "color": colors[i], "congruent": "Incongruent"})
    # Shuffle and ensure no back-to-back repeats of same word or color
    for attempt in range(100):
        random.shuffle(trials)
        valid = True
        for t in range(len(trials)-1):
            if trials[t]["color"] == trials[t+1]["color"] or trials[t]["word"] == trials[t+1]["word"]:
                valid = False
                break
        if valid:
            break
    return trials

# Prepare trials for Block 1 (native language) and Block 2 (second language)
trials_block1 = generate_stroop_trials(native_lang)
trials_block2 = generate_stroop_trials(second_lang)

# Show instructions and wait for a key press to start
instruction_stim.draw()
win.flip()
event.waitKeys()  # wait for participant to press any key to begin

# === Block 1: Native Language ===
cong_times_b1 = []; incong_times_b1 = []
cong_correct_b1 = 0; incong_correct_b1 = 0
trial_clock = core.Clock()
for idx, trial in enumerate(trials_block1):
    # Fixation cross (500 ms)
    fixation.draw()
    win.flip()
    core.wait(0.5)
    # Blank screen (500 ms)
    win.flip()
    core.wait(0.5)
    # Update progress bar for current trial
    progress = idx / float(len(trials_block1))
    progress_width = outline_width * progress
    progress_fill.width = progress_width
    progress_fill.pos = (left_edge + progress_width/2, -0.45)
    # Draw stimulus word and progress bar
    word_stim.text = trial["word"]
    word_stim.color = trial["color"]
    progress_outline.draw()
    progress_fill.draw()
    word_stim.draw()
    # Show the stimulus and start timing
    trial_clock.reset()
    win.flip()
    # Wait for response (1.0 s with word, then up to 1.5 s without word)
    keys = event.waitKeys(maxWait=1.0, keyList=["left", "right"], timeStamped=trial_clock)
    rt = None; key = None
    if keys:
        # Response within first 1 s
        key, rt = keys[0]
        win.flip()  # clear stimulus immediately after response
        # (No additional wait here; move to inter-trial after capturing response)
    else:
        # No response in 1 s, remove word and wait up to 1.5 s more
        win.flip()  # remove stimulus at 1.0 s
        keys = event.waitKeys(maxWait=1.5, keyList=["left", "right"], timeStamped=trial_clock)
        if keys:
            key, rt = keys[0]
    # Determine if response is correct
    corrAns = "right" if trial["congruent"] == "Congruent" else "left"
    correct = 1 if (key == corrAns) else 0
    # Record RT (in ms) and accuracy for this trial
    if rt is not None:
        cong_times_b1.append(rt*1000.0) if trial["congruent"] == "Congruent" else incong_times_b1.append(rt*1000.0)
    if trial["congruent"] == "Congruent":
        cong_correct_b1 += correct
    else:
        incong_correct_b1 += correct
    # Inter-trial interval (500 ms blank)
    win.flip()
    core.wait(0.5)

# End of Block 1 message (automatically proceed after 2 seconds)
end_block1_msg = visual.TextStim(win, text=end_block1_text, font=font_name, pos=(0,0), height=0.04, color="black")
end_block1_msg.draw()
win.flip()
core.wait(2.0)

# === Block 2: Second Language ===
cong_times_b2 = []; incong_times_b2 = []
cong_correct_b2 = 0; incong_correct_b2 = 0
trial_clock.reset()
for idx, trial in enumerate(trials_block2):
    # Fixation (500 ms)
    fixation.draw()
    win.flip()
    core.wait(0.5)
    # Blank (500 ms)
    win.flip()
    core.wait(0.5)
    # Progress bar update
    progress = idx / float(len(trials_block2))
    progress_width = outline_width * progress
    progress_fill.width = progress_width
    progress_fill.pos = (left_edge + progress_width/2, -0.45)
    # Draw stimulus and progress bar
    word_stim.text = trial["word"]
    word_stim.color = trial["color"]
    progress_outline.draw()
    progress_fill.draw()
    word_stim.draw()
    trial_clock.reset()
    win.flip()
    # Wait for response with the same timing logic
    keys = event.waitKeys(maxWait=1.0, keyList=["left", "right"], timeStamped=trial_clock)
    rt = None; key = None
    if keys:
        key, rt = keys[0]
        win.flip()
    else:
        win.flip()
        keys = event.waitKeys(maxWait=1.5, keyList=["left", "right"], timeStamped=trial_clock)
        if keys:
            key, rt = keys[0]
    corrAns = "right" if trial["congruent"] == "Congruent" else "left"
    correct = 1 if (key == corrAns) else 0
    if rt is not None:
        cong_times_b2.append(rt*1000.0) if trial["congruent"] == "Congruent" else incong_times_b2.append(rt*1000.0)
    if trial["congruent"] == "Congruent":
        cong_correct_b2 += correct
    else:
        incong_correct_b2 += correct
    win.flip()
    core.wait(0.5)

# End of Block 2 message
end_block2_msg = visual.TextStim(win, text=end_block2_text, font=font_name, pos=(0,0), height=0.04, color="black")
end_block2_msg.draw()
win.flip()
core.wait(1.5)
# Thank you message
thanks_msg = visual.TextStim(win, text=thanks_text, font=font_name, pos=(0,0), height=0.04, color="black")
thanks_msg.draw()
win.flip()
core.wait(2.0)

# Close the window at the end of experiment
win.close()

# Calculate mean and standard deviation of RTs for each condition
import math
def compute_stats(rt_list):
    if len(rt_list) == 0:
        return (0.0, 0.0)
    mean_val = sum(rt_list) / len(rt_list)
    if len(rt_list) > 1:
        var_val = sum((x - mean_val)**2 for x in rt_list) / len(rt_list)
    else:
        var_val = 0.0
    std_val = math.sqrt(var_val)
    return (mean_val, std_val)

mean_cong_b1, std_cong_b1 = compute_stats(cong_times_b1)
mean_incong_b1, std_incong_b1 = compute_stats(incong_times_b1)
mean_cong_b2, std_cong_b2 = compute_stats(cong_times_b2)
mean_incong_b2, std_incong_b2 = compute_stats(incong_times_b2)

# Prepare summary rows with accuracy
summary_rows = []
conditions = [
    ("Native", native_lang, "Congruent", cong_times_b1, cong_correct_b1, 5),
    ("Native", native_lang, "Incongruent", incong_times_b1, incong_correct_b1, 10),
    ("Second", second_lang, "Congruent", cong_times_b2, cong_correct_b2, 5),
    ("Second", second_lang, "Incongruent", incong_times_b2, incong_correct_b2, 10)
]

for block, lang, congruency, rt_list, correct_count, total_trials in conditions:
    mean_rt, std_rt = compute_stats(rt_list)
    accuracy = (correct_count / total_trials) * 100 if total_trials > 0 else 0.0
    summary_rows.append([
        participant_name, block, lang, congruency,
        f"{mean_rt:.1f}", f"{std_rt:.1f}", correct_count, f"{accuracy:.1f}%"
    ])


# Write results to CSV
# Стало:
# --- Создание папки для данных и определение пути к файлу ---
output_dir = 'data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
csv_filename = os.path.join(output_dir, "stroop_results.csv")
# -----------------------------------------------------------
file_exists = os.path.isfile(csv_filename)
with open(csv_filename, mode="a", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(["Participant", "Block", "Language", "Congruency", "Mean_RT(ms)", "StdDev", "Correct_Count", "Accuracy(%)"])
    writer.writerows(summary_rows)
