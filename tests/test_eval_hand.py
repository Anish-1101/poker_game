def eval_hand_test():
    # Test Royal Flush
    assert eval_hand([(10, 'S'), (11, 'S'), (12, 'S'), (13, 'S'), (14, 'S'), (2, 'D'), (3, 'D')])[0] == 9, "Failed on Royal Flush"

    # Test Straight Flush
    assert eval_hand([(6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (2, 'D'), (3, 'D')])[0] == 8, "Failed on Straight Flush"

    # Test Four of a Kind
    assert eval_hand([(9, 'C'), (9, 'D'), (9, 'H'), (9, 'S'), (2, 'D'), (3, 'H'), (4, 'D')])[0] == 7, "Failed on Four of a Kind"

    # Test Full House
    assert eval_hand([(10, 'D'), (10, 'C'), (10, 'H'), (7, 'C'), (7, 'D'), (2, 'S'), (3, 'S')])[0] == 6, "Failed on Full House"

    # Test Flush
    assert eval_hand([(2, 'D'), (4, 'D'), (5, 'D'), (7, 'D'), (9, 'D'), (10, 'S'), (11, 'H')])[0] == 5, "Failed on Flush"

    # Test Straight
    assert eval_hand([(3, 'S'), (4, 'D'), (5, 'H'), (6, 'C'), (7, 'D'), (9, 'S'), (10, 'D')])[0] == 4, "Failed on Straight"

    # Test Three of a Kind
    assert eval_hand([(8, 'C'), (8, 'D'), (8, 'S'), (2, 'H'), (3, 'D'), (4, 'S'), (5, 'H')])[0] == 3, "Failed on Three of a Kind"

    # Test Two Pair
    assert eval_hand([(4, 'D'), (4, 'S'), (7, 'H'), (7, 'D'), (2, 'C'), (3, 'H'), (5, 'S')])[0] == 2, "Failed on Two Pair"

    # Test One Pair
    assert eval_hand([(9, 'H'), (9, 'D'), (6, 'S'), (7, 'C'), (8, 'D'), (2, 'C'), (3, 'H')])[0] == 1, "Failed on One Pair"

    print("All tests passed!")

def eval_hand(hand):
    # Return ranking followed by tie-break information.

    # input - flop cards + player cards
    # player_values = array of player card values
    # player_suits = array of player suits 
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
    for value in set(card_values):
      if value_count[value] == 2:
        number_of_pairs += 1

    # 9 royal flush - combine flush logic & straight logic & (check if card_values has  (10,J,Q,K,A) and if these five cards are all the same suit)
    suited_values = []
    for suit in suit_count:
      if suit_count[suit] >= 5:
        for i in range(len(card_values)):
            if card_suits[i] == suit:
              suited_values.append(card_values[i])
        if sorted(suited_values) == [10, 11, 12, 13, 14]:
          return 9, max(card_values)

    # 8 straight flush - combine flush logic & straight logic (check if card_values has five in a row and if these five cards are all the same suit)
    suited_straight_counter = 1
    if len(sorted(suited_values)) > 4:
      for i in range(len(suited_values)-1):
        if sorted(suited_values)[i+1] - sorted(suited_values)[i] == 1:
          suited_straight_counter += 1
          if suited_straight_counter >= 5:
            return 8, max(suited_values)
        else:
          suited_straight_counter = 1

    # 7 quads - check if card_values has four of a kind
    for value in card_values:
      if value_count[value] == 4:
        return 7, value # add tie break info

    # 6 full-house logic - check if card_values has one three of a kind and one pair of a different value
    for value in card_values:
      if value_count[value] == 3 and number_of_pairs >= 1:
        return 6, value # add tie break info

    # 5 flush logic - check if card_suits has five of the same
    for suit in card_suits:
      if suit_count[suit] >= 5:
        highest_flush_card = max(suited_values)
        return 5, highest_flush_card # add tie break info

    # 4 straight logic -  check if card_values has five in a row
    straight_counter = 1
    sorted_values = sorted(set(card_values))
    for i in range(len(sorted_values)-1):
      if sorted_values[i+1] - sorted_values[i] == 1:
        straight_counter += 1
        if straight_counter >= 5:
          return 4, max(card_values) # add tie break info
      else:
        straight_counter = 1
      # have to consider A for high card and low card straight

    # 3 three of a kind - check if card_values have three of the same
    for value in card_values:
      if value_count[value] == 3:
        return 3, value # add tie break info

    # 2 two pair - check if card_values have two duplicates
    if number_of_pairs == 2:
      return 2, max(card_values) # add tie break info
    if value_count[value] == 2:
      number_of_pairs += 1

    # 1 one pair - check if card_values have any duplicates
    if number_of_pairs == 1:
      return 1, max(card_values) # add tie break info

    # 0 high card - find the highest card value of player_ values
    else:
      return 0, max(card_values)
      # return highest value in player_values





