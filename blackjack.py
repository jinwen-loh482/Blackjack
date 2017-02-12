from lib import * 

used_cards = []
player = Player()
dealer = Dealer()
initialize_game(used_cards, player, dealer)
player.bet()
print(player.bet_amount)