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

    def match_def(self, definition):
        for card in self.cards:
            if card.definition == definition:
                return card.term
        return None


class Card:

    def __init__(self, term, definition):
        self.term = term
        self.definition = definition


cards = Deck()


def add_card():
    n = int(input("Input the number of cards: \n"))

    for card in range(n):
        key = str(input("The term for card #{}:\n".format(card + 1)))

        while True:
            if cards.term_exists(key):
                key = str(input(f'The term "{key}" already exists. Try again:\n'))
            else:
                break

        definition = str(input("The definition for card #{}:\n".format(card + 1)))
        while True:
            if cards.definition_exists(definition):
                definition = str(input(f'The definition "{definition}" already exists. Try again:\n'))
            else:
                cards.add_card(key, definition)
                break


def check_all_answers():
    for x in cards.terms():
        print(f'Print the definition of "{x}": ')
        user_input = str(input())
        if user_input == cards.match(x):
            print("Correct!")
        else:
            if cards.match_def(user_input) is None:
                print(f'Wrong. The right answer is "{cards.match(x)}".')
            else:
                print(
                    f'Wrong. The right answer is "{cards.match(x)}", but your definition is correct for "{cards.match_def(user_input)}".')


if __name__ == "__main__":
    add_card()
    check_all_answers()
