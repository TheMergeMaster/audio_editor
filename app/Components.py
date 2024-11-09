import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import tkinter.messagebox
from ttkbootstrap import Style

from constants import COLORS, FONT_FAMILY, FONT_SIZES


def Button(parent, command, **kwargs) -> ttk.Button:
    b = ttk.Button(parent, command=command, style="primary.TButton", **kwargs)
    return b


def Input(parent, **kwargs) -> ttk.Entry:
    input = ttk.Entry(parent, style="primary.TEntry", **kwargs)
    return input


def Label(parent, *args, **kwargs) -> ttk.Label:
    lbl = ttk.Label(parent, *args, **kwargs)
    return lbl


def Slider(parent, **kwargs) -> ttk.Scale:
    kwargs["style"] = "warning.Horizontal.TScale"
    slider = ttk.Scale(parent, **kwargs)
    return slider


def Section(parent, title, **kwargs) -> ttk.LabelFrame:
    s = ttk.LabelFrame(parent, text=title, **kwargs)
    return s


def Window(title: str, geometry: str):
    w = tk.Tk()
    w.title(title)
    w.geometry(geometry)
    w.resizable(False, False)
    w.protocol("WM_DELETE_WINDOW",
               lambda: w.destroy() if tkinter.messagebox.askokcancel(
                   "Quit?", "Do you really want to exit?") else None
               )

    style = Style("pulse")
    style.map("primary.TButton", width="80")
    w.style = style

    return w
