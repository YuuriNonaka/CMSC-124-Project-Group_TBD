import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, sys
from parser import Parser, SyntaxError as LOLSyntaxError

# import modules (tokenizer + symbolizer)
script_dir = os.path.dirname(os.path.abspath(__file__))  # current script directory
sys.path.insert(0, script_dir)  # add script directory

try:
    from lexer import tokenize_program, TokenType  # tokenizer and token types
    from lexer.lol_tokens import TOKEN_DESCRIPTIONS  #  token descriptions
    from semantics.symbolizer import symbolize
except ImportError as e:
    print("import error:", e)  
    sys.exit(1)  # exit if import fails

# lolcode interpreter gui
class LOLCodeInterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lolcode Interpreter")
        self.root.geometry("1100x700")

        # color 
        self.bg_color = "#1e1e1e"     # main background
        self.fg_color = "#ffffff"     # main text
        self.text_bg = "#252526"      # text editor bg
        self.text_fg = "#dcdcdc"      # editor text
        self.highlight = "#0078d7"    # accent blue
        self.tree_bg = "#2d2d30"      # tree bg
        self.tree_alt = "#3e3e42"     # alternate row
        self.tree_fg = "#ffffff"      # tree text
        self.console_bg = "#1b1b1b"   # console bg
        self.console_fg = "#00ff9f"   # console text

        # store current file info and tokens 
        self.current_file = None
        self.original_content = ""
        self.tokens = []

        # gui layout 
        self.create_menu()   # menu
        self.create_layout() 

    # menu
    def create_menu(self):
        menubar = tk.Menu(self.root)  # main menu bar
        self.root.config(menu=menubar)

        # for file fropwdown
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="file", menu=file_menu)

        # menu options
        file_menu.add_command(label="open", command=self.open_file, accelerator="ctrl+o")
        file_menu.add_command(label="save", command=self.save_file, accelerator="ctrl+s")
        file_menu.add_command(label="save as...", command=self.save_file_as, accelerator="ctrl+shift+s")
        file_menu.add_separator()
        file_menu.add_command(label="exit", command=self.root.quit)

        # keyboard shorty
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_file_as())

    # main layout
    def create_layout(self):
        self.root.configure(bg=self.bg_color)  # set root bg

        container = tk.Frame(self.root, bg=self.bg_color)  # main container frame
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # label for opened file name
        self.file_label = tk.Label(container, text="(no file opened)", bg=self.bg_color,
                                   fg=self.fg_color, anchor="w", padx=10)
        self.file_label.pack(fill=tk.X, pady=(0, 5))

        # for the resizable panels
        paned = tk.PanedWindow(container, orient=tk.HORIZONTAL, sashwidth=4, bg=self.bg_color)
        paned.pack(fill=tk.BOTH, expand=True)

        # text editor
        self.text_editor = self.add_text_editor(paned, "code editor", width=400)

        # lexemes table
        self.lexemes_tree = self.add_treeview(paned, "lexemes", ["lexeme", "classification"], 200)

        # symbol table
        self.symbol_tree = self.add_treeview(paned, "symbol table", ["identifier", "value"], 150)

        # console output and execute button
        self.add_console_section(container)

    # helpers
    def add_text_editor(self, parent, label_text, width):
        frame = tk.Frame(parent, bg=self.bg_color)  # frame for editor
        parent.add(frame, width=width)  # add to paned window

        lbl = tk.Label(frame, text=label_text, font=("arial", 11, "bold"),
                       bg=self.bg_color, fg=self.fg_color)
        lbl.pack(fill=tk.X)

        scrollbar = tk.Scrollbar(frame)  # vertical scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, wrap="none", yscrollcommand=scrollbar.set,
                       font=("consolas", 11), bg=self.text_bg, fg=self.text_fg,
                       insertbackground=self.fg_color)  # editor text
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)  # link scrollbar
        return text  # return the text editor widget

    def add_treeview(self, parent, label_text, columns, col_width):
        frame = tk.Frame(parent, bg=self.bg_color)  # frame for tree
        parent.add(frame, width=300)

        lbl = tk.Label(frame, text=label_text, font=("arial", 11, "bold"),
                       bg=self.bg_color, fg=self.fg_color)
        lbl.pack(fill=tk.X)

        tree_frame = tk.Frame(frame)  # inner frame for tree + scrollbars
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # scrollbars
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = tk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # treeview widget
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                            yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=col_width, anchor="w")
        tree.pack(fill=tk.BOTH, expand=True)

        vsb.config(command=tree.yview)  # link vertical scrollbar
        hsb.config(command=tree.xview)  # link horizontal scrollbar

        # tree style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=self.tree_bg,
                        fieldbackground=self.tree_bg,
                        foreground=self.tree_fg,
                        rowheight=20)
        style.map("Dark.Treeview",
                  background=[("selected", self.highlight)],
                  foreground=[("selected", "#ffffff")])
        tree.configure(style="Dark.Treeview")

        # for the alternating row colors
        tree.tag_configure("oddrow", background=self.tree_bg)
        tree.tag_configure("evenrow", background=self.tree_alt)

        return tree

    def add_console_section(self, parent):
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=False, pady=5)

        # execute the button
        btn = tk.Button(frame, text="execute", bg=self.highlight, fg="white",
                        font=("arial", 11, "bold"), padx=20, pady=5, command=self.execute)
        btn.pack(pady=(0, 5))

        # console output area
        console_frame = tk.Frame(frame)
        console_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(console_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.console = tk.Text(console_frame, height=8, bg=self.console_bg,
                               fg=self.console_fg, font=("consolas", 10),
                               state=tk.DISABLED, yscrollcommand=scrollbar.set,
                               insertbackground=self.fg_color)
        self.console.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.console.yview)

    # file operations
    def open_file(self):
        if self.has_unsaved_changes():  # check unsaved changes
            res = messagebox.askyesnocancel("unsaved changes", "save before opening another file?")
            if res: self.save_file()
            elif res is None: return  # cancel

        filename = filedialog.askopenfilename(filetypes=[("lolcode", "*.lol"), ("text", "*.txt")])
        if not filename: return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, content)  # insert file content
            self.current_file = filename
            self.original_content = content
            self.file_label.config(text=os.path.basename(filename))
            self.clear_tables()  # clear previous lexemes/symbols
            self.update_console(f"opened: {filename}")  # log open
        except Exception as e:
            messagebox.showerror("error", str(e))

    def save_file(self):
        if not self.current_file:  # if no file, use save as
            return self.save_file_as()

        try:
            content = self.text_editor.get(1.0, tk.END)
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.original_content = content  # update saved content
            messagebox.showinfo("saved", "file saved successfully!")
        except Exception as e:
            messagebox.showerror("error", str(e))

    def save_file_as(self):
        filename = filedialog.asksaveasfilename(defaultextension=".lol",
                                                filetypes=[("lolcode", "*.lol")])
        if filename:
            self.current_file = filename
            self.save_file()

    def has_unsaved_changes(self):
        current = self.text_editor.get(1.0, tk.END).strip()  # get current editor content
        return current != self.original_content.strip()  # compare with original

    # exercution
    def execute(self):
        code = self.text_editor.get(1.0, tk.END).strip()  # get current code
        if not code:
            self.update_console("no code to execute!\n")
            return

        try:
            self.tokens = tokenize_program(code)  # tokenize code
            symbol_table = symbolize(self.tokens)  # generate symbol table
            self.update_lexemes()  # update lexeme table
            self.update_symbols(symbol_table)  # update symbol table
            self.update_console(f"lexical analysis complete!\ntokens: {len(self.tokens)}\n")  # log
        except Exception as e:
            self.update_console(f"error: {e}\n")
            messagebox.showerror("error", str(e))

    # table updates
    def clear_tables(self):
        for tree in [self.lexemes_tree, self.symbol_tree]:  # clear all tables
            for item in tree.get_children():
                tree.delete(item)

    def update_lexemes(self):
        self.clear_tables()
        filtered = [t for t in self.tokens if t[1] != TokenType.LINEBREAK]  # skip linebreak tokens
        for i, (lexeme, token_type, _) in enumerate(filtered):
            tag = "evenrow" if i % 2 == 0 else "oddrow"  # alternate row
            desc = TOKEN_DESCRIPTIONS.get(token_type, token_type.value)  # get description
            self.lexemes_tree.insert("", tk.END, values=(lexeme, desc), tags=(tag,))

    def update_symbols(self, symbols):
        for i, (name, val) in enumerate(symbols.items()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.symbol_tree.insert("", tk.END, values=(name, val), tags=(tag,))

    # console
    def update_console(self, text):
        self.console.config(state=tk.NORMAL)
        if not text.endswith("\n"):  # ensure newline
            text += "\n"
        self.console.insert(tk.END, text)  # append text
        self.console.see(tk.END)  # scroll to end
        self.console.config(state=tk.DISABLED)

# main
if __name__ == "__main__":
    root = tk.Tk()
    LOLCodeInterpreterGUI(root)  # start gui
    root.mainloop()
