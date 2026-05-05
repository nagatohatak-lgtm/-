import tkinter as tk
from tkinter import ttk, messagebox
from random import choice
import json

# --- 1. БЛОК: ИМПОРТ ДАННЫХ (ЦИТАТЫ) ---
try:
    from quotes import quotes
except ImportError:
    quotes = [
        {"text": "Секрет успеха — постоянство.", "author": "Джо Аберкромби", "theme": "мотивация"},
    ]

# --- 2. БЛОК: ПЕРЕМЕННЫЕ И ГЛОБАЛЬНЫЕ СПИСКИ ---
history = []

# --- Функции логики ---
def generate_quote():
    quote = choice(quotes)
    quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
    add_to_history(quote)

def add_to_history(quote):
    history.append(quote)
    update_history_display()
    save_history()

def update_history_display(filtered=None):
    data = filtered if filtered is not None else history
    history_listbox.delete(0, tk.END)
    for i, q in enumerate(data, 1):
        history_listbox.insert(tk.END, f"{i}. {q['text']} — {q['author']} ({q['theme']})")

def filter_history():
    author = author_filter.get().lower()
    theme = theme_filter.get().lower()
    filtered = [q for q in history if (not author or author in q["author"].lower()) and (not theme or theme in q["theme"].lower())]
    update_history_display(filtered)

def save_history():
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history():
    global history
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
            update_history_display()
    except FileNotFoundError:
        history = []

def add_quote():
    text = new_quote_text.get("1.0", tk.END).strip()
    author = new_quote_author.get().strip()
    theme = new_quote_theme.get().strip()
    if not text or not author or not theme:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    quotes.append({"text": text, "author": author, "theme": theme})
    new_quote_text.delete("1.0", tk.END)
    new_quote_author.delete(0, tk.END)
    new_quote_theme.delete(0, tk.END)
# --- 3. БЛОК: ФУНКЦИИ ЛОГИКИ (Генерация, сохранение, фильтрация) ---
# (Сюда копируй функции: generate_quote, add_to_history, save_history и т.д.)
# ... код функций из предыдущего ответа ...

# --- 4. БЛОК: ГРАФИЧ
# --- Создание окна ---
root = tk.Tk()
root.title("Генератор случайных цитат")
root.geometry("600x500")
root.resizable(False, False)

# --- Вкладки (Notebook) ---
tab_control = ttk.Notebook(root)
main_tab = ttk.Frame(tab_control)
add_tab = ttk.Frame(tab_control)
tab_control.add(main_tab, text="Главная")
tab_control.add(add_tab, text="Добавить цитату")
tab_control.pack(expand=1, fill="both")

# --- Вкладка Главная ---
quote_label = ttk.Label(main_tab, text="", font=("Arial", 12), wraplength=450)
quote_label.pack(pady=20)

generate_button = ttk.Button(main_tab, text="Сгенерировать цитату", command=generate_quote)
generate_button.pack()

# Фильтры
filter_frame = ttk.LabelFrame(main_tab, text="Фильтр истории")
filter_frame.pack(pady=10, fill="x")

ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5)
author_filter = ttk.Entry(filter_frame)
author_filter.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
filter_frame.columnconfigure(1, weight=1)

ttk.Label(filter_frame, text="Тема:").grid(row=1, column=0, padx=5, pady=5)
theme_filter = ttk.Entry(filter_frame)
theme_filter.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Button(filter_frame, text="Применить фильтр", command=filter_history).grid(row=2, column=0, columnspan=2, pady=5)

# История
history_frame = ttk.LabelFrame(main_tab, text="История")
history_frame.pack(pady=10, fill="both", expand=True)
history_scroll = ttk.Scrollbar(history_frame)
history_listbox = tk.Listbox(history_frame, yscrollcommand=history_scroll.set, height=8)
history_listbox.pack(side="left", fill="both", expand=True)
history_scroll.pack(side="right", fill="y")
history_scroll.config(command=history_listbox.yview)

# --- Вкладка Добавить цитату ---
ttk.Label(add_tab, text="Текст цитаты:").pack(pady=5)
new_quote_text = tk.Text(add_tab, height=4, width=50)
new_quote_text.pack(pady=5)
ttk.Label(add_tab, text="Автор:").pack(pady=5)
new_quote_author = ttk.Entry(add_tab)
new_quote_author.pack(pady=5)
ttk.Label(add_tab, text="Тема:").pack(pady=5)
new_quote_theme = ttk.Entry(add_tab)
new_quote_theme.pack(pady=5)
ttk.Button(add_tab, text="Добавить цитату", command=add_quote).pack(pady=10)
def main():
    # --- Создание главного окна ---
    root = tk.Tk()
    root.title("Генератор случайных цитат")
    root.geometry("600x500")
    root.resizable(False, False)

    # --- Вкладки (Notebook) ---
    tab_control = ttk.Notebook(root)
    main_tab = ttk.Frame(tab_control)
    add_tab = ttk.Frame(tab_control)
    tab_control.add(main_tab, text="Главная")
    tab_control.add(add_tab, text="Добавить цитату")
    tab_control.pack(expand=1, fill="both")

    # --- Вкладка Главная (Виджеты) ---
    quote_label = ttk.Label(main_tab, text="", font=("Arial", 12), wraplength=450)
    quote_label.pack(pady=20)

    generate_button = ttk.Button(main_tab, text="Сгенерировать цитату", command=generate_quote)
    generate_button.pack()

    # ... (код для Frame с фильтрами и Listbox с историей) ...

    # --- Вкладка Добавить цитату (Виджеты) ---
    # ... (код для Text и Entry для добавления новой цитаты) ...

# --- 5. БЛОК: ЗАПУСК ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    load_history() # Загружаем историю перед запуском окна
    root.mainloop()       # Запускаем функцию с интерфейсом