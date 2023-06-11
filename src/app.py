""" Main application module. """


import random
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Tuple, cast, Any

from .misc import GridCoordinates, HandmadeTextures, adjoining_coordinates


# increase recursion limit
sys.setrecursionlimit(2500)


class MineSweeperApplication(tk.Tk):
    """
    Main window of MineSweeper game. based on tk.Tk.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Main window of MineSweeper game. based on tk.Tk.

        :param args: tk.Tk args.
        :param kwargs: tk.Tk kwargs.
        """
        super().__init__(*args, **kwargs)

        # load all application textures in one dataclass object
        self.textures = HandmadeTextures()

        # add title to the window
        self.wm_title("MineSweeper")
        # make window not resizable
        self.resizable(False, False)
        # add icon photo
        self.iconphoto(True, self.textures.bomb_unhidden)

        # main container frame for all content inside window
        self.container = tk.Frame(self, height=400, width=400)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # frame for top management panel
        self.top_panel = tk.Frame(self.container)
        self.top_panel.pack(side="top", fill="none", expand=True)

        # create variables for all entries
        self.width_var = tk.IntVar(value=8)
        self.height_var = tk.IntVar(value=8)
        self.bombs_var = tk.IntVar(value=10)
        self.flags_var = tk.IntVar(value=self.bombs_var.get())
        self.time_var = tk.IntVar(value=0)
        self.time_count = False
        self.difficulty_list = ["Beginner", "Intermediate", "Expert", "Master", "Custom"]
        self.difficulty = tk.StringVar(value="Beginner")
        self.difficulty.trace_add("write", self.difficulty_change)

        # add entry for width
        self.width_label = tk.Label(self.top_panel, text="Width: ")
        self.width_label.grid(column=0, row=0)
        self.width_entry = tk.Entry(self.top_panel, textvariable=self.width_var, width=4)
        self.width_entry.grid(column=1, row=0)
        # add entry for height
        self.height_label = tk.Label(self.top_panel, text="Height: ")
        self.height_label.grid(column=0, row=1)
        self.height_entry = tk.Entry(self.top_panel, textvariable=self.height_var, width=4)
        self.height_entry.grid(column=1, row=1)
        # add entry for bomb count
        self.bombs_label = tk.Label(self.top_panel, text="Bombs: ")
        self.bombs_label.grid(column=0, row=2)
        self.bombs_entry = tk.Entry(self.top_panel, textvariable=self.bombs_var, width=4)
        self.bombs_entry.grid(column=1, row=2)

        # add reset button
        self.reset_button = tk.Button(self.top_panel, text="Reset", command=self.reset, width=6)
        self.reset_button.grid(column=2, row=1)

        # add difficulty combobox
        self.difficulty_combobox = ttk.Combobox(self.top_panel, values=self.difficulty_list,
                                                state="readonly", textvariable=self.difficulty, width=8)
        self.difficulty_combobox.grid(column=2, row=0)
        self.difficulty.set(value="Beginner")

        # add button to change flag and click mode
        self.mode_label = tk.Label(self.top_panel, text="Cursor: ")
        self.mode_label.grid(column=3, row=1)
        self.flag_button = tk.Button(self.top_panel, text="Click",
                                     command=self.change_mode, width=3)
        self.flag_button.grid(column=4, row=1)

        # add flags counter
        self.flags_counter_label = tk.Label(self.top_panel, text="Flags count: ")
        self.flags_counter_label.grid(column=3, row=2)
        self.flags_counter_entry = tk.Entry(self.top_panel, textvariable=self.flags_var, width=4, state="readonly")
        self.flags_counter_entry.grid(column=4, row=2)

        # add time counter
        self.time_counter_label = tk.Label(self.top_panel, text="Time count: ")
        self.time_counter_label.grid(column=3, row=0)
        self.time_counter_entry = tk.Entry(self.top_panel, textvariable=self.time_var, width=4, state="readonly")
        self.time_counter_entry.grid(column=4, row=0)

        # start timer
        self.update_time()

        # create game minefield
        self.minefield = MineField(self.container, self, n_columns=self.width_var.get(),
                                   n_rows=self.height_var.get(), n_bombs=self.bombs_var.get())
        self.minefield.pack(side="top", fill="none", expand=True)

    @property
    def number_of_flags(self) -> int:
        """ Get number of flags inside window minefield. """
        return self.flags_var.get()

    @number_of_flags.setter
    def number_of_flags(self, count: int) -> None:
        """ Set number of flags inside window minefield. """
        if isinstance(count, int):
            self.flags_var.set(count)
        else:
            raise ValueError(f"{self.__class__.__name__} property 'number_of_flags' "
                             f"accepts only a value with the type 'int'.")

    def validate_entry_values(self) -> None:
        """ Validate values in entries and raise ValueError if invalid. """
        try:
            width_value = self.width_var.get()
        except tk.TclError:
            raise ValueError("Width value must be integer number.")
        try:
            height_value = self.height_var.get()
        except tk.TclError:
            raise ValueError("Height value must be integer number.")
        try:
            bombs_value = self.bombs_var.get()
        except tk.TclError:
            raise ValueError("Bombs value must be integer number.")

        if width_value < 1 or width_value > 48:
            raise ValueError("Width must be between 1 and 48.")
        if height_value < 1 or height_value > 48:
            raise ValueError("height must be between 1 and 48.")
        if bombs_value < 1 or bombs_value > width_value * height_value:
            raise ValueError(f"bombs number must be between 1 and {width_value * height_value}.")

    def reset(self) -> None:
        """ Reset minefield object. """
        try:
            self.validate_entry_values()
        except ValueError as ve:
            messagebox.showerror("Validation error", str(ve))
        else:
            self.minefield.destroy()
            self.number_of_flags = self.bombs_var.get()
            self.flag_button.configure(text="Click")
            self.time_count = False
            self.time_var.set(0)
            self.minefield = MineField(self.container, self, n_columns=self.width_var.get(),
                                       n_rows=self.height_var.get(), n_bombs=self.bombs_var.get())
            self.minefield.pack(side="top", fill="none", expand=True)

    def change_mode(self) -> None:
        """ Switch is_flag to opposite. """
        if self.minefield.is_flag:
            self.minefield.is_flag = False
            self.flag_button.configure(text="Click")
        else:
            self.minefield.is_flag = True
            self.flag_button.configure(text="Flag")

    def difficulty_change(self, *args: Any) -> None:
        """ Change game based on difficulty value. """
        value = self.difficulty.get()
        if value == "Beginner":
            self.width_var.set(9)
            self.height_var.set(9)
            self.bombs_var.set(10)
        elif value == "Intermediate":
            self.width_var.set(16)
            self.height_var.set(16)
            self.bombs_var.set(40)
        elif value == "Expert":
            self.width_var.set(30)
            self.height_var.set(16)
            self.bombs_var.set(99)
        elif value == "Master":
            self.width_var.set(32)
            self.height_var.set(32)
            self.bombs_var.set(256)
        if value != "Custom":
            self.width_entry.configure(state="readonly")
            self.height_entry.configure(state="readonly")
            self.bombs_entry.configure(state="readonly")
        elif value == "Custom":
            self.width_entry.configure(state="normal")
            self.height_entry.configure(state="normal")
            self.bombs_entry.configure(state="normal")

    def update_time(self) -> None:
        """ Start constantly update of time in counter. """
        if self.time_count:
            self.time_var.set(value=int(self.time_var.get() + 1))
        self.after(1000, self.update_time)


class MineField(tk.Frame):
    """
    Frame with game minefield.
    """

    def __init__(self, master: tk.Widget, window: MineSweeperApplication,
                 n_columns: int = 9, n_rows: int = 9, n_bombs: int = 10) -> None:
        """
        Game minefield.
        Creates minefield with Square class objects inside based on given arguments.

        :param master: Master widget inside which MineField object will be stored.
        :param window: Main window object.
        :param n_columns: Number of columns in grid with Square objects.
        :param n_rows: Number of rows in grid with Square objects.
        :param n_bombs: Number of bombs among Square objects.
        """
        super().__init__(master=master)
        self.window = window

        # is in mode of flag set or in mode of mouse click
        self._is_flag = False
        # count of flags
        self._number_of_flags = self.window.number_of_flags

        # create list with all Square objects coordinates
        self.coordinates = [GridCoordinates(x, y) for x in range(n_columns) for y in range(n_rows)]

        # create set with Square objects coordinates which should contain the bomb
        self.bombs_coordinates = set()
        self.create_random_coordinates = lambda: GridCoordinates(random.randint(0, n_columns - 1),
                                                                 random.randint(0, n_rows - 1))
        random_coordinates = self.create_random_coordinates()
        for x in range(n_bombs):
            # make sure that's every coordinate for bomb is unique
            while random_coordinates in self.bombs_coordinates:
                random_coordinates = self.create_random_coordinates()
            self.bombs_coordinates.add(random_coordinates)

        # create Square objects on every coordinate in set and put in to MineField grid
        for coordinate in self.coordinates:
            square = Square(self, coordinate)
            square.grid(column=coordinate[0], row=coordinate[1], rowspan=1, columnspan=1)

        # add bombs to squares and add number to bomb counter inside other squares near to bombs
        for _square in self.children.items():
            square = cast(Square, _square[1])
            if square.grid_coordinates in self.bombs_coordinates:
                square.is_bomb = True
                coordinates_to_add = adjoining_coordinates(square.grid_coordinates)
                for _s in self.children.items():
                    s = cast(Square, _s[1])
                    if not s.is_bomb and s.grid_coordinates in coordinates_to_add:
                        try:
                            s.bomb_count += 1
                        except ValueError:
                            pass

    @property
    def is_flag(self) -> bool:
        """ Get flag status. """
        return self._is_flag

    @is_flag.setter
    def is_flag(self, state: bool) -> None:
        """ Set flag status. """
        if isinstance(state, bool):
            self._is_flag = state
        else:
            raise ValueError("MineField property 'is_flag' accepts only a value with the type 'bool'.")

    @property
    def number_of_flags(self) -> int:
        """ Get number of flags inside field. """
        return self._number_of_flags

    @number_of_flags.setter
    def number_of_flags(self, count: int) -> None:
        """ Set number of flags inside field. """
        if isinstance(count, int):
            self._number_of_flags = count
            self.window.number_of_flags = self._number_of_flags
        else:
            raise ValueError("MineField property 'number_of_flags' accepts only a value with the type 'int'.")

    def make_all_adjoining_blank_squares_unhidden(self, target_square: "Square") -> None:
        """
        Method for making all adjoining squares without bombs unhidden.

        :param target_square: Object of target square.
        :return: None.
        """
        adjoining_set = adjoining_coordinates(target_square.grid_coordinates)
        for _square in self.children.items():
            square = cast(Square, _square[1])
            if square.is_hidden and square.grid_coordinates in adjoining_set \
                    and not square.is_bomb and not square.is_flagged:
                square.is_hidden = False
                if square.bomb_count == 0:
                    self.make_all_adjoining_blank_squares_unhidden(square)

    def show_all_mines(self) -> None:
        """
        Method for showing all the mines on field.
        :return: None
        """
        for _square in self.children.items():
            square = cast(Square, _square[1])
            if square.is_bomb:
                square.is_hidden = False

    def flag_all_mines(self) -> None:
        """
        Method for flagging all the mines on field.
        :return: None
        """
        for _square in self.children.items():
            square = cast(Square, _square[1])
            if square.is_flagged:
                square.is_flagged = False
            if square.is_bomb:
                square.is_flagged = True

    def field_scan(self) -> None:
        """
        Method for scan state of squares inside this minefield and decide is it nothing, win or lose.
        Also, makes all adjoining squares to blank and 0 bombs count squares unhidden.

        :return: None.
        """
        # make all adjoining blank squares unhidden
        for square in self.children.items():
            s = cast(Square, square[1])
            if not s.is_bomb and s.bomb_count == 0 and not s.is_hidden:
                self.make_all_adjoining_blank_squares_unhidden(s)
        # check if the game state is win, lose, or nothing.
        self.window.time_count = True
        win, lose, lose_point = True, False, None
        for square in self.children.items():
            s = cast(Square, square[1])
            if s.is_bomb and not s.is_hidden:
                lose = True
                lose_point = s
            elif not s.is_bomb and s.is_hidden:
                win = False
        if lose:
            self.window.time_count = False
            self.show_all_mines()
            lose_point.label.configure(image=self.window.textures.fail_bomb_unhidden)
            messagebox.showwarning("MineSweeper", "you lose")
        elif win:
            self.window.time_count = False
            self.flag_all_mines()
            messagebox.showinfo("MineSweeper", "you win")
        if lose or win:
            for square in self.children.items():
                s = cast(Square, square[1])
                s.is_active = False


class Square(tk.Frame):
    """
    Frame of one minefield square.
    """

    def __init__(self, master: MineField, grid_coordinates: Tuple[int, int]) -> None:
        """
        One minefield square.

        :param master: MineField object inside which this square contains.
        :param grid_coordinates: Coordinates where this square placed inside MineField grid.
        """
        if isinstance(master, MineField):
            self._master = cast(MineField, master)
            super().__init__(master=master)
        else:
            raise ValueError("Argument 'master' should have type 'MineField' "
                             "in order to successfully create Square object.")

        try:
            if isinstance(grid_coordinates[0], int) and isinstance(grid_coordinates[1], int):
                self._grid_coordinates = GridCoordinates(column=grid_coordinates[0], row=grid_coordinates[1])
            else:
                raise ValueError
        except Exception:
            raise ValueError("Argument 'grid_coordinates' should looks like 'Tuple[int, int]' "
                             "in order to successfully create Square object.")

        # create private attributes of square state
        self._is_active = True
        self._is_bomb = False
        self._is_hidden = True
        self._is_flagged = False
        self._near_bomb_count = 0

        # create label which will display state of unhidden square (empty, or next to the bomb, or the bomb itself)
        self._label = tk.Label(self, image=self._master.window.textures.blank_unhidden)
        self._label.grid(column=0, row=0)

        # create button which will be under label while square is hidden and make it unhidden on press
        self._button = tk.Button(self, command=self._on_button_press, image=self._master.window.textures.blank_hidden)
        self._button.grid(column=0, row=0)

    @property
    def grid_coordinates(self) -> GridCoordinates:
        """Get square coordinates on minefield grid. """
        return self._grid_coordinates

    @property
    def is_active(self) -> bool:
        """ Get is square active or disabled. """
        return self._is_active

    @is_active.setter
    def is_active(self, state: bool) -> None:
        """ Set square state to active or disabled. """
        if isinstance(state, bool):
            self._is_active = state
            if state:
                for child in self.winfo_children():
                    child = cast(tk.Label, child)
                    child.configure(state="active")
            else:
                for child in self.winfo_children():
                    child = cast(tk.Label, child)
                    child.configure(state="disabled")
        else:
            raise ValueError("Square property 'is_active' accepts only a value with the type 'bool'.")

    @property
    def is_bomb(self) -> bool:
        """ Get is this square contains the bomb. """
        return self._is_bomb

    @is_bomb.setter
    def is_bomb(self, state: bool) -> None:
        """ Set is this square contains the bomb or not. """
        if isinstance(state, bool):
            self._is_bomb = state
            if state:
                self._label.configure(image=self._master.window.textures.bomb_unhidden)
            else:
                self.bomb_count = self.bomb_count
        else:
            raise ValueError("Square property 'is_bomb' accepts only a value with the type 'bool'.")

    @property
    def is_hidden(self) -> bool:
        """ Get is this square is hidden. """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, state: bool) -> None:
        """ Set this square to hidden or unhidden state. """
        if isinstance(state, bool):
            self._is_hidden = state
            if state:
                self._button.grid(column=0, row=0)
            else:
                self._button.grid_forget()
        else:
            raise ValueError("Square property 'is_hidden' accepts only a value with the type 'bool'.")

    @property
    def is_flagged(self) -> bool:
        """ Get is this square flagged. """
        return self._is_flagged

    @is_flagged.setter
    def is_flagged(self, state: bool) -> None:
        """ Set or get rid of the flag on this square. also, updates minefield number of flags."""
        if isinstance(state, bool):
            self._is_flagged = state
            if state:
                self._button.configure(image=self._master.window.textures.flag_hidden)
                self._master.number_of_flags -= 1
            else:
                self._button.configure(image=self._master.window.textures.blank_hidden)
                self._master.number_of_flags += 1
        else:
            raise ValueError("Square property 'is_flagged' accepts only a value with the type 'bool'.")

    @property
    def bomb_count(self) -> int:
        """ Get count of squares with bombs near this square. """
        return self._near_bomb_count

    @bomb_count.setter
    def bomb_count(self, state: int) -> None:
        """ Set count of squares with bombs near this square. """
        if not self.is_bomb:
            if isinstance(state, int):
                self._near_bomb_count = state
                if state == 0:
                    self._label.configure(image=self._master.window.textures.blank_unhidden)
                elif state == 1:
                    self._label.configure(image=self._master.window.textures.one_unhidden)
                elif state == 2:
                    self._label.configure(image=self._master.window.textures.two_unhidden)
                elif state == 3:
                    self._label.configure(image=self._master.window.textures.three_unhidden)
                elif state == 4:
                    self._label.configure(image=self._master.window.textures.four_unhidden)
                elif state == 5:
                    self._label.configure(image=self._master.window.textures.five_unhidden)
                elif state == 6:
                    self._label.configure(image=self._master.window.textures.six_unhidden)
                elif state == 7:
                    self._label.configure(image=self._master.window.textures.seven_unhidden)
                elif state == 8:
                    self._label.configure(image=self._master.window.textures.eight_unhidden)
                else:
                    raise ValueError("Square property 'bomb_count' can only have value between 0 and 8.")
            else:
                raise ValueError("Square property 'bomb_count' accepts only a value with the type 'int' or 'None'.")
        else:
            raise ValueError("Square property 'bomb_count' can't be changed if property 'is_bomb' is 'True'.")

    def is_adjoin(self, target_square: "Square") -> bool:
        """
        Method for check if target square is adjoin with this square or not.

        :param target_square: Target square object.
        :return: True or False.
        """
        coordinates = adjoining_coordinates(target_square.grid_coordinates)
        return self.grid_coordinates in coordinates

    def _on_button_press(self) -> None:
        """ Method for square button press. make square unhidden if not flag and run field scan. """
        if self._master.is_flag:
            if self.is_flagged:
                self.is_flagged = False
            elif not self._master.number_of_flags <= 0:
                self.is_flagged = True
        elif not self.is_flagged:
            self.is_hidden = False
            self._master.field_scan()

    @property
    def label(self) -> tk.Label:
        """ Get label of square. """
        return self._label








