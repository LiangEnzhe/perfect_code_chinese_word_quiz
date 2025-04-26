import json
import random
import os
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import cv2
import numpy as np
import pytesseract  # Ensure pytesseract is installed and configured

# Основные комманды
print("Commands:\n",
      "stop = STOP the words,\n",
      "all = print ALL words in lesson,\n",
      "new = chooses another BOOK with LESSON,\n",
      "add = ADDs difficult words to review,\n",
      "clear = CLEARS the review list,\n",
      "'s' = SKIP the word.\n")

# Открывает JSON
with open(os.getcwd() + "\\Triple_main_shit_book.json", "r+", encoding="utf-8") as f:
    words = json.load(f)

# Переменные
book = ""
lesson = ""

# GUI Class for Drawing
class DrawingApp:
    def __init__(self, root, expected_word):
        self.root = root
        self.root.title("Draw the Chinese Character")
        self.expected_word = expected_word

        self.canvas = tk.Canvas(root, width=300, height=300, bg='white')
        self.canvas.pack()

        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def paint(self, event):
        """Draw on the canvas with the mouse."""
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, fill=self.color, width=3)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        """Reset the old_x and old_y when the mouse button is released."""
        self.old_x = None
        self.old_y = None

    def submit(self):
        """Handle submission of the drawn character."""
        # Capture the canvas content as an image
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Save the image with the expected word as its name
        img_path = os.path.join(os.getcwd(), "img", f"{self.expected_word}.png")
        ImageGrab.grab((x, y, x1, y1)).save(img_path)
        
        self.process_image(img_path)
        
        self.root.destroy()

    def process_image(self, img_path):
        """Process the drawn image using OpenCV and extract text."""
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Perform OCR on the processed image
        ocr_result = pytesseract.image_to_string(threshold, lang='chi_sim')  # Use a Chinese language model
        print(f"OCR Result: {ocr_result.strip()}")
        
        # Check if the OCR result matches the expected word
        if ocr_result.strip() == self.expected_word:
            print("Correct!")
        else:
            print("Wrong, try again.")
        
        # Remove the saved image
        os.remove(img_path)

# Existing functions for book and lesson selection
def choosbook():
    x = str(input("What book: "))
    global book
    if x.upper() in ["O", "ORANGE", "ORANGE BOOK"]:
        book = "Orange book"        
    elif x.upper() in ["B", "BLUE", "BLUE BOOK"]:
        book = "Blue book"        
    elif x.upper() in ["G", "GREEN", "GREEN BOOK"]:
        book = "Green book"
    elif x.upper() in ["DF", "DIFFICULT WORDS", "D"]:
        book = "Difficult words"

def chooslesson():
    x = str(input("What lesson: "))
    x = x.upper() + " "
    global book, lesson
    for i in words[book].keys():
        if x in i:
            lesson = i
        elif x == "EXTRA " or x == "E ":
            lesson = "Extra"

# Function to check answer using Tkinter
def right(chosen_book, key, answer, chosen_lesson=""):
    if answer.lower() == "draw":
        # Launch the drawing window
        root = tk.Tk()
        app = DrawingApp(root, key.split(" (")[0])  # Pass the word without hints or parentheses
        root.mainloop()
    elif answer.lower() == key.split(" (")[0]:
        print("Correct!\n" + str(key) + "\n")
    else:
        print("Wrong!\n" + str(key) + "\n")

# Main function to pick a word for the quiz
def pick(book, lesson):
    key = random.choice(list(words[book][lesson].keys()))
    print(words[book][lesson][key])
    answer = str(input("- "))
    right(book, key, answer, lesson)

def dfpick():
    dictionary = random.choice(words["Difficult words"])
    key = list(dictionary.keys())[0]
    print(dictionary[key])
    answer = str(input("- "))
    right(book, key, answer)

# Main loop for the quiz
cont = True
while cont:
    try:
        pick(book, lesson)
    except KeyError:
        dfpick()
