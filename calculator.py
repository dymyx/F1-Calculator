import customtkinter as ctk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Calculator")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root.configure(fg_color=("#0f0f0f", "#0f0f0f"))
        self.root.resizable(False, False)
        
        # Calculator state variables
        self.current_expression = ""
        self.current_result = "0"
        self.should_reset = False
        
        self.create_header()
        self.create_display()
        self.create_buttons()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(
            self.root,
            fg_color="#e10600",
            corner_radius=0,
            height=60
        )
        header_frame.pack(fill='x', padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ F1 CALCULATOR ⚡",
            font=("Formula1 Display Bold", 28, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=15)
        
    def create_display(self):
        display_frame = ctk.CTkFrame(
            self.root, 
            fg_color="#1a1a1a",
            corner_radius=15,
            border_width=2,
            border_color="#e10600"
        )
        display_frame.pack(padx=15, pady=20, fill='x')
        
        self.expression_label = ctk.CTkLabel(
            display_frame,
            text="",
            font=("Formula1 Display Regular", 20),
            text_color=("#15ff00", "#15ff00"),
            anchor='e'
        )
        self.expression_label.pack(fill='x', pady=(12, 3), padx=15)
        
        self.result_label = ctk.CTkLabel(
            display_frame,
            text="0",
            font=("Formula1 Display Bold", 58, "bold"),
            text_color=("#ffffff", "#ffffff"),
            anchor='e'
        )
        self.result_label.pack(fill='x', pady=(0, 12), padx=15)
        
    def create_buttons(self):
        button_frame = ctk.CTkFrame(
            self.root, 
            fg_color="transparent",
            corner_radius=0
        )
        button_frame.pack(padx=15, pady=(0, 20))
        
        buttons = [
            ['C', 'CE', '⌫', '/'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                # Determine button colors
                if btn_text in ['/', '×', '-', '+']:
                    fg_color = "#0090ff"
                    hover_color = "#00b3ff"
                    text_color = "#ffffff"
                    border_color = "#0090ff"
                elif btn_text == '=':
                    fg_color = "#15ff00"
                    hover_color = "#3aff2a"
                    text_color = "#000000"
                    border_color = "#15ff00"
                elif btn_text in ['C', 'CE', '⌫']:
                    fg_color = "#e10600"
                    hover_color = "#ff1a0d"
                    text_color = "#ffffff"
                    border_color = "#e10600"
                else:
                    fg_color = "#2a2a2a"
                    hover_color = "#3d3d3d"
                    text_color = "#ffffff"
                    border_color = "#444444"
                
                # Determine button command
                if btn_text.isdigit():
                    command = lambda x=btn_text: self.on_number_click(x)
                elif btn_text in ['/', '×', '-', '+']:
                    command = lambda x=btn_text: self.on_operator_click(x)
                elif btn_text == '=':
                    command = self.on_equals_click
                elif btn_text == 'C':
                    command = self.on_clear_click
                elif btn_text == 'CE':
                    command = self.on_clear_entry_click
                elif btn_text == '⌫':
                    command = self.on_backspace_click
                elif btn_text == '.':
                    command = self.on_decimal_click
                elif btn_text == '+/-':
                    command = self.on_sign_change_click
                else:
                    command = None
                
                btn = ctk.CTkButton(
                    button_frame,
                    text=btn_text,
                    font=("Formula1 Display Bold", 26, "bold"),
                    text_color=text_color,
                    fg_color=fg_color,
                    hover_color=hover_color,
                    corner_radius=10,
                    width=75,
                    height=75,
                    border_width=2,
                    border_color=border_color,
                    cursor='hand2',
                    command=command
                )
                btn.grid(row=row_idx, column=col_idx, padx=4, pady=4, sticky='nsew')
        
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
    
    def on_number_click(self, number):
        """Handle number button clicks"""
        if self.should_reset:
            self.current_result = ""
            self.should_reset = False
        
        if self.current_result == "0":
            self.current_result = str(number)
        else:
            self.current_result += str(number)
        
        self.update_display()
    
    def on_operator_click(self, operator):
        """Handle operator button clicks"""
        if self.current_expression and not self.should_reset:
            self.calculate()
        
        # Convert × to * for calculation
        if operator == '×':
            operator = '*'
        
        self.current_expression = self.current_result + " " + operator + " "
        self.should_reset = True
        self.update_display()
    
    def calculate(self):
        """Perform the calculation"""
        try:
            if self.current_expression:
                # Build the full expression
                full_expression = self.current_expression + self.current_result
                # Replace × with * for eval
                full_expression = full_expression.replace('×', '*')
                # Calculate
                result = eval(full_expression)
                # Format the result
                if isinstance(result, float):
                    # Remove trailing zeros
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)
                        result = str(result).rstrip('0').rstrip('.')
                
                self.current_result = str(result)
                self.current_expression = ""
                self.should_reset = True
        except Exception:
            self.current_result = "Error"
            self.current_expression = ""
            self.should_reset = True
        
        self.update_display()
    
    def on_equals_click(self):
        """Handle equals button click"""
        self.calculate()
    
    def on_clear_click(self):
        """Handle C (Clear All) button click"""
        self.current_expression = ""
        self.current_result = "0"
        self.should_reset = False
        self.update_display()
    
    def on_clear_entry_click(self):
        """Handle CE (Clear Entry) button click"""
        self.current_result = "0"
        self.should_reset = False
        self.update_display()
    
    def on_backspace_click(self):
        """Handle backspace button click"""
        if not self.should_reset and len(self.current_result) > 1:
            self.current_result = self.current_result[:-1]
        else:
            self.current_result = "0"
        self.update_display()
    
    def on_decimal_click(self):
        """Handle decimal point button click"""
        if self.should_reset:
            self.current_result = "0"
            self.should_reset = False
        
        if '.' not in self.current_result:
            self.current_result += '.'
        
        self.update_display()
    
    def on_sign_change_click(self):
        """Handle +/- button click"""
        if self.current_result != "0" and self.current_result != "Error":
            if self.current_result.startswith('-'):
                self.current_result = self.current_result[1:]
            else:
                self.current_result = '-' + self.current_result
        self.update_display()
    
    def update_display(self):
        """Update the calculator display"""
        self.expression_label.configure(text=self.current_expression)
        self.result_label.configure(text=self.current_result)

def main():
    root = ctk.CTk()
    root.geometry('420x760')
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
#SIMPLY LOVELY
