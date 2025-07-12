import json, random, os, copy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

with open(os.path.join(os.getcwd(), "Complete_list_of_words.json"), "r", encoding="utf-8") as f:
    original_words = json.load(f)
current_words = copy.deepcopy(original_words)

root = tk.Tk()
root.title("Demo")
root.geometry("500x400")

current_frame = None
book = ""
lesson_name = ""

def clear():
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = tk.Frame(root)
    current_frame.pack(padx=10, pady=10)

def show_books():
    clear()
    tk.Label(current_frame, text="Select a Book:").pack(pady=10)
    for name in original_words:
        tk.Button(current_frame, text=name, width=20,
                  command=lambda n=name: show_lessons(n)).pack(pady=2)

def show_lessons(selected_book):
    global book
    book = selected_book
    clear()
    tk.Label(current_frame, text="Select a Lesson:").pack(pady=10)
    
    lessons = original_words[selected_book]
    lesson_container = tk.Frame(current_frame)
    lesson_container.pack()
    
    for i, lesson in enumerate(lessons):
        lesson_short = lesson[1:lesson.find(" :")]
        ttk.Button(lesson_container, text=lesson_short, width=6,
                   command=lambda l=lesson: start_quiz(l)).grid(row=i//5, column=i%5, padx=2, pady=2)
    
    tk.Button(current_frame, text="← Back to Books", command=show_books).pack(pady=10)

def start_quiz(lesson):
    global lesson_name
    lesson_name = lesson
    clear()
    
    words = list(current_words[book][lesson].items())
    random.shuffle(words)
    
    QuizSession(words)

class QuizSession:
    def __init__(self, words):
        self.words = words
        self.current_index = 0
        self.score = 0
        self.setup_widgets()
        self.show_next_word()

    def setup_widgets(self):
        nav_frame = tk.Frame(current_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(nav_frame, text="Show All Words", command=self.show_all_words).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="← Lessons", command=lambda: show_lessons(book)).pack(side=tk.RIGHT)
        ttk.Button(nav_frame, text="↻ Books", command=show_books).pack(side=tk.RIGHT, padx=5)

        self.english_label = tk.Label(current_frame, font=('Arial', 14))
        self.english_label.pack(pady=20)
        
        self.entry = ttk.Entry(current_frame, font=('Arial', 12))
        self.entry.pack()
        self.entry.bind("<Return>", self.check_answer)
        
        self.feedback = tk.Label(current_frame, fg="red")
        self.feedback.pack()
        
        btn_frame = tk.Frame(current_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Check", command=self.check_answer).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Skip", command=self.skip_word).pack(side=tk.LEFT, padx=5)

    def show_all_words(self):
        top = tk.Toplevel()
        top.title("All Words")
        text = tk.Text(top, wrap=tk.WORD, width=40, height=15)
        scroll = ttk.Scrollbar(top, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(fill=tk.BOTH, expand=True)
        
        for ch, en in current_words[book][lesson_name].items():
            text.insert(tk.END, f"{en} → {ch}\n")
        text.config(state=tk.DISABLED)

    def show_next_word(self):
        if self.current_index >= len(self.words):
            self.end_session()
            return
        
        self.english_label.config(text=self.words[self.current_index][1])
        self.entry.delete(0, tk.END)
        self.feedback.config(text="")
        self.entry.focus()

    def check_answer(self, event=None):
        answer = self.entry.get().strip()
        full = self.words[self.current_index]
        correct = self.words[self.current_index][0].split(" (")[0]
        
        if answer == correct:
            self.current_index += 1
            self.show_next_word()
        else:
            self.feedback.config(text=f"Correct answer: {full}")

    def skip_word(self):
        self.words.append(self.words.pop(self.current_index))
        self.show_next_word()

    def end_session(self):
        clear()
        tk.Label(current_frame, text="Lesson Completedd", font=('Arial', 16)).pack(pady=20)
        
        btn_frame = tk.Frame(current_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Retry Lesson", command=lambda: start_quiz(lesson_name)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Lessons", command=lambda: show_lessons(book)).pack(side=tk.LEFT, padx=5)

show_books()
root.mainloop()
