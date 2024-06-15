import tkinter as tk
from tkinter import scrolledtext
from searchAI import SearchAI

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reading Companion")

        self.search_ai = SearchAI()

        # Left frame for window selection
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(left_frame, text="Open Windows:").pack(anchor=tk.W)
        self.window_list = tk.Listbox(left_frame, height=15)
        self.window_list.pack()

        for i, window in enumerate(self.search_ai.windows):
            self.window_list.insert(tk.END, f"{i + 1}. {window}")

        self.window_entry = tk.Entry(left_frame)
        self.window_entry.pack(pady=5)

        self.select_button = tk.Button(left_frame, text="Select Window", command=self.select_window)
        self.select_button.pack()

        # Right frame for output display
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(right_frame, text="Output:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=20)
        self.output_text.pack()

        self.run_button = tk.Button(right_frame, text="Start", command=self.run_search_ai)
        self.run_button.pack(pady=5)

        self.stop_button = tk.Button(right_frame, text="Stop", command=self.stop_search_ai)
        self.stop_button.pack(pady=5)

        self.running = False

    def select_window(self):
        try:
            window_number = int(self.window_entry.get())
            if window_number < 1 or window_number > len(self.search_ai.windows):
                raise ValueError
            self.search_ai.select_window(window_number - 1)
            self.output_text.insert(tk.END, f"Selected window: {self.search_ai.selected_window}\n")
        except ValueError:
            self.output_text.insert(tk.END, "Invalid window number.\n")

    def run_search_ai(self):
        if not self.running:
            self.running = True
            self.search_ai_thread()

    def stop_search_ai(self):
        self.running = False

    def search_ai_thread(self):
        if self.running:
            result = self.search_ai.run_once()
            if result:
                self.output_text.insert(tk.END, result + "\n")
            self.root.after(1000, self.search_ai_thread)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
