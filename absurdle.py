GREEN = "🟩"
YELLOW = "🟨"
GREY = "⬜"  

def prep_dict(word_lst:list[str], word_length:int) -> set[str]:
  """
  Creates a collection of words from a given dictionary with 
  the given length.

  Args:
      word_lst: Dictionary of all words.
      word_length: Specific length of words to be collected.

  Returns:
      set: collection of all words with the given length.

  Raises:
      ValueError: If given word length is less than 1.

  """
  if word_length < 1:
    raise ValueError("Words cannot be shorter than 1 letter")
  my_set = set()
  for i in range(len(word_lst)):
    if len(word_lst[i]) == word_length:
      my_set.add(word_lst[i])
  return my_set

def is_finished(patterns:list[str]) -> bool:
  """
  Determines whether the game is finished or not.
  The game is finished if the lastest pattern has
  all green tiles.

  Args:
      patterns: Collection of patterns made after each input
        from the player.

  Returns:
      bool: True if the latest pattern has all green tiles, 
        False if not.
  """
  if len(patterns) == 0:
    return False
  last_pattern = patterns.pop()
  patterns.append(last_pattern)
  return last_pattern.find(YELLOW) == -1 and last_pattern.find(GREY) == -1

def record_guess(guess:str, final_word_set:set[str], word_length:int) -> str:
  """
  Prunes the dictionary and updates it to have only the 
  words that produce the best pattern.

  Args:
      guess: Player input word.
      final_word_set: Collection of words that player can
        guess from.
      word_length: Specified length of words.

  Returns:
      str: The pattern that is produced by the msot
        number of words in the dictionary.
  
  Raises: 
      TypeError: If dictionary of words is empty
      ValueError: If user guess has a word different
        word length.
  """
  if len(final_word_set) == 0:
    raise TypeError("Dictionary is Empty")
  if len(guess) != word_length:
    raise ValueError("Guess word is not the correct length.")
  pattern_to_words = {}
  for word in final_word_set:
    pattern = patternFor(word, guess)
    if pattern not in pattern_to_words:
      pattern_to_words[pattern] = set()
    pattern_to_words[pattern].add(word)
  pattern_to_words = dict(sorted(pattern_to_words.items()))
  best_pattern = find_best_pattern(pattern_to_words)
  final_word_set.clear()
  final_word_set.update(pattern_to_words[best_pattern])

  return best_pattern

def find_best_pattern(pattern_to_words:dict[str, set[str]]) -> str:
  """
  Determines the best pattern that is produced by the most number of 
  words in the dictionary.

  Args:
      pattern_to_words: Dictionary with patterns as keys and
        the set of all words that produce that pattern as values.

  Returns:
      str: Finds the pattern that is produced by the most number of
        words.
  """
  max_pattern = ""
  max_set_len = 0
  for pattern in pattern_to_words:
    words = pattern_to_words[pattern]
    if max_set_len < len(words):
      max_set_len = len(words)
      max_pattern = pattern
  return max_pattern

def patternFor(given:str, guess:str) -> str:
  """
  Finds the wordle pattern between a given word and the user's guess.
  It first greens out any letters in the guess that overlap in position
  with the given word. It then yellows any letters in the guess that
  are in the given word but do not overlap in position. Finally, it
  greys any letters in the guess word not in the given word.

  Args:
      given: The actual word that the guess is being compared to.
      guess: The user's guess that will be replaced with the
        colored tiles.

  Returns:
      str: The final pattern derived from the user's guess.
  """
  final = list(guess)
  counter = {}

  for i in range(len(given)):
    if list(counter.keys()).count(given[i]) == 0:
      counter[given[i]] = 1
    else:
      counter[given[i]] = counter[given[i]] + 1

  for i in range(len(given)):
    if given[i] == guess[i]:
      final[i] = GREEN
      counter[given[i]] = counter[given[i]] - 1

  for i in range(len(given)):
    if given.find(guess[i]) != -1 and counter[guess[i]] != 0:
      final[i] = YELLOW
      counter[guess[i]] = counter[guess[i]] - 1

  for i in range(len(given)):
    if final[i] != GREEN and final[i] != YELLOW:
      final[i] = GREY


  return "".join(final)

def main():
  print("Welcome to the game of Absurdle.")
  file_name = input("What dictionary would you like to use? ")
  word_length = int(input("What length word would you like to guess? "))
  with open(file_name, "r") as f:
    word_lst = f.read().splitlines()
  final_word_set = prep_dict(word_lst, word_length)
  guessed_patterns = []
  while not is_finished(guessed_patterns):
    guess = input("> ")
    pattern = record_guess(guess, final_word_set, word_length)
    guessed_patterns.append(pattern)
    print(f": {pattern}")
    print()
  print(f"Absurdle {len(guessed_patterns)}/inf")
  print()
  print("Replay: ")
  for pattern in guessed_patterns:
    print(pattern)

if __name__ == "__main__":
  main()