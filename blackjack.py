from lib import * 

used_cards = []
player = Player()
dealer = Dealer()
while player.cash >= 10:
	initialize_game(used_cards, player, dealer)
	player.bet()
	player.draw_sequence(used_cards)
	check_win(player, dealer)
	print("Next round?")
	response = get_yes_no()
	if response:
		os.system('clear')
		game_reset(used_cards, player, dealer)
		continue
	else:
		os.system('clear')
		print("Thank you for playing!")
		print("Final cash: $%d" % player.cash)
		quit()