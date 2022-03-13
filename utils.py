import os


def check_existence(prefix):
    path = os.path.join("./", prefix)
    if not os.path.exists(path):
        os.makedirs(path)
