class Species:
    def __init__(self, name, concentration, potential, decay=0, inflow=0):
        self.__name = name
        self.concentration = concentration
        self.potential = potential
        self.decay = decay
        self.inflow = inflow

    @property
    def name(self):
        return self.__name

    @property
    def concentration(self):
        return self.__concentration

    @concentration.setter
    def concentration(self, value):
        self.__concentration = max(0, value)

    @property
    def potential(self):
        return self.__potential

    @potential.setter
    def potential(self, value):
        self.__potential = value

    @property
    def decay(self):
        return self.__decay

    @decay.setter
    def decay(self, value):
        self.__decay = max(0, value)

    @property
    def inflow(self):
        return self.__inflow

    @inflow.setter
    def inflow(self, value):
        self.__inflow = max(0, value)
