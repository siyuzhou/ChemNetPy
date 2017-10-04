import unittest
import chemnet


class TestNetwork(unittest.TestCase):
    def test_network(self):
        c1 = chemnet.Species('10', 1, 0)
        c2 = chemnet.Species('01', 1, 0)
        c3 = chemnet.Species('1001', 2, 0)

        r1 = chemnet.Reaction([c1, c2], [c3], 1, 1)

        net = chemnet.Network()

        net.add_reaction(r1)
        self.assertIn(r1, net.reactions)

        c4 = chemnet.Species('0110', 1, 0)
        net.add_species(c4)
        self.assertIn(c4.name, net.species)

        with self.assertRaises(KeyError):
            net.form_reaction(['10', '0'], ['0110'], 1, 1)

        net.form_reaction(['10', '01'], ['0110'], 1, 1)
        self.assertEqual(len(net.reactions), 2)
        self.assertIn(c4.name, net.reactions[1].products)
        self.assertIn(c1.name, net.reactions[1].reactants)
        self.assertIn(c2.name, net.reactions[1].reactants)

        net.update(0.1)
        self.assertAlmostEqual(c1.concentration, 1.1)
        self.assertAlmostEqual(c2.concentration, 1.1)
        self.assertAlmostEqual(c3.concentration, 1.9)
        self.assertAlmostEqual(c4.concentration, 1)
