s = """2345A 1
Q2KJJ 13
Q2Q2Q 19
T3T3J 17
T3Q33 11
2345J 3
J345A 2
32T3K 5
T55J5 29
KK677 7
KTJJT 34
QQQJA 31
JJJJJ 37
JAAAA 43
AAAAJ 59
AAAAA 61
2AAAA 23
2JJJJ 53
JJJJ2 41"""

data = s.split('\n')

from collections import Counter
class CamelCards:
    def __init__(self, data):
        self.part = 1
        self.data = data
        self.hand_vals = {}
        self.hands = []
        self.card_order = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
        self.card_order2 = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}
        self.winning_combinations = {
            'highCard': [],
            '1': [],
            '2': [],
            '3': [],
            'fullHouse': [],
            '4': [],
            '5': []
        }
        self.winning_order = []
    
    def parse(self):
        for line in self.data:
            hand, value = line.split()
            self.hand_vals[hand] = int(value)
            self.hands.append(hand)
    
    def sort_combinations(self):
        for hand in self.hands:
            hand_type, hand = self.determine_hand_type(hand)
            self.winning_combinations[hand_type].append(hand)

    def determine_hand_type(self, hand):
        card_set = set(hand)
        card_count = Counter(hand)
        #all 5 cards are the same
        if len(card_set) == 1:
            hand_type = '5'
        #either 4 cards are the same or full house
        elif len(card_set) == 2:
            if 4 in card_count.values():
                hand_type = '4'
            else:
                hand_type = 'fullHouse'
        #either 3 cards are the same or 2 pairs
        elif len(card_set) == 3:
            if 3 in card_count.values():
                hand_type = '3'
            else:
                hand_type = '2'
        #2 cards are the same
        elif len(card_set) == 4:
            hand_type = '1'
        #all cards are different
        else:
            hand_type = 'highCard'
        if self.part == 2:
            hand_type, hand = self.replace_jokers(hand_type, hand)
        return hand_type, hand
    
    def translate(self, cards):
        return [self.card_order[card] for card in cards]

    def sort_hands(self, hand):
        sorted_hand = sorted(hand, key=self.translate)
        return sorted_hand
    
    def determine_winning_order(self):
        for key, hands in self.winning_combinations.items():
            if len(hands) > 0:
                sorted_hands = self.sort_hands(hands)
                self.winning_combinations[key] = sorted_hands
                self.winning_order.extend(sorted_hands)
    
    def calculate_winnings(self):
        total = 0
        for i in range(len(self.winning_order), 0, -1):
            total += self.hand_vals[self.winning_order[i-1]] * i
        return total
    
    def change_card_order(self):
        self.card_order = self.card_order2
    
    def replace_jokers(self, hand_type, hand):
        if 'J' not in hand:
            return hand_type, hand
        card_count = Counter(hand.replace('J', ''))
        #case 3333J
        if hand_type == '4':
            hand_type = '5'
        #case QQQJA
        elif hand_type == '3':
            hand_type = '4'
        #case QQQJJ or JJJ22
        elif hand_type == 'fullHouse':
            hand_type = '5'
        elif hand_type == '2':
            #case KKTTJ
            if all(x[1] == 2 for x in card_count.items()) and len(card_count) == 2:
                hand_type = 'fullHouse'
            #case KTJJT
            else:
                hand_type = '4'
        #case 2388J or 23J8J
        elif hand_type == '1':
            hand_type = '3'
        #case 2348J
        elif hand_type == 'highCard':
            hand_type = '1'
        return hand_type, hand
    
    def solve(self, n):
        if n not in (1, 2):
            raise ValueError('Invalid part number, choose 1 or 2')
        self.part = n
        if n == 2:
            self.change_card_order()
        self.parse()
        self.sort_combinations()
        self.determine_winning_order()
        print(self.calculate_winnings())
        
C = CamelCards(data)
C.solve(2)