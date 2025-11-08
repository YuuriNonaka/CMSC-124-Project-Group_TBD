import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add script directory to path (for package imports)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    #try importing the lexer package
    from lexer import tokenize_program, TokenType

except ImportError as e:
    print("\n========== IMPORT ERROR DEBUG ==========")
    print(f"⚠️ ImportError: {e}\n")
    print("🔍 Debug Info:")
    print(f"  • Script path: {__file__}")
    print(f"  • Script directory: {script_dir}")
    print(f"  • Current working directory: {os.getcwd()}")
    print(f"  • sys.path entries:")
    for p in sys.path:
        print(f"    - {p}")
    print("\n🧩 Expected structure (relative to script_dir):")
    print("  lexer/")
    print("    ├── __init__.py")
    print("    ├── lexer.py")
    print("    └── lol_tokens.py\n")
    print("💡 Tips:")
    print("  1. Make sure you're running the script *from the project root*, e.g.:")
    print("       cd", script_dir)
    print("       python lolcode_gui.py")
    print("  2. Check that 'lexer' folder exists in the same directory as this file.")
    print("  3. Ensure '__init__.py' exists inside the 'lexer' folder.\n")
    print("=========================================\n")
    sys.exit(1)



class LOLCodeInterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TBD LOLTERPRETER")
        self.root.geometry("1200x700")
        
        self.current_file = None
        self.tokens = []
        
        #create menu bar
        self.create_menu()
        
        #create main container
        main_container = tk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        #create top section (file path)
        self.create_file_path_section(main_container)
        
        #create middle section (3-column layout)
        self.create_middle_section(main_container)
        
        #create bottom section (execute button and console)
        self.create_bottom_section(main_container)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_file_as())
    
    def create_file_path_section(self, parent):
        path_frame = tk.Frame(parent, bg='#f0f0f0', height=30)
        path_frame.pack(fill=tk.X, pady=(0, 5))
        path_frame.pack_propagate(False)
        
        self.file_path_label = tk.Label(
            path_frame, 
            text="(None)", 
            bg='#f0f0f0', 
            fg='#666666',
            anchor='w',
            padx=10,
            font=('Arial', 10)
        )
        self.file_path_label.pack(fill=tk.BOTH, expand=True)
    
    def create_middle_section(self, parent):
        # Create PanedWindow for resizable columns
        paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Text Editor
        self.create_text_editor(paned)
        
        # Middle panel - Lexemes Table
        self.create_lexemes_table(paned)
        
        # Right panel - Symbol Table (placeholder)
        self.create_symbol_table(paned)
    
    def create_text_editor(self, paned):
        editor_frame = tk.Frame(paned)
        paned.add(editor_frame, width=400)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(editor_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget
        self.text_editor = tk.Text(
            editor_frame,
            wrap=tk.NONE,
            yscrollcommand=scrollbar.set,
            font=('Consolas', 11),
            bg='white',
            fg='black',
            insertbackground='black',
            selectbackground='#0078d7',
            selectforeground='white'
        )
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_editor.yview)
        
        self.add_line_numbers()
    
    def add_line_numbers(self):
        # This is a simple implementation - can be enhanced
        pass
    
    def create_lexemes_table(self, paned):
        lexemes_frame = tk.Frame(paned)
        paned.add(lexemes_frame, width=400)
        
        # Add label
        label = tk.Label(lexemes_frame, text="Lexemes", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        label.pack(fill=tk.X, pady=(0, 5))
        
        # Create treeview with scrollbar
        tree_frame = tk.Frame(lexemes_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = tk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.lexemes_tree = ttk.Treeview(
            tree_frame,
            columns=('Lexeme', 'Classification'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        self.lexemes_tree.heading('Lexeme', text='Lexeme')
        self.lexemes_tree.heading('Classification', text='Classification')
        
        self.lexemes_tree.column('Lexeme', width=150, anchor='w')
        self.lexemes_tree.column('Classification', width=200, anchor='w')
        
        self.lexemes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.lexemes_tree.yview)
        hsb.config(command=self.lexemes_tree.xview)
        
        # Configure alternating row colors
        self.lexemes_tree.tag_configure('oddrow', background='white')
        self.lexemes_tree.tag_configure('evenrow', background='#f0f0f0')
    
    def create_symbol_table(self, paned):
        symbol_frame = tk.Frame(paned, bg='white')
        paned.add(symbol_frame, width=300)
        
        # Add label
        label = tk.Label(symbol_frame, text="SYMBOL TABLE", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        label.pack(fill=tk.X, pady=(0, 5))
        
        # Placeholder content
        placeholder_frame = tk.Frame(symbol_frame, bg='white')
        placeholder_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview structure (non-functional for now)
        tree_frame = tk.Frame(placeholder_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.symbol_tree = ttk.Treeview(
            tree_frame,
            columns=('Identifier', 'Value'),
            show='headings',
            yscrollcommand=vsb.set
        )
        
        self.symbol_tree.heading('Identifier', text='Identifier')
        self.symbol_tree.heading('Value', text='Value')
        
        self.symbol_tree.column('Identifier', width=100, anchor='w')
        self.symbol_tree.column('Value', width=150, anchor='w')
        
        self.symbol_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self.symbol_tree.yview)
        
        # Configure alternating row colors
        self.symbol_tree.tag_configure('oddrow', background='white')
        self.symbol_tree.tag_configure('evenrow', background='#f0f0f0')
    
    def create_bottom_section(self, parent):
        bottom_frame = tk.Frame(parent)
        bottom_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 0))
        
        # Execute button
        self.execute_btn = tk.Button(
            bottom_frame,
            text="EXECUTE",
            command=self.execute,
            font=('Arial', 11, 'bold'),
            bg='#0078d7',
            fg='white',
            activebackground='#005a9e',
            activeforeground='white',
            padx=20,
            pady=8,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.execute_btn.pack(pady=(0, 5))
        
        # Console output (placeholder)
        console_frame = tk.Frame(bottom_frame, bg='white', relief=tk.SUNKEN, borderwidth=1)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for console
        console_scroll = tk.Scrollbar(console_frame)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.console_text = tk.Text(
            console_frame,
            height=8,
            bg='white',
            fg='black',
            font=('Consolas', 10),
            state=tk.DISABLED,
            yscrollcommand=console_scroll.set
        )
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scroll.config(command=self.console_text.yview)
    
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Open LOLCode File",
            filetypes=[("LOLCode Files", "*.lol"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                
                self.current_file = filename
                self.file_path_label.config(text=filename)
                
                # Clear previous tokens
                self.clear_lexemes_table()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_editor.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        filename = filedialog.asksaveasfilename(
            title="Save LOLCode File",
            defaultextension=".lol",
            filetypes=[("LOLCode Files", "*.lol"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                content = self.text_editor.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.current_file = filename
                self.file_path_label.config(text=filename)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def execute(self):
        # Get the code from text editor
        source_code = self.text_editor.get(1.0, tk.END)
        
        if not source_code.strip():
            messagebox.showwarning("Warning", "No code to execute!")
            return
        
        try:
            # Tokenize the program
            self.tokens = tokenize_program(source_code)
            
            # Update lexemes table
            self.update_lexemes_table()
            
            # Update console with success message
            self.update_console(f"Lexical analysis complete!\nTotal tokens: {len(self.tokens)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Lexical analysis failed:\n{str(e)}")
            self.update_console(f"ERROR: {str(e)}")
    
    def clear_lexemes_table(self):
        for item in self.lexemes_tree.get_children():
            self.lexemes_tree.delete(item)
    
    def update_lexemes_table(self):
        # Clear existing items
        self.clear_lexemes_table()
        
        # Filter out linebreaks
        display_tokens = [t for t in self.tokens if t[1] != TokenType.LINEBREAK]
        
        # Add tokens to the table
        for idx, (lexeme, token_type, line_num) in enumerate(display_tokens):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.lexemes_tree.insert(
                '',
                tk.END,
                values=(lexeme, token_type.value),
                tags=(tag,)
            )
    
    def update_console(self, message):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.insert(1.0, message)
        self.console_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = LOLCodeInterpreterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()