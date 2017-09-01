"""Wheel of Fortune with a Shakespearean twist!"""
import random
import os

spins = [300, 300, 300, 300, 300, 300, 350, 400, 400, 450, 500, 500,
         500, 550, 550, 600, 600, 600, 700, 800, 800, 800, 900, 900]
actions = ["spin", "vowel", "solve"]
possible_cons = ['b', 'c', 'd', 'f', 'g', 'h', 'j',
                 'k', 'l', 'm', 'n', 'p', 'q', 'r',
                 's', 't', 'v', 'w', 'x', 'y', 'z']
possible_vowels = ['a', 'e', 'i', 'o', 'u']


class Game:
    board = []
    cons = possible_cons[:]
    vowels = possible_vowels[:]

    def __init__(self, puzzle):
        string = ''
        for char in puzzle:
            if not char.isalpha() and not char == ' ':
                if string.endswith(' '):
                    string = string[:-1]
            string += char
        self.puzzle = string.strip()

        self.board = ["_" if char.isalpha() else char for char in self.puzzle]

    def print_list(self, lst):
        string = ''
        for i in lst:
            string += i + ' '
        print(string + '\n')


class Player:
    cash = 0
    play_order = {}

    def __init__(self, number):
        self.number = number
        self.name = input()
        Player.play_order[number] = self

    def play(self, game):
        game.print_list(game.board)
        if "_" in game.board:
            print("Your turn, {}!".format(self.name))
            action = actions[let_user_pick(actions) - 1]
            while action == "vowel" and self.cash < 250:
                action = ""
                print("Need $250 to buy a vowel")
                action = actions[let_user_pick(actions) - 1]
            if action == "spin":
                self.spin(game)
            elif action == "vowel":
                self.vowel(game)
            else:
                self.solve(game)
        else:
            if self.cash < 1000:
                self.cash = 1000
            print("Congratulations: {} wins ${}".format(self.name, self.cash))

    def spin(self, game):
        spin_val = random.choice(spins)
        print("You spun ${}".format(spin_val))
        guess = ""
        while guess not in possible_cons:
            print("Letter please:")
            guess = input().lower().strip()
        if guess in game.cons:
            game.cons.remove(guess)
            if guess in game.puzzle:
                game.board = [guess if game.puzzle[i] == guess else game.board[i] for i in range(len(game.puzzle))]
                appearances = sum([1 for i in game.puzzle if i == guess])
                self.cash += appearances * spin_val
                clear_screen()
                print("{} {}'s in the puzzle. {}'s total is ${}".format(appearances, guess, self.name, self.cash))
                self.play(game)
            else:
                clear_screen()
                print("No {} in puzzle. {}'s total is ${}".format(guess, self.name, self.cash))
                self.next_player(game)
        else:
            clear_screen()
            print("Letter already guessed! {}'s total is ${}".format(self.name, self.cash))
            self.next_player(game)

    def vowel(self, game):
        self.cash -= 250
        guess = ""
        while guess not in possible_vowels:
            print("Vowel please:")
            guess = input().lower().strip()
        if guess in game.vowels:
            game.vowels.remove(guess)
            if guess in game.puzzle:
                game.board = [guess if game.puzzle[i] == guess else game.board[i] for i in range(len(game.puzzle))]
                clear_screen()
                print("{} {}'s in the puzzle. {}'s total is ${}".format(sum([1 for i in game.puzzle if i == guess]), guess, self.name, self.cash))
                self.play(game)
            else:
                clear_screen()
                print("No {} in puzzle. {}'s total is ${}".format(guess, self.name, self.cash))
                self.next_player(game)
        else:
            clear_screen()
            print("Letter already guessed! {}'s total is ${}".format(self.name, self.cash))
            self.next_player(game)

    def solve(self, game):
        print("What's the answer?")
        if input().lower().strip() == game.puzzle:
            game.board = game.puzzle
            self.play(game)
        else:
            clear_screen()
            print("Sorry, that's incorrect. {}'s total is ${}".format(self.name, self.cash))
            self.next_player(game)

    def next_player(self, game):
        Player.play_order.get(self.number+1, Player.play_order[1]).play(game)


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2):
            continue
        line = aline
    return line.lower()


def let_user_pick(options):
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))
    while True:
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i)
        except:
            pass


def clear_screen():
    os.system('cls')
    center_char = ' '
    print("".center(100, center_char))
    print("".center(100, center_char))
    print(" __ __ __  __ __  _____  _____  __    ".center(100, center_char))
    print("|  |  |  ||  |  ||  ___||  ___||  |   ".center(100, center_char))
    print("|        ||     ||  ___||  ___||  |__ ".center(100, center_char))
    print(" \__/\__/ |__|__||_____||_____||_____|".center(100, center_char))
    print(" _____  _____ ".center(100, center_char))
    print("|  _  ||   __|".center(100, center_char))
    print("| |_| ||   _|".center(100, center_char))
    print("|_____||__|  ".center(100, center_char))
    print(" _____  __ __  _____  __ __  _____  _____  _____  _____  _____  _____  _____ ".center(100, center_char))
    print("|  ___||  |  ||  _  ||  /  /|  ___||  ___||  _  ||  ___||  _  ||  _  ||  ___|".center(100, center_char))
    print("|___  ||     ||     ||    \ |  ___||___  ||   __||  ___||     ||    _||  ___|".center(100, center_char))
    print("|_____||__|__||__|__||__\__\|_____||_____||__|   |_____||__|__||_|\__||_____|".center(100, center_char))
    print("".center(100, center_char))
    print("".center(100, center_char))

clear_screen()
print("Let's play Wheel of Fortune! Today's theme is Shakespeare!")
print("Here's your puzzle:")
game = Game(random_line(open("ShakespeareLines.txt", 'r')))

while True:
    print("How many players will be playing today? ", end='')
    try:
        num_of_players = int(input())
        if num_of_players > 0:
            break
    except Exception:
        pass

print("Players... What are your names?")
p1 = Player(1)
for i in range(2, num_of_players + 1):
    p = Player(i)
p1.play(game)
