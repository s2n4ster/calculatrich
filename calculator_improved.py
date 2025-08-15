import tkinter as tk
from tkinter import ttk
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # Переменные для вычислений
        self.current_number = tk.StringVar(value="0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True
        self.history = []
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка клавиатуры
        self.bind_keyboard()
        
        # Центрирование окна
        self.center_window()
        
    def setup_styles(self):
        """Настройка стилей для кнопок с использованием ttk"""
        style = ttk.Style()
        
        # Попробуем использовать современную тему
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Настройка стилей для разных типов кнопок
        style.configure('Calculator.TFrame', background='#f0f0f0')
        style.configure('Display.TFrame', background='#ffffff', relief='flat')
        
        # Стиль для кнопок с числами
        style.configure('Number.TButton',
                       background='#ffffff',
                       foreground='#000000',
                       font=('Segoe UI', 18, 'bold'),
                       padding=(20, 15),
                       relief='flat')
        
        # Стиль для операторов
        style.configure('Operator.TButton',
                       background='#ff9500',
                       foreground='#ffffff',
                       font=('Segoe UI', 18, 'bold'),
                       padding=(20, 15),
                       relief='flat')
        
        # Стиль для функций
        style.configure('Function.TButton',
                       background='#d4d4d2',
                       foreground='#000000',
                       font=('Segoe UI', 18, 'bold'),
                       padding=(20, 15),
                       relief='flat')
        
        # Стиль для равно
        style.configure('Equals.TButton',
                       background='#ff9500',
                       foreground='#ffffff',
                       font=('Segoe UI', 18, 'bold'),
                       padding=(20, 15),
                       relief='flat')
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root, style='Calculator.TFrame')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Дисплей
        display_frame = ttk.Frame(main_frame, style='Display.TFrame')
        display_frame.pack(fill='x', pady=(0, 20))
        
        # История вычислений
        self.history_label = tk.Label(display_frame,
                                    text="",
                                    font=('Segoe UI', 14),
                                    bg='#ffffff',
                                    fg='#666666',
                                    anchor='e',
                                    padx=20,
                                    pady=(10, 0))
        self.history_label.pack(fill='x')
        
        # Основной дисплей
        self.display_label = tk.Label(display_frame,
                                    textvariable=self.current_number,
                                    font=('Segoe UI', 42, 'bold'),
                                    bg='#ffffff',
                                    fg='#000000',
                                    anchor='e',
                                    padx=20,
                                    pady=(5, 20))
        self.display_label.pack(fill='x')
        
        # Кнопки
        buttons_frame = ttk.Frame(main_frame, style='Calculator.TFrame')
        buttons_frame.pack(fill='both', expand=True)
        
        # Сетка кнопок
        buttons = [
            ('C', 'Function', 0, 0), ('±', 'Function', 0, 1), ('%', 'Function', 0, 2), ('÷', 'Operator', 0, 3),
            ('7', 'Number', 1, 0), ('8', 'Number', 1, 1), ('9', 'Number', 1, 2), ('×', 'Operator', 1, 3),
            ('4', 'Number', 2, 0), ('5', 'Number', 2, 1), ('6', 'Number', 2, 2), ('−', 'Operator', 2, 3),
            ('1', 'Number', 3, 0), ('2', 'Number', 3, 1), ('3', 'Number', 3, 2), ('+', 'Operator', 3, 3),
            ('0', 'Number', 4, 0, 2), ('.', 'Number', 4, 2), ('=', 'Equals', 4, 3)
        ]
        
        # Настройка сетки
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Создание кнопок
        for button_data in buttons:
            if len(button_data) == 5:  # Кнопка занимает 2 колонки
                text, style_type, row, col, colspan = button_data
                btn = ttk.Button(buttons_frame, 
                               text=text,
                               style=f'{style_type}.TButton')
                btn.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=3, pady=3)
            else:
                text, style_type, row, col = button_data
                btn = ttk.Button(buttons_frame, 
                               text=text,
                               style=f'{style_type}.TButton')
                btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            
            # Привязка событий
            if text.isdigit() or text == '.':
                btn.configure(command=lambda t=text: self.number_click(t))
            elif text in ['+', '−', '×', '÷']:
                btn.configure(command=lambda op=text: self.operator_click(op))
            elif text == '=':
                btn.configure(command=self.calculate)
            elif text == 'C':
                btn.configure(command=self.clear)
            elif text == '±':
                btn.configure(command=self.negate)
            elif text == '%':
                btn.configure(command=self.percent)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def number_click(self, number):
        """Обработка нажатия на цифру"""
        if self.new_number:
            self.current_number.set(number)
            self.new_number = False
        else:
            if number == '.' and '.' in self.current_number.get():
                return
            current = self.current_number.get()
            if current == '0' and number != '.':
                self.current_number.set(number)
            else:
                self.current_number.set(current + number)
    
    def operator_click(self, op):
        """Обработка нажатия на оператор"""
        if self.operation and not self.new_number:
            self.calculate()
        
        self.stored_number = float(self.current_number.get())
        self.operation = op
        self.new_number = True
        
        # Обновление истории
        self.update_history(f"{self.stored_number} {op}")
    
    def calculate(self):
        """Выполнение вычисления"""
        if not self.operation:
            return
        
        current = float(self.current_number.get())
        result = 0
        
        if self.operation == '+':
            result = self.stored_number + current
        elif self.operation == '−':
            result = self.stored_number - current
        elif self.operation == '×':
            result = self.stored_number * current
        elif self.operation == '÷':
            if current == 0:
                self.current_number.set("Error")
                self.new_number = True
                self.operation = None
                self.update_history("Error")
                return
            result = self.stored_number / current
        
        # Форматирование результата
        if result.is_integer():
            result_str = str(int(result))
        else:
            result_str = str(round(result, 8)).rstrip('0').rstrip('.')
        
        self.current_number.set(result_str)
        
        # Обновление истории
        self.update_history(f"{self.stored_number} {self.operation} {current} = {result_str}")
        
        self.operation = None
        self.new_number = True
    
    def clear(self):
        """Очистка калькулятора"""
        self.current_number.set("0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True
        self.update_history("")
    
    def negate(self):
        """Смена знака числа"""
        current = float(self.current_number.get())
        self.current_number.set(str(-current))
    
    def percent(self):
        """Вычисление процента"""
        current = float(self.current_number.get())
        result = current / 100
        if result.is_integer():
            self.current_number.set(str(int(result)))
        else:
            self.current_number.set(str(round(result, 8)).rstrip('0').rstrip('.'))
    
    def update_history(self, text):
        """Обновление истории вычислений"""
        if text:
            self.history.append(text)
            if len(self.history) > 3:  # Показываем только последние 3 операции
                self.history.pop(0)
        
        # Отображение истории
        history_text = " | ".join(self.history[-2:]) if self.history else ""
        self.history_label.config(text=history_text)
    
    def bind_keyboard(self):
        """Привязка клавиатуры"""
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Delete>', lambda e: self.clear())
    
    def key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.char
        
        if key.isdigit():
            self.number_click(key)
        elif key == '.':
            self.number_click('.')
        elif key in ['+', '-', '*', '/']:
            operators = {'+': '+', '-': '−', '*': '×', '/': '÷'}
            self.operator_click(operators[key])
        elif key == '%':
            self.percent()
    
    def backspace(self):
        """Удаление последнего символа"""
        current = self.current_number.get()
        if len(current) > 1:
            self.current_number.set(current[:-1])
        else:
            self.current_number.set("0")

def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
