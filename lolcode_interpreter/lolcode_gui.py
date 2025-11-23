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
        
        # main content area
        main_container = tk.Frame(self.root, bg=self.header_bg)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # left sidebar container w/ collapse button
        left_container = tk.Frame(main_container, bg=self.header_bg)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # sidebarframe
        self.sidebar_container = tk.Frame(left_container, bg=self.sidebar_bg, width=540)
        self.sidebar_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # collapseible button
        collapse_btn_frame = tk.Frame(left_container, bg=self.sidebar_bg, width=30)
        collapse_btn_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.collapse_btn = tk.Button(collapse_btn_frame, text="◀", bg=self.sidebar_bg,
                                    fg="#7f8c8d", font=("Arial", 12, "bold"), border=0,
                                    activebackground="#dfe4ea", cursor="hand2",
                                    command=self.toggle_sidebar, relief=tk.FLAT)
        self.collapse_btn.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # create sidebar content
        self.create_sidebar(self.sidebar_container)
        
        # main paned window
        main_paned = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, sashwidth=3, bg="#34495e")
        main_paned.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # right side (editor and console)
        right_frame = tk.Frame(main_paned, bg=self.editor_bg)
        main_paned.add(right_frame)

        # vertical paned window for editor and console
        vertical_paned = tk.PanedWindow(right_frame, orient=tk.VERTICAL, sashwidth=3, bg="#34495e")
        vertical_paned.pack(fill=tk.BOTH, expand=True)

        # editor section
        self.create_editor_section(vertical_paned)

        # console section
        self.create_console_section(vertical_paned)

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
            # load and resize center logo
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
            print(f"Center logo error: {e}")
            import traceback
            traceback.print_exc() 
            logo_label = tk.Label(header, text="CUSTOM LOGO HERE", bg=self.header_bg,
                                fg="black", font=("Arial", 12, "bold"))

        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # right side subtitle image
        try:
            #lLoad and resize subtitle image
            subtitle_path = os.path.join(script_dir, "subtitle.png")
            pil_subtitle = Image.open(subtitle_path)
            
            # max_height
            max_height = 90  
            aspect_ratio = pil_subtitle.width / pil_subtitle.height
            new_height = max_height
            new_width = int(aspect_ratio * new_height)
            
            pil_subtitle = pil_subtitle.resize((new_width, new_height), Image.Resampling.LANCZOS)
            subtitle_img = ImageTk.PhotoImage(pil_subtitle)
            self.subtitle_img = subtitle_img
            subtitle_label = tk.Label(header, image=subtitle_img, bg=self.header_bg)
        except Exception as e:
            print(f"Subtitle image error: {e}")
            subtitle_label = tk.Label(header, text="OH HAI! I'M YR Interpreter!", bg=self.header_bg,
                                    fg="black", font=("Arial", 11))

        subtitle_label.pack(side=tk.RIGHT, padx=20)

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_container.pack_forget()
            self.collapse_btn.config(text="▶")
        else:
            self.sidebar_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, before=self.collapse_btn.master)
            self.collapse_btn.config(text="◀")
        self.sidebar_visible = not self.sidebar_visible

    def create_sidebar(self, parent):
        # top padding frame (for margin)
        top_margin = tk.Frame(parent, bg=self.sidebar_bg, height=10)
        top_margin.pack(fill=tk.X, side=tk.TOP)
        
        # container for notebook
        notebook_container = tk.Frame(parent, bg=self.sidebar_bg)
        notebook_container.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=0)
        
        # botebook for tabs
        style = ttk.Style()
        style.theme_use('default')
        
        # remove borders and fill width
        style.configure('Custom.TNotebook',
                    background=self.sidebar_bg,
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
        
        # change tabs to fill width and use proper colors
        style.configure('Custom.TNotebook.Tab',
                    background='#c8ff00',  # if unselected
                    foreground='#000000',
                    padding=[100, 12],  
                    font=('Arial', 11, 'bold'),
                    borderwidth=0,
                    focuscolor='none')
        
        style.map('Custom.TNotebook.Tab',
                background=[('selected', '#a8d000'), ('active', '#b8ef00')],  # when selected
                foreground=[('selected', '#000000')])
        
        # remove the white border between tabs
        style.layout('Custom.TNotebook.Tab', [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])
        
        # configure pane to remove gaps
        style.configure('Custom.TNotebook', tabmargins=0, relief='flat')
        
        notebook = ttk.Notebook(notebook_container, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # lexemes tab
        lexemes_frame = tk.Frame(notebook, bg=self.sidebar_bg)
        notebook.add(lexemes_frame, text='Lexemes')
        self.lexemes_tree = self.create_table(lexemes_frame, ["Lexeme", "Classification"])
        
        # symbol table tab
        symbols_frame = tk.Frame(notebook, bg=self.sidebar_bg)
        notebook.add(symbols_frame, text='Symbol Table')
        self.symbol_tree = self.create_table(symbols_frame, ["Identifier", "Value"])

    def create_table(self, parent, columns):
        container = tk.Frame(parent, bg=self.sidebar_bg)
        container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # header frame with custom height
        header_container = tk.Frame(container, bg=self.sidebar_bg)
        header_container.pack(fill=tk.X, padx=0, pady=0)
        
        header_frame = tk.Frame(header_container, bg=self.table_header, height=40)
        header_frame.pack(fill=tk.BOTH, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # column headers
        for i, col in enumerate(columns):
            header_label = tk.Label(header_frame, text=col, bg=self.table_header,
                                fg="white", font=('Arial', 10, 'bold'), anchor='center')
            header_label.place(relx=i/len(columns), rely=0, relwidth=1/len(columns), relheight=1)
        
        # table content frame 
        table_frame = tk.Frame(container, bg=self.sidebar_bg)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        # inner white frame for content
        content_frame = tk.Frame(table_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # scrollbar
        vsb = tk.Scrollbar(content_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (without headings since we made custom ones)
        tree = ttk.Treeview(content_frame, columns=columns, show="tree",
                        yscrollcommand=vsb.set, selectmode='none')
        tree['show'] = ''  # hide tree column
        
        for col in columns:
            tree.column(col, width=250, anchor="w")
        
        tree.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=tree.yview)
        
        # no no clicking
        tree.bind("<Button-1>", lambda e: "break")
        tree.bind("<ButtonRelease-1>", lambda e: "break")
        
        # styling for tables
        style = ttk.Style()
        style.configure("Light.Treeview",
                    background="white",
                    fieldbackground="white",
                    foreground="#2c3e50",
                    rowheight=25,
                    borderwidth=0)
        
        style.map("Light.Treeview",
                background=[("selected", "white")],
                foreground=[("selected", "#2c3e50")])
        
        tree.configure(style="Light.Treeview")
        
        # for alternating row colors
        tree.tag_configure("oddrow", background="#f8f9fa")
        tree.tag_configure("evenrow", background="white")
        
        return tree
    
    def create_editor_section(self, parent):
        editor_frame = tk.Frame(parent, bg=self.editor_bg)
        parent.add(editor_frame, height=500)
        
        # file tabs container
        tabs_container = tk.Frame(editor_frame, bg=self.editor_bg)
        tabs_container.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # scrollable tabs frame
        tabs_canvas = tk.Canvas(tabs_container, bg=self.editor_bg, height=35, highlightthickness=0)
        tabs_scrollbar = tk.Scrollbar(tabs_container, orient="horizontal", command=tabs_canvas.xview)
        self.tabs_frame = tk.Frame(tabs_canvas, bg=self.editor_bg)
        
        tabs_canvas.create_window((0, 0), window=self.tabs_frame, anchor="nw")
        tabs_canvas.configure(xscrollcommand=tabs_scrollbar.set)
        
        tabs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tabs_frame.bind("<Configure>", lambda e: tabs_canvas.configure(scrollregion=tabs_canvas.bbox("all")))
        self.tabs_canvas = tabs_canvas
        
        # file button
        new_file_btn = tk.Button(self.tabs_frame, text="+", bg="#34495e", fg="white",
                                font=("Arial", 12, "bold"), padx=10, pady=2,
                                border=0, command=self.new_file, cursor="hand2",
                                activebackground="#4a5f7a")
        new_file_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # run code button
        run_btn = tk.Button(tabs_container, text="▶ Run Code", bg=self.accent_yellow,
                        fg="#2c3e50", font=("Arial", 11, "bold"), padx=15, pady=5,
                        border=0, command=self.execute, cursor="hand2",
                        activebackground="#c4ef00")
        run_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # editor container with line numbers
        editor_container = tk.Frame(editor_frame, bg=self.editor_bg)
        editor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # line numbers
        self.line_numbers = tk.Text(editor_container, width=5, bg=self.editor_bg,
                                    fg="#4a5f7a", font=("Consolas", 10), state=tk.DISABLED,
                                    padx=10, pady=5, borderwidth=0, highlightthickness=0,
                                    spacing1=0, spacing3=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.line_numbers.tag_configure("right", justify="right")
        
        # scrollbar
        scrollbar = tk.Scrollbar(editor_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # container for text editor
        self.editors_container = tk.Frame(editor_container, bg=self.editor_bg)
        self.editors_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_console_section(self, parent):
        console_frame = tk.Frame(parent, bg=self.console_bg)
        parent.add(console_frame, height=200)
        
        # console header
        console_header = tk.Label(console_frame, text="LOLCode Shell", bg=self.console_bg,
                                fg="#7f8c8d", font=("Consolas", 9, "bold"),
                                anchor="w", padx=15, pady=5)
        console_header.pack(fill=tk.X)
        
        # console text area
        console_container = tk.Frame(console_frame, bg=self.console_bg)
        console_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        console_scroll = tk.Scrollbar(console_container)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.console = tk.Text(console_container, bg=self.console_bg, fg=self.console_text,
                            font=("Consolas", 9), state=tk.DISABLED,
                            yscrollcommand=console_scroll.set, borderwidth=0,
                            highlightthickness=0, padx=5, pady=5)
        self.console.pack(fill=tk.BOTH, expand=True)
        console_scroll.config(command=self.console.yview)

    def new_file(self):
        tab_id = "untitled_tab"
        
        # if untitled tab already exists, just switch to it
        if tab_id in self.open_files:
            self.switch_tab(tab_id)
            return
        
        # create text editor
        text_editor = tk.Text(self.editors_container, wrap="none",
                            yscrollcommand=self.on_text_scroll,
                            font=("Consolas", 10), bg=self.editor_bg,
                            fg=self.editor_text, insertbackground="white",
                            padx=5, pady=5, borderwidth=0, highlightthickness=0,
                            selectbackground="#3498db", spacing1=0, spacing3=0)
        
        # bind events
        text_editor.bind("<KeyRelease>", self.update_line_numbers)
        text_editor.bind("<MouseWheel>", self.on_mousewheel)
        text_editor.bind("<ButtonRelease-1>", self.update_line_numbers)
        
        # store file info
        self.open_files[tab_id] = {
            'path': None,
            'content': '',
            'widget': text_editor,
            'original': '',
            'button': None
        }
        
        # create tab button
        self.create_tab_button(tab_id, "Untitled")
        
        # switch to new tab
        self.switch_tab(tab_id)

    def create_tab_button(self, tab_id, display_name):
        tab_frame = tk.Frame(self.tabs_frame, bg="#34495e")
        tab_frame.pack(side=tk.LEFT, padx=2)
        
        # tab button
        tab_btn = tk.Button(tab_frame, text=display_name, bg="#34495e", fg="white",
                        font=("Consolas", 9), padx=12, pady=5, border=0,
                        cursor="hand2", activebackground="#4a5f7a",
                        command=lambda: self.switch_tab(tab_id))
        tab_btn.pack(side=tk.LEFT)
        
        # cose button
        close_btn = tk.Button(tab_frame, text="×", bg="#34495e", fg="#95a5a6",
                            font=("Arial", 12, "bold"), padx=5, pady=0, border=0,
                            cursor="hand2", activebackground="#e74c3c",
                            activeforeground="white",
                            command=lambda: self.close_tab(tab_id))
        close_btn.pack(side=tk.LEFT)
        
        self.open_files[tab_id]['button'] = tab_btn
        self.open_files[tab_id]['tab_frame'] = tab_frame

    def switch_tab(self, tab_id):
        if tab_id not in self.open_files:
            return
        
        # save current tab content
        if self.current_tab_id and self.current_tab_id in self.open_files:
            current_widget = self.open_files[self.current_tab_id]['widget']
            self.open_files[self.current_tab_id]['content'] = current_widget.get(1.0, tk.END)
            current_widget.pack_forget()
            # reset button color
            self.open_files[self.current_tab_id]['button'].config(bg="#34495e")
        
        # show new tab
        self.current_tab_id = tab_id
        new_widget = self.open_files[tab_id]['widget']
        new_widget.pack(fill=tk.BOTH, expand=True)
        
        # highlight active tab
        self.open_files[tab_id]['button'].config(bg="#4a5f7a")
        
        # update line numbers
        self.update_line_numbers()
        
        # configure scrollbar
        scrollbar = self.editors_container.master.children.get('!scrollbar')
        if scrollbar:
            scrollbar.config(command=new_widget.yview)
            new_widget.config(yscrollcommand=self.on_text_scroll)

    def close_tab(self, tab_id):
        if tab_id not in self.open_files:
            return
        
        # check for unsaved changes
        file_info = self.open_files[tab_id]
        current_content = file_info['widget'].get(1.0, tk.END).strip()
        if current_content != file_info['original'].strip():
            filename = file_info['path'] if file_info['path'] else "Untitled"
            res = messagebox.askyesnocancel("Unsaved Changes",
                                        f"Save changes to {os.path.basename(filename)}?")
            if res:
                old_tab = self.current_tab_id
                self.current_tab_id = tab_id
                self.save_file()
                self.current_tab_id = old_tab
            elif res is None:
                return
        
        # remove tab
        file_info['widget'].destroy()
        file_info['tab_frame'].destroy()
        del self.open_files[tab_id]
        
        # switch to another tab or clear editor
        if self.current_tab_id == tab_id:
            if self.open_files:
                self.switch_tab(list(self.open_files.keys())[0])
            else:
                # No tabs left, clear everything
                self.current_tab_id = None
                self.line_numbers.config(state=tk.NORMAL)
                self.line_numbers.delete("1.0", tk.END)
                self.line_numbers.config(state=tk.DISABLED)

    def close_current_tab(self):
        if self.current_tab_id:
            self.close_tab(self.current_tab_id)

    def execute(self):
        print("Execute clicked")

    def update_line_numbers(self, event=None):
        if not self.current_tab_id or self.current_tab_id not in self.open_files:
            return
        
        text_editor = self.open_files[self.current_tab_id]['widget']
        
        # get line count from text widget
        line_count = int(text_editor.index('end-1c').split('.')[0])
        
        # generate line numbers
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
        # update line numbers with right alignment
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", line_numbers_string, "right")
        self.line_numbers.config(state=tk.DISABLED)
        
        # sync scroll position
        self.line_numbers.yview_moveto(text_editor.yview()[0])

    def on_text_scroll(self, *args):
        if not self.current_tab_id:
            return
        # sync line numbers when text editor scrolls
        self.line_numbers.yview_moveto(float(args[0]))
        # update scrollbar
        scrollbar = self.editors_container.master.children.get('!scrollbar')
        if scrollbar:
            scrollbar.set(*args)

    def on_scrollbar(self, *args):
        if not self.current_tab_id:
            return
        text_editor = self.open_files[self.current_tab_id]['widget']
        # scroll both text editor and line numbers
        text_editor.yview(*args)
        self.line_numbers.yview(*args)

    def on_mousewheel(self, event):
        if not self.current_tab_id:
            return "break"
        text_editor = self.open_files[self.current_tab_id]['widget']
        # handle mousewheel scrolling
        text_editor.yview_scroll(int(-1*(event.delta/120)), "units")
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def save_file(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    LOLCodeInterpreterGUI(root)
    root.mainloop()