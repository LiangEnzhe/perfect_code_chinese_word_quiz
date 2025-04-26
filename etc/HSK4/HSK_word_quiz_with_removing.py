import json
import random
import os

with open(os.getcwd() + "\\HSK4.json", "r+", encoding="utf-8") as f:
    words = json.load(f)

book = "HSK"
lesson = "L1 : 1-2"

#Для оценки ответа
def right(chosen_book, key, answer, chosen_lesson = ""):
    if answer == "stop":
        global cont
        cont = False
        exit()
    elif answer == "all":
        for key, value in words[chosen_book][chosen_lesson].items():
            print(key, ":", value)
        print("\n")
    elif answer == str(key[ : key.find(" (")]) or answer == "s":
        words[chosen_book][chosen_lesson].pop(key)
        with open(os.getcwd() + "\\HSK4.json", "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
        print("Correct\n" + str(key) + "\n")
    else:
        print("Wrong\n" + str(key) + "\n")

def pick(book, lesson):    
    key = random.choice(list(words[book][lesson].keys()))
    print(words[book][lesson][key])
    answer = str(input("- "))
    right(book, key, answer, lesson)

cont = True
while cont:
    pick(book, lesson)
