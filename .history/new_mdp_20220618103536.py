__authors__ = ["Jie Fu", "Lening Li"]
__emails__ = ["fujie@ufl.edu", "lli4@wpi.edu"]
__copyright__ = "Copyright 2022, The Qualitative Logic + Temporal Logic Project"
__date__ = "2022-03-12"

__license__ = "GPL"
__version__ = "0.0.1"
__description__ = "This code defines a class of Markov Decision Process."
__status__ = "Production"

import numpy as np
import yaml
from collections import defaultdict
import pandas as pd
from tabulate import tabulate
from pprint import pformat
from utils import *


class MDP(object):
    """
    A Markov Decision Process defined by
     1. an initial state,
     2. transition model --- the probability transition matrix implemented as a dictionary: prob[s][a][s'] is the probability of going from s to s' with action a,
     3. reward function.
     4. gamma value, for use by algorithms
     5. AP: a set of atomic propositions implemented as a list: Each proposition is identified by an index between 0-N.
     6. L: the labeling function implemented as a dictionary: L[s]: a subset of AP.
     7. obstacles: a list of terminal states
    We keep track of the possible actions for state s: prob[s].keys() and possible next states with action a: prob[s][a].keys()
    """

    def __init__(self, **kwargs):
        """If file path is not empty, initialize from the file"""
        if "file_path" in kwargs:
            # Read YAML file
            with open(kwargs["file_path"], "r") as stream:
                data_loaded = yaml.safe_load(stream)

            # directly assign the values to the variables in the yaml files besides "P"
            for key in data_loaded:
                if key != "P":
                    setattr(self, key, data_loaded[key])
            # process specifically for the transition probabilities
            self.prob = defaultdict(lambda: defaultdict(dict))
            for x in data_loaded["P"]:
                s, a, ns, p = x
                self.prob[s][a][ns] = p
            # call to validate the transition probabilities
            self.validate()
            return
