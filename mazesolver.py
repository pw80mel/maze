from tkinter import *
from functools import partial
import itertools
class Application():

    def __init__(self, master):
        '''initilizes application class, which creates maze class, mazesolver created when solve button is clicked'''
        self.master = master

    def create_widgets(self):
        '''creates menubar and adds button frame to root'''
        #grid
        self.create_button_grid(20, 20)
        #Menubar
        menubar = Menu(root)
        menubar.add_command(label='Solve!', command = self.start_maze_solver)
        menubar.add_command(label='Reset', command = self.reset_button_grid)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Change size', command = partial(self.text_window, 'Change Grid Size', 'What size would you like the grid to be?\n(Maximum size is column = 40, row = 90)\n(Minimum size is column = 5, row = 5)\n(Column, Row)', True))
        filemenu.add_command(label='Help/Instructions', command = partial(self.text_window, 'Help',
'''Click once on a square to change to path(white).
Click twice on a square to change to finish square(red).
Click three times on a square to change back to wall(grey).
\n
Click Settings and then Change size to change size of grid.
Start of maze has to be the yellow block.\n'''))
        filemenu.add_command(label='Information', command = partial(self.text_window, 'Information', '\tMade using Python 3.3\t '))#, command=self.get_information
        menubar.add_cascade(label='Settings', menu=filemenu)

        root.config(menu=menubar)

    def change_value(self, button, button_row, button_column):
        '''tests what value button has to change it to next value'''
        if button['bg'] == 'grey':
            button['bg'] = 'white'
            Maze.maze[button_row - 1][button_column] = ' '#white(' ' on list) is path
        elif button['bg'] == 'white':
            button['bg'] = 'red'
            Maze.maze[button_row - 1][button_column] = '*'#red('*' on list) is finish
        else:
            button['bg'] = 'grey'
            Maze.maze[button_row - 1][button_column] = '@'#grey('@' on list) is wall

    def create_button_grid(self, row_size, column_size):
        '''creates grid of buttons using loops given row and column size'''
        self.master.resizable(width=TRUE, height=TRUE)
        self.frame = Frame(self.master)
        self.button_list = []
        self.button_list.append(Button(self.frame, bg='grey',width = 1, relief = FLAT, state = DISABLED))
        
        for row in range(1, row_size + 1):
            self.button_list.append([])
            for column in range(0, column_size):
                if row == 2 and column == 0:
                    self.button_list[row].append(Button(self.frame, bg='yellow',width = 1, relief = SUNKEN, state = DISABLED))
                    self.button_list[row][column].grid(row = row + 1, column = column + 1, sticky = W)
                elif (column == 0 or row == 1 or column == (column_size - 1) or row == row_size):
                    self.button_list[row].append(Button(self.frame, bg='grey',width = 1, relief = FLAT, state = DISABLED))
                    self.button_list[row][column].grid(row = row + 1, column = column + 1, sticky = W)
                else:
                    self.button_list[row].append(Button(self.frame, bg='grey',width = 1, relief = SUNKEN))
                    self.button_list[row][column].grid(row = row + 1, column = column + 1, sticky = W)
                    self.button_list[row][column]['command'] = partial(self.change_value, self.button_list[row][column], row, column)
                    #command added after for no errors with classes not being created
        self.frame.pack()
        self.master.resizable(width=FALSE, height=FALSE)
        
    def reset_button_grid(self):
        '''resets grid of buttons using loops given row and column size'''
        self.frame.destroy()
        self.create_button_grid(len(Maze.maze), len(Maze.maze[0]))
        Maze.create_maze_grid(len(Maze.maze), len(Maze.maze[0]))

    def create_solved_button_grid(self, solved_list):
        '''creates grid of buttons using loops given the solved list'''
        window = Tk()
        window.resizable(width = FALSE, height = FALSE)
        window.title('Solved maze')
        frame = Frame(window)
        
        for row in range(0, len(solved_list)):
            for column in range(0, len(solved_list[0])):
                if solved_list[row][column] == '#':
                    bg_color = 'blue'
                elif solved_list[row][column] == '*':
                    bg_color = 'red'
                elif solved_list[row][column] == ' ':
                    bg_color = 'white'
                else:
                    bg_color = 'grey'

                if column == 0 or row == 0 or column == (len(solved_list[0]) - 1) or row == (len(solved_list) - 1):
                    button = Button(frame, bg = bg_color, width = 1, relief = FLAT, state = DISABLED).grid(row = row + 1, column = column + 1, sticky = W)
                else:
                    button = Button(frame, bg = bg_color, width = 1, relief = SUNKEN, state = DISABLED).grid(row = row + 1, column = column + 1, sticky = W)
     
        frame.pack()

    def text_window(self, title, maintext, text_entry = False):
        '''creates text window, given title and text'''
        window = Tk()
        window.resizable(width = FALSE, height = FALSE)
        window.title(title)
        Label(window, text = maintext).pack()
            
        if text_entry: #if text entry is needed == True
            self.entry_box_row = Entry(window, width = 20)
            self.entry_box_row.pack()
            self.entry_box_column = Entry(window, width = 20)
            self.entry_box_column.pack()
            enter_button = Button(window, text = 'OK',command = self.get_values)
            enter_button.pack(fill = X)
            cancel_button = Button(window, text = 'Close', command = window.destroy).pack(fill = X)
            
        else:#else just gives close button
            exitbutton = Button(window, text = 'OK', command = window.destroy).pack(fill = X)
            
        window.mainloop()
        
    def get_values(self):
        ''' gets row and column values from entry boxes'''
        try:
            if int(self.entry_box_row.get()) <= 40 and int(self.entry_box_column.get()) <= 90 and int(self.entry_box_row.get()) >= 5 and int(self.entry_box_column.get()) >= 5:
                self.row_size = int(self.entry_box_row.get())
                self.cloumn_size = int(self.entry_box_column.get())
                
                self.frame.destroy()#closes old grid                                                                   
                self.create_button_grid(self.row_size, self.cloumn_size)#gets row/column values
                Maze.create_maze_grid(self.row_size, self.cloumn_size)#creates maze with those values
                self.master.update()#updates screen
            else:
                app.text_window('Error', 'Invalid grid size!\n\n(Maximum size is column = 40, row = 90)\n(Minimum size is column = 5, row = 5)\n(Column, Row).')
        except:
            app.text_window('Error', 'Invalid grid size!\n\n(Maximum size is column = 40, row = 90)\n(Minimum size is column = 5, row = 5)\n(Column, Row).')
            
    def start_maze_solver(self):
        '''creates new mazesolver object each time solve button is pressed, so variables are refreshed each time'''
        mazesolver = MazeSolver()
        
class Maze():
    
    def create_maze_grid(row_size, column_size):
        '''creates maze 2d list using only @ so gui can change elements, row_size, column_size are the amount of rows/columns in button grid'''
        Maze.maze = []
        for row in range(row_size):
            Maze.maze.append(['@'] * column_size)

class MazeSolver():

    def __init__(self):
        self.unsolvable = False
        self.valid_moves = list(itertools.permutations(((0, +1),(+1, 0),(0, -1),(-1, 0)), 4))

        self.all_used_moves = [[]]
        
        for move_list in self.valid_moves:
            self.used_moves = []#stored as (y, x)
            self.x_position = 0
            self.y_position = 1
            self.next_valid_moves = [] #stored as ((y,x), (y,x))
            self.choice_moves = [] #stored as (choice position y, choice position x,(choice1y, choice1x, choice2y, choice2x))
            self.move(move_list)#start moves
            
        if self.unsolvable == True:
            app.text_window('Error', 'Cannot solve maze!\n\nMake sure you have added in a red block\nin a valid place.')
        else:
            final_co_ordinates = self.get_final_co_ordinates()
            self.show_final_co_ordinates(final_co_ordinates)

    def move(self, move_list):
        ''' Finds next moves by finding elements beside it'''

        while Maze.maze[self.y_position][self.x_position] != '*' and self.unsolvable == False:#while hasnt found the end

            for move in move_list:
                next_y = self.y_position + move[1]
                next_x = self.x_position + move[0]

                if Maze.maze[next_y][next_x] == ' ' and (next_y, next_x) not in self.used_moves and (next_y, next_x) not in self.next_valid_moves:#if (move(next position) is == x) and if (tuple(y, x) is not in self.used_moves)are true
                    self.next_valid_moves.append([next_y, next_x])
                    
                elif Maze.maze[next_y][next_x] == '*' :#if it has found the end
                    self.next_valid_moves.append([next_y, next_x])
                    self.normal_move()#finds final move
                    if len(self.used_moves) < len(self.all_used_moves[-1]) or self.all_used_moves[-1] == []:#if is less than last move set(finds shortest route), deletes that move set, and adds new one
                        del self.all_used_moves[-1]
                        self.all_used_moves.append(self.used_moves)
                    
            self.calculate_moves()#after next valid moves are calculated see if there is more than one choice

    def calculate_moves(self):
        ''' test if move is normal/dead end/multi choice'''
        list_len = len(self.next_valid_moves)

        if list_len == 1: #one choice of move(foward path)
            self.normal_move()
            self.next_valid_moves = [] #clear valid moves as in next x/y position
        elif list_len >= 2: #more than 2 choices of move(intersection)
            self.choice_moves.append((self.y_position, self.x_position,(self.next_valid_moves[:]))) #appending relevent choices and information see line 25
            self.normal_move()
            self.next_valid_moves = []
        elif list_len <= 0: #no choice of move(dead end)
            self.dead_end_move()
            self.next_valid_moves = []

    def normal_move(self):
        ''' moves to next "x" '''
        self.used_moves.append((self.y_position, self.x_position)) #add move to list of used moves

        #change mazesolver to new valid position from last element in next_valid_moves
        self.y_position = self.next_valid_moves[-1][0]
        self.x_position = self.next_valid_moves[-1][1]

    def dead_end_move(self):
        ''' sends back to saved position if dead end'''
        self.used_moves.append((self.y_position, self.x_position)) #add move to list of used moves
        try:
            self.y_position = self.choice_moves[-1][0] #make y the y of next choice
            self.x_position = self.choice_moves[-1][1] #make x the x of next choice
            del self.choice_moves[-1]#removing last choice that lead to dead end
        except IndexError:
            self.unsolvable = True
                    
    def get_final_co_ordinates(self):
        ''' find co_ordinates to print out, removes dead ends'''
        final_co_ordinates = []

        for element in self.all_used_moves[0]:
            if element in final_co_ordinates:
                del final_co_ordinates[final_co_ordinates.index(element) + 1:] # delete all elements after co_ordinate e.g. dead ends
            else:
                final_co_ordinates.append(element)
        return final_co_ordinates

    def show_final_co_ordinates(self, co_ordinates):
        ''' prints maze nicely'''
        maze_copy = []

        for row in Maze.maze:
            maze_copy.append(list(row))#makes copy of maze, so it doesnt put # in it
        for element in co_ordinates[:-1]:#gets used co-ordinates and replaces them with #
            maze_copy[element[0]][element[1]] = '#'

        app.create_solved_button_grid(maze_copy)
        
root = Tk()
root.title('Maze Solver')
root.resizable(width=FALSE,height=FALSE)
Maze.create_maze_grid(20, 20)
app = Application(root)
app.create_widgets()
root.mainloop()
