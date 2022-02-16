"""6.009 Lab 10: Snek Is You Video Game"""

import doctest

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
WORDS = NOUNS | PROPERTIES | {"AND", "IS"}

# Maps a keyboard direction to a (delta_row, delta_column) vector.
direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}
class object():
    def try_move(self, dir, game, first = True):
        """
        attempts to move the object, if it can, it moves the object in the game_board and returns True
        otherwise it returns false and
        """
        vec = direction_vector[dir]
        if self.pos[0]+vec[0] < 0 or self.pos[0]+vec[0] >= game.height or self.pos[1]+vec[1] < 0 or self.pos[1]+vec[1] > game.width-1:
            return False # can't move outside the game

        if game.contains_rule('STOP', (self.pos[0]+vec[0], self.pos[1]+vec[1])):
            return False # can't move objects with "STOP" property
        for item in game.board[self.pos[0]+vec[0]][self.pos[1]+vec[1]]:
            if game.rule_book.contains(str(item), "PUSH"):
                if not item.try_move(dir, game, False):
                    return False # it can't move if there are objects in the way
        return True

    def move(self, dir, game, first = True):
        """
        actually moves the object according to the normal rules and then calls recursivly to objects that have PULL and PUSH properties
        """
        self.moved_this_turn = True # objects will never be moved twice in a singe move
        vec = direction_vector[dir]
        if self.pos[0]+vec[0] < 0 or self.pos[0]+vec[0] >= game.height or self.pos[1]+vec[1] < 0 or self.pos[1]+vec[1] > game.width-1:
            return False # can't move outside of the game
        if game.contains_rule('STOP', (self.pos[0]+vec[0], self.pos[1]+vec[1])):
            return False # can't move an object with a stop property

        game.remove_item(self.pos, self) # we remove the item from the game and then we will call recursivly on other objects

        """ Queue for moving PUSH items"""
        queue = [] # queue of objects to be moved
        for item in game.board[self.pos[0]+vec[0]][self.pos[1]+vec[1]]:
            if game.rule_book.contains(str(item), "PUSH"):
                queue.append(item) # add the object to be moved to the queue
        for item in queue:
            if item.try_move(dir, game) and not item.moved_this_turn:
                item.move(dir, game) # now move all the objects in the queue

        if not game.contains_rule('DEFEAT', (self.pos[0]+vec[0], self.pos[1]+vec[1])):
            game.add_item((self.pos[0]+vec[0], self.pos[1]+vec[1]), self) # add the item back into the game at the new position unless it has been defeated
            self.pos = (self.pos[0]+vec[0], self.pos[1]+vec[1]) # assign the new position

        """ Queue for moving PULL items"""
        if first and not (self.pos[0]-2*vec[0] < 0 or self.pos[0]-2*vec[0] >= game.height or self.pos[1]-2*vec[1] < 0 or self.pos[1]-2*vec[1] > game.width-1):
            queue = []
            for item in game.board[self.pos[0]-2*vec[0]][self.pos[1]-2*vec[1]]:
                if game.rule_book.contains(str(item), "PULL"):
                    queue.append(item) # add pull item to queue
            for item in queue:
                if item.try_move(dir, game) and not item.moved_this_turn:
                    item.move(dir, game) # move item in queue
        return False

    def __str__(self):
        """
        Prints out the name of the object
        """
        return self.name

class text_object(object):
    def __init__(self, name, pos):
        """
        Properties is a set of all the properties that are true.
        This creates an object that has a name, position, and properties.
        """
        self.name = name
        self.pos = pos
        self.moved_this_turn = False

class graphic(object):
    def __init__(self, name, pos):
        """
        Properties is a set of all the properties that are true.
        This creates an object that has a name, position, and properties.
        """
        self.name = name
        self.pos = pos
        self.moved_this_turn = False

default_rules = {} #{'wall': {'STOP'}} #{'rock': {'PUSH'}, 'wall': {'STOP'}, 'computer': {'PULL'}, 'bug': {'DEFEAT'}, 'flag': {'WIN'}, 'snek':{'YOU'}}

class rule_book():
    """
    rule_book stores a dictionary of rules inside self.rules
    These rules are keys with the item names and map to a set of the rules for that item
    """
    def __init__(self):
        """
        Initial rules are given by default rules (which is normally empty)
        Otherwise we could initialize with an empty dictionary
        """
        self.rules = {key: default_rules[key] for key in default_rules}
    def add_rules(self, dict_of_rules):
        """
        Adds the rules by combining the dictionary of new rules with existing rules
        """
        for i in dict_of_rules:
            if i in self.rules:
                self.rules[i] = set.union(dict_of_rules[i], self.rules[i]) # item already in self.rules
            else:
                self.rules[i] = dict_of_rules[i] # item not in self.rules
    def contains(self, object, rule):
        """
        check to see if an item has a certain rule
        """
        if object.isupper() and rule == 'PUSH':
            return True # default rule such that text items are always pushable
        if object not in self.rules:
            return False # the rule doesn't exist
        return rule in self.rules[object] # returns if the rule is in it or not

class game_board():
    def __init__(self, board):
        """
        creates a new object gameboard with:
            height, width, game_won (True/False),
            items (which are "object" objects),
            ifstats (list of objects that are "IS" statements),
            and board (which is the same, but lists of lists of sets of the items)
        Also finds the rules and assigns them to self.rule_book
        """
        self.height = len(board)
        self.width = len(board[0])
        new_board = [[set() for i in range(self.width)] for y in range(self.height)]
        self.items = set()
        self.game_won = False
        self.ifstats = set()
        for x, row in enumerate(board): # adding items to self.item and creating new_board
            for y, pos in enumerate(row):
                for item in pos:
                    if item.islower():
                        obj_toadd = graphic(item, (x, y)) # create graphic object
                        self.items.add(obj_toadd) # add it to the items
                        new_board[x][y].add(obj_toadd) # add it to the new_board

                    else:
                        obj_toadd = text_object(item, (x, y)) # create text object
                        self.items.add(obj_toadd) # add it to the items
                        new_board[x][y].add(obj_toadd) # add it to the new_board
                        if item == 'IS':
                            self.ifstats.add(obj_toadd) # if it is a "IS" statement, add it to self.ifstats
        self.board = new_board
        self.find_rules(False)
        print(f"internal rulebook is {self.rule_book.rules}")
        pass

    def step_item(self, dir):
        """
        moves the item in the direction specified and moves other items according to the rules
        """
        queue = [] # items to move
        for i in self.items:
            if self.rule_book.contains(str(i), "YOU"):
                queue.append(i)
        for i in queue:
            if i.try_move(dir, self): # test to see if we even can move the item
                i.move(dir, self)
        self.find_rules() # find the new rules
        for item in self.items:
            item.moved_this_turn = False # reset the items so they can be moved again later
        return self.game_status() # return if it is won or not

    def contains_rule(self, rule, pos):
        """
        check to see if a position contains an object with a certain rule (such as "STOP")
        """
        for item in self.board[pos[0]][pos[1]]:
            if self.rule_book.contains(str(item), rule):
                return True
        return False

    def find_rules(self, switching = True):
        """
        finds given rules given an input of an IF statement
        """
        switches = set() # some items are mapped together
        self.rule_book = rule_book() # create a new rule_book

        for i in self.ifstats: # find all the rules from the "IS" statements
            new_rules, new_switches = parse_rule(self, i)
            self.rule_book.add_rules(new_rules)
            switches = set.union(switches, new_switches)

        reverse_switches = set()
        if switching: # simplifying set of items that are going to be switched
            for switch in switches:
                if (switch[1], switch[0]) in switches:
                    if not (switch[1], switch[0]) in reverse_switches:
                        reverse_switches.add(switch)
                else:
                    for item in self.items:
                        if item.name == switch[0].lower():
                            item.name = switch[1].lower()
            for switch in reverse_switches: # makeing switches specified
                items1 = [i for i in self.items if i.name == switch[0].lower()]
                items2 = [i for i in self.items if i.name == switch[1].lower()]
                for item in items1:
                    item.name = switch[1].lower()
                for item in items2:
                    item.name = switch[0].lower()


        for item in self.rule_book.rules: # items that are "PUSH" can't also be "STOP"
            if "STOP" in self.rule_book.rules[item] and "PUSH" in self.rule_book.rules[item]:
                self.rule_book.rules[item].remove("STOP")
        pass

    def remove_item(self, pos, item):
        """
        Takes an item out of the items and the board (also the ifstats if "IS")
        """
        self.board[pos[0]][pos[1]].remove(item)
        self.items.remove(item)
        if item in self.ifstats:
            self.ifstats.remove(item)
        return item

    def add_item(self, pos, item):
        """
        Adds and item to the board and the items list (also the ifstats if "IS")
        """
        self.board[pos[0]][pos[1]].add(item)
        self.items.add(item)
        if item.name == 'IS':
            self.ifstats.add(item)
        return item

    def game_status(self):
        """
        Checks to see if the game is won, also removes items that have been defeated
        """
        items_to_remove = []
        for item in self.items: # removes items that have been defeated
            if self.rule_book.contains(str(item), "DEFEAT") and self.rule_book.contains(str(item), "YOU"):
                items_to_remove.append(item)
        for item in items_to_remove:
            self.remove_item(item.pos, item)
        if self.game_won: # the game has previously been won
            return True
        for item_rules in self.rule_book.rules: # You are win
            if "YOU" in item_rules and "WON" in item_rules:
                self.game_won = True
                return True
        for item in self.items: # win and you are in the same position
            if self.rule_book.contains(str(item).lower(), "YOU") and self.contains_rule('WIN', item.pos):
                self.game_won = True
                return True
        return False # the game is not won


def parse_rule(graph, ifstat):
    """
    given the graph and a set of "IS" objects, parse_rules finds all the rules
    and returns a dictionary of the rules and a set of switches to be made
    """
    def find_dir_rules(dir, inter):
        """
        Using a direction, it finds the number of items that are inside the inter set provided. 
        """
        new_items = set()
        i = ifstat.pos
        while i[0]+dir[0] >= 0 and i[1]+dir[1] >= 0 and i[0]+dir[0] < graph.height and i[1]+dir[1] < graph.width:
            """
            collecting
            """
            i = (i[0]+dir[0], i[1]+dir[1])
            new_vals = {str(item) for item in graph.board[i[0]][i[1]]}.intersection(inter)
            new_items = set.union(new_vals, new_items)
            total_items = set.union({str(item) for item in graph.board[i[0]][i[1]]}.intersection(PROPERTIES), {str(item) for item in graph.board[i[0]][i[1]]}.intersection(NOUNS))
            i = (i[0]+dir[0], i[1]+dir[1])
            if not (i[0]+dir[0] >= 0 and i[1]+dir[1] >= 0 and i[0]+dir[0] < graph.height and i[1]+dir[1] < graph.width) or not "AND" in {str(i) for i in graph.board[i[0]][i[1]]} or len(total_items) == 0:
                break
        return new_items

    def collect_rules(new_nouns, new_props, new_switches):
        """
        Adds rules to the return_rules and switches to the switches set
        """
        for noun in new_nouns: # adding new rules to return_rules and switches
            if noun.lower() not in return_rules:
                return_rules[noun.lower()] = set()
            for prop in new_props:
                 return_rules[noun.lower()].add(prop)
            for snoun in new_switches:
                 switches.add((noun, snoun))

    return_rules = {}
    switches = set()
    # collecting horizontal rules
    hNouns = find_dir_rules((0, -1), NOUNS)
    hProps = find_dir_rules((0, 1), PROPERTIES)
    switch_noun = find_dir_rules((0, 1), NOUNS)
    collect_rules(hNouns, hProps, switch_noun)

    # collecting vertical rules
    vNouns = find_dir_rules((-1, 0), NOUNS)
    vProps = find_dir_rules((1, 0), PROPERTIES)
    switch_noun = find_dir_rules((1, 0), NOUNS)
    collect_rules(vNouns, vProps, switch_noun)

    return return_rules, switches



def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, where UPPERCASE
    strings represent word objects and lowercase strings represent regular
    objects (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['snek'], []],
        [['SNEK'], ['IS'], ['YOU']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    return game_board(level_description)


def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    game.step_item(direction)
    return game.game_won


def dump_game(game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    return_game = []
    for row in game.board:
        level = []
        for pos in row:
            level.append([str(i) for i in pos])
        return_game.append(level)
    return return_game
