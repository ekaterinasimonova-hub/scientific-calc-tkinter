import tkinter as tk
from tkinter import ttk
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Scientific Calculator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Modern styling
        self.setup_theme()
        
        # Calculator state
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.history = []  # List of (expression, result) tuples
        self.degrees_mode = True  # True = degrees, False = radians
        
        self.create_widgets()
        
    def setup_theme(self):
        """Configure modern dark theme"""
        style = ttk.Style()
        
        # Configure main window
        self.root.configure(bg='#1e1e1e')
        
        # Custom styles
        style.theme_use('clam')
        
        # Button styles
        style.configure('Operator.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=10,
                       background='#ff9500',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Operator.TButton',
                 background=[('active', '#ffb347'), ('pressed', '#e68900')])
        
        style.configure('Number.TButton',
                       font=('Segoe UI', 13),
                       padding=10,
                       background='#2d2d2d',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Number.TButton',
                 background=[('active', '#404040'), ('pressed', '#2d2d2d')])
        
        style.configure('Function.TButton',
                       font=('Segoe UI', 9),
                       padding=10,
                       background='#404040',
                       foreground='#ff9500',
                       borderwidth=0)
        
        style.map('Function.TButton',
                 background=[('active', '#505050'), ('pressed', '#404040')])
        
        style.configure('Sci.TButton',
                       font=('Segoe UI', 9),
                       padding=10,
                       background='#5ac8fa',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Sci.TButton',
                 background=[('active', '#74d0fc'), ('pressed', '#4ab8ea')])
        
        style.configure('Clear.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=10,
                       background='#ff3b30',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Clear.TButton',
                 background=[('active', '#ff5c52'), ('pressed', '#ff3b30')])
        
        style.configure('Equals.TButton',
                       font=('Segoe UI', 13, 'bold'),
                       padding=10,
                       background='#34c759',
                       foreground='white',
                       borderwidth=0)
        
        style.map('Equals.TButton',
                 background=[('active', '#5dd986'), ('pressed', '#34c759')])
        
        style.configure('History.TButton',
                       font=('Segoe UI', 9),
                       padding=6,
                       background='#404040',
                       foreground='white',
                       borderwidth=0)
        
        style.map('History.TButton',
                 background=[('active', '#505050'), ('pressed', '#404040')])
        
        # Display style
        style.configure('Display.TLabel',
                       font=('Segoe UI', 20, 'bold'),
                       background='#1e1e1e',
                       foreground='white',
                       anchor='e')
        
        # History listbox style
        style.configure('History.TListbox',
                       font=('Segoe UI', 9),
                       background='#2d2d2d',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('HistoryClear.TButton',
                       font=('Segoe UI', 8, 'bold'),
                       padding=5,
                       background='#ff3b30',
                       foreground='white',
                       borderwidth=0)
        
        style.map('HistoryClear.TButton',
                 background=[('active', '#ff5c52'), ('pressed', '#ff3b30')])
        
    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#1e1e1e')
        title_frame.pack(fill='x', pady=(0, 10))
        title_label = tk.Label(title_frame, text="Scientific Calculator", 
                              font=('Segoe UI', 14, 'bold'),
                              bg='#1e1e1e', fg='white')
        title_label.pack()
        
        # Mode indicator
        self.mode_label = tk.Label(title_frame, text="DEG", 
                                 font=('Segoe UI', 10),
                                 bg='#1e1e1e', fg='#5ac8fa')
        self.mode_label.pack(anchor='e')
        
        # Top frame: Display + History toggle
        top_frame = tk.Frame(main_frame, bg='#1e1e1e')
        top_frame.pack(fill='x', pady=(0, 15))
        
        # Display
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Label(top_frame, textvariable=self.display_var,
                               style='Display.TLabel')
        self.display.pack(fill='x')
        
        # History toggle button
        self.history_visible = False
        self.history_btn = ttk.Button(top_frame, text="📋 History", 
                                    style='History.TButton',
                                    command=self.toggle_history)
        self.history_btn.pack(anchor='e', pady=(5, 0))
        
        # History panel (initially hidden)
        self.history_frame = tk.Frame(main_frame, bg='#1e1e1e')
        
        self.history_listbox = tk.Listbox(self.history_frame,
                                        bg='#2d2d2d',
                                        fg='white',
                                        font=('Segoe UI', 9),
                                        selectbackground='#ff9500',
                                        selectforeground='white',
                                        borderwidth=0,
                                        highlightthickness=0,
                                        relief='flat')
        self.history_listbox.pack(fill='both', expand=True, padx=(0, 5))
        
        self.clear_history_btn = ttk.Button(self.history_frame, text="Clear All",
                                          style='HistoryClear.TButton',
                                          command=self.clear_history)
        self.clear_history_btn.pack(fill='x', pady=(5, 0))
        
        # Calculator buttons frame - Now 2 rows: Scientific + Main
        self.sci_frame = tk.Frame(main_frame, bg='#1e1e1e')
        self.button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        
        # Scientific functions row
        sci_buttons = [
            ('sin', 0, 0, 'Sci.TButton'),
            ('cos', 1, 0, 'Sci.TButton'),
            ('tan', 2, 0, 'Sci.TButton'),
            ('cot', 3, 0, 'Sci.TButton'),
            ('π', 4, 0, 'Sci.TButton')
        ]
        
        for (text, col, row, style) in sci_buttons:
            btn = ttk.Button(self.sci_frame, text=text, style=style,
                           command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=2)
        
        self.sci_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        
        # Main calculator buttons (5x4 grid)
        buttons = [
            ('C', 0, 0, 'Clear.TButton'),
            ('±', 1, 0, 'Function.TButton'),
            ('%', 2, 0, 'Function.TButton'),
            ('÷', 3, 0, 'Operator.TButton'),
            
            ('7', 0, 1, 'Number.TButton'),
            ('8', 1, 1, 'Number.TButton'),
            ('9', 2, 1, 'Number.TButton'),
            ('×', 3, 1, 'Operator.TButton'),
            
            ('4', 0, 2, 'Number.TButton'),
            ('5', 1, 2, 'Number.TButton'),
            ('6', 2, 2, 'Number.TButton'),
            ('-', 3, 2, 'Operator.TButton'),
            
            ('1', 0, 3, 'Number.TButton'),
            ('2', 1, 3, 'Number.TButton'),
            ('3', 2, 3, 'Number.TButton'),
            ('+', 3, 3, 'Operator.TButton'),
            
            ('0', 0, 4, 'Number.TButton'),
            ('.', 2, 4, 'Number.TButton'),
            ('=', 3, 4, 'Equals.TButton')
        ]
        
        for (text, col, row, style) in buttons:
            if text == '0':  # Make 0 button span 2 columns
                btn = ttk.Button(self.button_frame, text=text, style=style,
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, columnspan=2, sticky='nsew', padx=2, pady=2)
            else:
                btn = ttk.Button(self.button_frame, text=text, style=style,
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        
        # Initially show scientific row + button frame
        self.sci_frame.pack(fill='x', pady=(0, 5))
        self.button_frame.pack(fill='both', expand=True)
    
    def toggle_history(self):
        """Toggle history panel visibility"""
        if self.history_visible:
            self.history_frame.pack_forget()
            self.sci_frame.pack(fill='x', pady=(0, 5))
            self.button_frame.pack(fill='both', expand=True)
            self.history_btn.configure(text="📋 History")
            self.history_visible = False
        else:
            self.button_frame.pack_forget()
            self.sci_frame.pack_forget()
            self.history_frame.pack(fill='both', expand=True)
            self.history_btn.configure(text="⌨️  Calculator")
            self.history_visible = True
        
        self.root.update_idletasks()
    
    def button_click(self, char):
        """Handle button clicks"""
        if char.isdigit() or char == '.':
            self.input_number(char)
        elif char in '+-×÷':
            self.input_operator(char)
        elif char == '=':
            self.calculate()
        elif char == 'C':
            self.clear()
        elif char == '±':
            self.toggle_sign()
        elif char == '%':
            self.percentage()
        elif char == 'π':
            self.pi()
        elif char in ['sin', 'cos', 'tan', 'cot']:
            self.scientific_function(char)
    
    def scientific_function(self, func):
        """Handle scientific functions"""
        try:
            value = float(self.current)
            if not self.degrees_mode:
                value = math.radians(value)
            
            if func == 'sin':
                result = math.sin(value)
            elif func == 'cos':
                result = math.cos(value)
            elif func == 'tan':
                if abs(math.cos(value)) < 1e-10:
                    self.display_var.set("Error")
                    return
                result = math.tan(value)
            elif func == 'cot':
                if abs(math.sin(value)) < 1e-10:
                    self.display_var.set("Error")
                    return
                result = 1 / math.tan(value)
            
            result_str = str(result) if abs(result - round(result)) < 1e-10 else f"{result:.8g}"
            expression = f"{func}({self.current}°)"
            
            self.add_to_history(expression, result_str)
            self.current = result_str
            self.display_var.set(self.current)
            
        except:
            self.display_var.set("Error")
    
    def pi(self):
        """Insert π constant"""
        self.current = str(math.pi)
        self.display_var.set(self.current)
    
    def add_to_history(self, expression, result):
        """Add calculation to history"""
        self.history.insert(0, f"{expression} = {result}")
        self.update_history_display()
    
    def update_history_display(self):
        """Update history listbox"""
        self.history_listbox.delete(0, tk.END)
        for item in self.history[-10:]:  # Show last 10 entries
            self.history_listbox.insert(tk.END, item)
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.update_history_display()
    
    def input_number(self, char):
        """Handle number input"""
        if self.waiting_for_operand:
            self.current = "0"
            self.waiting_for_operand = False
        
        if char == '.' and '.' in self.current:
            return
        
        if self.current == "0" and char != '.':
            self.current = char
        else:
            self.current += char
        
        self.display_var.set(self.current)
    
    def input_operator(self, op):
        """Handle operator input"""
        self.previous = self.current
        self.operator = self._map_operator(op)
        self.waiting_for_operand = True
    
    def calculate(self):
        """Perform calculation and add to history"""
        if self.previous and self.operator:
            try:
                if self.operator == '/' and self.current == '0':
                    self.display_var.set("Error")
                    self.clear_state()
                    return
                
                prev_display = self.previous.replace('**', '^').replace('*', '×').replace('/', '÷')
                curr_display = self.current.replace('**', '^').replace('*', '×').replace('/', '÷')
                expression = f"{prev_display} {self._map_display_operator(self.operator)} {curr_display}"
                
                result = eval(f"{float(self.previous)} {self._map_operator(self.operator)} {float(self.current)}")
                result_str = str(result) if result.is_integer() else f"{result:.8g}"
                
                self.add_to_history(expression, result_str)
                
                self.current = result_str
                self.display_var.set(self.current)
                self.clear_state()
            except:
                self.display_var.set("Error")
                self.clear_state()
    
    def clear(self):
        """Clear everything"""
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.display_var.set("0")
    
    def clear_state(self):
        """Clear operation state"""
        self.previous = ""
        self.operator = ""
        self.waiting_for_operand = False
    
    def toggle_sign(self):
        """Toggle sign of current number"""
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display_var.set(self.current)
    
    def percentage(self):
        """Convert current number to percentage"""
        try:
            value = float(self.current) / 100
            self.current = str(value) if value.is_integer() else f"{value:.8g}"
            self.display_var.set(self.current)
        except:
            pass
    
    def _map_operator(self, op):
        """Map display operator to Python operator"""
        return {'÷': '/', '×': '*', '-': '-', '+': '+'}[op]
    
    def _map_display_operator(self, py_op):
        """Map Python operator back to display operator"""
        return {'/': '÷', '*': '×', '-': '-', '+': '+'}[py_op]

def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
