import os
import tkinter as tk
from tkinter import ttk, messagebox
import encryptutils
import passutils

'''
This module implements the primary Graphical User Interface (GUI) for the Secure Password Manager application.
It provides screens for setup, unlocking, searching, adding, editing, deleting, copying, and migrating vault records.
'''

class PasswordManagerGUI:
    def __init__(self, root):
        '''
        This constructor initializes the primary window settings, default directories,
        color palette style configurations, state variables, and initiates the authentication state check.
        '''
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("850x550")
        self.root.minsize(750, 480)
        
        # Ensure VAULT directory exists
        if not os.path.exists("VAULT"):
            os.makedirs("VAULT")
            
        self.master_key = "" # Hashed master password used for encryption/decryption
        
        # Define Color Palette (Modern Deep Blue / Slate Dark Theme)
        self.colors = {
            "bg": "#1e272e",          # Dark Slate Charcoal
            "sidebar": "#2f3640",     # Deep Slate Gray
            "card": "#1c222b",        # Inner Card Dark Gray
            "accent": "#00a8ff",      # Vibrant Cyan
            "accent_hover": "#0097e6",# Darker Cyan
            "text": "#f5f6fa",        # Off-white
            "text_dim": "#a4b0be",    # Muted Gray
            "success": "#4cd137",     # Pastel Green
            "success_hover": "#44bd32",
            "danger": "#e84118",      # Pastel Red
            "danger_hover": "#c23616"
        }
        
        # Apply window background color
        self.root.configure(bg=self.colors["bg"])
        
        # Apply standard style configurations for TTK components
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()
        
        # Initialize GUI state variables
        self.current_records = []
        self.selected_record = None
        self.show_password_var = tk.BooleanVar(value=False)
        self.edit_mode_var = tk.BooleanVar(value=False)
        
        # Construct primary frame container
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True)
        
        # Validate current master password file state
        self.check_auth_state()
        
    def configure_styles(self):
        '''
        This function configures style properties for ttk components such as Frames and Scrollbars.
        '''
        # Configure TFrame and other container elements with theme colors
        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("Sidebar.TFrame", background=self.colors["sidebar"])
        self.style.configure("Card.TFrame", background=self.colors["card"])
        
        # Scrollbar custom design (use standard Scrollbar with colored components)
        self.style.configure("TScrollbar", background=self.colors["sidebar"], troughcolor=self.colors["bg"])
        
    def create_button(self, parent, text, command, bg_key="accent", fg_key="text", hover_key=None, font=("Segoe UI", 10, "bold"), **kwargs):
        '''
        This function creates and returns a highly styled flat button with custom hover event listeners.
        '''
        # Determine background and foreground colors from theme palette
        bg = self.colors.get(bg_key, bg_key)
        fg = self.colors.get(fg_key, fg_key)
        
        # Automatic hover key determination based on standard conventions
        if hover_key is None:
            hover_key = f"{bg_key}_hover" if f"{bg_key}_hover" in self.colors else bg_key
        hover_bg = self.colors.get(hover_key, hover_key)
        
        # Instantiate flat tkinter Button
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            font=font,
            bd=0,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            **kwargs
        )
        
        # Bind dynamic hover animation effects
        def on_enter(e):
            if btn['state'] != "disabled":
                btn.config(bg=hover_bg)
        def on_leave(e):
            if btn['state'] != "disabled":
                btn.config(bg=bg)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def check_auth_state(self):
        '''
        This function examines the current authentication state of the vault to verify if a master password exists and is populated, routing the interface accordingly.
        '''
        # Clear the main container widgets
        for widget in self.container.winfo_children():
            widget.destroy()
            
        has_master = passutils.find_MASTERPASS("VAULT")
        
        # Check if the master password file contains non-empty contents
        is_empty = True
        if has_master:
            with open("VAULT/MASTERPASS.txt", "r") as f:
                if f.read().strip() != "":
                    is_empty = False
                    
        # Route to appropriate setup or unlock screen
        if not has_master or is_empty:
            self.show_setup_screen()
        else:
            self.show_unlock_screen()
            
    def show_setup_screen(self):
        '''
        This function renders the initial setup screen, prompting the user to define and confirm a master password.
        '''
        # Place the main form centered in the container
        setup_frame = tk.Frame(self.container, bg=self.colors["bg"])
        setup_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title and description labels
        title_lbl = tk.Label(setup_frame, text="Setup Master Password", font=("Segoe UI", 18, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        title_lbl.pack(pady=(0, 10))
        
        desc_lbl = tk.Label(
            setup_frame, 
            text="Welcome! Create a master password to initialize your password vault.\nThis password will be used to encrypt all your credentials.",
            font=("Segoe UI", 10), 
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            justify="center"
        )
        desc_lbl.pack(pady=(0, 20))
        
        # Password entry field
        pass_lbl = tk.Label(setup_frame, text="Enter Master Password:", font=("Segoe UI", 10, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"])
        pass_lbl.pack(anchor="w", pady=(0, 5))
        
        pass_entry = tk.Entry(setup_frame, font=("Segoe UI", 12), show="*", width=32, bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        pass_entry.pack(pady=(0, 15))
        pass_entry.focus()
        
        # Confirm password entry field
        confirm_lbl = tk.Label(setup_frame, text="Confirm Master Password:", font=("Segoe UI", 10, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"])
        confirm_lbl.pack(anchor="w", pady=(0, 5))
        
        confirm_entry = tk.Entry(setup_frame, font=("Segoe UI", 12), show="*", width=32, bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        confirm_entry.pack(pady=(0, 20))
        
        # Show/Hide toggle variable and callback function
        show_pass = tk.BooleanVar(value=False)
        def toggle_pass_visibility():
            char = "" if show_pass.get() else "*"
            pass_entry.config(show=char)
            confirm_entry.config(show=char)
            
        show_cb = tk.Checkbutton(
            setup_frame, 
            text="Show Passwords", 
            variable=show_pass, 
            command=toggle_pass_visibility,
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            bd=0,
            highlightthickness=0
        )
        show_cb.pack(anchor="w", pady=(0, 15))
        
        # Handle verification, hashing, and submission of setup details
        def handle_setup():
            pw = pass_entry.get()
            cpw = confirm_entry.get()
            
            if not pw:
                messagebox.showerror("Error", "Password cannot be empty.", parent=self.root)
                return
            if pw != cpw:
                messagebox.showerror("Error", "Passwords do not match.", parent=self.root)
                return
                
            # Create master password by hashing input
            hashed_pw = encryptutils.hash_(pw)
            with open("VAULT/MASTERPASS.txt", "w") as f:
                f.write(str(hashed_pw))
                
            messagebox.showinfo("Success", "Master password set successfully!", parent=self.root)
            self.check_auth_state()
            
        # Submission button
        setup_btn = self.create_button(setup_frame, "Create Master Password", handle_setup, font=("Segoe UI", 11, "bold"))
        setup_btn.pack(fill="x")
        
        # Keyboard navigation/bindings for easy access
        pass_entry.bind("<Return>", lambda e: handle_setup())
        confirm_entry.bind("<Return>", lambda e: handle_setup())

    def show_unlock_screen(self):
        '''
        This function displays the vault unlock screen, prompting the user for their master password.
        '''
        # Place unlock widgets container in center
        unlock_frame = tk.Frame(self.container, bg=self.colors["bg"])
        unlock_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Visual key icon and introductory messages
        logo_lbl = tk.Label(unlock_frame, text="🔑", font=("Segoe UI", 48), bg=self.colors["bg"], fg=self.colors["accent"])
        logo_lbl.pack(pady=(0, 10))
        
        title_lbl = tk.Label(unlock_frame, text="Unlock Vault", font=("Segoe UI", 18, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        title_lbl.pack(pady=(0, 5))
        
        desc_lbl = tk.Label(
            unlock_frame, 
            text="Enter your master password to decrypt your secure credentials.",
            font=("Segoe UI", 9), 
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"]
        )
        desc_lbl.pack(pady=(0, 20))
        
        # Password entry field
        pass_lbl = tk.Label(unlock_frame, text="Master Password:", font=("Segoe UI", 10, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"])
        pass_lbl.pack(anchor="w", pady=(0, 5))
        
        pass_entry = tk.Entry(unlock_frame, font=("Segoe UI", 12), show="*", width=32, bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        pass_entry.pack(pady=(0, 10))
        pass_entry.focus()
        
        # Show password checkbox controls
        show_pass = tk.BooleanVar(value=False)
        def toggle_pass_visibility():
            char = "" if show_pass.get() else "*"
            pass_entry.config(show=char)
            
        show_cb = tk.Checkbutton(
            unlock_frame, 
            text="Show Password", 
            variable=show_pass, 
            command=toggle_pass_visibility,
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            bd=0,
            highlightthickness=0
        )
        show_cb.pack(anchor="w", pady=(0, 15))
        
        # Verification, hashing match, and routing handler
        def handle_unlock():
            pw = pass_entry.get()
            if not pw:
                messagebox.showerror("Error", "Password cannot be empty.", parent=self.root)
                return
                
            hashed_input = encryptutils.hash_(pw)
            
            with open("VAULT/MASTERPASS.txt", "r") as f:
                saved_pw = f.read().strip()
                
            if hashed_input == saved_pw:
                # Key used for encryption is the string content of MASTERPASS.txt (which matches hashed_input)
                self.master_key = hashed_input
                self.show_main_dashboard()
            else:
                messagebox.showerror("Error", "Incorrect master password. Please try again.", parent=self.root)
                pass_entry.delete(0, tk.END)
                pass_entry.focus()
                
        # Unlock submission button
        unlock_btn = self.create_button(unlock_frame, "Unlock", handle_unlock, font=("Segoe UI", 11, "bold"))
        unlock_btn.pack(fill="x")
        
        # Return key bindings for rapid input
        pass_entry.bind("<Return>", lambda e: handle_unlock())

    def show_main_dashboard(self):
        '''
        This function renders the main workspace layout, partitioning the dashboard into sidebar navigation and detail display panels.
        '''
        # Clear container before building dashboard layout
        for widget in self.container.winfo_children():
            widget.destroy()
            
        # Left sidebar pane (fixed-width, deep slate grey background)
        self.sidebar = tk.Frame(self.container, bg=self.colors["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Keep width fixed
        
        # Right detail pane for showing credentials
        self.detail_pane = tk.Frame(self.container, bg=self.colors["bg"])
        self.detail_pane.pack(side="right", fill="both", expand=True)
        
        # Assemble sub-components
        self.build_sidebar()
        self.show_welcome_detail()

    def build_sidebar(self):
        '''
        This function constructs the left sidebar interface, including search, file listing, and control buttons.
        '''
        # Header/App Title in Sidebar
        sb_header = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        sb_header.pack(fill="x", padx=15, pady=15)
        
        logo_lbl = tk.Label(sb_header, text="🛡️ Passmanage", font=("Segoe UI", 14, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"])
        logo_lbl.pack(side="left")
        
        # Search panel and interactive string trace setup
        search_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_records())
        
        search_lbl = tk.Label(search_frame, text="Search Records:", font=("Segoe UI", 9, "bold"), bg=self.colors["sidebar"], fg=self.colors["text_dim"])
        search_lbl.pack(anchor="w", pady=(0, 2))
        
        self.search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=("Segoe UI", 10), 
            bg=self.colors["bg"], 
            fg="#ffffff", 
            bd=1, 
            relief="solid",
            insertbackground="white"
        )
        self.search_entry.pack(fill="x")
        
        # List of records container with custom scrollbars
        list_lbl = tk.Label(self.sidebar, text="VAULT RECORDS:", font=("Segoe UI", 9, "bold"), bg=self.colors["sidebar"], fg=self.colors["text_dim"])
        list_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        
        list_container = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        list_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.record_listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.record_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar mapping for navigating the record listbox
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.record_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.record_listbox.config(yscrollcommand=scrollbar.set)
        
        # Select record click listener binding
        self.record_listbox.bind("<<ListboxSelect>>", self.on_record_selected)
        
        # Action Buttons frame configuration at the bottom of the sidebar
        btn_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        add_btn = self.create_button(btn_frame, "+ Add New Password", self.show_add_record_dialog, bg_key="success", hover_key="success")
        add_btn.pack(fill="x", pady=(0, 8))
        
        settings_btn = self.create_button(btn_frame, "⚙️ Change Master Password", self.show_change_master_dialog, bg_key="sidebar", fg_key="text_dim", hover_key="bg")
        settings_btn.pack(fill="x")
        
        # Populate initial list of directories in vault
        self.refresh_records_list()

    def refresh_records_list(self):
        '''
        This function queries the password storage directory to synchronize the interface with the actual filesystem contents.
        '''
        # Fetch current record directory array from helper utils
        self.current_records = passutils.return_records("VAULT")
        self.filter_records()
        
    def filter_records(self):
        '''
        This function filters list items based on matching criteria from the search query entry box.
        '''
        search_term = self.search_var.get().lower().strip()
        self.record_listbox.delete(0, tk.END)
        
        # Populate matching records alphabetically
        for record in sorted(self.current_records, key=lambda s: s.lower()):
            if search_term in record.lower():
                self.record_listbox.insert(tk.END, record)

    def show_welcome_detail(self):
        '''
        This function renders the default workspace welcome screen displayed when no specific record is selected.
        '''
        # Clear right detail pane
        for widget in self.detail_pane.winfo_children():
            widget.destroy()
            
        welcome_frame = tk.Frame(self.detail_pane, bg=self.colors["bg"])
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Render visual decorative widgets
        logo_lbl = tk.Label(welcome_frame, text="🛡️", font=("Segoe UI", 48), bg=self.colors["bg"], fg=self.colors["accent"])
        logo_lbl.pack(pady=(0, 10))
        
        welcome_lbl = tk.Label(
            welcome_frame, 
            text="Passmanage Unlocked", 
            font=("Segoe UI", 16, "bold"), 
            bg=self.colors["bg"], 
            fg=self.colors["text"]
        )
        welcome_lbl.pack(pady=(0, 5))
        
        hint_lbl = tk.Label(
            welcome_frame, 
            text="Select a password record from the left-hand sidebar\nto securely decrypt, copy, or edit its fields.", 
            font=("Segoe UI", 10), 
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            justify="center"
        )
        hint_lbl.pack()

    def load_record_details(self, record_name):
        '''
        This function loads metadata and content attributes of a single credential record from storage.
        '''
        filepath = f"VAULT/{record_name}/{record_name}.txt"
        if not os.path.exists(filepath):
            return None, None, None
            
        # Parse credential fields row by row
        with open(filepath, "r") as f:
            lines = f.readlines()
            
        title = ""
        username = ""
        encrypted_pass = ""
        
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("Title:"):
                title = line_str[len("Title:"):].strip()
            elif line_str.startswith("Username:"):
                username = line_str[len("Username:"):].strip()
            elif line_str.startswith("Password:"):
                encrypted_pass = line_str[len("Password:"):].strip()
                
        return title, username, encrypted_pass

    def on_record_selected(self, event):
        '''
        This function handles the listbox selection event, initiating decryption and viewing protocols for the target record.
        '''
        selection = self.record_listbox.curselection()
        if not selection:
            return
            
        # Retrieve target record name from listbox selection
        record_name = self.record_listbox.get(selection[0])
        self.selected_record = record_name
        self.show_record_detail(record_name)

    def show_record_detail(self, record_name):
        '''
        This function builds and displays details (Title, Username, Password) for a specific record inside the main workspace view pane.
        '''
        # Clear details container pane
        for widget in self.detail_pane.winfo_children():
            widget.destroy()
            
        title, username, encrypted_pass = self.load_record_details(record_name)
        if title is None:
            messagebox.showerror("Error", f"Could not load file for '{record_name}'", parent=self.root)
            self.show_welcome_detail()
            return
            
        # Decrypt password using stored master_key (which is the hashed key)
        try:
            decrypted_pass = encryptutils.decrypt(self.master_key, encrypted_pass)
        except Exception as e:
            decrypted_pass = "[Decryption Failure]"
            
        # Initialize viewing states
        self.show_password_var.set(False)
        self.edit_mode_var.set(False)
        
        # Detail view frame layout
        detail_container = tk.Frame(self.detail_pane, bg=self.colors["bg"])
        detail_container.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Card Header widgets
        title_frame = tk.Frame(detail_container, bg=self.colors["bg"])
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_icon = tk.Label(title_frame, text="🔒", font=("Segoe UI", 20), bg=self.colors["bg"])
        title_icon.pack(side="left", padx=(0, 10))
        
        self.title_label_val = tk.Label(title_frame, text=title, font=("Segoe UI", 18, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        self.title_label_val.pack(side="left")
        
        # Styled Inner Display Card container
        grid_frame = tk.Frame(detail_container, bg=self.colors["card"], bd=1, relief="solid")
        grid_frame.pack(fill="x", pady=(0, 20), padx=2)
        
        card_inner = tk.Frame(grid_frame, bg=self.colors["card"])
        card_inner.pack(fill="both", expand=True, padx=20, pady=20)
        card_inner.columnconfigure(1, weight=1)
        
        # --- Username Row ---
        u_lbl = tk.Label(card_inner, text="USERNAME", font=("Segoe UI", 9, "bold"), bg=self.colors["card"], fg=self.colors["text_dim"])
        u_lbl.grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        self.username_entry = tk.Entry(
            card_inner, 
            font=("Segoe UI", 11), 
            bg=self.colors["sidebar"], 
            fg="#ffffff", 
            bd=1, 
            relief="solid", 
            state="disabled",
            disabledbackground=self.colors["card"],
            disabledforeground=self.colors["text"],
            insertbackground="white"
        )
        self.username_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 15))
        self.username_entry.config(state="normal")
        self.username_entry.insert(0, username)
        self.username_entry.config(state="disabled")
        
        # Copy Username button trigger
        copy_u_btn = self.create_button(
            card_inner, "📋 Copy", 
            lambda: self.copy_to_clipboard(self.username_entry.get(), "Username"),
            bg_key="sidebar", fg_key="text_dim", hover_key="bg", font=("Segoe UI", 9, "bold")
        )
        copy_u_btn.grid(row=1, column=2, sticky="e", pady=(0, 15))
        
        # --- Password Row ---
        p_lbl = tk.Label(card_inner, text="PASSWORD", font=("Segoe UI", 9, "bold"), bg=self.colors["card"], fg=self.colors["text_dim"])
        p_lbl.grid(row=2, column=0, sticky="w", pady=(0, 2))
        
        self.password_entry = tk.Entry(
            card_inner, 
            font=("Segoe UI", 11), 
            bg=self.colors["sidebar"], 
            fg="#ffffff", 
            bd=1, 
            relief="solid", 
            show="*",
            state="disabled",
            disabledbackground=self.colors["card"],
            disabledforeground=self.colors["text"],
            insertbackground="white"
        )
        self.password_entry.grid(row=3, column=1, sticky="ew", padx=(0, 10))
        self.password_entry.config(state="normal")
        self.password_entry.insert(0, decrypted_pass)
        self.password_entry.config(state="disabled")
        
        # Password view/copy control buttons
        p_controls = tk.Frame(card_inner, bg=self.colors["card"])
        p_controls.grid(row=3, column=2, sticky="e")
        
        # Toggle password characters display callback
        def toggle_pw():
            if self.show_password_var.get():
                self.password_entry.config(show="*")
                self.show_password_var.set(False)
                show_p_btn.config(text="👁️ Show")
            else:
                self.password_entry.config(show="")
                self.show_password_var.set(True)
                show_p_btn.config(text="👁️ Hide")
                
        show_p_btn = self.create_button(
            p_controls, "👁️ Show", 
            toggle_pw,
            bg_key="sidebar", fg_key="text_dim", hover_key="bg", font=("Segoe UI", 9, "bold")
        )
        show_p_btn.pack(side="left", padx=(0, 5))
        
        copy_p_btn = self.create_button(
            p_controls, "📋 Copy", 
            lambda: self.copy_to_clipboard(self.password_entry.get(), "Password"),
            bg_key="sidebar", fg_key="text_dim", hover_key="bg", font=("Segoe UI", 9, "bold")
        )
        copy_p_btn.pack(side="left")
        
        # Action Buttons container (Edit / Delete)
        self.actions_frame = tk.Frame(detail_container, bg=self.colors["bg"])
        self.actions_frame.pack(fill="x", pady=10)
        
        self.show_standard_actions(record_name)

    def show_standard_actions(self, record_name):
        '''
        This function renders the default set of control buttons (Edit and Delete) available for a displayed credential record.
        '''
        # Clear action layout container
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
            
        edit_btn = self.create_button(
            self.actions_frame, "✏️ Edit Record", 
            lambda: self.enable_edit_mode(record_name),
            bg_key="accent", hover_key="accent_hover"
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = self.create_button(
            self.actions_frame, "🗑️ Delete Record", 
            lambda: self.delete_record(record_name),
            bg_key="danger", hover_key="danger_hover"
        )
        delete_btn.pack(side="left")
        
    def show_edit_actions(self, record_name):
        '''
        This function displays action controls (Save and Cancel) when a record's interactive fields are in edit mode.
        '''
        # Clear action layout container
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
            
        save_btn = self.create_button(
            self.actions_frame, "💾 Save Changes", 
            lambda: self.save_record_edits(record_name),
            bg_key="success", hover_key="success"
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = self.create_button(
            self.actions_frame, "❌ Cancel", 
            lambda: self.disable_edit_mode(record_name),
            bg_key="sidebar", hover_key="bg"
        )
        cancel_btn.pack(side="left")

    def enable_edit_mode(self, record_name):
        '''
        This function unlocks individual record fields for direct user input edits and exposes active editing control buttons.
        '''
        self.edit_mode_var.set(True)
        
        # Make entry widgets interactive and visible
        self.username_entry.config(state="normal", bg=self.colors["sidebar"])
        self.password_entry.config(state="normal", bg=self.colors["sidebar"])
        
        # Force password visibility during active edit session
        self.password_entry.config(show="")
        self.show_password_var.set(True)
        
        self.show_edit_actions(record_name)
        
    def disable_edit_mode(self, record_name):
        '''
        This function disables direct inputs and discards any uncommitted field values by reloading original values.
        '''
        self.edit_mode_var.set(False)
        self.show_record_detail(record_name) # Discards modifications by reloading details

    def save_record_edits(self, record_name):
        '''
        This function validates modifications, re-encrypts the target credential, and writes back updated values to storage.
        '''
        new_user = self.username_entry.get().strip()
        new_pass = self.password_entry.get()
        
        # Validate input entries are not empty
        if not new_user:
            messagebox.showerror("Error", "Username cannot be empty.", parent=self.root)
            return
        if not new_pass:
            messagebox.showerror("Error", "Password cannot be empty.", parent=self.root)
            return
            
        filepath = f"VAULT/{record_name}/{record_name}.txt"
        
        # Load existing file lines if file already exists
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                lines = f.readlines()
        else:
            lines = [f"Title: {record_name} \n", "Username: \n", "Password: \n"]
            
        # Align lines layout
        while len(lines) < 3:
            lines.append("\n")
            
        lines[0] = f"Title: {record_name} \n"
        lines[1] = f"Username: {new_user}\n"
        
        # Re-encrypt utilizing stored master_key string
        encrypted_new_pass = encryptutils.encrypt(self.master_key, new_pass)
        lines[2] = f"Password: {encrypted_new_pass}\n"
        
        # Write updated text elements back to filesystem
        try:
            with open(filepath, "w") as f:
                for line in lines:
                    f.write(line)
                    
            messagebox.showinfo("Success", "Password record updated successfully!", parent=self.root)
            self.edit_mode_var.set(False)
            self.show_record_detail(record_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record changes: {e}", parent=self.root)

    def delete_record(self, record_name):
        '''
        This function handles deletion workflow, confirming intent and purging corresponding file directories from storage.
        '''
        # Request double confirmation before permanent deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to permanently delete the password record '{record_name}'?\nThis action cannot be undone.",
            parent=self.root
        )
        if not confirm:
            return
            
        filepath = f"VAULT/{record_name}/{record_name}.txt"
        folderpath = f"VAULT/{record_name}"
        
        # Perform deletions of folders and credential text files
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            if os.path.exists(folderpath):
                os.rmdir(folderpath)
                
            messagebox.showinfo("Deleted", f"Record '{record_name}' successfully deleted.", parent=self.root)
            self.refresh_records_list()
            self.show_welcome_detail()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}", parent=self.root)

    def show_add_record_dialog(self):
        '''
        This function presents a modal dialog prompt for initiating and saving new credential entries to the vault directory.
        '''
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Password Record")
        dialog.geometry("400x360")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog relative to parent window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        dialog_w = 400
        dialog_h = 360
        dialog.geometry(f"{dialog_w}x{dialog_h}+{root_x + (root_w - dialog_w)//2}+{root_y + (root_h - dialog_h)//2}")
        
        title_lbl = tk.Label(dialog, text="Add New Record", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        title_lbl.pack(pady=(15, 15))
        
        # Main form inputs container
        form_frame = tk.Frame(dialog, bg=self.colors["bg"])
        form_frame.pack(fill="both", expand=True, padx=25)
        
        # Title field (must not have spaces, like addpass.py validation)
        tk.Label(form_frame, text="Record Title (No spaces):", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        title_entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        title_entry.pack(fill="x", pady=(0, 10))
        title_entry.focus()
        
        # Username field
        tk.Label(form_frame, text="Username:", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        username_entry = tk.Entry(form_frame, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        username_entry.pack(fill="x", pady=(0, 10))
        
        # Password field
        tk.Label(form_frame, text="Password:", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        password_entry = tk.Entry(form_frame, font=("Segoe UI", 10), show="*", bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        password_entry.pack(fill="x", pady=(0, 5))
        
        # Show/hide password option checkbox
        show_p_var = tk.BooleanVar(value=False)
        def toggle_p_vis():
            char = "" if show_p_var.get() else "*"
            password_entry.config(show=char)
            
        tk.Checkbutton(
            form_frame, 
            text="Show Password", 
            variable=show_p_var, 
            command=toggle_p_vis,
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            bd=0,
            highlightthickness=0
        ).pack(anchor="w", pady=(0, 15))
        
        # Handle field validations, directory creation, encryption, and write processes
        def save_new():
            title = title_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not title:
                messagebox.showerror("Error", "Title cannot be empty.", parent=dialog)
                return
            if " " in title:
                messagebox.showerror("Error", "Title cannot contain spaces.", parent=dialog)
                return
            if not username:
                messagebox.showerror("Error", "Username cannot be empty.", parent=dialog)
                return
            if not password:
                messagebox.showerror("Error", "Password cannot be empty.", parent=dialog)
                return
                
            record_folder = f"VAULT/{title}"
            record_file = f"{record_folder}/{title}.txt"
            
            if os.path.exists(record_folder):
                messagebox.showerror("Error", f"A record named '{title}' already exists.", parent=dialog)
                return
                
            # Perform folder creation and encrypted file write processes
            try:
                os.makedirs(record_folder, exist_ok=True)
                
                # Encrypt utilizing master_key (hashed master password string)
                encrypted_password = encryptutils.encrypt(self.master_key, password)
                
                with open(record_file, "w") as f:
                    f.write(f"Title: {title} \nUsername: {username}\n")
                    f.write(f"Password: {encrypted_password}")
                    
                messagebox.showinfo("Success", "Password record created successfully!", parent=dialog)
                dialog.destroy()
                self.refresh_records_list()
                
                # Automatically highlight and load the newly created record
                try:
                    idx = sorted(self.current_records, key=lambda s: s.lower()).index(title)
                    self.record_listbox.selection_clear(0, tk.END)
                    self.record_listbox.selection_set(idx)
                    self.record_listbox.see(idx)
                    self.show_record_detail(title)
                except:
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save password record: {e}", parent=dialog)
                
        # Dialog footer action buttons layout
        btns_frame = tk.Frame(dialog, bg=self.colors["bg"])
        btns_frame.pack(fill="x", side="bottom", pady=15, padx=25)
        
        save_btn = self.create_button(btns_frame, "Save Record", save_new, bg_key="success", hover_key="success")
        save_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        cancel_btn = self.create_button(btns_frame, "Cancel", dialog.destroy, bg_key="sidebar", hover_key="bg")
        cancel_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        # Bind enter key for rapid submission
        title_entry.bind("<Return>", lambda e: save_new())
        username_entry.bind("<Return>", lambda e: save_new())
        password_entry.bind("<Return>", lambda e: save_new())

    def show_change_master_dialog(self):
        '''
        This function initializes a migration interface to safely transition existing vault data under a newly defined master password.
        '''
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Master Password")
        dialog.geometry("400x380")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog relative to main window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        dialog_w = 400
        dialog_h = 380
        dialog.geometry(f"{dialog_w}x{dialog_h}+{root_x + (root_w - dialog_w)//2}+{root_y + (root_h - dialog_h)//2}")
        
        title_lbl = tk.Label(dialog, text="Change Master Password", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        title_lbl.pack(pady=(15, 5))
        
        # Warning visual text
        warn_lbl = tk.Label(
            dialog, 
            text="⚠️ WARNING: Changing your master password will safely re-encrypt all existing password records. Please do not close this window during execution.",
            font=("Segoe UI", 8, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["danger"],
            wraplength=340,
            justify="center"
        )
        warn_lbl.pack(pady=(0, 15), padx=20)
        
        # Form inputs container
        form_frame = tk.Frame(dialog, bg=self.colors["bg"])
        form_frame.pack(fill="both", expand=True, padx=25)
        
        # Current Master Password field
        tk.Label(form_frame, text="Current Master Password:", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        curr_entry = tk.Entry(form_frame, font=("Segoe UI", 10), show="*", bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        curr_entry.pack(fill="x", pady=(0, 10))
        curr_entry.focus()
        
        # New Master Password field
        tk.Label(form_frame, text="New Master Password:", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        new_entry = tk.Entry(form_frame, font=("Segoe UI", 10), show="*", bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        new_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm New Master Password field
        tk.Label(form_frame, text="Confirm New Master Password:", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(anchor="w", pady=(0, 2))
        confirm_entry = tk.Entry(form_frame, font=("Segoe UI", 10), show="*", bg=self.colors["sidebar"], fg="#ffffff", bd=1, relief="solid", insertbackground="white")
        confirm_entry.pack(fill="x", pady=(0, 5))
        
        # Show password toggle checkbox option
        show_p_var = tk.BooleanVar(value=False)
        def toggle_p_vis():
            char = "" if show_p_var.get() else "*"
            curr_entry.config(show=char)
            new_entry.config(show=char)
            confirm_entry.config(show=char)
            
        tk.Checkbutton(
            form_frame, 
            text="Show Passwords", 
            variable=show_p_var, 
            command=toggle_p_vis,
            bg=self.colors["bg"], 
            fg=self.colors["text_dim"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["bg"],
            bd=0,
            highlightthickness=0
        ).pack(anchor="w", pady=(0, 10))
        
        # Handle verification of inputs, reading all records, and re-encrypting them safely
        def handle_change():
            curr_pw = curr_entry.get()
            new_pw = new_entry.get()
            confirm_pw = confirm_entry.get()
            
            if not curr_pw:
                messagebox.showerror("Error", "Current master password is required.", parent=dialog)
                return
            if not new_pw:
                messagebox.showerror("Error", "New master password is required.", parent=dialog)
                return
            if new_pw != confirm_pw:
                messagebox.showerror("Error", "Confirm password does not match new password.", parent=dialog)
                return
                
            # Verify current master key correctness
            hashed_curr = encryptutils.hash_(curr_pw)
            if hashed_curr != self.master_key:
                messagebox.showerror("Error", "Incorrect current master password.", parent=dialog)
                return
                
            if curr_pw == new_pw:
                messagebox.showerror("Error", "New password must be different from current password.", parent=dialog)
                return
                
            # Perform re-encryption migrations of all records in storage
            records = passutils.return_records("VAULT")
            hashed_new = encryptutils.hash_(new_pw)
            
            # Step 1: Read and decrypt all passwords into temporary memory buffer
            decrypted_records = {}
            try:
                for rec in records:
                    title, user, enc_pass = self.load_record_details(rec)
                    if title is not None:
                        dec_pass = encryptutils.decrypt(self.master_key, enc_pass)
                        decrypted_records[rec] = (user, dec_pass)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt records prior to migration. Aborting.\nDetails: {e}", parent=dialog)
                return
                
            # Step 2: Write back each entry re-encrypted under the new master key
            success_count = 0
            try:
                for rec, (user, dec_pass) in decrypted_records.items():
                    enc_new_pass = encryptutils.encrypt(hashed_new, dec_pass)
                    filepath = f"VAULT/{rec}/{rec}.txt"
                    
                    with open(filepath, "r") as f:
                        lines = f.readlines()
                    while len(lines) < 3:
                        lines.append("\n")
                        
                    lines[0] = f"Title: {rec} \n"
                    lines[1] = f"Username: {user}\n"
                    lines[2] = f"Password: {enc_new_pass}\n"
                    
                    with open(filepath, "w") as f:
                        for line in lines:
                            f.write(line)
                    success_count += 1
                    
                # Step 3: Write new master password hash to standard MASTERPASS file
                with open("VAULT/MASTERPASS.txt", "w") as f:
                    f.write(str(hashed_new))
                    
                # Step 4: Update internal runtime state with new master_key string
                self.master_key = hashed_new
                
                messagebox.showinfo(
                    "Success", 
                    f"Master password updated and {success_count} record(s) re-encrypted successfully!", 
                    parent=dialog
                )
                dialog.destroy()
                
                # Update visual display with newly re-encrypted values
                if self.selected_record:
                    self.show_record_detail(self.selected_record)
            except Exception as e:
                messagebox.showerror(
                    "Critical Error", 
                    f"An error occurred during password migration! Some records may be corrupted. \nDetails: {e}", 
                    parent=dialog
                )
                
        # Footer Action buttons
        btns_frame = tk.Frame(dialog, bg=self.colors["bg"])
        btns_frame.pack(fill="x", side="bottom", pady=15, padx=25)
        
        change_btn = self.create_button(btns_frame, "Change Password", handle_change, bg_key="success", hover_key="success")
        change_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        cancel_btn = self.create_button(btns_frame, "Cancel", dialog.destroy, bg_key="sidebar", hover_key="bg")
        cancel_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        # Key bindings for Return triggers
        curr_entry.bind("<Return>", lambda e: handle_change())
        new_entry.bind("<Return>", lambda e: handle_change())
        confirm_entry.bind("<Return>", lambda e: handle_change())

    def copy_to_clipboard(self, text, field_name):
        '''
        This function copies target data to the system clipboard and renders a brief confirmation visual indicator.
        '''
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        
        # Show styled non-blocking "Copied" alert toast at bottom right of detail pane
        status_lbl = tk.Label(self.detail_pane, text=f"✓ {field_name} copied to clipboard!", font=("Segoe UI", 9, "bold"), bg=self.colors["bg"], fg=self.colors["success"])
        status_lbl.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-10)
        
        # Self-destruct toast after 2 seconds
        self.root.after(2000, status_lbl.destroy)

if __name__ == "__main__":
    # Initialize the tkinter runtime and main window loops
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
