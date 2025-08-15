import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import math

class WindowsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        
        # Переменные для вычислений
        self.current_number = ttk.StringVar(value="0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True
        self.history = []
        self.memory = 0
        
        # Настройка темы
        self.setup_theme()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка клавиатуры
        self.bind_keyboard()
        
        # Центрирование окна
        self.center_window()
        
    def setup_theme(self):
        """Настройка современной темы"""
        self.root.style.theme_use("flatly")
        
    def create_widgets(self):
        """Создание элементов интерфейса в стиле Windows Calculator"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Дисплей
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill='x', pady=(0, 20))
        
        # История вычислений
        self.history_label = ttk.Label(display_frame,
                                     text="",
                                     font=("Segoe UI", 12),
                                     anchor='e',
                                     padding=(20, 10, 20, 5))
        self.history_label.pack(fill='x')
        
        # Основной дисплей
        self.display_label = ttk.Label(display_frame,
                                    textvariable=self.current_number,
                                    font=("Segoe UI", 48, "bold"),
                                    anchor='e',
                                    padding=(20, 5, 20, 20))
        self.display_label.pack(fill='x')
        
        # Кнопки
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='both', expand=True)
        
        # Сетка кнопок (точно как в Windows Calculator)
        buttons = [
            # Первый ряд: память и функции
            ('MC', 'Function', 0, 0), ('MR', 'Function', 0, 1), ('M+', 'Function', 0, 2), ('M-', 'Function', 0, 3),
            ('MS', 'Function', 0, 4), ('M▾', 'Function', 0, 5),
            
            # Второй ряд: функции
            ('%', 'Function', 1, 0), ('CE', 'Function', 1, 1), ('C', 'Function', 1, 2), ('⌫', 'Function', 1, 3),
            ('±', 'Function', 1, 4), ('÷', 'Operator', 1, 5),
            
            # Третий ряд: цифры и операторы
            ('7', 'Number', 2, 0), ('8', 'Number', 2, 1), ('9', 'Number', 2, 2), ('×', 'Operator', 2, 3),
            ('1/x', 'Function', 2, 4), ('x²', 'Function', 2, 5),
            
            # Четвертый ряд
            ('4', 'Number', 3, 0), ('5', 'Number', 3, 1), ('6', 'Number', 3, 2), ('−', 'Operator', 3, 3),
            ('√', 'Function', 3, 4), ('=', 'Equals', 3, 5),
            
            # Пятый ряд
            ('1', 'Number', 4, 0), ('2', 'Number', 4, 1), ('3', 'Number', 4, 2), ('+', 'Operator', 4, 3),
            ('0', 'Number', 5, 0, 2), ('.', 'Number', 5, 2), ('=', 'Equals', 5, 3)
        ]
        
        # Настройка сетки
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Создание кнопок
        for button_data in buttons:
            if len(button_data) == 6:  # Кнопка занимает 2 колонки
                text, style_type, row, col, colspan, _ = button_data
                btn = self.create_button(buttons_frame, text, style_type)
                btn.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=2, pady=2)
            else:
                text, style_type, row, col = button_data
                btn = self.create_button(buttons_frame, text, style_type)
                btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
    
    def create_button(self, parent, text, style_type):
        """Создание кнопки с соответствующим стилем"""
        if style_type == 'Number':
            btn = ttk.Button(parent, text=text, bootstyle="primary", width=8)
            btn.configure(command=lambda t=text: self.number_click(t))
        elif style_type == 'Operator':
            btn = ttk.Button(parent, text=text, bootstyle="secondary", width=8)
            btn.configure(command=lambda op=text: self.operator_click(op))
        elif style_type == 'Function':
            btn = ttk.Button(parent, text=text, bootstyle="light", width=8)
            btn.configure(command=lambda f=text: self.function_click(f))
        elif style_type == 'Equals':
            btn = ttk.Button(parent, text=text, bootstyle="success", width=8)
            btn.configure(command=self.calculate)
        
        return btn
    
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
    
    def function_click(self, func):
        """Обработка нажатия на функцию"""
        current = float(self.current_number.get())
        
        if func == 'C':
            self.clear()
        elif func == 'CE':
            self.current_number.set("0")
            self.new_number = True
        elif func == '⌫':
            self.backspace()
        elif func == '±':
            self.current_number.set(str(-current))
        elif func == '%':
            result = current / 100
            self.current_number.set(self.format_number(result))
        elif func == '1/x':
            if current != 0:
                result = 1 / current
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == 'x²':
            result = current ** 2
            self.current_number.set(self.format_number(result))
        elif func == '√':
            if current >= 0:
                result = math.sqrt(current)
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == 'MC':
            self.memory = 0
        elif func == 'MR':
            self.current_number.set(str(self.memory))
            self.new_number = True
        elif func == 'M+':
            self.memory += current
        elif func == 'M-':
            self.memory -= current
        elif func == 'MS':
            self.memory = current
    
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
        result_str = self.format_number(result)
        self.current_number.set(result_str)
        
        # Обновление истории
        self.update_history(f"{self.stored_number} {self.operation} {current} = {result_str}")
        
        self.operation = None
        self.new_number = True
    
    def format_number(self, number):
        """Форматирование числа для отображения"""
        if number.is_integer():
            return str(int(number))
        else:
            # Ограничиваем количество знаков после запятой
            return str(round(number, 10)).rstrip('0').rstrip('.')
    
    def clear(self):
        """Очистка калькулятора"""
        self.current_number.set("0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True
        self.update_history("")
    
    def backspace(self):
        """Удаление последнего символа"""
        current = self.current_number.get()
        if len(current) > 1:
            self.current_number.set(current[:-1])
        else:
            self.current_number.set("0")
    
    def update_history(self, text):
        """Обновление истории вычислений"""
        if text:
            self.history.append(text)
            if len(self.history) > 2:  # Показываем только последние 2 операции
                self.history.pop(0)
        
        # Отображение истории
        history_text = " | ".join(self.history) if self.history else ""
        self.history_label.config(text=history_text)
    
    def bind_keyboard(self):
        """Привязка клавиатуры"""
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<KP_Enter>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Delete>', lambda e: self.clear())
        self.root.bind('<KeyPress>', self.key_press)
    
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
            self.function_click('%')

def main():
    root = ttk.Window(themename="flatly")
    app = WindowsCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
