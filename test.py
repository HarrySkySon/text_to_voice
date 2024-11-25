# This script creates a simple GUI application using Tkinter that allows users to convert text to speech.
# It utilizes the gTTS library for text-to-speech conversion and pydub for audio manipulation.
# The application provides options for users to select input text and save the generated audio file.

import os
from tkinter import Tk, Label, Button, StringVar, OptionMenu, filedialog, messagebox
from gtts import gTTS
from pydub import AudioSegment

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        file_path.set(filename)

def convert_to_audio():
    path = file_path.get()
    lang = language.get()
    audio_format = format_choice.get()

    if not os.path.isfile(path):
        messagebox.showerror("Error", "Файл не знайдено. Будь ласка, перевірте шлях.")
        return

    try:
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()

        tts = gTTS(text=text, lang=lang)
        temp_file = os.path.join(os.path.dirname(path), "temp.mp3")
        tts.save(temp_file)

        # Конвертуємо в обраний формат
        output_file = os.path.join(os.path.dirname(path), f"output.{audio_format}")
        audio = AudioSegment.from_mp3(temp_file)
        audio.export(output_file, format=audio_format)

        # Видалити тимчасовий файл
        os.remove(temp_file)

        messagebox.showinfo("Success", f"Аудіофайл збережено як: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Основне вікно
root = Tk()
root.title("Text to Audio Converter")
root.geometry("400x400")

# Змінні
file_path = StringVar()
language = StringVar(value='de')  # За замовчуванням німецька
voice_gender = StringVar(value='male')  # За замовчуванням чоловічий голос
format_choice = StringVar(value='mp3')  # За замовчуванням mp3

# Віджети
Label(root, text="Ця програма конвертує текст у формат аудіо").pack(pady=16)

Label(root, text="Виберіть мову:").pack(pady=5)
OptionMenu(root, language, 'de', 'en', 'fr', 'es', 'it', 'uk').pack(pady=5)

Label(root, text="Виберіть формат:").pack(pady=5)
OptionMenu(root, format_choice, 'mp3', 'wav', 'ogg').pack(pady=5)

Label(root, text="Вкажіть файл з текстом:").pack(pady=5)
Button(root, text="Browse", command=browse_file).pack(pady=10)

Label(root, text="Розпочати конвертацію тексту в аудіо:").pack(pady=5)
Button(root, text="START", command=convert_to_audio).pack(pady=20)

# Запуск програми
root.mainloop()