import random

# SI 507 Fall 2018
# Homework 3 - Code

##COMMENT YOUR CODE WITH:
# Section Day/Time: Wednesday
# People you worked with: feiyi

######### DO NOT CHANGE PROVIDED CODE #########
### Scroll down for assignment instructions.
#########

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)

	def deal(self, hands_num, cards_per_hand):
		hands_list = []
		for i in range(hands_num):
			hands_list.append(Hand([]))
		if cards_per_hand == -1:
			for j in range(len(self.cards)):
				hands_list[j%hands_num].add_card(self.pop_card())

		else:
			for i in range(cards_per_hand):
				for j in range(hands_num):
					hands_list[j].add_card(self.pop_card())
		return hands_list

class Hand:
	# create the Hand with an initial set of cards
	# param: a list of cards
	def __init__(self, init_cards):
		self.cards = init_cards 
		self.books = []

	# add a card to the hand
	# silently fails if the card is already in the hand
	# param: the card to add
	# returns: nothing
	def add_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	# remove a card from the hand
	# param: the card to remove
	# returns: the card, or None if the card was not in the Hand
	def remove_card(self, card):
		i = 0
		for card1 in self.cards:
			if str(card1)==str(card):
				return self.cards.pop(i)
			else:
				i+=1


	# draw a card from a deck and add it to the hand
	# side effect: the deck will be depleted by one card
	# param: the deck from which to draw
	# returns: nothing
	def draw(self, deck):
		card = deck.pop_card()
		self.add_card(card)

	def remove_pairs(self):
		# for card1 in self.cards:
		# 	for card2 in self.cards:
		# 		if card1.rank_num == card2.rank_num and card1.suit != card2.suit:
		# 			self.remove_card(card1)
		# 			self.remove_card(card2)
		# 			break
		i = 0
		range1 = len(self.cards) - 1
		range2 = len(self.cards)
		while i < range1:
			j = i + 1
			remove = False
			while  j < range2:
				if self.cards[i].rank == self.cards[j].rank:
					self.cards.pop(j)
					self.cards.pop(i)
					range1-=2
					range2-=2
					remove = True
					break
				else:
					j+=1

			if not remove:
				i+=1

	def ask_for_valid_request(self):
		request_not_valid = True
		while request_not_valid:
			#rank_requested = int(input("Please choose a card rank you would like to ask the other player if they have (between 1-13): "))
			rank_requested = self.random_request()
			for card in self.cards:
				if card.rank_num == rank_requested:
					request_not_valid = False
					break
			if request_not_valid:
				print("Invalid Request!")
				print("You must choose a card rank you have!")
		return rank_requested


	def random_request(self):
		rank_list = []
		for card in  self.cards:
			if card.rank_num not in rank_list:
				rank_list.append(card.rank_num)
		return rank_list[random.randint(0,len(rank_list) - 1)]

	def show_cards(self):
		print("You currently have: ")
		for card in self.cards:
			print(str(card))

	def remove_books(self):
		rank_count = [0]*13
		for card in self.cards:
			rank_count[card.rank_num - 1]+=1

		book_flag = False

		for i in range(len(rank_count)):
			if rank_count[i] == 4:
				book_flag = True
				book_rank = i + 1
				self.books.append(book_rank)
				print("You have a new book of " + str(book_rank))
				break

		if book_flag:
			i = 0
			removed_num = 0
			while removed_num < 4:
				if self.cards[i].rank_num == book_rank:
					self.cards.pop(i)
					removed_num+=1
				else:
					i+=1

		return book_flag

def play(player_id, player_num, deck, players):
	print("Player" + str(player_id + 1) + "'s turn:")
	player1 = players[player_id]

	another_player_id = random.randint(0, player_num - 1) # pick another player randomly
	while(another_player_id == player_id):
		another_player_id = random.randint(0, player_num - 1)
	player2 = players[another_player_id]

	player1.show_cards()
	if len(player1.cards) != 0:
		rank_requested = player1.ask_for_valid_request()
		fish_flag = True
		range1 = len(player2.cards)
		i = 0
		j = 0
		while i < range1:
			if player2.cards[i].rank_num == rank_requested:
				j+=1
				player1.add_card(player2.cards[i])
				player2.cards.pop(i)
				fish_flag = False
				range1-=1
			else:
				i+=1
		if fish_flag:
			print("Go fish!")
			card_fish = deck.pop_card()
			player1.add_card(card_fish)
			print("Player"+ str(player_id + 1) + " draws " + str(card_fish))
			if card_fish.rank_num == rank_requested:
				print("It's still player" + str(player_id + 1) + "'s turn.")
				return 1
			else:
				return 0
		else:
			print("Player"+ str(player_id + 1) + " gets " + str(j) + " cards with rank " + str(rank_requested))
			return 0
	else:
		draw_card = deck.pop_card()
		player1.cards.append(draw_card)
		print("Player1 has no card in hand.")
		print("Player1 draws " + str(draw_card) + " from the deck.")
		return 0


				

#main
player_num = int(input("How many computer players do you want? (2-4) "))
deck = Deck()
deck.shuffle()
# players = []
# for i in range(player_num):
# 	hand = Hand([])
# 	players.append(hand)
# 	for j in range(7):
# 		players[i].draw(deck)
players = deck.deal(player_num, 7) #change to deal
num_of_books = 0
player_id = 0

print("Game Start")
print("==========")
while num_of_books < 13:
	if len(deck.cards) == 0 and player_num != 2:
		break
	if (play(player_id, player_num, deck, players)):
		if players[player_id].remove_books():
			num_of_books+=1
	else:
		if players[player_id].remove_books():
			num_of_books+=1
		player_id = (player_id + 1) % player_num

	print("==============")
	for i in range(player_num):
		print("Player" + str(i + 1) + " has books of: ")
		print(players[i].books)
	print("==============")


print("==============")
book_max = 0
for i in range(player_num):
	if book_max < len(players[i].books):
		book_max = len(players[i].books)
print("==============")

for i in range(player_num): #possible for mulfiplayers to win
	if book_max == len (players[i].books):
		print("Player" + str(i + 1) + " wins")



