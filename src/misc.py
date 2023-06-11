""" Module with various miscellaneous things. """


from dataclasses import dataclass
from abc import ABC
import tkinter as tk
from typing import NamedTuple


class GridCoordinates(NamedTuple):
    """
    Named tuple for coordinates on grid.

    GridCoordinates(column: int, row: int)
    """
    column: int
    row: int


def adjoining_coordinates(coordinates: GridCoordinates) -> set:
    """
    Function for making set of all adjoining grid coordinates to given coordinates.
    :param coordinates: Target coordinates.
    :return: Set with all adjoining coordinates.
    """
    x, y = coordinates[0], coordinates[1]
    return {GridCoordinates(x + 1, y), GridCoordinates(x, y + 1), GridCoordinates(x - 1, y),
            GridCoordinates(x, y - 1), GridCoordinates(x + 1, y - 1), GridCoordinates(x - 1, y + 1),
            GridCoordinates(x + 1, y + 1), GridCoordinates(x - 1, y - 1)}


@dataclass
class Textures(ABC):
    """
    Base abstract class for all game texture-packs.

    Textures objects should ne added as tk.PhotoImage class variables.

    attributes:
            blank_hidden: tk.PhotoImage
            flag_hidden: tk.PhotoImage
            blank_unhidden: tk.PhotoImage
            one_unhidden: tk.PhotoImage
            two_unhidden: tk.PhotoImage
            three_unhidden: tk.PhotoImage
            four_unhidden: tk.PhotoImage
            five_unhidden: tk.PhotoImage
            six_unhidden: tk.PhotoImage
            seven_unhidden: tk.PhotoImage
            eight_unhidden: tk.PhotoImage
            bomb_unhidden: tk.PhotoImage
            fail_bomb_unhidden: tk.PhotoImage

    """
    blank_hidden: tk.PhotoImage
    flag_hidden: tk.PhotoImage
    blank_unhidden: tk.PhotoImage
    one_unhidden: tk.PhotoImage
    two_unhidden: tk.PhotoImage
    three_unhidden: tk.PhotoImage
    four_unhidden: tk.PhotoImage
    five_unhidden: tk.PhotoImage
    six_unhidden: tk.PhotoImage
    seven_unhidden: tk.PhotoImage
    eight_unhidden: tk.PhotoImage
    bomb_unhidden: tk.PhotoImage
    fail_bomb_unhidden: tk.PhotoImage


@dataclass
class HandmadeTextures(Textures):
    """
    My handmade texture-pack.

    attributes:
        blank_hidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/base_hidden.png")
        flag_hidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/flag_hidden.png")
        blank_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/base_unhidden.png")
        one_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/1_unhidden.png")
        two_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/2_unhidden.png")
        three_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/3_unhidden.png")
        four_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/4_unhidden.png")
        five_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/5_unhidden.png")
        six_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/6_unhidden.png")
        seven_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/7_unhidden.png")
        eight_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/8_unhidden.png")
        bomb_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/bomb_unhidden.png")
        fail_bomb_unhidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/fail_bomb_unhidden.png")

    """
    blank_hidden: tk.PhotoImage = None
    flag_hidden: tk.PhotoImage = None
    blank_unhidden: tk.PhotoImage = None
    one_unhidden: tk.PhotoImage = None
    two_unhidden: tk.PhotoImage = None
    three_unhidden: tk.PhotoImage = None
    four_unhidden: tk.PhotoImage = None
    five_unhidden: tk.PhotoImage = None
    six_unhidden: tk.PhotoImage = None
    seven_unhidden: tk.PhotoImage = None
    eight_unhidden: tk.PhotoImage = None
    bomb_unhidden: tk.PhotoImage = None
    fail_bomb_unhidden: tk.PhotoImage = None

    def __post_init__(self):
        """ Add textures after initialization. """
        self.blank_hidden = tk.PhotoImage(file="./src/assets/textures/base_hidden.png") \
            if self.blank_hidden is None else self.blank_hidden
        self.flag_hidden = tk.PhotoImage(file="./src/assets/textures/flag_hidden.png") \
            if self.flag_hidden is None else self.flag_hidden
        self.blank_unhidden = tk.PhotoImage(file="./src/assets/textures/base_unhidden.png") \
            if self.blank_unhidden is None else self.blank_unhidden
        self.one_unhidden = tk.PhotoImage(file="./src/assets/textures/1_unhidden.png") \
            if self.one_unhidden is None else self.one_unhidden
        self.two_unhidden = tk.PhotoImage(file="./src/assets/textures/2_unhidden.png") \
            if self.two_unhidden is None else self.two_unhidden
        self.three_unhidden = tk.PhotoImage(file="./src/assets/textures/3_unhidden.png") \
            if self.three_unhidden is None else self.three_unhidden
        self.four_unhidden = tk.PhotoImage(file="./src/assets/textures/4_unhidden.png") \
            if self.four_unhidden is None else self.four_unhidden
        self.five_unhidden = tk.PhotoImage(file="./src/assets/textures/5_unhidden.png") \
            if self.five_unhidden is None else self.five_unhidden
        self.six_unhidden = tk.PhotoImage(file="./src/assets/textures/6_unhidden.png") \
            if self.six_unhidden is None else self.six_unhidden
        self.seven_unhidden = tk.PhotoImage(file="./src/assets/textures/7_unhidden.png") \
            if self.seven_unhidden is None else self.seven_unhidden
        self.eight_unhidden = tk.PhotoImage(file="./src/assets/textures/8_unhidden.png") \
            if self.eight_unhidden is None else self.eight_unhidden
        self.bomb_unhidden = tk.PhotoImage(file="./src/assets/textures/bomb_unhidden.png") \
            if self.bomb_unhidden is None else self.bomb_unhidden
        self.fail_bomb_unhidden = tk.PhotoImage(file="./src/assets/textures/fail_bomb_unhidden.png") \
            if self.fail_bomb_unhidden is None else self.fail_bomb_unhidden











