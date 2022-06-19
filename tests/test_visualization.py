import pygame
from visualization.visualizer import Visualizer


def test_visualize_trajectory(construct_mdp):
    trajectory = [(0, 0), (0, 1), (0, 2), (1, 2)]
    visualizer = Visualizer(mdp=construct_mdp, trajectory=trajectory)
    visualizer.visualize()
