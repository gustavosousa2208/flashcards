# TODO: remove functions that are not used
# TODO: fix card matching by term or definition
import builtins
import random
import logging
from io import StringIO
import sys

log_stream = StringIO()
handler = logging.StreamHandler(log_stream)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def print(*args, sep=' ', end='\n', file=sys.stdout):
    logger.info(sep.join(map(str, args)).replace('\n', ''))
    builtins.print(*args, sep=sep, end=end, file=file)


def input(*args, **kwargs):
    print(*args, **kwargs, end='',)
    log_input = builtins.input()
    logger.info(log_input)
    return log_input


def log(file):
    try:
        with open(file, 'w') as f:
            f.write(log_stream.getvalue())
    except FileNotFoundError:
        pass


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

    def add_card(self, term, definition, mistakes=0):
        self.cards.append(Card(term, definition, mistakes))

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
                old_def = card.definition
                card.definition = definition
                return True
        return False

    def shuffle(self):
        random.shuffle(self.cards)

    def hardest(self):
        hardest = None
        for x in self.cards:
            if x.mistakes > 0:
                if hardest is None:
                    hardest = x
                elif x.mistakes > hardest.mistakes:
                    hardest = x

        return hardest

    def reset_stats(self):
        for card in self.cards:
            card.mistakes = 0


class Card:

    def __init__(self, term, definition, mistakes=0):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes


class Menu:
    def __init__(self, deck):
        self.deck = deck

    def menu(self):
        while True:
            action = str(
                input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats): \n'))
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
            elif action == 'hardest card':
                self.hardest_card()
            elif action == 'reset stats':
                self.deck.reset_stats()
                print("Card statistics have been reset. \n")
            elif action == 'log':
                file = str(input("File name: \n"))
                log(file)
                print("The log has been saved. \n")

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
        action = str(input('Which card? \n'))
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
                    term, definition, mistakes = line.strip('\n').split(':')
                    if self.deck.term_exists(term):
                        self.deck.update_card(term, definition)
                    else:
                        self.deck.add_card(term, definition, mistakes)
                    count += 1
            print(f'{count} cards have been loaded.\n')
        except FileNotFoundError:
            print('File not found.\n')

    def export(self):
        action = str(input("File name: \n"))
        try:
            with open(action, 'a+') as f:
                count = 0
                f.seek(0)
                data = f.readlines()
                for card in self.deck.cards:
                    # TODO: find the best way to write the file
                    writing = f'{card.term}:{card.definition}:{card.mistakes}\n'
                    if writing not in data:
                        f.writelines(writing)
                        count += 1
            print(f"{count} cards have been saved.\n")
        except FileNotFoundError:
            print('File not found')

    def ask(self):
        n = int(input('How many times to ask?\n'))
        for _ in range(n):
            x = random.randint(0, len(self.deck.cards) - 1)
            ans = str(input(f'Print the definition of "{self.deck.cards[x].term}":\n'))
            if self.deck.match_def(ans, self.deck.cards[x].term):
                print('Correct!\n')
            else:
                self.deck.cards[x].mistakes += 1
                if self.deck.definition_exists(ans):
                    print(
                        f'Wrong. The right answer is "{self.deck.cards[x].definition}", but your definition is '
                        f'correct for "{self.deck.match_def(ans)}".')
                else:
                    print(f'Wrong. The right answer is "{self.deck.cards[x].definition}".\n')

    def hardest_card(self):
        hardest = self.deck.hardest()
        if hardest is not None:
            print(f'The hardest card is "{hardest.term}". You have {hardest.mistakes} errors answering it.')
        else:
            print('There are no cards with errors.\n')


if __name__ == "__main__":
    Menu(Deck()).menu()
