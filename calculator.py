import customtkinter as ctk
import math

class ModernCalculator:
    def __init__(self):
        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Создание окна
        self.root = ctk.CTk()
        self.root.title("Modern Calculator")
        self.root.geometry("400x800")
        self.root.resizable(False, False)
        
        # Переменные для вычислений
        self.current_number = ctk.StringVar(value="0")
        self.stored_number = 0
        self.operation = None
        self.new_number = True
        self.history = []
        self.memory = 0
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка клавиатуры
        self.bind_keyboard()
        
        # Центрирование окна
        self.center_window()
        
    def create_widgets(self):
        """Создание современного интерфейса в стиле iPhone"""
        # Главный контейнер
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Вкладки
        self.create_tabs(main_frame)
        
        # Дисплей
        self.create_display(main_frame)
        
        # Кнопки
        self.create_buttons(main_frame)
        
    def create_tabs(self, parent):
        """Создание современных вкладок"""
        tab_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tab_frame.pack(fill='x', pady=(0, 20))
        
        # Создание вкладок
        self.notebook = ctk.CTkTabview(tab_frame, fg_color="transparent")
        self.notebook.pack(fill='x')
        
        # Стандартный калькулятор
        self.standard_frame = self.notebook.add("Стандартный")
        
        # Инженерный калькулятор
        self.engineering_frame = self.notebook.add("Инженерный")
        
        # Программист
        self.programmer_frame = self.notebook.add("Программист")
        
    def create_display(self, parent):
        """Создание современного дисплея"""
        display_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=20)
        display_frame.pack(fill='x', pady=(0, 20))
        
        # История вычислений
        self.history_label = ctk.CTkLabel(display_frame,
                                        text="",
                                        font=ctk.CTkFont(family="SF Pro Display", size=16),
                                        text_color="#8e8e93",
                                        anchor='e')
        self.history_label.pack(fill='x', padx=25, pady=(15, 5))
        
        # Основной дисплей
        self.display_label = ctk.CTkLabel(display_frame,
                                        textvariable=self.current_number,
                                        font=ctk.CTkFont(family="SF Pro Display", size=48, weight="bold"),
                                        text_color="#ffffff",
                                        anchor='e')
        self.display_label.pack(fill='x', padx=25, pady=(0, 20))
        
    def create_buttons(self, parent):
        """Создание кнопок для разных режимов"""
        # Стандартные кнопки
        self.create_standard_buttons()
        
        # Инженерные кнопки
        self.create_engineering_buttons()
        
        # Кнопки программиста
        self.create_programmer_buttons()
        
    def create_standard_buttons(self):
        """Создание стандартных кнопок в стиле iPhone"""
        buttons_frame = ctk.CTkFrame(self.standard_frame, fg_color="transparent")
        buttons_frame.pack(fill='both', expand=True)
        
        # Сетка кнопок (как в iPhone)
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
                btn = self.create_button_widget(buttons_frame, text, style_type)
                btn.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=4, pady=4)
            else:
                text, style_type, row, col = button_data
                btn = self.create_button_widget(buttons_frame, text, style_type)
                btn.grid(row=row, column=col, sticky='nsew', padx=4, pady=4)
    
    def create_engineering_buttons(self):
        """Создание инженерных кнопок"""
        buttons_frame = ctk.CTkFrame(self.engineering_frame, fg_color="transparent")
        buttons_frame.pack(fill='both', expand=True)
        
        # Сетка инженерных кнопок
        buttons = [
            ('sin', 'Scientific', 0, 0), ('cos', 'Scientific', 0, 1), ('tan', 'Scientific', 0, 2), ('log', 'Scientific', 0, 3),
            ('ln', 'Scientific', 1, 0), ('x²', 'Scientific', 1, 1), ('x³', 'Scientific', 1, 2), ('√', 'Scientific', 1, 3),
            ('1/x', 'Scientific', 2, 0), ('x^y', 'Scientific', 2, 1), ('e^x', 'Scientific', 2, 2), ('10^x', 'Scientific', 2, 3),
            ('π', 'Scientific', 3, 0), ('e', 'Scientific', 3, 1), ('n!', 'Scientific', 3, 2), ('mod', 'Scientific', 3, 3),
            ('(', 'Scientific', 4, 0), (')', 'Scientific', 4, 1), ('C', 'Function', 4, 2), ('=', 'Equals', 4, 3)
        ]
        
        # Настройка сетки
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Создание кнопок
        for button_data in buttons:
            text, style_type, row, col = button_data
            btn = self.create_button_widget(buttons_frame, text, style_type)
            btn.grid(row=row, column=col, sticky='nsew', padx=4, pady=4)
    
    def create_programmer_buttons(self):
        """Создание кнопок программиста"""
        buttons_frame = ctk.CTkFrame(self.programmer_frame, fg_color="transparent")
        buttons_frame.pack(fill='both', expand=True)
        
        # Сетка кнопок программиста
        buttons = [
            ('HEX', 'Function', 0, 0), ('DEC', 'Function', 0, 1), ('OCT', 'Function', 0, 2), ('BIN', 'Function', 0, 3),
            ('AND', 'Scientific', 1, 0), ('OR', 'Scientific', 1, 1), ('XOR', 'Scientific', 1, 2), ('NOT', 'Scientific', 1, 3),
            ('LSH', 'Scientific', 2, 0), ('RSH', 'Scientific', 2, 1), ('ROL', 'Scientific', 2, 2), ('ROR', 'Scientific', 2, 3),
            ('A', 'Scientific', 3, 0), ('B', 'Scientific', 3, 1), ('C', 'Scientific', 3, 2), ('D', 'Scientific', 3, 3),
            ('E', 'Scientific', 4, 0), ('F', 'Scientific', 4, 1), ('C', 'Function', 4, 2), ('=', 'Equals', 4, 3)
        ]
        
        # Настройка сетки
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Создание кнопок
        for button_data in buttons:
            text, style_type, row, col = button_data
            btn = self.create_button_widget(buttons_frame, text, style_type)
            btn.grid(row=row, column=col, sticky='nsew', padx=4, pady=4)
    
    def create_button_widget(self, parent, text, style_type):
        """Создание современной кнопки с соответствующим стилем"""
        if style_type == 'Number':
            btn = ctk.CTkButton(parent, text=text, 
                               font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"),
                               fg_color="#333333", hover_color="#444444",
                               corner_radius=25, height=60)
            btn.configure(command=lambda t=text: self.number_click(t))
        elif style_type == 'Operator':
            btn = ctk.CTkButton(parent, text=text, 
                               font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"),
                               fg_color="#ff9500", hover_color="#ffaa33",
                               corner_radius=25, height=60)
            btn.configure(command=lambda op=text: self.operator_click(op))
        elif style_type == 'Function':
            btn = ctk.CTkButton(parent, text=text, 
                               font=ctk.CTkFont(family="SF Pro Display", size=20, weight="bold"),
                               fg_color="#a5a5a5", hover_color="#b5b5b5",
                               corner_radius=25, height=60)
            btn.configure(command=lambda f=text: self.function_click(f))
        elif style_type == 'Equals':
            btn = ctk.CTkButton(parent, text=text, 
                               font=ctk.CTkFont(family="SF Pro Display", size=24, weight="bold"),
                               fg_color="#ff9500", hover_color="#ffaa33",
                               corner_radius=25, height=60)
            btn.configure(command=self.calculate)
        elif style_type == 'Scientific':
            btn = ctk.CTkButton(parent, text=text, 
                               font=ctk.CTkFont(family="SF Pro Display", size=18, weight="bold"),
                               fg_color="#2d2d2d", hover_color="#3d3d3d",
                               corner_radius=20, height=50)
            btn.configure(command=lambda f=text: self.scientific_click(f))
        
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
        try:
            current = float(self.current_number.get())
        except ValueError:
            # Если не удается преобразовать в число (например, только точка), очищаем
            self.current_number.set("0")
            current = 0
        
        if func == 'C':
            self.clear()
        elif func == '±':
            self.current_number.set(str(-current))
        elif func == '%':
            result = current / 100
            self.current_number.set(self.format_number(result))
    
    def scientific_click(self, func):
        """Обработка нажатия на научную функцию"""
        current = float(self.current_number.get())
        
        if func == 'sin':
            result = math.sin(math.radians(current))
            self.current_number.set(self.format_number(result))
        elif func == 'cos':
            result = math.cos(math.radians(current))
            self.current_number.set(self.format_number(result))
        elif func == 'tan':
            result = math.tan(math.radians(current))
            self.current_number.set(self.format_number(result))
        elif func == 'log':
            if current > 0:
                result = math.log10(current)
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == 'ln':
            if current > 0:
                result = math.log(current)
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == 'x²':
            result = current ** 2
            self.current_number.set(self.format_number(result))
        elif func == 'x³':
            result = current ** 3
            self.current_number.set(self.format_number(result))
        elif func == '√':
            if current >= 0:
                result = math.sqrt(current)
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == '1/x':
            if current != 0:
                result = 1 / current
                self.current_number.set(self.format_number(result))
            else:
                self.current_number.set("Error")
        elif func == 'π':
            self.current_number.set(str(math.pi))
            self.new_number = True
        elif func == 'e':
            self.current_number.set(str(math.e))
            self.new_number = True
        elif func == 'n!':
            if current >= 0 and current.is_integer():
                result = math.factorial(int(current))
                self.current_number.set(str(result))
            else:
                self.current_number.set("Error")
    
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
    
    def update_history(self, text):
        """Обновление истории вычислений"""
        if text:
            self.history.append(text)
            if len(self.history) > 2:  # Показываем только последние 2 операции
                self.history.pop(0)
        
        # Отображение истории
        history_text = " | ".join(self.history) if self.history else ""
        self.history_label.configure(text=history_text)
    
    def bind_keyboard(self):
        """Привязка клавиатуры"""
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())
    
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
    app = ModernCalculator()
    app.root.mainloop()

if __name__ == "__main__":
    main()
