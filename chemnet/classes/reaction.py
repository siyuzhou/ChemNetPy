from .species import Species


class Reaction:
    def __init__(self, reactants, products, forward_rate, backward_rate):
        if not isinstance(reactants, (list, tuple)):
            raise TypeError('reactants must be a sequence of Species')
        if not isinstance(products, (list, tuple)):
            raise TypeError('products must be a sequence of Species')

        self.reactants = {}
        self.products = {}

        for reactant in reactants:
            if not isinstance(reactant, Species):
                raise TypeError('reactants must be an sequence of Species')
            self.reactants[reactant.name] = reactant

        for product in products:
            if not isinstance(product, Species):
                raise TypeError('product must be an instance of Species')
            self.products[product.name] = product

        self.forward_rate = forward_rate
        self.backward_rate = backward_rate

        self.formula = ('+'.join(sorted(self.reactants)) +
                        '<->' +
                        '+'.join(sorted(self.products)))

    def __eq__(self, other):
        return self.formula == other.formula

    def has_reactant(self, name):
        return name in self.reactants

    def has_product(self, name):
        return name in self.products

    def has_species(self, name):
        return self.has_reactant(name) or self.has_product(name)

    def react(self, dt, update=False):
        forward_effect = self.forward_rate
        backward_effect = self.backward_rate
        for reactant in self.reactants.values():
            forward_effect *= reactant.concentration
        for product in self.products.values():
            backward_effect *= product.concentration

        change = {}
        for reactant in self.reactants.values():
            change[reactant.name] = dt * (backward_effect
                                          - forward_effect
                                          - reactant.concentration * reactant.decay
                                          + reactant.inflow)
        for product in self.products.values():
            change[product.name] = dt * (forward_effect
                                         - backward_effect
                                         - product.concentration * product.decay
                                         + product.inflow)

        if update:
            self.update(change)

        return change

    def update(self, change):
        for reactant in self.reactants.values():
            reactant.concentration += change[reactant.name]

        for product in self.products.values():
            product.concentration += change[product.name]
