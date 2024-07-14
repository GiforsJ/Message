import tkinter as tk  # Импортируем библиотеку для создания графического интерфейса
from tkinter import simpledialog  # Импортируем модуль для диалоговых окон
import random  # Импортируем модуль для работы со случайными числами
import pickle  # Импортируем модуль для сохранения и загрузки данных
import os  # Импортируем модуль для работы с операционной системой
import keyboard  # Импортируем модуль для работы с клавишами

class TextManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Manager")
        self.root.geometry("600x400")  # Устанавливаем размер главного окна

        self.text_fields = []  # Список для хранения текстовых полей
        self.text_arrays = {}  # Словарь для хранения слов из текстовых полей

        # Создаем и размещаем виджет метки
        text = tk.Label(root, text="Напишите текст и используйте {№ набора} в местах где нужно создать слово из набора \nНомер начинается с 0\nТекст автоматически копируется, также можно создавать сообщение при нажатии на клавишу L")
        text.pack(pady=10)

        # Создаем и размещаем текстовое поле для ввода шаблона сообщения
        self.text_message = tk.Text(self.root, height=5, width=70)
        self.text_message.pack(pady=5)

        # Создаем и размещаем кнопку для добавления новых текстовых полей
        self.add_text_field_button = tk.Button(root, text="Добавить набор слов", command=self.add_text_field)
        self.add_text_field_button.pack(pady=5)

        # Создаем и размещаем кнопку для создания и копирования сообщения
        self.create_and_output_button = tk.Button(root, text="Создать сообщение", command=self.create_and_copy_text)
        self.create_and_output_button.pack(pady=5)

        # Создаем и размещаем виджет метки
        text_w = tk.Label(root, text="Напишите слова через пробел")
        text_w.pack(pady=10)

        self.load_state()  # Загружаем сохраненное состояние

        # Устанавливаем глобальный обработчик клавиши 'L'
        keyboard.add_hotkey('l', self.create_and_copy_text)

    def add_text_field(self, content=""):
        # Создаем и размещаем новое текстовое поле
        text_field = tk.Text(self.root, height=2, width=70)  
        text_field.pack(pady=5)
        text_field.insert(tk.END, content)  # Заполняем текстовое поле содержимым
        self.text_fields.append(text_field)  # Добавляем текстовое поле в список

    def create_and_copy_text(self):
        # Проходим по всем текстовым полям и сохраняем их содержимое в словарь
        for index, text_field in enumerate(self.text_fields):
            text_content = text_field.get("1.0", tk.END).strip()
            if text_content:
                self.text_arrays[index] = text_content.split()

        message_template = self.text_message.get("1.0", tk.END).strip()  # Получаем шаблон сообщения
        message = self.generate_message_from_template(message_template)  # Генерируем сообщение из шаблона

        self.copy_to_clipboard(message)  # Копируем сообщение в буфер обмена

    def generate_message_from_template(self, template):
        # Заменяем плейсхолдеры в шаблоне случайными словами из соответствующих наборов
        for index in range(len(self.text_fields)):
            placeholder = f"{{{index}}}"
            if placeholder in template:
                random_word = random.choice(self.text_arrays.get(index, [""]))
                template = template.replace(placeholder, random_word, 1)
        return template

    def copy_to_clipboard(self, message):
        self.root.clipboard_clear()  # Очищаем буфер обмена
        self.root.clipboard_append(message)  # Добавляем сообщение в буфер обмена
        self.root.update()  # Обновляем интерфейс, чтобы изменения вступили в силу

    def save_state(self):
        # Сохраняем состояние текстовых полей и шаблона сообщения в файл
        state = {
            'text_message': self.text_message.get("1.0", tk.END).strip(),
            'text_fields': [text_field.get("1.0", tk.END).strip() for text_field in self.text_fields]
        }
        with open('state.pkl', 'wb') as f:
            pickle.dump(state, f)

    def load_state(self):
        # Загружаем состояние из файла, если он существует
        if os.path.exists('state.pkl'):
            with open('state.pkl', 'rb') as f:
                state = pickle.load(f)
                self.text_message.insert(tk.END, state['text_message'])
                for content in state['text_fields']:
                    self.add_text_field(content)

    def on_closing(self):
        self.save_state()  # Сохраняем состояние перед закрытием окна
        self.root.destroy()  # Закрываем окно

if __name__ == "__main__":
    root = tk.Tk()
    app = TextManager(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Обработчик закрытия окна
    root.mainloop()  # Запускаем главный цикл приложения
