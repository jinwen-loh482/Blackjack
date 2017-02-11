from random import randint, choice

# TODO:
# Add dealer mechanic
# Implement UI
# Implement a betting system

class Cards(object):
	suit_name = ["Diamonds", "Clubs", "Hearts", "Spades"]
	rank_name = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

	# sets the card
	def __init__(self, suit_choice, rank_choice):
		self.suit = Cards.suit_name[suit_choice]
		self.rank = Cards.rank_name[rank_choice]
		self.suit_choice = suit_choice
		self.rank_choice = rank_choice

	# returns the chosen card (human readable)
	def card_chosen_human(self):
		return "%s of %s" % (self.rank, self.suit)

	# returns the chosen card (machine readable)
	def card_chosen_machine(self):
		return [self.suit_choice, self.rank_choice]

# "Deck" class stores an array of cards whose power doesn't exceed bust
# An array of "Decks" is used to store hands with identical ranks
class Deck(object):
	def __init__(self):
		self.hand = []
		self.power = 0
		self.bet = 0

	def add_to_hand(self, card):
		self.hand.append(card)

	def get_hand_power(self):
		total_power = 0
		ace_count = 0
		for i in range(0, len(self.hand)):
			if self.hand[i].rank_choice >= 9:
				total_power += 10
				continue
			elif self.hand[i].rank_choice == 0:
				ace_count += 1
				continue
			total_power += self.hand[i].rank_choice + 1
		total_power = maximize_ace_power(total_power, ace_count)
		self.power = total_power

def get_yes_no():
	try:
		response = int(input("Response(1 for yes, 0 for no): "))
		while response != 1 and response != 0:
			response = int(input("Response(1 for yes, 0 for no): "))
		if response == 1:
				return True
		return False
	except ValueError:
		return get_yes_no()

def pick_suit():
	return randint(0, 3)

def pick_rank():
	return randint(0, 12)

# identification of cards will be in the form of double-element array: [suit, rank]
# suit and rank will be numbers 
def collect_used_cards(used_cards, card):
	used_cards.append(card.card_chosen_machine())

# checks whether two of the same cards have been chosen
def check_card_machine(used_cards, card):
	num_cards = len(used_cards)
	if num_cards == 0:
		return False
	for i in range(0, num_cards):
		if used_cards[i][0] == card.suit_choice:
			if used_cards[i][1] == card.rank_choice:
				return True
				break
	return False

# draw card
# hands is the array which stores "Decks", the class for card hands
def draw(used_cards, hands):
	count = 1
	repeat_flag = False
	while count == 1 or repeat_flag:
		card = Cards(pick_suit(), pick_rank())
		repeat_flag = check_card_machine(used_cards, card)
		if repeat_flag:
			continue
		used_cards.append(card.card_chosen_machine())
		hands[0].add_to_hand(card)
		count -= 1

# check for available splits
# returns 0 if false
# returns the array index of the identical cards in hand
# the split card is always the last card in the hand
def check_split(Deck):
	n = len(Deck.hand)
	if n <= 1:
		return 0
	for i in range(0, n - 1):
		if Deck.hand[i].rank == Deck.hand[n - 1].rank:
			return i, (n - 1)
	return 0

# splits the hand to a new hand
# takes the first hand in the array and appends a new list at hands
# hand index should be returned by check_split()
def split_hand(hands):
	if check_split(hands[0]) == 0:
		return
	split_tupl = check_split(hands[0])
	print("Do you want to split your %s and %s?" % (hands[0].hand[split_tupl[0]].card_chosen_human(), hands[0].hand[split_tupl[1]].card_chosen_human()))
	to_split = get_yes_no()
	if not to_split:
		return
	hands.append(Deck())
	n = len(hands)
	hands[n - 1].add_to_hand(hands[0].hand[split_tupl[1]])
	hands[0].hand.pop(split_tupl[1])

def maximize_ace_power(current_power, ace_count):
	for i in range(0, ace_count):
		if (current_power + 11) < 21:
			current_power += 11
		elif (current_power + 11) == 21:
			if i == (ace_count - 1):
				current_power += 11
		else:
			current_power += 1
	return current_power

def win_or_bust(hands):
	if hands[0].power > 21:
		return -1
	elif hands[0].power == 21:
		return 1
	return 0

def print_first_hand(hands):
	print("")
	print("--Current Hand--")
	for i in range(0, len(hands[0].hand)):
		print(hands[0].hand[i].card_chosen_human())

def print_power(hands):
	hands[0].get_hand_power()
	print("Total power: %d" % hands[0].power)
	print("")

def initialize_game(used_cards, hands):
	draw(used_cards, hands)
	draw(used_cards, hands)
	if check_split(hands[0]) != 0:
		print_first_hand(hands)
		split_hand(hands)
		return

used_cards = []
hands = [Deck()]
dealer_hands = [Deck()]

initialize_game(used_cards, hands)
while len(hands) > 0:
	print_first_hand(hands)
	print_power(hands)
	if win_or_bust(hands) == 1:
		print("Blackjack!")
		break
	print("Would you like to keep drawing for the current hand?")
	keep_drawing = get_yes_no()
	if not keep_drawing:
		hands.pop(0)
		continue
	draw(used_cards, hands)
	print_first_hand(hands)
	if check_split(hands[0]):
		split_hand(hands)
	print_power(hands)
	if win_or_bust(hands) == 1:
		print("Blackjack!")
		hands.pop(0)
	elif win_or_bust(hands) == -1:
		print("Bust!")
		hands.pop(0)

