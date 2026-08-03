import tkinter as tk
from tkinter import ttk

PRIMARY_BG = "#cce6ff"
SECONDARY_BG = "#f0f8ff"
HEADER_BG = "#0066cc"
HEADER_FG = "white"
BUTTON_PRIMARY_BG = "#0066cc"
BUTTON_SECONDARY_BG = "#4CAF50"
BUTTON_DANGER_BG = "#f44336"
BUTTON_INFO_BG = "#2196F3"
BUTTON_WARNING_BG = "#f0ad4e"
BUTTON_TEXT_FG = "white"
TREE_BG = "#e6f2ff"
TREE_ALT_BG = "#f7fbff"
TREE_SEL_BG = "#3399ff"
TREE_HEADING_BG = "#0066cc"
TREE_HEADING_FG = "silver"
TEXT_PRIMARY_FG = "black"
ROW_BG = "#ffffff"
SUCCESS_FG = "green"
ERROR_FG = "red"
INFO_FG = "blue"
WARNING_FG = BUTTON_WARNING_BG
INPUT_BG = BUTTON_TEXT_FG
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 11, "bold")


def apply_theme(window):
    window.configure(bg=PRIMARY_BG)
    style = ttk.Style(window)
    try:
        style.theme_use("default")
    except Exception:
        pass

    for btn_style in ["TButton", "App.TButton"]:
        style.configure(btn_style,
            background=BUTTON_PRIMARY_BG,
            foreground=BUTTON_TEXT_FG,
            font=FONT_BUTTON,
            padding=(8, 4))
        style.map(btn_style,
            foreground=[("active", BUTTON_TEXT_FG), ("pressed", BUTTON_TEXT_FG)],
            background=[("active", BUTTON_SECONDARY_BG), ("pressed", BUTTON_PRIMARY_BG)])

    for entry_style in ["TEntry", "App.TEntry"]:
        style.configure(entry_style,
            font=FONT_ENTRY,
            fieldbackground=INPUT_BG)

    style.configure("TCombobox",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=TEXT_PRIMARY_FG)

    for label_style in ["TLabel", "App.TLabel"]:
        style.configure(label_style,
            background=PRIMARY_BG,
            foreground=TEXT_PRIMARY_FG,
            font=FONT_LABEL)

    style.configure("TRadiobutton",
        background=PRIMARY_BG,
        foreground=TEXT_PRIMARY_FG,
        font=FONT_LABEL)

    style.configure("TCheckbutton",
        background=PRIMARY_BG,
        foreground=TEXT_PRIMARY_FG,
        font=FONT_LABEL)

    style.configure("TMenubutton",
        background=BUTTON_PRIMARY_BG,
        foreground=BUTTON_TEXT_FG,
        font=FONT_BUTTON,
        padding=(6, 3))

    style.configure("Treeview",
        background=TREE_BG,
        foreground=TEXT_PRIMARY_FG,
        fieldbackground=TREE_BG,
        rowheight=24)
    style.map("Treeview",
        background=[("selected", TREE_SEL_BG)],
        foreground=[("selected", BUTTON_TEXT_FG)])
    style.configure("Treeview.Heading",
        background=TREE_HEADING_BG,
        foreground=TREE_HEADING_FG,
        font=FONT_LABEL)


BUTTON_KINDS = {
    "primary": BUTTON_PRIMARY_BG,
    "secondary": BUTTON_SECONDARY_BG,
    "danger": BUTTON_DANGER_BG,
    "info": BUTTON_INFO_BG,
    "warning": BUTTON_WARNING_BG,
}

def styled_button(master, text, command=None, kind="primary", fg=BUTTON_TEXT_FG, **kwargs):
    bg = BUTTON_KINDS.get(kind, BUTTON_PRIMARY_BG)
    return tk.Button(master, text=text, bg=bg, fg=fg, command=command, **kwargs)


def maximize_window(window):
    """Tenta maximizar a janela e usa fallback para geometry quando necessário."""
    try:
        window.state("zoomed")
    except Exception:
        pass

    try:
        window.attributes("-zoomed", True)
    except Exception:
        pass

    try:
        if window.wm_state() not in ("zoomed", "iconic"):
            window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")
    except Exception:
        pass


def remember_window_state(window):
    """Guarda o estado atual da janela para restaurá-lo depois."""
    if not window:
        return

    try:
        state = window.wm_state()
        if state in ("normal", "zoomed", "iconic"):
            window._saved_window_state = state
        else:
            window._saved_window_state = "normal"
    except Exception:
        window._saved_window_state = "normal"


def restore_window(window):
    """Reexibe a janela e restaura o estado anterior, reaplicando maximização apenas se necessário."""
    if not window:
        return

    exists = getattr(window, "winfo_exists", None)
    if exists is not None and not exists():
        return

    try:
        window.deiconify()
    except Exception:
        pass

    try:
        window.update_idletasks()
    except Exception:
        pass

    def apply_state():
        saved_state = getattr(window, "_saved_window_state", "normal")
        if saved_state == "zoomed":
            maximize_window(window)
        elif saved_state == "iconic":
            try:
                window.state("iconic")
            except Exception:
                pass
        else:
            try:
                window.state("normal")
            except Exception:
                pass

    try:
        window.after(0, apply_state)
    except Exception:
        apply_state()
