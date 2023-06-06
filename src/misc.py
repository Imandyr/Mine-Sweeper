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

    Because tk.PhotoImage don't create image object without defined base window, I can't set them as default values.
    But I can add them as a comments.

    attributes:
        blank_hidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/flag_hidden.png")
        flag_hidden: tk.PhotoImage = tk.PhotoImage(file="./src/assets/textures/base_hidden.png")
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
    blank_hidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/flag_hidden.png")
    flag_hidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/base_hidden.png")
    blank_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/base_unhidden.png")
    one_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/1_unhidden.png")
    two_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/2_unhidden.png")
    three_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/3_unhidden.png")
    four_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/4_unhidden.png")
    five_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/5_unhidden.png")
    six_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/6_unhidden.png")
    seven_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/7_unhidden.png")
    eight_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/8_unhidden.png")
    bomb_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/bomb_unhidden.png")
    fail_bomb_unhidden: tk.PhotoImage  # = tk.PhotoImage(file="./src/assets/textures/fail_bomb_unhidden.png")











