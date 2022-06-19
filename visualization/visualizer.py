import sys
import time
import pygame
from pygame.locals import QUIT

from mdp.mdp import MDP
from visualization.gridworld import GridWorld


class Visualizer:
    def __init__(
        self,
        mdp: MDP,
        trajectory: list,
        pause_time: float = 2,
        window_title: str = "Grid world",
        surface_size: tuple = (800, 800),
    ) -> None:
        """
        Construct a visualizer of a trajectory

        :param mdp: a mdp, the environment
        :param trajectory: a list of states
        :param pause_time: the time to pause between states, defaults to 2
        :param window_title: the tile of the window, defaults to "Grid world"
        :param surface_size: the size of the surface, defaults to (800, 800)
        """
        self.mdp = mdp
        self.trajectory = trajectory
        self.pause_time = pause_time

        self.surface_size = surface_size
        self.window_title = window_title

    def visualize(self) -> None:
        """
        Start the visualization
        """
        pygame.init()
        self.surface = pygame.display.set_mode(self.surface_size, 0, 0)

        pygame.display.set_caption(self.window_title)
        board = GridWorld(
            self.surface,
            board_size=self.mdp.grid_world_size,
            obs_coords=self.mdp.obstacles,
            sub_goals_coords={
                k: v for k, v in self.mdp.L.items() if v in {"a", "b", "c"}
            },
            start_coord=self.trajectory[0],
        )
        board.draw()

        pygame.display.update()
        for position in self.trajectory:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            board.step(position)

            board.draw()

            pygame.display.update()

            time.sleep(self.pause_time)

        pygame.quit()
