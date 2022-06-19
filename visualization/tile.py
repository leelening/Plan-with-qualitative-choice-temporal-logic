import pygame


# User-defined classes
white_color = pygame.Color(247, 247, 247)
blue_color = pygame.Color(100, 143, 255)
purple_color = pygame.Color(120, 94, 240)
red_color = pygame.Color(220, 38, 127)
orange_color = pygame.Color(254, 97, 0)
yellow_color = pygame.Color(255, 176, 0)


class Tile:
    borderColor = pygame.Color("black")
    borderWidth = 4

    robot_image = pygame.image.load("visualization/figures/robot.png")
    pattern_image = pygame.image.load("visualization/figures/pattern_small.png")

    def __init__(
        self,
        x: float,
        y: float,
        obs: bool,
        sub_goal: bool,
        surface: pygame.Surface,
        tile_size: tuple = (100, 100),
        text: str = None,
    ):
        """
        Construct a tile

        :param x: x on the coordinate
        :param y: y on the coordinate
        :param obs: if this tile is an obstacle
        :param sub_goal: if this tile is a sub goal
        :param surface: the current surface
        :param tile_size: the size of the tile, defaults to (100, 100)
        :param text: the text of the current tile, defaults to None
        """
        self.obs = obs
        self.sub_goal = sub_goal
        self.surface = surface
        self.tile_size = tile_size
        self.text = text

        self.origin = (x, y)

    def draw(self, pos: list) -> None:
        """
        draw the tile

        :param pos: the position of the tile
        """
        rectangle = pygame.Rect(self.origin, self.tile_size)
        font = pygame.font.SysFont("Times New Roman", 72)
        pygame.draw.rect(self.surface, white_color, rectangle, 0)

        if self.obs:
            self.surface.blit(Tile.pattern_image, self.origin)
        elif self.sub_goal:
            pygame.draw.rect(self.surface, purple_color, rectangle, 0)
            self.surface.blit(
                font.render(self.text, True, white_color),
                (self.origin[0] + 35, self.origin[1] + 10),
            )

        if pos == [self.origin[0] // 100, self.origin[1] // 100]:
            self.surface.blit(Tile.robot_image, (self.origin[0] + 10, self.origin[1]))

        pygame.draw.rect(self.surface, Tile.borderColor, rectangle, Tile.borderWidth)
