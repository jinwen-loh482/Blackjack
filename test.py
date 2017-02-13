from lib import * 

used_cards = []
hands = [Deck()]
draw(used_cards, hands)
draw(used_cards, hands)
split_hand(hands)
print(hands[0].hand[0].card_chosen_human())
print(hands[1].hand[0].card_chosen_human())