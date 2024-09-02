import itertools, os, pygame, random
from cards import *
from settings import *

class Hand:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.winner = None
    self.font = pygame.font.Font(GAME_FONT, 120)
    self.win_rotation_angle = random.uniform(-10, 10)
    self.p1 = Player()
    self.p2 = Player()
    self.flop = Flop()
    self.player_list = [self.p1, self.p2]
    self.dealer = Dealer(self.player_list, self.flop)

  def render_cards(self):
    # Draw cards at current positions
    for player in self.player_list:
      for card in player.cards:
        self.display_surface.blit(card.card_surf, card.start_position)
    for card in self.flop.cards:
      self.display_surface.blit(card.card_surf, card.position)

  def render_winner(self):
    if self.dealer.determined_winner is not None:
      # Set the text and color based on the winner
      if self.dealer.determined_winner == "Player 1":
        text = "Player 1 Wins!"
        text_color = (115, 235, 0) # Blue
      elif self.dealer.determined_winner == "Player 2":
        text = "Player 2 Wins!"
        text_color = (135, 206, 235) # Green
      elif self.dealer.determined_winner == "Tie":
        text = "Split Pot!"
        text_color = (255, 192, 203) # Pink

      coordinates = (520, 100)
      # Winner text
      text_surface = self.font.render(text, True, text_color)
      text_rect = text_surface.get_rect()
      text_rect.topleft = coordinates
      rotated_surface = pygame.transform.rotate(text_surface, self.win_rotation_angle)
      rotated_rect = rotated_surface.get_rect(center=text_rect.center)
      self.display_surface.blit(rotated_surface, rotated_rect)

  def update(self):
    self.dealer.update()
    self.render_cards()
    self.render_winner()


class Dealer():
  def __init__(self, players, flop):
    self.determined_winner = None
    self.players_list = players
    self.num_players = len(players)
    self.current_player_index = 0
    self.current_flop_index = 0
    self.printed_flop = False
    self.deck = self.generate_deck()
    random.shuffle(self.deck)
    self.animating_card = None
    self.can_deal = True
    self.can_deal_flop = False

    self.can_deal_turn = False
    self.can_deal_river = False

    self.last_dealt_card_time = None
    self.last_dealt_flop_time = None
    self.dealt_cards = 0
    self.flop = flop
    self.display_surface = pygame.display.get_surface()

    self.mouse_down = False
    self.player_checked = False


  def generate_deck(self):
    fresh_deck = []
    for cv in cardvalues:
      for cs in cardsuits:
        fresh_deck.append(Card(cv, cs))
    return fresh_deck

  def cooldowns(self):
    # Need to use delta time
    current_time = pygame.time.get_ticks()
    if self.last_dealt_card_time and current_time - 200 > self.last_dealt_card_time:
      self.can_deal = True

    if self.last_dealt_flop_time and \
            current_time - random.randint(120, 200) > self.last_dealt_flop_time:
      self.can_deal_flop = True

  def animate_hole_card(self, card):
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - self.last_dealt_card_time

    current_card = card
    animation_duration = 200

    if elapsed_time < animation_duration:
      # Calculate the increment for each frame to move the card and update position
      x_orig, y_orig = current_card.orig_position
      x_final, y_final = current_card.position
      elapsed_ratio = elapsed_time / animation_duration
      x_change = x_orig + (x_final - x_orig) * elapsed_ratio
      y_change = y_orig + (y_final - y_orig) * elapsed_ratio
      current_card.start_position = (x_change, y_change)
    else:
      card.animation_complete = True

  def deal_hole_cards(self):
    if self.can_deal:
      # Deal card to current player's hand
      current_player = self.players_list[self.current_player_index]
      current_player.cards.append(self.deck[-1])

      # Card one of two; sets positions for both players
      if self.current_player_index == 0:
        if len(current_player.cards) == 1:
          current_player.cards[0].position = (P1_C1[0], current_player.cards[0].card_y)
        elif len(current_player.cards) == 2:
          current_player.cards[1].position = (P1_C2[0], current_player.cards[1].card_y)
        self.animating_card = current_player.cards[-1]
      # Card two of two
      elif self.current_player_index == 1:
        if len(current_player.cards) == 1:
          current_player.cards[0].position = ((P2_C1[0] - current_player.cards[0].card_surf.get_width() - 80), current_player.cards[0].card_y)
        elif len(current_player.cards) == 2:
          current_player.cards[1].position = ((P2_C2[0] - current_player.cards[1].card_surf.get_width() - 20), current_player.cards[1].card_y)
        self.animating_card = current_player.cards[-1]

      if self.animating_card:
        self.last_dealt_card_time = pygame.time.get_ticks()
        self.animate_hole_card(self.animating_card)

      # Play audio
      # self.card_audio()

      # Remove dealt card from deck; change player index; prompt card dealing cooldown
      self.deck.pop(-1)
      self.current_player_index = (self.current_player_index + 1) % self.num_players
      self.can_deal = False

  def deal_flop(self):
    # Set flop card locations
    flop_x = self.players_list[0].cards[0].card_surf.get_width()
    if self.current_flop_index == 0:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2
    elif self.current_flop_index == 1:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() + 20)
    elif self.current_flop_index == 2:
      flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() * 2 + 40)

    if self.can_deal and self.can_deal_flop and self.dealt_cards - (self.num_players * 2) < 3:
      self.flop.cards.append(self.deck[-1])
      self.flop.cards[self.current_flop_index].position = (flop_x, self.flop.cards[self.current_flop_index].card_y)
      self.deck.pop(-1)
      self.last_dealt_flop_time = pygame.time.get_ticks()
      self.can_deal_flop = False
      self.current_flop_index += 1

  def deal_turn(self):
      if self.can_deal_turn:
          flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() * 3 + 40)  
          self.flop.cards.append(self.deck[-1])
          self.deck.pop(-1)
          self.flop.cards[3].position = (flop_x, self.flop.cards[3].card_y)
          self.can_deal_turn = False
          print("Turn card dealt.")

  def deal_river(self):
      if self.can_deal_river:
          flop_x = self.players_list[0].cards[0].card_surf.get_width() * 2 + (self.players_list[0].cards[0].card_surf.get_width() * 4 + 60)  
          self.flop.cards.append(self.deck[-1])
          self.deck.pop(-1)
          self.flop.cards[4].position = (flop_x, self.flop.cards[4].card_y)
          self.can_deal_river = False
          print("River card dealt.")

  def calculate_card_position(self, index):
      # Calculate the x-position based on the index of the card
      card_width = self.players_list[0].cards[0].card_surf.get_width()
      spacing = 20  # Space between cards
      start_x = card_width * 2
      return start_x + (card_width + spacing) * index


    # Print length of deck after card is dealt for troubleshooting
    # print(f"{len(self.deck)} cards left in deck; {self.update_dealt_card_count()} dealt.")

  def eval_hand(self, hand):
    # input - flop cards + player cards
    # card_values = array of player card values and flop card values
    # card_suits = array of player card suits and flop card suits 

    card_values = [c[0] for c in hand]
    card_suits = [c[1] for c in hand]

    #suit count function
    suit_count = {}

    for suit in card_suits:
      if suit in suit_count:
        suit_count[suit] += 1
      else:
        suit_count[suit] = 1
    
    # value count function
    value_count = {}

    for value in card_values:
      if value in value_count:
        value_count[value] += 1
      else:
        value_count[value] = 1

    # number of pairs counter
    number_of_pairs = 0
    pair_values = []
    for value in set(card_values):
      if value_count[value] == 2:
        number_of_pairs += 1
        pair_values.append(value)

    # 9 royal flush - gather suited values & check if top five highest values are 10, J , Q, K , A
    suited_values = []
    for suit in suit_count:
      if suit_count[suit] >= 5:
        for i in range(len(card_values)):
            if card_suits[i] == suit:
              suited_values.append(card_values[i])
        if sorted(suited_values)[-5:] == [10, 11, 12, 13, 14]:
          return 9, 14

    # 8 straight flush - sort suited values & check if they are consecutive
    suited_straight_counter = 1
    sorted_suited_values = sorted(suited_values)

    # check for ace low straight flush
    if set([2, 3, 4, 5, 14]).issubset(sorted_suited_values):
      return 8, max(suited_values)
    
    if len(sorted_suited_values) > 4:
      for i in range(len(suited_values)-1):
        if sorted_suited_values[i+1] - sorted_suited_values[i] == 1:
          suited_straight_counter += 1
          if suited_straight_counter >= 5:
            return 8, max(suited_values)
        else:
          suited_straight_counter = 1

    # 7 quads - check if card_values has four of a kind
    for value in card_values:
      if value_count[value] == 4:
        return 7, value 

    # 6 full-house logic - check if card_values has one three of a kind and at least one pair
    for value in card_values:
      if value_count[value] == 3 and number_of_pairs >= 1:
        return 6, value 

    # 5 flush logic - check if card_suits has five of the same
    for suit in card_suits:
      if suit_count[suit] >= 5:
        highest_flush_card = max(suited_values)
        return 5, highest_flush_card 

    # 4 straight logic -  check if card_values has five in a row
    straight_counter = 1
    sorted_values = sorted(set(card_values))

    # check for ace low straight
    if set([2, 3, 4, 5, 14]).issubset(sorted_values):
      return 4, max(card_values)
    
    straight_values = []
    for i in range(len(sorted_values)-1):
      if sorted_values[i+1] - sorted_values[i] == 1:
        straight_counter += 1
        straight_values.append(sorted_values[i+1])
        if straight_counter >= 5:
          return 4, max(straight_values)
      else:
        straight_counter = 1

        # tie breaker improvement - consider > 5 card straights

    # 3 three of a kind - check if card_values have three of the same
    for value in card_values:
      if value_count[value] == 3:
        return 3, value 

    # 2 two pair - check number of pairs value
    if number_of_pairs == 2:
      return 2, max(pair_values) 
    if value_count[value] == 2:
      number_of_pairs += 1

      # tie breaker improvement - consider value of second pair if top pair is same

    # 1 one pair - check number of pairs value
    if number_of_pairs == 1:
      return 1, max(pair_values) 

    # 0 high card - find the highest card value of player_ values
    else:
      return 0, max(card_values) 

    
  def eval_winner(self, hand_to_eval):
    eval_cards = [(value_dict[x[0]], x[1]) for x in hand_to_eval]
    player_1_combo = self.eval_hand(eval_cards[:7])
    player_2_combo = self.eval_hand(eval_cards[7:])
    
    if player_1_combo[0] > player_2_combo[0]:
      print(f"P1 WIN: {self.eval_hand(eval_cards[:7])}")
      return "Player 1"
    elif player_2_combo[0] > player_1_combo[0]:
      print(f"P2 WIN: {self.eval_hand(eval_cards[7:])}")
      return "Player 2"
    else:
      # tie-break info using the highest card info (second value in the tuple returned from eval_hand)
      if player_1_combo[1] > player_2_combo[1]:
        print(f"P1 WIN BY HIGH CARD: {self.eval_hand(eval_cards[:7])}")
        return "Player 1"
      elif player_2_combo[1] > player_1_combo[1]:
        print(f"P2 WIN BY HIGH CARD: {self.eval_hand(eval_cards[7:])}")
        return "Player 2" 
      else:
        print("SPLIT")
        return "Tie"

  # Print to console
  def print_hands(self):
    for i in range(len(self.players_list)):
      print(f"P{i+1}: {[card.id for card in self.players_list[i].cards]}")
    print(f"FL: {[card.id for card in self.flop.cards]}")

  # Getter for number of dealt cards
  def update_dealt_card_count(self):
    total_card_count = 0
    for player in self.players_list:
      total_card_count += len(player.cards)
    total_card_count += len(self.flop.cards)
    return total_card_count

  def update(self):
    self.dealt_cards = self.update_dealt_card_count()
    self.cooldowns()

    if self.dealt_cards < (self.num_players * 2):
      self.deal_hole_cards()

    if self.animating_card:
      self.animate_hole_card(self.animating_card)

    # Deal flop after hole cards are dealt and animations are done
    if self.dealt_cards == (self.num_players * 2) and (not self.animating_card or self.animating_card.animation_complete) and self.player_checked:
      self.can_deal_flop = True
      self.deal_flop()
    # Slightly redundant
    if self.dealt_cards < (self.num_players * 2) + 5 and self.can_deal_flop:
      self.deal_flop()
    # Print hand data to console
    if not self.printed_flop and self.dealt_cards == (self.num_players * 2) + 5:
      self.print_hands()
      self.printed_flop = True
    
    if self.can_deal_flop:
      self.deal_turn()

    if self.can_deal_flop:
      self.deal_river()

    if self.dealt_cards == ((self.num_players * 2) + 5) and self.determined_winner is None:
      eval_cards = [card_id.id for card_id in self.players_list[0].cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.flop.cards] + [card_id.id for card_id in self.players_list[1].cards]
      self.determined_winner = self.eval_winner(eval_cards) 