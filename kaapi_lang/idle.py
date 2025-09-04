import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import sys

# Import your Kaapi runner
from kaapi_lang.main import run_code


class LineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, width=40, **kwargs)
        self.text_widget = text_widget

    def update(self, event=None):
        """Redraw line numbers"""
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=line_num,
                             font=("Consolas", 11), fill="gray")
            i = self.text_widget.index(f"{i}+1line")


class KaapiIDLE:
    def __init__(self, root):
        self.root = root
        self.root.title("Kaapi IDLE - Hot Filter Kaapi")
        self.root.geometry("800x600")

        # ------------------ Menu ------------------
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        run_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Code", command=self.run_code)

        # ------------------ Editor + Line Numbers ------------------
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(
            editor_frame, wrap=tk.WORD, font=("Consolas", 12), undo=True
        )
        self.editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.line_numbers = LineNumbers(editor_frame, self.editor, bg="#2e2e2e")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Update line numbers on typing, scrolling, resizing
        self.editor.bind("<KeyRelease>", self.line_numbers.update)
        self.editor.bind("<MouseWheel>", self.line_numbers.update)
        self.editor.bind("<Button-1>", self.line_numbers.update)
        self.editor.bind("<Configure>", self.line_numbers.update)

        self.line_numbers.update()

        # ------------------ Output Area ------------------
        self.output = scrolledtext.ScrolledText(self.root, height=10,
                                                font=("Consolas", 11))
        self.output.pack(fill=tk.X)
        self.output.insert(tk.END, "☕ Welcome to Kaapi IDLE!\n")

        # File state
        self.current_file = None

    # ------------------ File Menu ------------------
    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".kaapi", filetypes=[("Kaapi files", "*.kaapi")]
        )
        if file_path:
            with open(file_path, "r") as f:
                code = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", code)
            self.current_file = file_path
        self.line_numbers.update()

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".kaapi", filetypes=[("Kaapi files", "*.kaapi")]
            )
            if not file_path:
                return
            self.current_file = file_path
        with open(self.current_file, "w") as f:
            f.write(self.editor.get("1.0", tk.END).rstrip())

    # ------------------ Run Menu ------------------
    def run_code(self):
        code = self.editor.get("1.0", tk.END).rstrip()
        self.output.delete("1.0", tk.END)

        try:
            old_stdout = sys.stdout
            sys.stdout = self
            run_code(code)
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}\n")
        finally:
            sys.stdout = old_stdout

    # ------------------ Redirect stdout ------------------
    def write(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def flush(self):
        pass


def main():
    root = tk.Tk()
    app = KaapiIDLE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
