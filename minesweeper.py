import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the mine_count is equal to 0, that means there are no mines in
        # the given set
        mine_count = self.count
        
        # If there are as many mines as there are cells, all cells contain a mine
        if len(self.cells) == mine_count and mine_count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        #if all cells are safe, return all cells
        if self.count == 0:
            return self.cells
        return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


#checks if a set is a subset of another set

def is_subset(set1, set2):
    if len(set1.cells) > len(set2.cells):
        big_set = set1.cells
        small_set = set2.cells
    else:
        big_set = set2.cells
        small_set = set1.cells

    for cell in small_set:
        if cell not in big_set:
            return False
    return True






class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # print("AI knowledge updating...")
        self.moves_made.add(cell)
        self.mark_safe(cell)

        cells = set()

        row_cord = cell[0]
        col_cord = cell[1]

        #iterate through each neghbor cell around the provided cell
        for i in range(row_cord - 1, row_cord + 2):
            for j in range(col_cord - 1, col_cord + 2):

                #if neighbor = cell, continue to next cell
                if cell == (i, j):
                    continue

                #if the coordinate is in bounds
                
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (i, j)
                    #if we don't know about the status of the cell yet
                    if not (neighbor in self.mines or neighbor in self.safes):
                        cells.add(neighbor)
                    elif neighbor in self.mines:
                        count -= 1
        self.knowledge.append(Sentence(cells, count))


        # print("First loop end")


        # print("\nStarting second loop...")
        #compare each sentence inside the knowledge base

        #mark cells as safe and mines

        knowledge_changed = True

        while knowledge_changed:
            print("Updating knowledge")
            knowledge_changed = False

            safes = set()
            mines = set()

            
            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())


            if len(safes) > 0:
                knowledge_changed = True
                for safe in safes:
                    self.mark_safe(safe) 
            if len(mines) > 0:
                knowledge_changed = True
                for mine in mines:
                    self.mark_mine(mine)


            print("Marked mines and safes")
            index = 0

            while index < len(self.knowledge):
                sentence = self.knowledge[index]
                if len(sentence.cells) == 0:
                    self.knowledge.pop(index)
                else:
                    index += 1
                

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence2.cells == sentence1.cells:
                        continue

                    print("Checking if subset...")
                    if is_subset(sentence1, sentence2):

                        if len(sentence1.cells) > len(sentence2.cells):
                            big, small = sentence1, sentence2
                        else:
                            big, small = sentence2, sentence1

                        new_cells = big.cells.copy()
                        mine_count = big.count - small.count
                        # print("Iterating through the cells of sentence...")
                        for cell_small in small.cells.copy():
                            new_cells.remove(cell_small)
                        # print("Finished iterating.")
                        print("PRINTING SUBSET")
                        print(new_cells)


                        new_sentence = Sentence(new_cells, mine_count)
                        if new_sentence not in self.knowledge:
                            knowledge_changed = True
                            self.knowledge.append(new_sentence)
        # print("AI knowledge updated")

        # print("\n\nSAFE MOVES: ", self.safes)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:

            if cell not in self.moves_made:
                print("SAFE MOVE: ", cell)
                return cell
        return None
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """


        while True:
            rand_i = random.randint(0, self.height - 1)
            rand_j = random.randint(0, self.width  - 1)

            cords = (rand_i, rand_j)
            if not (cords in self.mines or cords in self.moves_made):
                print("AI making move:",cords)
                return cords
            

