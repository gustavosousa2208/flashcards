# TODO: remove functions that are not used
import random


class Deck:
    def __init__(self):
        self.cards = []

    def term_exists(self, term):
        if term in self.terms():
            return True
        else:
            return False

    def definition_exists(self, definition):
        if definition in self.definitions():
            return True
        else:
            return False

    def add_card(self, term, definition):
        self.cards.append(Card(term, definition))

    def terms(self):
        terms = []
        for card in self.cards:
            terms.append(card.term)
        return terms

    def definitions(self):
        definitions = []
        for card in self.cards:
            definitions.append(card.definition)
        return definitions

    def match(self, term):
        for card in self.cards:
            if card.term == term:
                return card.definition
        return None

    def match_def(self, definition, ans=None):
        if ans is None:
            for card in self.cards:
                if card.definition == definition:
                    return card.term
            return None
        else:
            for card in self.cards:
                if card.term == ans and card.definition == definition:
                    return True

    def remove_card(self, term):
        for card in self.cards:
            if card.term == term:
                try:
                    self.cards.remove(card)
                    return True
                except ValueError:
                    return False

    def update_card(self, term, definition):
        for card in self.cards:
            if card.term == term:
                card.definition = definition
                return True
        return False

    def shuffle(self):
        random.shuffle(self.cards)


class Card:

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition


class Menu:
    def __init__(self, deck):
        self.deck = deck

    def menu(self):
        while True:
            action = str(input('Input the action (add, remove, import, export, ask, exit): \n'))
            if action == 'add':
                self.add()
            elif action == 'remove':
                self.remove()
            elif action == 'import':
                self.import_()
            elif action == 'export':
                self.export()
            elif action == 'ask':
                self.ask()
            elif action == 'exit':
                print("Bye bye!")
                break
            elif action == 'oi':
                for x in self.deck.cards:
                    print(x.term, x.definition)

    def add(self):
        term = str(input('The card: \n'))
        while True:
            if self.deck.term_exists(term):
                term = str(input(f'The card "{term}" already exists. Try again: \n'))
            else:
                break

        definition = str(input('The definition of the card: \n'))
        while True:
            if self.deck.definition_exists(definition):
                definition = str(input(f'The definition "{definition}" already exists. Try again:'))
            else:
                break
        self.deck.add_card(term, definition)
        print(f'The pair ("{term}":"{definition}") has been added.\n')

    def remove(self):
        action = str(input('Which card? '))
        if self.deck.remove_card(action):
            print(f'The card has been removed.\n')
        else:
            print(f'Can\'t remove "{action}": there is no such card.')

    def import_(self):
        # TODO: find the best way to import the file
        file = str(input('File name: \n'))
        try:
            with open(file, 'r') as f:
                count = 0
                for line in f:
                    term, definition = line.strip('\n').split(':')
                    if self.deck.term_exists(term):
                        self.deck.update_card(term, definition)
                    else:
                        self.deck.add_card(term, definition)
                    count += 1
            print(f'{count} cards have been loaded.\n')
        except FileNotFoundError:
            print('File not found.\n')

    def export(self):
        action = str(input("File name: \n"))
        try:
            with open(action, 'a') as f:
                for card in self.deck.cards:
                    # TODO: find the best way to write the file
                    f.writelines(f'{card.term}:{card.definition}\n')
            print(f"{len(self.deck.cards)} cards have been saved.")
        except FileNotFoundError:
            print('File not found')

    def ask(self):
        n = int(input('How many times to ask?\n'))
        self.deck.shuffle()
        for _ in range(n):
            x = random.randint(0, len(self.deck.cards) - 1)
            ans = str(input(f'Print the definition of "{self.deck.cards[x].term}":\n'))
            if self.deck.match_def(ans, self.deck.cards[x].term):
                print('Correct!\n')
            else:
                if self.deck.definition_exists(ans):
                    print(
                        f'Wrong. The right answer is "{self.deck.cards[x].definition}", but your definition is '
                        f'correct for "{self.deck.match_def(ans)}".')
                else:
                    print(f'Wrong. The right answer is "{self.deck.cards[x].definition}".\n')


def add_card(c):
    n = int(input("Input the number of cards: \n"))

    for card in range(n):
        key = str(input("The term for card #{}:\n".format(card + 1)))

        while True:
            if c.term_exists(key):
                key = str(input(f'The term "{key}" already exists. Try again:\n'))
            else:
                break

        definition = str(input("The definition for card #{}:\n".format(card + 1)))
        while True:
            if c.definition_exists(definition):
                definition = str(input(f'The definition "{definition}" already exists. Try again:\n'))
            else:
                c.add_card(key, definition)
                break


def check_all_answers(cards):
    for x in cards.terms():
        print(f'Print the definition of "{x}": ')
        user_input = str(input())
        if user_input == cards.match(x):
            print("Correct!")
        else:
            if cards.match_def(user_input, ) is None:
                print(f'Wrong. The right answer is "{cards.match(x)}".')
            else:
                print(
                    f'Wrong. The right answer is "{cards.match(x)}", but your definition is correct for "{cards.match_def(user_input, )}".')


if __name__ == "__main__":
    Menu(Deck()).menu()
