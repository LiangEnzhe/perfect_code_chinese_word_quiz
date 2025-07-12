import json, random, os, copy

print("Commands:\n",
      "stop = STOP the words flow,\n",
      "all = print ALL words in lesson,\n",
      "new = chooses another BOOK with LESSON,\n",
      "add = ADDs difficult words to review,\n",
      "clear = CLEARS the review list,\n",
      "'s' = SKIP the word.\n")

#Открывает JSON
with open(os.path.join(os.getcwd(), "Complete_list_of_words.json"), "r+", encoding="utf-8") as f:
    original_words = json.load(f)
current_words = copy.deepcopy(original_words)

#Для new цикла книг
def choosebook():
    #Меню выбора, отсек для книг
    for choice_of_books in original_words:
        print(choice_of_books)
        
    letter = str(input("\nWhat book: ")).strip()[0].upper()
    match letter:
        case "O" :
            if int(input("Which part?(1;2): ")) == 1:
                return "Orange book"
            else:
                return "Orange book 2"
        case "B":
            if int(input("Which part?(1;2): ")) == 1:
                return "Blue book"
            else:
                return "Blue book 2"
        case "G":
            return "Green book"
        case "S":
            return "Science"
        case "H":
            return "HSK5"
        case "K":
            return "Keji"
        case _:
            return "Unknown name"

#Для new цикла книг
def chooselesson():
    for lesson in original_words[book].keys():
        print(lesson)
    lesson = 'L' + ''.join(filter(str.isdigit, input("\nWhat lesson: "))) + ' '
    for index in original_words[book]:
        if lesson in index:
            return index

#Переменные
book = choosebook()
lesson = chooselesson()
fremov = int(input("Removing feature(0 = False; 1 = True): "))

#Для оценки ответа
def right(key, answer):
    correct = key[ : key.find(" (")]
    match answer:
        case "stop":
            exit()
        case "new":
            global book, lesson
            book = choosebook()
            lesson = chooselesson()
            print(f"New book: {book}; New lesson: {lesson}\n")
        case "all":
            for key, value in current_words[book][lesson].items():
                print(f"{key}: {value}")
        case _ if answer.__eq__(correct) or answer.__eq__("s"):
            print(f"Correct\n{key}\n")
            if fremov == 1:
                current_words[book][lesson].pop(key)
        case _:
            while answer.__ne__(correct) and answer.__ne__("s"):
                print(f"Wrong\n{key}\n")
                answer = str(input("> "))
            print("Correct\n")

while True:
    try:
        word_list = list(current_words[book][lesson].keys())
        key = random.choice(word_list)
        print(current_words[book][lesson][key])
        answer = str(input("> "))
        right(key, answer)
    except IndexError:
        print("======================================================",
              "\nThis Lesson ended. Choose another one")
        if int(input("\nRepeat? (0 = False; 1 = True): ")) == 1:
            # Сброс к оригинальным словам урока
            current_words[book][lesson] = copy.deepcopy(original_words[book][lesson])
            print(f"Restarting {lesson}")
        else:
            original_words[book].pop(lesson)
            lesson = chooselesson()
