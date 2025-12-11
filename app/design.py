# app/design.py
import tkinter as tk

# 🎨 Updated Color Scheme (Pink Theme)
COLORS = {
    "primary": "#D81B60",       # Dark pink
    "secondary": "#F06292",     # Light pink
    "background": "#F8F9FA",
    "text": "#212529",
    "light_text": "#6C757D",
    "success": "#EC407A",       # Bright pink for headings and hover
    "danger": "#E53935",
    "warning": "#FB8C00",
    "info": "#1E88E5"
}

FONTS = {
    "title": ("Segoe UI", 18, "bold"),
    "header": ("Segoe UI", 16),
    "normal": ("Segoe UI", 12),
    "label": ("Segoe UI", 12),
    "button": ("Segoe UI", 12, "bold")
}

def apply_style(widget):
    """Apply background color and font"""
    widget.configure(bg=COLORS["background"], fg=COLORS["text"])
    if isinstance(widget, tk.Label):
        widget.configure(font=FONTS["label"])
    elif isinstance(widget, tk.Entry):
        widget.configure(font=FONTS["normal"], relief="flat", bd=2, highlightthickness=2,
                         insertbackground=COLORS["text"])
    elif isinstance(widget, tk.Button):
        widget.configure(font=FONTS["button"], relief="flat", bd=0, padx=10, pady=5)

class StyledFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg=COLORS["background"])
        self.pack(fill="both", expand=True)

class StyledLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        # Only apply default style if not overridden
        if "font" not in kwargs:
            self.configure(font=FONTS["label"])
        if "bg" not in kwargs:
            self.configure(bg=COLORS["background"])
        if "fg" not in kwargs:
            self.configure(fg=COLORS["text"])
        else:
            self.configure(fg=kwargs["fg"])

        # Ensure padding/margin consistency
        if "anchor" not in kwargs:
            self.configure(anchor="center")

class StyledEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        apply_style(self)
        self.configure(highlightbackground=COLORS["secondary"], highlightcolor=COLORS["primary"])

class StyledButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        apply_style(self)
        self.configure(bg=COLORS["primary"], fg="white", activebackground=COLORS["success"])
        self.bind("<Enter>", lambda e: self.config(bg=COLORS["success"]))
        self.bind("<Leave>", lambda e: self.config(bg=COLORS["primary"]))

class StyledRadiobutton(tk.Radiobutton):
    def __init__(self, parent, *args, **kwargs):
        tk.Radiobutton.__init__(self, parent, *args, **kwargs)
        apply_style(self)
        self.configure(selectcolor=COLORS["background"])