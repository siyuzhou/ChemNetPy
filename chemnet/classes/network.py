from .species import Species
from .reaction import Reaction


class Network:
    def __init__(self, species=None, reactions=None):
        self.reactions = {}
        self.species = {}

        if species:
            if not isinstance(species, (list, tuple)):
                raise TypeError('species must be a sequence of Species')
            for s in species:
                self.add_species(s)

        if reactions:
            if not isinstance(reactions, (list, tuple)):
                raise TypeError('reactions must be a sequence of Reaction')

            for r in reactions:
                self.add_reaction(r)

    def has_species(self, species):
        if isinstance(species, Species):
            return species.name in self.species
        return species in self.species

    def has_reaction(self, reaction):
        return reaction.formula in self.reactions

    def has_formula(self, formula):
        return formula in self.reactions

    def add_species(self, species):
        if not isinstance(species, Species):
            raise TypeError('species must be an instance of Species')
        return self.species.setdefault(species.name, species)

    def form_reaction(self, reactant_names, product_names, forward_rate, backward_rate):
        """Form a new reaction with reactants and products in the network."""
        try:
            reactants = [self.species[rname] for rname in reactant_names]
            products = [self.species[pname] for pname in product_names]

            new_reaction = Reaction(reactants, products, forward_rate, backward_rate)

            if self.has_reaction(new_reaction):
                return None

            self.reactions[new_reaction.formula] = new_reaction
            return new_reaction

        except KeyError:
            raise ValueError('cannot form reaction with species not in network')

    def add_reaction(self, reaction):
        if not isinstance(reaction, Reaction):
            raise TypeError('reaction must be an instance of Reaction')

        if self.has_reaction(reaction):
            return self.reactions[reaction.formula]

        self.reactions[reaction.formula] = reaction

        for rname, reactant in reaction.reactants.items():
            reaction.reactants[rname] = self.species.setdefault(rname, reactant)
        for pname, product in reaction.products.items():
            reaction.products[pname] = self.species.setdefault(pname, product)

        return self.reactions[reaction.formula]

    def remove_reaction(self, reactant_names, product_names):
        formula = ('+'.join(sorted(reactant_names)) +
                   '<->' +
                   '+'.join(sorted(product_names)))
        try:
            return self.reactions.pop(formula)
        except KeyError:
            raise ValueError('reaction not in network')

    def remove_formula(self, formula):
        if formula in self.reactions:
            return self.reactions.pop(formula)

        left, right = formula.split('<->')
        reactant_names = left.strip().split('+')
        product_names = right.strip().splie('+')
        new_formula = ('+'.join(sorted(rname.strip() for rname in reactant_names)) +
                       '<->' +
                       '+'.join(sorted(pname.strip() for pname in product_names)))

        if new_formula not in self.reactions:
            raise ValueError('{} not in reactions'.format(formula))
        return self.reactions.pop(new_formula)

    def remove_species(self, name):
        try:
            self.species.pop(name)

            formulas_to_remove = []
            for formula, reaction in self.reactions.items():
                if reaction.has_species(name):
                    formulas_to_remove.append(formula)

            for formula in formulas_to_remove:
                self.reactions.pop(formula)

        except KeyError:
            raise ValueError('"{}" not in network'.format(name))

    def update(self, dt):
        total_change = {}
        for reaction in self.reactions.values():
            concentration_change = reaction.react(dt)
            for name in concentration_change:
                total_change[name] = total_change.get(
                    name, 0) + concentration_change[name]

        for name, species in self.species.items():
            species.concentration += total_change.get(name, 0)
