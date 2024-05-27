import tkinter as tk
from tkinter import messagebox
import itertools


class BullsAndCows:
    def __init__(self, master):
        """
        Инициализирует объект игры BullsAndCows.

        Args:
            master (tk.Tk): Главный объект окна приложения.
        """
        self.master = master
        self.master.title("Bulls and Cows")

        # Генерация всех возможных четырехзначных чисел с уникальными цифрами
        self.possible_numbers = self.generate_possible_numbers()
        self.history = []

        self.current_guess = tk.StringVar()
        self.bulls = tk.StringVar()
        self.cows = tk.StringVar()

        self.create_widgets()
        self.make_guess()

    def create_widgets(self):
        """
        Создает и размещает виджеты интерфейса пользователя.
        """
        tk.Label(self.master, text="Current Guess:").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.current_guess, state='readonly').grid(row=0, column=1)

        tk.Label(self.master, text="Bulls:").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.bulls).grid(row=1, column=1)

        tk.Label(self.master, text="Cows:").grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.cows).grid(row=2, column=1)

        tk.Button(self.master, text="Submit", command=self.submit_response).grid(row=3, column=0, columnspan=2)

        self.history_text = tk.Text(self.master, state='disabled', height=10, width=40)
        self.history_text.grid(row=4, column=0, columnspan=2)

    def generate_possible_numbers(self):
        """
        Генерирует все возможные четырехзначные числа с уникальными цифрами.

        Returns:
            list: Список строк, каждая из которых является уникальным четырехзначным числом.
        """
        numbers = [''.join(p) for p in itertools.permutations('0123456789', 4)]
        return numbers

    def make_guess(self):
        """
        Делает текущее предположение, выбирая первое число из возможных.
        """
        if not self.possible_numbers:
            messagebox.showinfo("Game Over", "No valid numbers left!")
            return

        self.current_guess.set(self.possible_numbers[0])

    def submit_response(self):
        """
        Обрабатывает ответ пользователя, обновляет историю и фильтрует возможные числа.
        """
        guess = self.current_guess.get()
        try:
            bulls = int(self.bulls.get())
            cows = int(self.cows.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Bulls and Cows must be integers.")
            return

        if bulls == 4:
            messagebox.showinfo("Game Over", f"The number was {guess}. The program guessed it!")
            self.master.quit()
            return

        self.history.append((guess, bulls, cows))
        self.update_history()
        self.filter_numbers(guess, bulls, cows)
        self.make_guess()

    def update_history(self):
        """
        Обновляет текстовое поле истории ходов.
        """
        self.history_text.configure(state='normal')
        self.history_text.delete('1.0', tk.END)
        for guess, bulls, cows in self.history:
            self.history_text.insert(tk.END, f"Guess: {guess}, Bulls: {bulls}, Cows: {cows}\n")
        self.history_text.configure(state='disabled')

    def filter_numbers(self, guess, bulls, cows):
        """
        Фильтрует возможные числа на основе ответа пользователя.

        Args:
            guess (str): Число, предложенное пользователем.
            bulls (int): Количество быков.
            cows (int): Количество коров.
        """

        def count_bulls_and_cows(num1, num2):
            bulls = sum(1 for a, b in zip(num1, num2) if a == b)
            cows = sum(1 for a in num1 if a in num2) - bulls
            return bulls, cows

        self.possible_numbers = [num for num in self.possible_numbers
                                 if count_bulls_and_cows(num, guess) == (bulls, cows)]


if __name__ == "__main__":
    root = tk.Tk()
    game = BullsAndCows(root)
    root.mainloop()
