class Species:
    def __init__(self, name, concentration, potential, decay=0, inflow=0):
        self.name = name
        self.concentration = concentration
        self.potential = potential
        self.decay = decay
        self.inflow = inflow


class Reaction:
    def __init__(self, reactants, products, forward_rate, backward_rate, name=None):
        self.reactants = {r.name: r for r in reactants}
        self.products = {p.name: p for p in products}
        self.forward_rate = forward_rate
        self.backward_rate = backward_rate
        self.name = name

    def react(self, dt, update=False):
        forward_effect = self.forward_rate
        backward_effect = self.backward_rate
        for reactant in self.reactants.values():
            forward_effect *= reactant.concentration
        for product in self.products.values():
            backward_effect *= product.concentration

        concentration_change = {}
        for reactant in self.reactants.values():
            concentration_change[reactant.name] = dt * (backward_effect
                                                        - forward_effect
                                                        - reactant.concentration * reactant.decay
                                                        + reactant.inflow)
        for product in self.products.values():
            concentration_change[product.name] = dt * (forward_effect
                                                       - backward_effect
                                                       - product.concentration * product.decay
                                                       + product.inflow)

        if update:
            self.update(concentration_change)

        return concentration_change

    def update(self, concentration_change):
        for reactant in self.reactants.values():
            reactant.concentration += concentration_change[reactant.name]

        for product in self.products.values():
            product.concentration += concentration_change[product.name]


class Network:
    def __init__(self):
        self.reactions = []
        self.species = {}

    def add_reaction(self, reaction):
        self.reactions.append(reaction)
        for species in reaction.reactants.values():
            self.add_species(species)
        for species in reaction.products.values():
            self.add_species(species)

    def add_species(self, species):
        if species.name not in self.species:
            self.species[species.name] = species

    def form_reaction(self, reactant_names, product_names, forward_rate, backward_rate, name=None):
        reactants = []
        products = []
        try:
            for name in reactant_names:
                reactants.append(self.species[name])
            for name in product_names:
                products.append(self.species[name])

            self.reactions.append(
                Reaction(reactants, products, forward_rate, backward_rate, name))
        except KeyError:
            raise KeyError('"{}" not in network species'.format(name))

    def update(self, dt):
        total_change = {}
        for reaction in self.reactions:
            concentration_change = reaction.react(dt)
            for name in concentration_change:
                total_change[name] = total_change.get(
                    name, 0) + concentration_change[name]

        for name, species in self.species.items():
            species.concentration += total_change.get(name, 0)
