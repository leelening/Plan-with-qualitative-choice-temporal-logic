import pygame, sys, time, random
from pygame.locals import *
from visualization.tile import Tile


class GridWorld:
    # An object in this class represents a Grid_World game.
    tile_width = 100
    tile_height = 100

    def __init__(
        self,
        surface: pygame.Surface,
        board_size: list,
        obs_coords: list,
        sub_goals_coords: dict,
    ):
        """
        Initialize a grid world

        :param surface: the surface to draw on
        :param board_size: the size of the board
        :param obs_coords: the coordinates of the obstacles
        :param sub_goals_coords: the coordinates of the sub goals
        """
        self.surface = surface
        self.bgColor = pygame.Color("black")
        self.board_size = list(board_size)
        self.obs_coords = obs_coords

        self.sub_goals_coords = sub_goals_coords

        self.position = list(start_coord)

        self.calc_obs_coords()
        self.calc_sub_goals_coords()
        self.create_tile()

    def calc_obs_coords(self):
        self.board_obs_coords = [
            [x, self.board_size[1] - y - 1] for x, y in self.obs_coords
        ]

    def calc_sub_goals_coords(self):
        self.board_sub_goals_coords = {
            v: [x, self.board_size[1] - y - 1]
            for (x, y), v in self.sub_goals_coords.items()
        }

    def find_board_coords(self, pos):
        if pos is not None:
            return [pos[0], self.board_size[1] - pos[1] - 1]
        return None

    def create_tile(self):
        # Create the Tiles
        # - self is the Grid_World game
        self.board = []
        for rowIndex in range(0, self.board_size[0]):
            row = []
            text = None
            for columnIndex in range(0, self.board_size[1]):
                x = columnIndex * self.tile_width
                y = rowIndex * self.tile_height
                if [columnIndex, rowIndex] in self.board_obs_coords:
                    obs = True
                else:
                    obs = False
                if [columnIndex, rowIndex] in self.board_sub_goals_coords.values():
                    sub_goal = True
                    for k, v in self.board_sub_goals_coords.items():
                        if [columnIndex, rowIndex] == v:
                            text = k
                            break
                else:
                    sub_goal = False

                tile = Tile(x, y, obs, sub_goal, self.surface, text=text)
                row.append(tile)
            self.board.append(row)

    def draw(self):
        # Draw the tiles.
        # - self is the Grid_World game
        pos = self.find_board_coords(self.position)

        self.surface.fill(self.bgColor)
        for row in self.board:
            for tile in row:
                tile.draw(pos)

    def step(
        self,
        position: list,
    ):
        self.position = list(position)
