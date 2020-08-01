from random import choice
from bs4 import BeautifulSoup
import requests
from time import sleep
from csv import DictReader
import pyfiglet
from termcolor import colored
art = pyfiglet.figlet_format("Guess-72")
color_art = colored(art, color="green")
print(art)


def read_file(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(QOUTE):
    base = "http://quotes.toscrape.com"
    round = int(input("how many time you wanna play "))
    score = float(round)
    while round > 0:
        quote = choice(QOUTE)
        remaining_guess = 4
        print(quote["txt"])
        guess = ''
        while guess.lower() != quote["author"].lower() and remaining_guess > 0:
            guess = input(f"who said this? remaining:{remaining_guess} ")
            if guess.lower() == quote["author"].lower():
                print("you got it!!!")
                break
            remaining_guess -= 1
            if remaining_guess == 3:
                res = requests.get(f"{base}{quote['bio']}")
                soup = BeautifulSoup(res.text, "html.parser")
                birth_date = soup.find(class_="author-born-date").get_text()
                birth_p = soup.find(class_="author-born-location").get_text()
                print(
                    f"here's a hint: the authour was born in{birth_date} {birth_p}")
                score -= 0.25
            elif remaining_guess == 2:
                first_in = quote["author"][0]
                print(f"here is another hint first name of author {first_in}")
                score -= 0.25
            elif remaining_guess == 1:
                last_in = quote["author"].split(" ")[1][0]
                print(f" you can do it: the author last name {last_in} ")
                score -= 0.5
            else:
                name = quote["author"]
                print(f"sorry you ran out of guesses, the answer was {name}")
        round -= 1
        again = ''
        while again not in ('y', 'yes', 'n', 'no'):
            if round == 0:
                result(score)
                quit()
            again = input("do you want to you want to play next round(y/n)? ")
            if again.lower() in ('n', 'no'):
                print("you will lose all remaining your point!!")
                confirm = input("confirm by again typing 'n' :-")
                if confirm.lower() == 'n':
                    score = score-float(round)
                    result(score)
                    quit()
            elif again.lower() in ('y', 'yes'):
                print("you play again")


def result(score):
    print(f"your score is {score}")
    print("okay good bye")


QOUTE = read_file("quotes.csv")
start_game(QOUTE)
