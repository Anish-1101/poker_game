import timeit

test_cases = [
    ([(10, 'S'), (11, 'S'), (12, 'S'), (13, 'S'), (14, 'S'), (2, 'D'), (3, 'D')], 9),
    ([(10, 'H'), (11, 'H'), (12, 'H'), (13, 'H'), (14, 'H'), (2, 'D'), (3, 'D')], 9),
    ([(10, 'D'), (11, 'D'), (12, 'D'), (13, 'D'), (14, 'D'), (2, 'D'), (3, 'D')], 9),
    ([(10, 'C'), (11, 'C'), (12, 'C'), (13, 'C'), (14, 'C'), (2, 'S'), (3, 'S')], 9),
    ([(2, 'S'), (3, 'S'), (10, 'C'), (11, 'C'), (12, 'C'), (13, 'C'), (14, 'C')], 9),
    ([(6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (2, 'D'), (3, 'D')], 8),
    ([(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (2, 'D'), (3, 'D')], 8),
    ([(6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (2, 'D'), (3, 'D')], 8),
    ([(6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (13, 'H'), (14, 'H')], 8),
    ([(2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (13, 'D'), (14, 'D')], 8),
    ([(2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'D'), (13, 'D'), (14, 'C')], 8),
    ([(9, 'C'), (9, 'D'), (9, 'H'), (9, 'S'), (2, 'D'), (3, 'H'), (4, 'D')], 7),
    ([(8, 'D'), (8, 'H'), (8, 'S'), (8, 'C'), (5, 'D'), (6, 'C'), (7, 'H')], 7),
    ([(14, 'D'), (14, 'C'), (14, 'H'), (14, 'S'), (9, 'C'), (8, 'H'), (7, 'S')], 7),
    ([(3, 'C'), (3, 'D'), (3, 'H'), (10, 'C'), (10, 'D'), (3, 'S'), (12, 'H')], 7),
    ([(10, 'D'), (10, 'C'), (10, 'H'), (10, 'S'), (4, 'D'), (6, 'C'), (8, 'H')], 7),
    ([(10, 'D'), (10, 'C'), (10, 'H'), (7, 'C'), (7, 'D'), (2, 'S'), (3, 'S')], 6),
    ([(5, 'D'), (5, 'C'), (5, 'S'), (2, 'H'), (2, 'C'), (9, 'H'), (8, 'D')], 6),
    ([(13, 'D'), (13, 'C'), (13, 'H'), (4, 'S'), (4, 'C'), (6, 'H'), (7, 'D')], 6),
    ([(6, 'D'), (6, 'C'), (6, 'H'), (11, 'S'), (11, 'D'), (3, 'H'), (2, 'C')], 6),
    ([(14, 'D'), (14, 'C'), (14, 'S'), (3, 'H'), (3, 'D'), (7, 'C'), (8, 'H')], 6),
    ([(2, 'D'), (4, 'D'), (5, 'D'), (7, 'D'), (9, 'D'), (10, 'S'), (11, 'H')], 5),
    ([(14, 'D'), (2, 'D'), (5, 'D'), (8, 'D'), (10, 'D'), (3, 'S'), (6, 'H')], 5),
    ([(2, 'C'), (3, 'C'), (4, 'C'), (6, 'C'), (7, 'C'), (9, 'S'), (10, 'H')], 5),
    ([(6, 'H'), (11, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (2, 'D'), (3, 'C')], 5),
    ([(4, 'S'), (7, 'S'), (9, 'S'), (11, 'S'), (13, 'S'), (10, 'H'), (2, 'D')], 5),
    ([(3, 'S'), (4, 'D'), (5, 'H'), (6, 'C'), (7, 'D'), (9, 'S'), (10, 'D')], 4),
    ([(10, 'S'), (11, 'D'), (12, 'H'), (13, 'C'), (14, 'S'), (2, 'D'), (3, 'H')], 4),
    ([(6, 'D'), (7, 'C'), (8, 'H'), (9, 'S'), (10, 'D'), (2, 'C'), (3, 'S')], 4),
    ([(3, 'S'), (4, 'D'), (5, 'H'), (6, 'C'), (7, 'D'), (7, 'S'), (8, 'D')], 4),
    ([(2, 'C'), (3, 'C'), (4, 'C'), (5, 'D'), (6, 'C'), (13, 'D'), (14, 'H')], 4),
    ([(8, 'C'), (8, 'D'), (8, 'S'), (2, 'H'), (3, 'D'), (4, 'S'), (5, 'H')], 3),
    ([(2, 'D'), (2, 'C'), (2, 'H'), (10, 'D'), (11, 'S'), (13, 'H'), (14, 'S')], 3),
    ([(9, 'D'), (9, 'C'), (9, 'H'), (12, 'D'), (13, 'S'), (14, 'H'), (10, 'S')], 3),
    ([(6, 'D'), (6, 'C'), (6, 'H'), (4, 'D'), (5, 'D'), (9, 'S'), (10, 'S')], 3),
    ([(14, 'D'), (14, 'C'), (14, 'H'), (3, 'D'), (4, 'S'), (6, 'H'), (8, 'S')], 3),
    ([(4, 'D'), (4, 'S'), (7, 'H'), (7, 'D'), (2, 'C'), (3, 'H'), (5, 'S')], 2),
    ([(10, 'D'), (10, 'S'), (13, 'H'), (13, 'D'), (4, 'C'), (8, 'H'), (9, 'S')], 2),
    ([(6, 'D'), (6, 'S'), (14, 'H'), (14, 'D'), (3, 'C'), (5, 'H'), (7, 'S')], 2),
    ([(5, 'D'), (5, 'S'), (9, 'H'), (9, 'D'), (8, 'C'), (3, 'H'), (4, 'S')], 2),
    ([(3, 'D'), (3, 'S'), (11, 'H'), (11, 'D'), (14, 'C'), (7, 'H'), (8, 'S')], 2),
    ([(9, 'H'), (9, 'D'), (6, 'S'), (7, 'C'), (8, 'D'), (2, 'C'), (3, 'H')], 1),
    ([(14, 'H'), (14, 'D'), (10, 'S'), (12, 'C'), (13, 'D'), (4, 'C'), (5, 'H')], 1),
    ([(2, 'H'), (2, 'D'), (6, 'S'), (7, 'C'), (8, 'D'), (10, 'C'), (11, 'H')], 1),
    ([(11, 'D'), (11, 'S'), (9, 'D'), (10, 'D'), (8, 'D'), (3, 'H'), (4, 'S')], 1),
    ([(3, 'H'), (3, 'D'), (14, 'S'), (5, 'C'), (6, 'D'), (9, 'C'), (10, 'H')], 1)
]

def run_tests():
    for hand, expected_rank in test_cases:
        assert eval_hand(hand)[0] == expected_rank, f"Failed on hand {hand}"

def record_speed():
  execution_time = timeit.timeit(run_tests, number=1000)
  print(f"Execution time for 1000 runs: {execution_time} seconds")


def eval_hand(hand):
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
