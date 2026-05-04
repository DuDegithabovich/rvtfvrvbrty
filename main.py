import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f0f0')
        
        # Инициализация данных
        self.quotes = [
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Философия"},
            {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Мотивация"},
            {"text": "Не судите о каждом дне по собранному урожаю, а по семенам, которые вы посадили.", "author": "Роберт Льюис Стивенсон", "topic": "Философия"},
            {"text": "Сложно победить того, кто никогда не сдается.", "author": "Бейб Рут", "topic": "Мотивация"},
            {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"},
            {"text": "Все, что мы слышим, — это мнение, а не факт.", "author": "Марк Аврелий", "topic": "Философия"},
            {"text": "Искусство быть мудрым — это искусство знать, на что не обращать внимания.", "author": "Уильям Джеймс", "topic": "Мудрость"},
            {"text": "Только тот, кто рискует идти слишком далеко, может узнать, как далеко можно зайти.", "author": "Т.С. Элиот", "topic": "Мотивация"},
            {"text": "Не ждите. Время никогда не будет идеальным.", "author": "Наполеон Хилл", "topic": "Мотивация"}
        ]
        
        # Файл для сохранения истории
        self.history_file = "quotes.json"
        
        # Загрузка истории
        self.history = self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление выпадающих списков
        self.update_filter_options()
        
    def create_widgets(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="Генератор случайных цитат", 
                               font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=10)
        
        # Фрейм для отображения цитаты
        quote_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        quote_frame.pack(pady=10, fill='both', expand=True)
        
        self.quote_text = tk.Text(quote_frame, height=6, font=('Arial', 12), wrap='word',
                                  bg='white', fg='#333333', relief='flat')
        self.quote_text.pack(padx=15, pady=15, fill='both', expand=True)
        
        # Кнопка генерации
        generate_btn = tk.Button(main_frame, text="🎲 Сгенерировать цитату", 
                                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                                 command=self.generate_quote, cursor='hand2', padx=20, pady=10)
        generate_btn.pack(pady=10)
        
        # Фрейм для фильтрации
        filter_frame = tk.LabelFrame(main_frame, text="Фильтрация", 
                                     font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333333')
        filter_frame.pack(pady=10, fill='x')
        
        # Фильтр по автору
        tk.Label(filter_frame, text="Автор:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5)
        self.author_filter = ttk.Combobox(filter_frame, values=["Все"], state='readonly', width=20)
        self.author_filter.grid(row=0, column=1, padx=5, pady=5)
        self.author_filter.set("Все")
        self.author_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Фильтр по теме
        tk.Label(filter_frame, text="Тема:", bg='#f0f0f0').grid(row=0, column=2, padx=5, pady=5)
        self.topic_filter = ttk.Combobox(filter_frame, values=["Все"], state='readonly', width=20)
        self.topic_filter.grid(row=0, column=3, padx=5, pady=5)
        self.topic_filter.set("Все")
        self.topic_filter.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # История
        history_frame = tk.LabelFrame(main_frame, text="История цитат", 
                                      font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333333')
        history_frame.pack(pady=10, fill='both', expand=True)
        
        # Список истории с прокруткой
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_list = tk.Listbox(history_frame, font=('Arial', 9), 
                                       yscrollcommand=scrollbar.set, height=8)
        self.history_list.pack(padx=5, pady=5, fill='both', expand=True)
        scrollbar.config(command=self.history_list.yview)
        
        # Кнопка очистки истории
        clear_btn = tk.Button(main_frame, text="🗑 Очистить историю", 
                              font=('Arial', 10), bg='#f44336', fg='white',
                              command=self.clear_history, cursor='hand2')
        clear_btn.pack(pady=5)
        
        # Фрейм для добавления новой цитаты
        add_frame = tk.LabelFrame(main_frame, text="Добавить новую цитату", 
                                  font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#333333')
        add_frame.pack(pady=10, fill='x')
        
        tk.Label(add_frame, text="Текст:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.new_text = scrolledtext.ScrolledText(add_frame, height=3, width=50)
        self.new_text.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
        
        tk.Label(add_frame, text="Автор:", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.new_author = tk.Entry(add_frame, width=30)
        self.new_author.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Тема:", bg='#f0f0f0').grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.new_topic = tk.Entry(add_frame, width=20)
        self.new_topic.grid(row=1, column=3, padx=5, pady=5)
        
        add_btn = tk.Button(add_frame, text="➕ Добавить цитату", 
                           font=('Arial', 10), bg='#2196F3', fg='white',
                           command=self.add_quote, cursor='hand2')
        add_btn.grid(row=2, column=1, columnspan=2, pady=10)
        
    def update_filter_options(self):
        """Обновление вариантов в фильтрах"""
        # Уникальные авторы
        authors = sorted(set(quote["author"] for quote in self.quotes))
        self.author_filter['values'] = ["Все"] + authors
        
        # Уникальные темы
        topics = sorted(set(quote["topic"] for quote in self.quotes))
        self.topic_filter['values'] = ["Все"] + topics
        
    def get_filtered_quotes(self):
        """Получение цитат с учетом фильтров"""
        filtered = self.quotes.copy()
        
        if self.author_filter.get() != "Все":
            filtered = [q for q in filtered if q["author"] == self.author_filter.get()]
        
        if self.topic_filter.get() != "Все":
            filtered = [q for q in filtered if q["topic"] == self.topic_filter.get()]
        
        return filtered
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        filtered_quotes = self.get_filtered_quotes()
        
        if not filtered_quotes:
            messagebox.showwarning("Нет цитат", "Нет цитат, соответствующих выбранным фильтрам!")
            return
        
        quote = random.choice(filtered_quotes)
        
        # Отображение цитаты
        self.quote_text.delete(1.0, tk.END)
        display_text = f'"{quote["text"]}"\n\n— {quote["author"]}\n📚 Тема: {quote["topic"]}'
        self.quote_text.insert(1.0, display_text)
        
        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "timestamp": timestamp,
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"]
        }
        self.history.insert(0, history_entry)
        self.update_history_display()
        self.save_history()
        
    def update_history_display(self):
        """Обновление отображения истории"""
        self.history_list.delete(0, tk.END)
        for entry in self.history:
            display = f'[{entry["timestamp"]}] {entry["text"][:50]}... — {entry["author"]}'
            self.history_list.insert(tk.END, display)
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.update_history_display()
            self.save_history()
            self.quote_text.delete(1.0, tk.END)
            
    def add_quote(self):
        """Добавление новой цитаты"""
        text = self.new_text.get(1.0, tk.END).strip()
        author = self.new_author.get().strip()
        topic = self.new_topic.get().strip()
        
        # Проверка корректности ввода
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        
        if not author:
            messagebox.showerror("Ошибка", "Автор цитаты не может быть пустым!")
            return
        
        if not topic:
            messagebox.showerror("Ошибка", "Тема цитаты не может быть пустой!")
            return
        
        # Добавление цитаты
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        
        self.quotes.append(new_quote)
        self.update_filter_options()
        
        # Очистка полей ввода
        self.new_text.delete(1.0, tk.END)
        self.new_author.delete(0, tk.END)
        self.new_topic.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
        
    def on_filter_change(self, event=None):
        """Обработка изменения фильтров"""
        self.generate_quote()
        
    def load_history(self):
        """Загрузка истории из файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохранение истории в файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")

def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
