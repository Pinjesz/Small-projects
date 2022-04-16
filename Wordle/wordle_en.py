import requests
from bs4 import BeautifulSoup
import tkinter as tk


def main(form: str, letters: str, not_in: str) -> list:
    for letter in form:
        if letter != '_':
            letters += letter

    if len(letters) < 2:
        return ['Too little letters given!']
    elif len(letters) == 2:
        result = multiple_requests(letters, not_in, form)
    else:
        result = single_request(letters, not_in, form)

    return result


def single_request(letters: str, not_in: str, form: str) -> list:
    while len(letters) < 5:
        letters += '_'
    online_words = get_words_online(letters)
    after_exclude = []
    if len(not_in) > 0:
        for word in online_words:
            if check_letters(word, not_in):
                after_exclude.append(word)
    else:
        after_exclude = online_words

    after_form = []
    for word in after_exclude:
        if check_form(word, form):
            after_form.append(word)

    return after_form


def multiple_requests(letters: str, not_in: str, form: str) -> list:
    result = set()
    alphabet = 'abcdefghijklmnopqrstuvwyxz'
    for letter in alphabet:
        if letter not in not_in:
            result.update(single_request(letters+letter, not_in, form))
    result = list(result)
    result.sort()
    return result


def check_letters(word: str, wrong_letters: str) -> bool:
    for letter in wrong_letters:
        if letter in word:
            return False
    return True


def check_form(word: str, form: str) -> bool:
    for letter, f in zip(word, form):
        if f != '_':
            if letter != f:
                return False
    return True


def get_words_online(letters: str) -> list:
    url = f'https://wordfind.com/unscramble/{letters}#results'
    headers = {'User-Agent': 'Mozilla/5.0'}
    text = requests.get(url, headers=headers).text

    soup = BeautifulSoup(text, 'html.parser')
    try:
        words = soup.body.find(
            'div', attrs={'class': 'lBlock', 'id': '5-letter-words'}).find_all('a')
    except AttributeError:
        words = []

    word_list = []
    for word in words:
        word_list.append(word.text)

    return word_list


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordle helper")
        self.geometry("800x600")
        self.boxes = []
        self.place()

    def place(self):
        font1 = "none 40 bold"
        font2 = "none 15 bold"

        self.green_label = tk.Label(self, text='Green:', font=font1)
        self.green_label.grid(row=0, column=0, columnspan=5)

        for i in range(5):
            self.boxes.append(tk.Entry(self, font=font1, width=2))
            self.boxes[i].grid(row=1, column=i)

        self.yellow_label = tk.Label(self, text='Yellow:', font=font1)
        self.yellow_label.grid(row=2, column=0, columnspan=5)

        self.yellow_box = tk.Entry(self, font=font1, width=10)
        self.yellow_box.grid(row=3, column=0, columnspan=5)

        self.grey_label = tk.Label(self, text='Grey:', font=font1)
        self.grey_label.grid(row=4, column=0, columnspan=5)

        self.grey_box = tk.Entry(self, font=font1, width=10)
        self.grey_box.grid(row=5, column=0, columnspan=5)

        self.grey_box2 = tk.Entry(self, font=font1, width=10)
        self.grey_box2.grid(row=6, column=0, columnspan=5)

        self.button = tk.Button(
            self, text="Go", font=font1, command=self.read_input)
        self.button.grid(row=7, column=0, columnspan=5)

        tk.Label(self, width=10).grid(row=0, column=5, rowspan=6)

        self.result_label = tk.Label(
            self, text='Results:', font=font1, width=8)
        self.result_label.grid(row=0, column=6)

        self.results = tk.Text(self, width=30, height=20, font=font2)
        self.results.grid(row=1, column=6, rowspan=7)

        self.results.config(state=tk.DISABLED)

    def read_input(self):
        green = ''
        for box in self.boxes:
            content = box.get()
            if len(content) == 0:
                green += '_'
            elif len(content) == 1:
                green += content
            else:
                self.results.config(state=tk.NORMAL)
                self.results.delete('1.0', tk.END)
                self.results.insert(
                    tk.INSERT, 'Write only one letter per box!')
                self.results.config(state=tk.DISABLED)
        yellow = self.yellow_box.get()
        grey = self.grey_box.get() + self.grey_box2.get()

        word_list = main(green, yellow, grey)
        self.results.config(state=tk.NORMAL)
        self.results.delete('1.0', tk.END)
        for word in word_list:
            self.results.insert(tk.INSERT, word + '\n')
        if len(word_list) == 0:
            self.results.insert(tk.INSERT, 'NO MATCHES!')
        self.results.config(state=tk.DISABLED)


if __name__ == "__main__":
    window = Window()
    window.mainloop()
