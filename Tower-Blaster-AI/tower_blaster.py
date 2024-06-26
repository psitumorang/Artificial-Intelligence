import random

def setup_bricks():
    """
    Creates a main pile of 60 bricks, represented as a list containing the integers 1 – 60.
    Creates a discard pile of 0 bricks, represented as an empty list.

    This function returns both lists.

    The method of returning 2 things from a function is to make a tuple out of the return
    values. For an example of this, refer to the lecture slides/code where we return both the
    maximum and minimum in a list.
    """

    main_pile = []
    discard_pile = []

    for i in range(1, 61):
        main_pile.append(i)

    piles = (main_pile, discard_pile)
    return piles

def shuffle_bricks(bricks):
    """
    Shuffle the given bricks (represented as a list).     
	This function does not return anything.
   
    """
    random.shuffle(bricks)


def check_bricks(main_pile, discard):
    """
    Check if there are any cards left in the given main pile of bricks.
    If not, shuffle the discard pile (using the shuffle function) and move those bricks to the main pile.
    Then turn over the top card to be the start of the new discard pile.
    """
    if (main_pile == []):
        random.shuffle(discard) # shuffle the discard pile
        main_pile = discard  # main pile becomes the discard pile
        discard = []  # empty the discard pile
        discard.append(main_pile[0])  # add the top brick from the main pile to start the new discard pile
        main_pile.pop(0)  # remove the top brick from the main pile

    piles = (main_pile, discard)

    return piles

def check_tower_blaster(tower):
    """
    Given a tower (the user’s or the computer’s list), determine if stability has been achieved.
    This function returns a boolean value.
    """

    check_list = sorted(tower)  # we want to sort the tower and store it in a check list
    return check_list == tower  # if the sorted list == tower, then we conclude that bricks are ascending

def get_top_brick(brick_pile):
    """
    Remove and return the top brick from any given pile of bricks. This can be the main_pile, the
    discard pile, or player tower or the computer's tower. In short, remove and return the first
    element of any given list.

    It is used at the start of game play for dealing bricks. This function will also be used during each
    player’s turn to take the top brick from either the discarded brick pile or from the main pile.

    Note: Brick piles are vertically oriented structures, with the top having index 0.
    This function must return an integer.
    """

    top_brick = brick_pile[0]
    brick_pile = brick_pile.pop(0)

    return top_brick

def deal_initial_bricks(main_pile):
    """
    Start the game by dealing two sets of 10 bricks each, from the given main_pile.

    The computer is always the first person that gets dealt to and always plays first.
    """

    computer_hand = []
    player_hand = []

    counter = 1
    while counter <= 10: # we want to repeat the process 10 times to give each hand ten bricks
        i = random.choice(main_pile) # choose a random brick from the main pile
        computer_hand.append(i) # append that randomly chosen brick to computer hand (computer gets dealt first)
        main_pile.remove(i) # remove the brick from the main pile

        i = random.choice(main_pile) # same process for the player
        player_hand.append(i)
        main_pile.remove(i)

        counter += 1 # repeat 10 times to give each 10 bricks

    towers = (computer_hand, player_hand)
    return towers

def add_brick_to_discard(brick, discard):
    """
    Add the given brick (represented as an integer) to the top of the given discard pile (which is a
    list)

    this function does not return anything.
    """
    discard.insert(0, brick)

def find_and_replace(new_brick, brick_to_be_replaced, tower, discard):
    """
    Find the given brick to be replaced (represented by an integer) in the given tower and replace it
    with the given new brick.

    Return True if the given brick is replaced, otherwise return False.
    """

    if brick_to_be_replaced in tower:
        brick_location = tower.index(brick_to_be_replaced) # finds the index of the brick to be replaced
        tower.remove(brick_to_be_replaced) # removes the brick to be replaced from the tower
        tower.insert(brick_location, new_brick) # inserts the new brick to the tower; the location is based on the index we found before
        discard.insert(0, brick_to_be_replaced) # inserts the brick to be replaced to the top of the discard pile
        return True
    else:
        return False

###############################
### computer_play functions ###
###############################

def bricks_to_keep(tower):
    """
    Generates a list of bricks to keep given the current tower.

    This is based on criteria set in this function. The criteria is very simple.
    The computer will determine whether to keep each position based on the below:
    criteria = [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9]
    criteria = [1 to 6, 7 to 12, 13 to 18, 19 to 24, 25 to 30, 31 to 36, 37 to 42, 43 to 48, 49 to 54, 55 to 60]

    For example, if the current tower is [1, 8, 22, 14, 54, 25, 3, 31, 48, 59]
    the function will return bricks_to_keep = [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]
    because 1 meets the pos_0 criteria (1 to 6), 8 meets the pos_1 criteria (7 to 12), and so on.
    note that 22 does not meet the pos_3 criteria (13 to 18) and the function inserts 0 in its location.

    Zeros indicate locations of the bricks in current tower that needs to be replaced.
    Non-zeroes indicate the bricks in the current tower that will be kept.

    For example: [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]
    """

    pos_0 = [1, 2, 3, 4, 5, 6]
    pos_1 = [7, 8, 9, 10, 11, 12]
    pos_2 = [13, 14, 15, 16, 17, 18]
    pos_3 = [19, 20, 21, 22, 23, 24]
    pos_4 = [25, 26, 27, 28, 29, 30]
    pos_5 = [31, 32, 33, 34, 35, 36]
    pos_6 = [37, 38, 39, 40, 41, 42]
    pos_7 = [43, 44, 45, 46, 47, 48]
    pos_8 = [49, 50, 51, 52, 53, 54]
    pos_9 = [55, 56, 57, 58, 59, 60]
    criteria = [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9]

    bricks_to_keep = []
    index_counter = 0
    for i in tower:
        if i in criteria[index_counter]: # if the current brick in that position meets the respective position criteria
            bricks_to_keep.append(i) # the brick is added to "bricks to keep" list
        else:
            bricks_to_keep.append(0)  # we'll mark the bricks we want to replace with 0s

        index_counter += 1

    return bricks_to_keep # i.e. [1, 8, 0, 0, 0, 0, 0, 0, 0, 59] where zeroes indicate location of bricks in tower to replace

def generate_search_list(bricks_to_keep):
    """
    This function generates a "search list" based on "bricks to keep" input.

    For example, if the current tower is [1, 8, 22, 14, 54, 25, 3, 31, 48, 59]
    we want to keep bricks 1, 8, and 59 based on the criteria we set in bricks_to_keep function.
    That function will return bricks_to_keep = [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]
    Where 0s are our markers of the locations of bricks that need to be replaced.

    This function iterates through the bricks_to_keep list = [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]
    If it sees a non-zero number (i.e. 1) it appends an empty list to the search list
    If it otherwise sees a zero, it appends the criteria set for the position the 0 is located.

    The result is a list of lists of bricks we are "searching."
    The computer uses this list to determine whether to take from the top of the discard or main piles.

    :param bricks_to_keep:
    :return: search_list
    """
    pos_0 = [1, 2, 3, 4, 5, 6]
    pos_1 = [7, 8, 9, 10, 11, 12]
    pos_2 = [13, 14, 15, 16, 17, 18]
    pos_3 = [19, 20, 21, 22, 23, 24]
    pos_4 = [25, 26, 27, 28, 29, 30]
    pos_5 = [31, 32, 33, 34, 35, 36]
    pos_6 = [37, 38, 39, 40, 41, 42]
    pos_7 = [43, 44, 45, 46, 47, 48]
    pos_8 = [49, 50, 51, 52, 53, 54]
    pos_9 = [55, 56, 57, 58, 59, 60]
    criteria = [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9]

    search_list = []

    index_counter = 0
    for i in bricks_to_keep:
        if (i == 0): # this tells the computer that it needs to start "searching" for bricks to fill this location
            search_list.insert(index_counter, criteria[index_counter]) # add the search list with a list of bricks that meets the criteria for the respective location
        else:
            search_list.append([]) # if i is non-zero, we tell the computer to not search for new bricks for this position, hence we add an empty list.

        index_counter += 1

    return search_list

def check_pile(search_list, pile):
    """
    Given a search list and a discard or main pile, checks to see if top of pile is part of the search list.
    If it is, the function returns True and the index of the location of where we should put the brick.
    """

    location_key = []  # location key tells you where to put the top brick of the given pile if it is part of the search list
    for i in search_list: # we iterate through search list, which is a list of lists
        if pile[0] in i:  # if top of pile is in the search list
            location_key.append(pile[0])  # append the top brick to the location key
        else:
            location_key.append(0)  # else append 0

    # for example, say top discard brick is 27
    # and search list = [[], [], [13, 14, 15, 16, 17, 18], [], [25, 26, 27, 28, 29, 30], ...]
    # the loop would create location_key = [0, 0, 0, 0, 27, 0, 0, 0, 0, 0]
    # if the top brick is not part of the search list, then location_key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if location_key == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        take_top_brick = False
        replace_index = None
    else:
        take_top_brick = True
        replace_index = location_key.index(pile[0]) # say if location_key = [0, 0, 0, 0, 27, 0, 0, 0, 0, 0], this will return the location of 27

    return_value = (take_top_brick, replace_index)

    return return_value


def computer_play(tower, main_pile, discard):
    """
    The general strategy for the computer is fairly simple:

    Each of the ten positions in the tower has a criteria.
    If the current brick meets that position's criteria, keep the brick, otherwise replace it.

    The criteria is set to equal [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9]

    pos_0 = [1, 2, 3, 4, 5, 6]
    pos_1 = [7, 8, 9, 10, 11, 12]
    pos_2 = [13, 14, 15, 16, 17, 18]
    pos_3 = [19, 20, 21, 22, 23, 24]
    pos_4 = [25, 26, 27, 28, 29, 30]
    pos_5 = [31, 32, 33, 34, 35, 36]
    pos_6 = [37, 38, 39, 40, 41, 42]
    pos_7 = [43, 44, 45, 46, 47, 48]
    pos_8 = [49, 50, 51, 52, 53, 54]
    pos_9 = [55, 56, 57, 58, 59, 60]

    For example, if the computer tower is [1, 8, 22, 14, 54, 25, 3, 31, 48, 59]
    The computer will keep bricks         [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]
    This is because 1 meets the pos_0 criteria, 8 meets the pos_1 criteria, and 59 meets the pos_9 criteria

    The computer then will generate a search list, which is based on the criteria above.

    For example above, only pos_0, pos_1, and pos_9 has a brick that meets the criteria for each position
    The search list will simply be pos_2, pos_3, and all other positions with bricks that do not meet the criteria.
    Such as search_list = [[], [], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24], ... ]

    The computer will then look at the top discard and main pile bricks and and see if either is part of the search list.
    If either one is, we take that brick and put it in the tower.
    We then generate a new "keep bricks" list and a new "search list" based on the new tower structure.

    For example:

    computer_tower = [1, 8, 22, 14, 54, 25, 3, 31, 48, 59]   -> gives us the list of bricks to keep
    keep_bricks    = [1, 8, 0, 0, 0, 0, 0, 0, 0, 59]   -> search list then becomes
    search_list    = [[], [], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24], ... ]

    top_discard_brick = [13]   -> the computer then iterates through search list and see that 13 is part of pos_2

    new_computer_tower = [1, 8, 13, 14, 54, 25, 3, 31, 48, 59]  -> note 13 is now is in position 2
    keep_bricks        = [1, 8, 13, 0, 0, 0, 0, 0, 0, 59]
    search_list        = [[], [], [], [19, 20, 21, 22, 23, 24], ... ] -> pos_2 no longer part of our search list

    top_discard_brick = [2]    -> the computer does not select this because it is not part of the search list
    top_main_pile_brick = [23] -> the computer takes this brick because it is part of the current search list (pos_3)

    new_computer_tower = [1, 8, 13, 23, 54, 25, 3, 31, 48, 59]
    keep_bricks        = [1, 8, 13, 23, 0, 0, 0, 0, 0, 59]
    search_list        = [[], [], [], [], ... ]

    And the process go on until the keep_bricks list is full and search_list is empty.
    At that point the function check_tower_blaster will determine that the structure has been completed.
    """

    # from the current tower, select which bricks to keep
    keep_bricks = bricks_to_keep(tower)

    # from the list of bricks to keep, generate a search list
    search_list = generate_search_list(keep_bricks)

    # check the top of the discard pile and see if it is in the search list
    check_discard = check_pile(search_list, discard)
    take_top_discard = check_discard[0]  # if top discard brick is part of the search list, take_top_discard = True, otherwise false
    replace_index_discard = check_discard[1]  # if the above is True, replace index will indicate the index of the current brick in the tower that will be replaced by the new brick

    check_main = check_pile(search_list, main_pile) # checks the top of the main pile
    take_top_main = check_main[0] # True if the top of the main pile is in search list
    replace_index_main = check_main[1] # If the above is True, replace index will indicate the index of the current brick in the tower that will be replaced by the new brick

    new_tower = tower.copy()

    if take_top_discard: # if the top discard brick is part of the search list this will be True (as described above)
        new_brick = discard[0]
        brick_to_be_replaced = tower[replace_index_discard]
        new_tower.remove(brick_to_be_replaced) # remove the brick to be replaced from the current tower
        new_tower.insert(replace_index_discard, new_brick) # adds the new brick to the tower based on the index determined previously
        discard.remove(new_brick) # remove the new brick from the discard pile (it's been moved to the tower)
        add_brick_to_discard(brick_to_be_replaced, discard) # move the replaced brick to the top of the discard pile

    elif take_top_main: # this will be true if the top discard brick is NOT part of the search list, AND the top main pile brick is
        new_brick = main_pile[0]
        brick_to_be_replaced = tower[replace_index_main]
        new_tower.remove(brick_to_be_replaced) # remove the brick to be replaced from the current tower
        new_tower.insert(replace_index_main, new_brick) # adds the new brick to the tower based on the index determined previously
        main_pile.remove(new_brick) # remove the new brick from the main pile (it's been moved to the tower_
        add_brick_to_discard(brick_to_be_replaced, discard) # move the replaced brick to the top of the discard pile

    else:  # else no change to the tower. And we move the top of the main pile to the discard pile
        top_brick_main = main_pile[0]
        main_pile.remove(top_brick_main)
        add_brick_to_discard(top_brick_main, discard)

    return new_tower

#############################
### player_turn functions ###
#############################

def display_tower(player_tower):
    """
    Displays to the player their current tower.
    """
    print("Your current tower is: " + str(player_tower))
    print("")

    for i in player_tower:
        if i in range(1, 11):
            brick_i = ("      [{}]      ").format(i)
        elif i in range(11, 21):
            brick_i = ("     [ {} ]    ").format(i)
        elif i in range(21, 31):
            brick_i = ("    [  {}  ]   ").format(i)
        elif i in range(31, 41):
            brick_i = ("   [   {}   ]  ").format(i)
        elif i in range(41, 51):
            brick_i = ("  [    {}    ] ").format(i)
        else:
            brick_i = (" [     {}     ]").format(i)
        print(brick_i)

def display_top_discard_brick(discard):
    """
    Displays to the player the current top brick of the discard pile.
    """
    top_discard_brick = discard[0]

    if top_discard_brick in range(1, 11):
        brick_display = ("      [{}]      ").format(top_discard_brick)
    elif top_discard_brick in range(11, 21):
        brick_display = ("     [ {} ]    ").format(top_discard_brick)
    elif top_discard_brick in range(21, 31):
        brick_display = ("    [  {}  ]   ").format(top_discard_brick)
    elif top_discard_brick in range(31, 41):
        brick_display = ("   [   {}   ]  ").format(top_discard_brick)
    elif top_discard_brick in range(41, 51):
        brick_display = ("  [    {}    ] ").format(top_discard_brick)
    else:
        brick_display = (" [     {}     ]").format(top_discard_brick)

    print("")
    print(str(brick_display) + " is the top brick on the discard pile")

def take_top_discard_brick(discard):
    """
    Asks the player whether they want to take the top brick of the discard pile.

    Requires the player to give a valid answer y/n. Else it will prompt the question again.
    :return: True/False
    """
    top_discard_brick = discard[0]
    take_top_discard_brick = None # to store True/False.

    not_answered = True
    while not_answered: # Requires the player to give a valid answer y/n. Else it will prompt the question again.
        print("")
        answer = input("Would you like to take the top brick on the discard pile? (enter y/n)")
        if answer == "y":
            print("")
            print("You took the brick " + str(top_discard_brick))
            take_top_discard_brick = True
            not_answered = False
        elif answer == "n":
            print("")
            print("You did not take the brick " + str(top_discard_brick))
            take_top_discard_brick = False
            not_answered = False
        else:
            print("Please enter a valid entry")
            continue

    return take_top_discard_brick

def select_top_discard_brick(player_tower, discard):
    """
    Asks the player where to place the new brick and returns the resulting new tower.
    The function requires that the player give a valid answer when selecting brick to be replaced,
    (the brick number must be part of the current tower structure).

    Also removes the new brick from the original pile and moves the replaced brick to the discard pile.

    :param player_tower:
    :param discard:
    :return: new_player_tower
    """

    top_discard_brick = discard[0]
    new_player_tower = player_tower.copy()

    not_answered = True
    while not_answered:
        print("")
        answer = int(input("Which brick in your tower would you like to replace with the new brick? (enter the number of the brick)"))
        if answer in new_player_tower: # if player's answer is one of the ten bricks in the current structure then we go to the process of replacing the selected brick
            new_brick = top_discard_brick
            replace_index = player_tower.index(answer) # this identifies the index of the brick_to_be_replaced. we need this to know where to put the new brick.
            brick_to_be_replaced = player_tower[replace_index]
            new_player_tower.remove(brick_to_be_replaced)
            new_player_tower.insert(replace_index, new_brick) # put the new brick based on the index of replace_index determined above
            discard.remove(new_brick)
            discard.insert(0, brick_to_be_replaced) # move the brick that was replaced to the top of the discard pile
            print("")
            print("You discarded the brick " + str(brick_to_be_replaced) + " and replaced it with brick " + str(new_brick))
            not_answered = False
        else:
            print("The brick number you entered is not part of your current tower structure")
            print("Please enter a valid entry")
            continue

    return new_player_tower

def display_top_main_pile_brick(main_pile):
    """
    Displays the top main pile brick to the player.
    :param main_pile:
    :return: none
    """
    top_main_pile_brick = main_pile[0]

    if top_main_pile_brick in range(1, 11):
        brick_display = ("      [{}]      ").format(top_main_pile_brick)
    elif top_main_pile_brick in range(11, 21):
        brick_display = ("     [ {} ]    ").format(top_main_pile_brick)
    elif top_main_pile_brick in range(21, 31):
        brick_display = ("    [  {}  ]   ").format(top_main_pile_brick)
    elif top_main_pile_brick in range(31, 41):
        brick_display = ("   [   {}   ]  ").format(top_main_pile_brick)
    elif top_main_pile_brick in range(41, 51):
        brick_display = ("  [    {}    ] ").format(top_main_pile_brick)
    else:
        brick_display = (" [     {}     ]").format(top_main_pile_brick)

    print("")
    print(str(brick_display) + " is the top brick on the main pile")

def take_top_main_pile_brick(main_pile):
    """
    Asks the player whether they want to take the top brick of the main pile.
    Requires the player to give a valid answer y/n. Else it will prompt the question again.

    :return: True/False
    """

    top_main_pile_brick = main_pile[0]
    take_top_main_pile_brick = None

    not_answered = True
    while not_answered: # Requires the player to give a valid answer y/n. Else it will prompt the question again.
        print("")
        answer = input("Would you like to take the top brick on the main pile? (enter y/n)")
        if answer == "y":
            take_top_main_pile_brick = True
            not_answered = False
            print("")
            print("You took the brick " + str(top_main_pile_brick))
        elif answer == "n":
            take_top_main_pile_brick = False
            not_answered = False
            print("")
            print("You did not take the brick " + str(top_main_pile_brick))
        else:
            print("Please enter a valid entry")
            continue

    return take_top_main_pile_brick

def select_top_main_pile_brick(player_tower, main_pile, discard):
    """
    Asks the player where to place the new brick and returns the resulting new tower.
    The function requires that the player give a valid answer when selecting brick to be replaced,
    (the brick number must be part of the current tower structure).

    Also removes the new brick from the original pile and moves the replaced brick to the discard pile.
    """

    top_main_pile_brick = main_pile[0]
    new_player_tower = player_tower.copy()

    not_answered = True
    while not_answered:
        print("")
        answer = int(input("Which brick in your tower would you like to replace with the new brick? (enter the number of the brick)"))
        if answer in new_player_tower: # if player's answer is one of the ten bricks in the current structure then we go to the process of replacing the selected brick
            new_brick = top_main_pile_brick
            replace_index = player_tower.index(answer) # this identifies the index of the brick_to_be_replaced. we need this to know where to put the new brick.
            brick_to_be_replaced = player_tower[replace_index]
            new_player_tower.remove(brick_to_be_replaced)
            new_player_tower.insert(replace_index, new_brick) # put the new brick based on the index of replace_index determined above
            main_pile.remove(new_brick)
            discard.insert(0, brick_to_be_replaced) # move the replaced brick to the top of the discard pile
            print("")
            print("You discarded the brick " + str(brick_to_be_replaced) + " and replaced it with brick " + str(new_brick))
            not_answered = False
        else:
            print("The brick number you entered is not part of your current tower structure")
            print("Please enter a valid entry")
            continue

    return new_player_tower


def player_turn(player_tower, main_pile, discard):
    """
    The function defines what the player will see and do during their turn.
    Returns new player tower based on what the player decides to do during the turn.

    :param player_tower:
    :param main_pile:
    :param discard:
    :return: new_player_tower
    """

    # display the current tower to the player
    display_tower(player_tower)

    # display the top brick of the discard pile
    display_top_discard_brick(discard)

    # asks the player if they want to take the top brick of the discard pile
    if take_top_discard_brick(discard):
        new_player_tower = select_top_discard_brick(player_tower, discard) # if yes, set up a new tower based on the selected brick

    # else we display the top brick of the main pile and asks the player if they want to take it
    else:
        display_top_main_pile_brick(main_pile)
        if take_top_main_pile_brick(main_pile):
            new_player_tower = select_top_main_pile_brick(player_tower, main_pile, discard) # if yes, set up a new tower based on the selected brick
        else:
            new_player_tower = player_tower # else nothing changes to the tower

    display_tower(new_player_tower)
    return new_player_tower

#######################
### print functions ###
#######################

def print_initial_instructions():
    """
    Prints the initial game instructions for the player.
    """
    print("Welcome to Tower Blaster!")
    print("")
    print("The goal of the game is to build a tower structure with one condition:")
    print("Each brick must of smaller size than ones below it.")
    print("")
    print("For example: ")
    print("")
    print("     [1]")
    print("     [7]")
    print("    [ 13 ]")
    print("    [ 19 ]")
    print("   [  25  ]")
    print("  [   31   ]")
    print("  [   37   ]")
    print(" [    43    ]")
    print(" [    49    ]")
    print("[     55     ]")
    print("")
    print("The goal of the game is to complete your tower before the computer completes its tower.")
    print("")
    print("Each turn you will have the opportunity to take the top brick of the discard pile.")
    print("If you decide not to, the top brick of the main pile will be revealed, and you may take that brick.")
    print("")
    print("Each turn you may replace any brick from your tower with the new brick you selected.")
    print("The replaced brick will then go to the top of the discard pile.")
    print("")
    print("If you choose not to take any brick, your current tower structure remains,")
    print("and the top brick of the main pile will go to the top of the discard pile")
    print("")
    input("Are you ready to play? Press enter to start (the computer will go first).")

def print_computer_play_complete(discard):
    """
    This function prints statements that tells the player that the computer has completed its turn.
    :return:
    """
    print("")
    print("The computer has finished its turn.")
    print("The computer discarded the brick " + str(discard[0]) + " to the top of the discard pile.")
    print("")
    input("Press enter to start your turn.")

def print_final_towers(winner, computer_tower, player_tower):
    """
    This function prints the display of final computer and player towers once the game ends.

    :param winner:
    :param computer_tower:
    :param player_tower:
    :return:
    """

    print("")
    if (winner == "computer"):
        print("**********************************")
        print("*****    The Computer Won    *****")
        print("**********************************")
        print("")
    elif (winner == "player"):
        print("***********************************")
        print("**   Congratulations, You Won!   **")
        print("***********************************")
        print("")

    print(" Final Computer Tower: ")
    print("")
    for i in computer_tower:
        if i in range(1, 11):
            brick_i = ("      [{}]      ").format(i)
        elif i in range(11, 21):
            brick_i = ("     [ {} ]    ").format(i)
        elif i in range(21, 31):
            brick_i = ("    [  {}  ]   ").format(i)
        elif i in range(31, 41):
            brick_i = ("   [   {}   ]  ").format(i)
        elif i in range(41, 51):
            brick_i = ("  [    {}    ] ").format(i)
        else:
            brick_i = (" [     {}     ]").format(i)
        print(brick_i)

    print("")
    print(" Your Final Tower: ")
    print("")
    for i in player_tower:
        if i in range(1, 11):
            brick_i = ("      [{}]      ").format(i)
        elif i in range(11, 21):
            brick_i = ("     [ {} ]    ").format(i)
        elif i in range(21, 31):
            brick_i = ("    [  {}  ]   ").format(i)
        elif i in range(31, 41):
            brick_i = ("   [   {}   ]  ").format(i)
        elif i in range(41, 51):
            brick_i = ("  [    {}    ] ").format(i)
        else:
            brick_i = (" [     {}     ]").format(i)
        print(brick_i)

    print("")
    input("Press enter to exit.")


##############
### main() ###
##############

def main():
    """
    The function that puts it all together.
    The player plays until either the user or the computer gets Tower Blaster, which means their tower
    stability has been achieved.
 
    """
    # print initial instructions
    print_initial_instructions()

    # set up the initial piles
    piles = setup_bricks()
    main_pile = piles[0].copy()
    discard = piles[1].copy()

    # shuffle the bricks in the main_pile
    shuffle_bricks(main_pile)

    # deal the initial bricks from main pile to start computer and player towers
    towers = deal_initial_bricks(main_pile)
    computer_tower = towers[0].copy()
    player_tower = towers[1].copy()

    # start the discard pile: take the top brick of what remains in main pile and put it in discard pile
    discard.append(main_pile[0])
    main_pile.pop(0)

    game_running = True
    winner = None # to store who the winner is

    while game_running:
        computer_tower = computer_play(computer_tower, main_pile, discard) # computer's turn
        print_computer_play_complete(discard)
        if check_tower_blaster(computer_tower):
            winner = "computer"
            game_running = False
            break
        player_tower = player_turn(player_tower, main_pile, discard) #player's turn
        if check_tower_blaster(player_tower):
            winner = "player"
            game_running = False

    print_final_towers(winner, computer_tower, player_tower)

if __name__ == "__main__":
    main()