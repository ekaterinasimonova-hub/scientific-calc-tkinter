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
        self.current_expression = "0"  # Full expression shown in display
        self.current_number = "0"      # Current number being entered
        self.previous_number = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.history = []  # List of (expression, result) tuples
        self.last_result = ""  # Last calculation result for history
        self.degrees_mode = True
        
        self.create_widgets()
        
    def setup_theme(self):
        """Configure modern dark theme"""
        style = ttk.Style()
        self.root.configure(bg='#1e1e1e')
        style.theme_use('clam')
        
        # Button styles (same as original)
        style.configure('Operator.TButton', font=('Segoe UI', 11, 'bold'), padding=10,
                       background='#ff9500', foreground='white', borderwidth=0)
        style.map('Operator.TButton', background=[('active', '#ffb347'), ('pressed', '#e68900')])
        
        style.configure('Number.TButton', font=('Segoe UI', 13), padding=10,
                       background='#2d2d2d', foreground='white', borderwidth=0)
        style.map('Number.TButton', background=[('active', '#404040'), ('pressed', '#2d2d2d')])
        
        style.configure('Function.TButton', font=('Segoe UI', 9), padding=10,
                       background='#404040', foreground='#ff9500', borderwidth=0)
        style.map('Function.TButton', background=[('active', '#505050'), ('pressed', '#404040')])
        
        style.configure('Sci.TButton', font=('Segoe UI', 9), padding=10,
                       background='#5ac8fa', foreground='white', borderwidth=0)
        style.map('Sci.TButton', background=[('active', '#74d0fc'), ('pressed', '#4ab8ea')])
        
        style.configure('Clear.TButton', font=('Segoe UI', 11, 'bold'), padding=10,
                       background='#ff3b30', foreground='white', borderwidth=0)
        style.map('Clear.TButton', background=[('active', '#ff5c52'), ('pressed', '#ff3b30')])
        
        style.configure('Equals.TButton', font=('Segoe UI', 13, 'bold'), padding=10,
                       background='#34c759', foreground='white', borderwidth=0)
        style.map('Equals.TButton', background=[('active', '#5dd986'), ('pressed', '#34c759')])
        
        style.configure('History.TButton', font=('Segoe UI', 9), padding=6,
                       background='#404040', foreground='white', borderwidth=0)
        style.map('History.TButton', background=[('active', '#505050'), ('pressed', '#404040')])
        
        # Enhanced display styles
        style.configure('MainDisplay.TLabel', font=('Segoe UI', 28, 'bold'),
                       background='#1e1e1e', foreground='white', anchor='e')
        style.configure('ExpressionDisplay.TLabel', font=('Segoe UI', 14),
                       background='#2d2d2d', foreground='#a0a0a0', anchor='e')
        
        style.configure('History.TListbox', font=('Segoe UI', 9),
                       background='#2d2d2d', foreground='white', borderwidth=0,
                       focuscolor='none')
        style.configure('HistoryClear.TButton', font=('Segoe UI', 8, 'bold'), padding=5,
                       background='#ff3b30', foreground='white', borderwidth=0)
        style.map('HistoryClear.TButton', background=[('active', '#ff5c52'), ('pressed', '#ff3b30')])
        
    def create_widgets(self):
        """Create and layout all widgets"""
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#1e1e1e')
        title_frame.pack(fill='x', pady=(0, 10))
        tk.Label(title_frame, text="Scientific Calculator", 
                font=('Segoe UI', 14, 'bold'), bg='#1e1e1e', fg='white').pack()
        self.mode_label = tk.Label(title_frame, text="DEG", 
                                 font=('Segoe UI', 10), bg='#1e1e1e', fg='#5ac8fa')
        self.mode_label.pack(anchor='e')
        
        # Enhanced display area
        display_frame = tk.Frame(main_frame, bg='#1e1e1e')
        display_frame.pack(fill='x', pady=(0, 15))
        
        # Expression display (shows full calculation)
        self.expression_var = tk.StringVar(value="")
        self.expression_display = ttk.Label(display_frame, textvariable=self.expression_var,
                                          style='ExpressionDisplay.TLabel')
        self.expression_display.pack(fill='x', pady=(0, 5))
        
        # Main result display
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Label(display_frame, textvariable=self.display_var,
                               style='MainDisplay.TLabel')
        self.display.pack(fill='x')
        
        # History toggle
        self.history_visible = False
        self.history_btn = ttk.Button(display_frame, text="📋 History", 
                                    style='History.TButton', command=self.toggle_history)
        self.history_btn.pack(anchor='e', pady=(5, 0))
        
        # History panel
        self.history_frame = tk.Frame(main_frame, bg='#1e1e1e')
        self.history_listbox = tk.Listbox(self.history_frame, bg='#2d2d2d', fg='white',
                                        font=('Segoe UI', 9), selectbackground='#ff9500',
                                        selectforeground='white', borderwidth=0,
                                        highlightthickness=0, relief='flat')
        self.history_listbox.pack(fill='both', expand=True, padx=(0, 5))
        self.clear_history_btn = ttk.Button(self.history_frame, text="Clear All",
                                          style='HistoryClear.TButton',
                                          command=self.clear_history)
        self.clear_history_btn.pack(fill='x', pady=(5, 0))
        
        # Calculator buttons (same layout as original)
        self.sci_frame = tk.Frame(main_frame, bg='#1e1e1e')
        self.button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        
        # Scientific functions
        sci_buttons = [
            ('sin', 0, 0, 'Sci.TButton'), ('cos', 1, 0, 'Sci.TButton'),
            ('tan', 2, 0, 'Sci.TButton'), ('cot', 3, 0, 'Sci.TButton'), ('π', 4, 0, 'Sci.TButton')
        ]
        for (text, col, row, style) in sci_buttons:
            ttk.Button(self.sci_frame, text=text, style=style,
                     command=lambda t=text: self.button_click(t)).grid(row=row, column=col, sticky='nsew', padx=1, pady=2)
        self.sci_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        
        # Main buttons
        buttons = [
            ('C', 0, 0, 'Clear.TButton'), ('±', 1, 0, 'Function.TButton'), ('%', 2, 0, 'Function.TButton'), ('÷', 3, 0, 'Operator.TButton'),
            ('7', 0, 1, 'Number.TButton'), ('8', 1, 1, 'Number.TButton'), ('9', 2, 1, 'Number.TButton'), ('×', 3, 1, 'Operator.TButton'),
            ('4', 0, 2, 'Number.TButton'), ('5', 1, 2, 'Number.TButton'), ('6', 2, 2, 'Number.TButton'), ('-', 3, 2, 'Operator.TButton'),
            ('1', 0, 3, 'Number.TButton'), ('2', 1, 3, 'Number.TButton'), ('3', 2, 3, 'Number.TButton'), ('+', 3, 3, 'Operator.TButton'),
            ('0', 0, 4, 'Number.TButton'), ('.', 2, 4, 'Number.TButton'), ('=', 3, 4, 'Equals.TButton')
        ]
        
        for (text, col, row, style) in buttons:
            if text == '0':
                btn = ttk.Button(self.button_frame, text=text, style=style,
                               command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, columnspan=2, sticky='nsew', padx=2, pady=2)
            else:
                ttk.Button(self.button_frame, text=text, style=style,
                         command=lambda t=text: self.button_click(t)).grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        
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
    
    def update_displays(self):
        """Update both expression and main displays"""
        self.display_var.set(self.current_number)
        self.expression_var.set(self.current_expression)
    
    def input_number(self, char):
        """Handle number input - updates both displays"""
        if self.waiting_for_operand:
            self.current_number = "0"
            self.current_expression = "0"
            self.waiting_for_operand = False
        
        if char == '.' and '.' in self.current_number:
            return
        
        if self.current_number == "0" and char != '.':
            self.current_number = char
        else:
            self.current_number += char
        
        self.current_expression = self.current_number
        self.update_displays()
    
    def input_operator(self, op):
        """Handle operator input - builds expression"""
        if self.current_number:
            if self.previous_number and self.operator:
                # Chain calculation
                self.calculate()
            
            self.previous_number = self.current_number
            self.operator = self._map_operator(op)
            self.waiting_for_operand = True
            
            # Update expression display
            display_op = self._map_display_operator(self.operator)
            self.current_expression = f"{self.previous_number} {display_op}"
            self.update_displays()
    
    def calculate(self):
        """Perform calculation with full expression history"""
        if self.previous_number and self.operator and self.current_number != "":
            try:
                if self.operator == '/' and self.current == '0':
                    self.display_var.set("Error")
                    self.clear_state()
                    return
                
                # Full expression for history
                display_op = self._map_display_operator(self.operator)
                full_expression = f"{self.previous_number} {display_op} {self.current_number}"
                
                # Perform calculation
                result = eval(f"{float(self.previous_number)} {self.operator} {float(self.current_number)}")
                result_str = str(result) if result.is_integer() else f"{result:.10g}"
                
                # Add to history
                self.add_to_history(full_expression, result_str)
                
                # Update state
                self.last_result = result_str
                self.current_number = result_str
                self.current_expression = full_expression  # Keep expression visible
                self.clear_state()
                self.update_displays()
                
            except:
                self.display_var.set("Error")
                self.expression_var.set("Error")
                self.clear_state()
    
    def scientific_function(self, func):
        """Handle scientific functions with expression tracking"""
        try:
            value = float(self.current_number)
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
            
            result_str = str(result) if abs(result - round(result)) < 1e-10 else f"{result:.10g}"
            expression = f"{func}({self.current_number}{'°' if self.degrees_mode else 'rad'})"
            
            self.add_to_history(expression, result_str)
            self.current_number = result_str
            self.current_expression = expression
            self.update_displays()
            
        except:
            self.display_var.set("Error")
            self.expression_var.set("Error")
    
    def pi(self):
        """Insert π constant"""
        pi_str = f"{math.pi:.10g}"
        self.current_number = pi_str
        self.current_expression = "π"
        self.update_displays()
    
    def add_to_history(self, expression, result):
        """Add calculation to history"""
        self.history.insert(0, f"{expression} = {result}")
        self.update_history_display()
    
    def update_history_display(self):
        """Update history listbox"""
        self.history_listbox.delete(0, tk.END)
        for item in self.history[-10:]:
            self.history_listbox.insert(tk.END, item)
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.update_history_display()
    
    def clear(self):
        """Clear everything"""
        self.current_number = "0"
        self.current_expression = "0"
        self.previous_number = ""
        self.operator = ""
        self.waiting_for_operand = False
        self.update_displays()
    
    def clear_state(self):
        """Clear operation state"""
        self.previous_number = ""
        self.operator = ""
        self.waiting_for_operand = False
    
    def toggle_sign(self):
        """Toggle sign of current number"""
        if self.current_number != "0":
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.current_expression = self.current_number
            self.update_displays()
    
    def percentage(self):
        """Convert current number to percentage"""
        try:
            value = float(self.current_number) / 100
            result_str = str(value) if value.is_integer() else f"{value:.10g}"
            self.current_number = result_str
            self.current_expression = f"{self.current_number}%"
            self.update_displays()
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
