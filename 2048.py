#-------------------------------------------------------------------------------
# 2048.py
# Gregory Kubiski-Moshansky
# Nov 2, 2018
# This program allows the user to play a game of 2048 on the command line.
#-------------------------------------------------------------------------------

import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self.grid = self.createGrid(row, col)       # creates the grid specified above

        self.emptiesSet = []                        # list of empty cells
        self.updateEmptiesSet()

        for _ in range(self.initial):               # assign two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        # This function generates and returns a row*col grid filled with 0's
        grid = [0] * row
        for i in range(row):
            grid[i] = [0] * col
           
        return(grid)


    def assignRandCell(self, init=False):

        """
        This function assigns a random empty cell of the grid
        a value of 2 or 4.

        In __init__() it only assigns cells the value of 2.

        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned
        a value of 4
        """

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.grid[cell[0]][cell[1]] = 2
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.grid[cell[0]][cell[1]] = 4
                else:
                    self.grid[cell[0]][cell[1]] = 2
            self.emptiesSet.remove(cell)


    def drawGrid(self):
        # This function draws the grid representing the state of the game
        # grid
        

        for row_index in range(self.row):
            line = '\t|'
            for col_index in range(self.col):
                if not self.grid[row_index][col_index]:
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.grid[row_index][col_index]).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self):
        # This function updates the list of empty tiles of the grid.
        
        self.emptiesSet = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0:
                    self.emptiesSet.append([row, col])
        
                    
        
        
        


    def collapsible(self):
        """
        This function tests if the grid of the game is collapsible
        in any direction (left, right, up or down.)

        It returns True if the grid is collapsible.
        It returns False otherwise.
        """        
        
        collapsible = False
        
        if len(self.emptiesSet) < 0:
            collapsible = True
        else:
            for row in range(len(self.grid)-1):
                for col in range(len(self.grid[row])-1):
                    if self.grid[row][col] == self.grid[row][col + 1]:
                        collapsible = True
                    if self.grid[row][col] == self.grid[row + 1][col]:
                        collapsible = True
        
        return collapsible

    def collapseRow(self, lst):

        """
        This function takes a list lst and collapses it to the LEFT.

        This function returns two values:
        1. the collapsed list and
        2. True if the list is collapsed and False otherwise.
        """
        
        collapsed = False
        lstAfter = []
        for i in range(len(lst)):
            if lst[i] != 0:
                lstAfter.append(lst[i])
        for i in range(len(lst)):
            if lst[i] == 0:
                lstAfter.append(0)
        for i in range(len(lstAfter)-1):
            if lstAfter[i] == lstAfter[i+1]:
                lstAfter[i] += lstAfter.pop(i+1)
                self.score += lstAfter[i]
                lstAfter.append(0)
        if lstAfter != lst:
            collapsed = True
        
        return lstAfter, collapsed
                    
                




    def collapseLeft(self):
        """
        This function uses collapseRow() to collapse all the rows
        in the grid to the LEFT.

        This function returns True if any row of the grid is collapsed
        and False otherwise.
        """
        
        gridCollapsed = False
        
        for row in range(len(self.grid)):
            updatedRow, collapsed = self.collapseRow(self.grid[row])
            self.grid[row] = updatedRow
            if collapsed == True:
                gridCollapsed = True
        
        return gridCollapsed





    def collapseRight(self):
        """
        This function uses collapseRow() to collapse all the rows
        in the grid to the RIGHT.

        This function returns True if any row of the grid is collapsed
        and False otherwise.
        """        
        
        gridCollapsed = False
        
        for row in range(len(self.grid)):
            updatedRow, collapsed = self.collapseRow(list(reversed(self.grid[row])))
            updatedRow = list(reversed(updatedRow))
            self.grid[row] = updatedRow
            if collapsed == True:
                gridCollapsed = True
        
        return gridCollapsed        


    def collapseUp(self):
        """
        This function uses collapseRow() to collapse all the columns
        in the grid to UPWARD.

        This function returns True if any column of the grid is
        collapsed and False otherwise.
        """
        
        gridCollapsed = False
        
        for row in range(len(self.grid)):
            column = []
            for col in range(len(self.grid[row])):
                column.append(self.grid[col][row])
            updatedColumn, collapsed = self.collapseRow(column)
            for col in range(len(updatedColumn)):
                self.grid[col][row] = updatedColumn[col]
            if collapsed == True:
                gridCollapsed = True
        
        return gridCollapsed           


    def collapseDown(self):
        """
        This function uses collapseRow() to collapse all the columns
        in the grid to DOWNWARD.

        This function returns True if any column of the grid is
        collapsed and False otherwise.
        """
        
        gridCollapsed = False
        
        for row in range(len(self.grid)):
            column = []
            for col in range(len(self.grid[row])):
                column.append(self.grid[col][row])
            updatedColumn, collapsed = self.collapseRow(list(reversed(column)))
            updatedColumn = list(reversed(updatedColumn))
            for col in range(len(updatedColumn)):
                self.grid[col][row] = updatedColumn[col]
            if collapsed == True:
                gridCollapsed = True
        
        return gridCollapsed                  


class Game():
    def __init__(self, row=4, col=4, initial=2):
        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):
        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")
        print('Enter "w", "a", "s", or "d" to move Up, Left, Down, or Right (respectively).')
        print('Enter "p" to exit the program.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


# -----------------------------------------------------------------------------
# Main Function ---------------------------------------------------------------
# -----------------------------------------------------------------------------

# This condition ensures that the game isn't run if the file is loaded as
# a module. Will only run if the file is executed.

if __name__ == '__main__':
    game = Game()
