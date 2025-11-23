import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os, sys

# import modules (tokenizer + symbolizer)
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from lexer import tokenize_program, TokenType
    from lexer.lol_tokens import TOKEN_DESCRIPTIONS
    from semantics import interpret, lol_to_str
    from parser import Parser, SyntaxError as LOLSyntaxError
except ImportError as e:
    print("import error:", e)
    sys.exit(1)

class LOLCodeInterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")
        self.root.geometry("1400x800")
        
        # color scheme
        self.header_bg = "#ffffff"  # Light header
        self.sidebar_bg = "#ecf0f1"  # Light sidebar
        self.editor_bg = "#1e2a38"  # Dark editor
        self.editor_text = "#ffffff"  # White text
        self.console_bg = "#151e28"  # Darker console
        self.console_text = "#00ff9f"  # Green console text
        self.accent_yellow = "#d4ff00"  # Yellow accent
        self.table_header = "#34495e"  # Table header
        
        # for multi-file support
        self.open_files = {}
        self.current_tab_id = None
        self.tab_counter = 0
        
        self.tokens = []
        self.sidebar_visible = True
        
        self.create_layout()
    
    def create_layout(self):
        self.root.configure(bg=self.header_bg)
    
        # top header bar
        self.create_header()
        
        # placeholder for content
        content = tk.Frame(self.root, bg=self.sidebar_bg)
        content.pack(fill=tk.BOTH, expand=True)
        label = tk.Label(content, text="Content Area - Under Construction", 
                        bg=self.sidebar_bg, font=("Arial", 14))
        label.pack(expand=True)

        
    def create_header(self):
        header = tk.Frame(self.root, bg=self.header_bg, height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # file menu button
        file_btn = tk.Menubutton(header, text="File", bg=self.header_bg, fg="black",
                                font=("Arial", 11), activebackground="#d6d6d6",
                                relief=tk.FLAT, cursor="hand2")
        file_btn.pack(side=tk.LEFT, padx=20, pady=10)
        
        file_menu = tk.Menu(file_btn, tearoff=0, bg="#34495e", fg="white")
        file_menu.add_command(label="Open", command=lambda: print("Open"))
        file_menu.add_command(label="Save", command=lambda: print("Save"))
        file_menu.add_command(label="Save As...", command=lambda: print("Save As"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        file_btn.config(menu=file_menu)
        
        # center logo with image
        try:     
            logo_path = os.path.join(script_dir, "logo_lolcode.png")
            pil_image = Image.open(logo_path)
            
            # max height for aspect ratio
            max_height = 80
            aspect_ratio = pil_image.width / pil_image.height
            new_height = max_height
            new_width = int(aspect_ratio * new_height)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(pil_image)
            self.logo_img = logo_img
            logo_label = tk.Label(header, image=logo_img, bg=self.header_bg)
        except Exception as e:
            print(f"Logo error: {e}")
            logo_label = tk.Label(header, text="LOLCODE LOGO", bg=self.header_bg,
                                fg="black", font=("Arial", 12, "bold"))

        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # right side title
        title_label = tk.Label(header, text="OH HAI! I'M YR Interpreter!", bg=self.header_bg,
                            fg="black", font=("Arial", 11))
        title_label.pack(side=tk.RIGHT, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    LOLCodeInterpreterGUI(root)
    root.mainloop()