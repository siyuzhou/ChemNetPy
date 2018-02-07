import random
import chemnet
import numpy as np

INIT_CONCENTRATION_LIMIT = 2
INIT_INFLOW_LIMIT = 1
INIT_DECAY_LIMIT = 1

POTENTIAL_LIMIT = 7.5
CONCENTRATION_LIMIT = 5
INFLOW_LIMIT = 5
DECAY_LIMIT = 10

INIT_POPULATION = 20


def random_species(name=None, l=3, isfood=False):
    if not name:
        name = []
        for _ in range(l):
            name.append(random.choice(['0', '1']))
        name = ''.join(name)

    concentration = random.random() * INIT_CONCENTRATION_LIMIT
    potential = random.random() * POTENTIAL_LIMIT
    decay = random.random() * INIT_DECAY_LIMIT

    inflow = random.random() * INIT_INFLOW_LIMIT if isfood else 0

    return chemnet.Species(name, concentration, potential, decay, inflow)


def add_reaction(reactant1, reactant2=None, chemistry=3):
    if reactant2:
        if chemistry == 3:
            name3 = reactant1.name + reactant2.name
            product = random_species(name3)
        reaction = chemnet.Reaction([reactant1, reactant2], [product], 1, 1)
    return reaction


def main():
    net = chemnet.Network()

    for _ in range(4):
        net.add_species(random_species())
