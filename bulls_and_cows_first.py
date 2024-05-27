import tkinter as tk
from tkinter import messagebox
import random


class BullsAndCowsGame:
    def __init__(self, master):
        """
        Инициализирует объект игры BullsAndCowsGame.

        Args:
            master (tk.Tk): Главный объект окна приложения.
        """
        self.master = master
        self.master.title("Bulls and Cows")

        # Генерация загаданного компьютером числа
        self.secret_number = self.generate_secret_number()
        self.history = []

        self.user_guess = tk.StringVar()
        self.result = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """
        Создает и размещает виджеты интерфейса пользователя.
        """
        tk.Label(self.master, text="Enter your guess:").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.user_guess).grid(row=0, column=1)

        tk.Button(self.master, text="Submit", command=self.submit_guess).grid(row=1, column=0, columnspan=2)

        self.result_label = tk.Label(self.master, textvariable=self.result)
        self.result_label.grid(row=2, column=0, columnspan=2)

        self.history_text = tk.Text(self.master, state='disabled', height=10, width=40)
        self.history_text.grid(row=3, column=0, columnspan=2)

    def generate_secret_number(self):
        """
        Генерирует четырехзначное число с уникальными цифрами.

        Returns:
            str: Загаданное компьютером четырехзначное число.
        """
        digits = '0123456789'
        return ''.join(random.sample(digits, 4))

    def validate_guess(self, guess):
        """
        Проверяет введенное пользователем число на корректность.

        Args:
            guess (str): Введенное пользователем число.

        Returns:
            str: Сообщение об ошибке, если число некорректно. Иначе None.
        """
        if len(guess) != 4:
            return "Некорректный запрос: Длина числа должна быть 4 цифры."
        if not guess.isdigit():
            return "Некорректный запрос: Введите только цифры."
        if len(set(guess)) != 4:
            return "Некорректный запрос: Все цифры должны быть разными."
        return None

    def count_bulls_and_cows(self, guess):
        """
        Считает количество быков и коров для заданного числа.

        Args:
            guess (str): Введенное пользователем число.

        Returns:
            tuple: Количество быков и коров.
        """
        bulls = sum(1 for a, b in zip(self.secret_number, guess) if a == b)
        cows = sum(1 for a in guess if a in self.secret_number) - bulls
        return bulls, cows

    def submit_guess(self):
        """
        Обрабатывает ввод пользователя, проверяет число, обновляет историю и выводит результат.
        """
        guess = self.user_guess.get()
        validation_error = self.validate_guess(guess)
        if validation_error:
            self.result.set(validation_error)
        else:
            bulls, cows = self.count_bulls_and_cows(guess)
            if bulls == 4:
                self.result.set("Число угадано!")
                self.history.append(f"Guess: {guess}, Result: Число угадано!")
                self.update_history()
                messagebox.showinfo("Game Over", "Поздравляем! Вы угадали число!")
                self.master.quit()
            else:
                result_text = f"{bulls} бык., {cows} кор."
                self.result.set(result_text)
                self.history.append(f"Guess: {guess}, Result: {result_text}")
                self.update_history()

    def update_history(self):
        """
        Обновляет текстовое поле истории ходов.
        """
        self.history_text.configure(state='normal')
        self.history_text.delete('1.0', tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    game = BullsAndCowsGame(root)
    root.mainloop()
