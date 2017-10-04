import unittest
import chemnet


class TestSpecies(unittest.TestCase):
    def test_species(self):
        sp = chemnet.Species('01', 0.5, 0.7, 0.3, 0.1)
        self.assertEqual(sp.name, '01')
        self.assertEqual(sp.concentration, 0.5)
        self.assertEqual(sp.potential, 0.7)
        self.assertEqual(sp.decay, 0.3)
        self.assertEqual(sp.inflow, 0.1)
