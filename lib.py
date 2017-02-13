from random import randint, choice
import os

class Cards(object):
	suit_name = ["Diamonds", "Clubs", "Hearts", "Spades"]
	rank_name = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

	def __init__(self, suit_choice, rank_choice):
		self.suit = Cards.suit_name[suit_choice]
		self.rank = Cards.rank_name[rank_choice]
		self.suit_choice = suit_choice
		self.rank_choice = rank_choice

	def card_chosen_human(self):
		return "%s of %s" % (self.rank, self.suit)

	def card_chosen_machine(self):
		return [self.suit_choice, self.rank_choice]

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

	def print_hand_power(self):
		self.get_hand_power()
		print("Hand power: %d\n" % self.power)

	def print_hand(self):
		for i in range(0, len(self.hand)):
			print(self.hand[i].card_chosen_human())

	def maximize_ace_power(self, current_power, ace_count):
		for i in range(0, ace_count):
			if (current_power + 11) < 21:
				current_power += 11
			elif (current_power + 11) == 21:
				if i == (ace_count - 1):
					current_power += 11
			else:
				current_power += 1
		return current_power

class Player():
	def __init__(self):
		self.hands = [Deck()]
		self.cash = 1000
		self.bet_amount = 0

	def bet_menu(self):
		print("1 - $10")
		print("2 - $50")
		print("3 - $100")

	def bet_choice_mapper(self, choice):
		if choice == 3:
			if self.cash >= 100:
				return 100
			elif self.cash >= 50:
				print("Insufficient funds! Betting 50$.")
			else:
				print("Insufficient funds! Betting 10$.")
		elif choice == 2:
			if self.cash >= 50:
				return 50
			else:
				print("Insufficient funds! Betting 10$.")
		return 10

	def get_bet_choice(self):
		try:
			choice = int(input("Response: "))
			print("")
			if choice < 1 or choice > 3:
				return self.get_bet_choice()
			return choice
		except ValueError:
			return self.get_bet_choice()

	def bet(self):
		print("How much do you want to bet?")
		print("Cash: $%s" % self.cash)
		self.bet_menu()
		self.bet_amount = self.bet_choice_mapper(self.get_bet_choice())
		os.system('clear')

	def draw_another(self, index):
		print("")
		self.hands[index].get_hand_power()
		if self.hands[index].power > 21:
			self.hands[index].print_hand()
			self.hands[index].print_hand_power()
			print("Bust!\n")
			return False
		elif self.hands[index].power == 21:
			self.hands[index].print_hand()
			self.hands[index].print_hand_power()
			print("Blackjack!")
			return False
		print("Do you want to keep drawing for the current hand?")
		print("--Current hand--")
		self.hands[index].print_hand()
		self.hands[index].print_hand_power()
		response = get_yes_no()
		return response

	def draw_sequence(self, used_cards):
		for i in range(0, len(self.hands)):
			response = self.draw_another(i)
			while response and self.hands[i].power < 21:
				self.draw_v2(used_cards, self.hands, i)
				os.system('clear')
				response = self.draw_another(i)
			continue

	def draw_v2(self, used_cards, hands, index):
		count = 1
		repeat_flag = False
		while count == 1 or repeat_flag:
			if len(used_cards) == 52:
				print("You have drawn all cards!")
				break
			card = Cards(pick_suit(), pick_rank())
			repeat_flag = check_card_machine(used_cards, card)
			if repeat_flag:
				continue
			collect_used_cards(used_cards, card)
			hands[index].add_to_hand(card)
			count -= 1

class Dealer():
	def __init__(self):
		self.dealer_hands = [Deck()]

	def dealer_init(self, used_cards):
		draw(used_cards, self.dealer_hands)
		draw(used_cards, self.dealer_hands)
		print("--Dealer's first card--")
		print(self.dealer_hands[0].hand[0].card_chosen_human())
		print("")
		self.dealer_AI(used_cards)

	def dealer_AI(self, used_cards):
		self.dealer_hands[0].get_hand_power()
		while self.dealer_hands[0].power < 17:
			draw(used_cards, self.dealer_hands)
			self.dealer_hands[0].get_hand_power()

	def print_dealer_hand(self):
		for i in range(0, len(self.dealer_hands[0].hand)):
			print("%s\n" % self.dealer_hands[0].hand.card_chosen_human())

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

def collect_used_cards(used_cards, card):
	used_cards.append(card.card_chosen_machine())

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

def draw(used_cards, hands):
	count = 1
	repeat_flag = False
	while count == 1 or repeat_flag:
		if len(used_cards) == 52:
			print("You have drawn all cards!")
			break
		card = Cards(pick_suit(), pick_rank())
		repeat_flag = check_card_machine(used_cards, card)
		if repeat_flag:
			continue
		collect_used_cards(used_cards, card)
		hands[0].add_to_hand(card)
		count -= 1

def check_split(Deck):
	n = len(Deck.hand)
	if n <= 1:
		return 0
	for i in range(0, n - 1):
		if Deck.hand[i].rank == Deck.hand[n - 1].rank:
			return i, (n - 1)
	return 0

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

def win_or_bust(power):
	if power > 21:
		return 0
	elif power == 21:
		return 1
	return power

def print_first_hand(hands):
	print("")
	print("--Current Hand--")
	for i in range(0, len(hands[0].hand)):
		print(hands[0].hand[i].card_chosen_human())

def check_win(Player, Dealer):
	for i in range(0, len(Player.hands)):
		if win_or_bust(Player.hands[i].power) > win_or_bust(Dealer.dealer_hands[0].power):
			if win_or_bust(Dealer.dealer_hands[0].power) == 1:
				if i == (len(Player.hands) - 1):
					print("You lost!\n")
					Player.cash -= Player.bet_amount
				continue
			else:
				print("You won!\n")
				Player.cash += Player.bet_amount
			break
		elif win_or_bust(Player.hands[i].power) == 1:
			print("You won!\n")
			Player.cash += Player.bet_amount
			break
		elif win_or_bust(Player.hands[i].power) < win_or_bust(Dealer.dealer_hands[0].power):
			if i == (len(Player.hands) - 1):
				print("You lost!\n")
				Player.cash -= Player.bet_amount
			continue
		elif win_or_bust(Player.hands[i].power) == 0:
			if i == (len(Player.hands) - 1):
				if win_or_bust(Dealer.dealer_hands[0].power) == 0:
					print("Draw!\n")
				else:
					print("You lost!\n")
					Player.cash -= Player.bet_amount
			continue
		else:
			if i == (len(Player.hands) - 1):
				print("Draw!\n")
			continue
	print("--Dealer's hand--") 
	Dealer.dealer_hands[0].print_hand()
	Dealer.dealer_hands[0].print_hand_power()
	print("Current cash: %d\n" % Player.cash)

def initialize_game(used_cards, Player, Dealer):
	draw(used_cards, Player.hands)
	draw(used_cards, Player.hands)
	print_first_hand(Player.hands)
	Player.hands[0].print_hand_power()
	Dealer.dealer_init(used_cards)
	if check_split(Player.hands[0]) != 0:
		split_hand(Player.hands)
		print_first_hand(Player.hands)
		Player.hands[0].print_hand_power()  

def game_reset(used_cards, Player, Dealer):
	used_cards.clear()
	Player.hands.clear()
	Dealer.dealer_hands.clear()
	Player.hands = [Deck()]
	Dealer.dealer_hands = [Deck()]
