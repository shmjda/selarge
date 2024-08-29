import math
import random

class Krypto:

    def __init__(self):
        # Create and shuffle deck
        self.deck = list()
        [[self.deck.append(i) for i in range(1, 7)] for j in range(3)]
        [[self.deck.append(i) for i in range(7, 11)] for j in range(4)]
        [[self.deck.append(i) for i in range(11, 18)] for j in range(2)]
        [[self.deck.append(i) for i in range(18, 26)] for j in range(1)]
        random.shuffle(self.deck)


    def shuffle(self):
        # Reshuffle deck
        random.shuffle(self.deck) 


    def get_objective(self):
        # Get objective card
        return self.deck[0]


    def get_cards(self):
        # Get played cards
        return self.deck[1:6]


    def draw_board(self):
        # Get cards and draw board state
        o = str(self.get_objective()).rjust(2)
        c = [str(card).rjust(2) for card in self.get_cards()]
        board = f"""
                ┌──────┐
                │      │
                │  {o}  │
                │      │
                └──────┘
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│      ││      ││      ││      ││      │
│  {c[0]}  ││  {c[1]}  ││  {c[2]}  ││  {c[3]}  ││  {c[4]}  │
│      ││      ││      ││      ││      │
└──────┘└──────┘└──────┘└──────┘└──────┘
        """

        print(board)


    def is_winnable(self):
        # Check all possible combinations
        objective = self.get_objective()
        cards = self.get_cards()
        self.solutions = []

        # Only possible operators
        ops = [
            lambda x, y: x + y,
            lambda x, y: x * y,
            lambda x, y: x - y,
            lambda x, y: y - x,
            lambda x, y: x / y if y != 0 else math.nan,
            lambda x, y: y / x if x != 0 else math.nan,
        ]

        # Perform every possible combination
        for c0 in cards:
            for c1 in [c for c in cards if c not in [c0]]:
                for c2 in [c for c in cards if c not in [c0, c1]]:
                    for c3 in [c for c in cards if c not in [c0, c1, c2]]:
                        for c4 in [c for c in cards if c not in [c0, c1, c2, c3]]:
                            for o0 in range(len(ops)):
                                for o1 in range(len(ops)):
                                    for o2 in range(len(ops)):
                                        for o3 in range(len(ops)):
                                            if objective == ops[o3](ops[o2](ops[o1](ops[o0](c0, c1), c2), c3), c4):
                                                self.solutions.append(('f0', [c0, c1, c2, c3, c4], [o0, o1, o2, o3]))
                                            if objective == ops[o3](ops[o0](c0, c1), ops[o2](ops[o1](c2, c3), c4)):
                                                self.solutions.append(('f1', [c0, c1, c2, c3, c4], [o0, o1, o2, o3]))
                                            if objective == ops[o3](ops[o2](ops[o0](c0, c1), ops[o1](c2, c3)), c4):
                                                self.solutions.append(('f2', [c0, c1, c2, c3, c4], [o0, o1, o2, o3]))

        return len(self.solutions) > 0


    def get_playable_hand(self):
        # Shuffle until hand can win
        while not self.is_winnable():
            self.shuffle()
        self.draw_board()


    def get_solutions(self):
        ops = [
            lambda x, y: x + y,
            lambda x, y: x * y,
            lambda x, y: x - y,
            lambda x, y: y - x,
            lambda x, y: x / y if y != 0 else math.nan,
            lambda x, y: y / x if x != 0 else math.nan,
        ]

        user_input = ""

        while user_input is "":
            user_input = input("Press Enter to reveal a solution... ")
            self.draw_solution(random.choice(self.solutions))


    def draw_solution(self, solution):
        family = solution[0]
        c0, c1, c2, c3, c4 = solution[1]
        o0, o1, o2, o3 = solution[2]
        p = self.get_pair_str
        if family == 'f0':
            print(p(p(p(p(c0, c1, o0), c2, o1), c3, o2), c4, o3))
        elif family == 'f1':
            print(p(p(c0, c1, o0), p(p(c2, c3, o1), c4, o2), o3))
        elif family == 'f2':
            print(p(p(p(c0, c1, o0), p(c2, c3, o1), o2), c4, o3))
        print()



    def get_pair_str(self, c0, c1, op):
        if op == 0:
            return f"({c0} + {c1})"
        elif op == 1:
            return f"({c0} * {c1})"
        elif op == 2:
            return f"({c0} - {c1})"
        elif op == 3:
            return f"({c1} - {c0})"
        elif op == 4:
            return f"({c0} / {c1})"
        elif op == 5:
            return f"({c1} * {c0})"



game = Krypto()
game.get_playable_hand()
game.get_solutions()