from visualization.visualizer import Visualizer


def test_visualize_trajectory(construct_mdp):
    trajectory = [(6, 6), (0, 1), (0, 2), (1, 2)]
    visualizer = Visualizer(
        mdp=construct_mdp, trajectory=trajectory, pause_time=0, draw=False
    )
    visualizer.visualize()


def test_visualize_trajectory(construct_a_inaccessiable_mdp):
    trajectory = [(6, 6), (0, 1), (0, 2), (1, 2)]
    visualizer = Visualizer(
        mdp=construct_a_inaccessiable_mdp,
        trajectory=trajectory,
        pause_time=6,
        draw=True,
    )
    visualizer.visualize()
