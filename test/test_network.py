import unittest
import chemnet


class TestNetwork(unittest.TestCase):
    def test_add_species(self):
        net = chemnet.Network()

        c4 = chemnet.Species('0110', 1, 0)
        net.add_species(c4)
        self.assertIn(c4.name, net.species)
        self.assertTrue(net.has_species(c4))

    def test_add_reaction(self):
        c1 = chemnet.Species('10', 1, 0)
        c2 = chemnet.Species('01', 1, 0)
        c3 = chemnet.Species('1001', 2, 0)

        r1 = chemnet.Reaction([c1, c2], [c3], 1, 1)

        net = chemnet.Network()
        net.add_reaction(r1)

        self.assertIn(r1.formula, net.reactions)
        self.assertTrue(net.has_reaction(r1))
        self.assertTrue(net.has_species(c1))
        self.assertTrue(net.has_species(c2))
        self.assertTrue(net.has_species(c3))

    def test_form_reaction(self):
        c1 = chemnet.Species('10', 1, 0)
        c2 = chemnet.Species('01', 1, 0)
        c3 = chemnet.Species('1001', 2, 0)

        net = chemnet.Network([c1, c2, c3])

        with self.assertRaises(ValueError):
            net.form_reaction(['10', '0'], ['0110'], 1, 1)

        net.form_reaction(['10', '01'], ['1001'], 1, 1)
        self.assertTrue(net.has_formula('01+10<->1001'))

    def test_update(self):
        c1 = chemnet.Species('10', 1, 0)
        c2 = chemnet.Species('01', 1, 0)
        c3 = chemnet.Species('1001', 2, 0)

        r1 = chemnet.Reaction([c1, c2], [c3], 1, 1)
        c4 = chemnet.Species('0110', 1, 0)

        net = chemnet.Network([c4], [r1])
        net.form_reaction(['01', '10'], ['0110'], 1, 1)
        net.update(0.1)
        self.assertEqual(c1.concentration, 1.1)
        self.assertEqual(c2.concentration, 1.1)
        self.assertEqual(c3.concentration, 1.9)

    def test_remove_species(self):
        c1 = chemnet.Species('10', 1, 0)
        c2 = chemnet.Species('01', 1, 0)
        c3 = chemnet.Species('1001', 2, 0)

        r1 = chemnet.Reaction([c1, c2], [c3], 1, 1)
        c4 = chemnet.Species('0110', 1, 0)

        net = chemnet.Network([c4], [r1])

        self.assertTrue(net.has_species('0110'))
        net.remove_species('0110')
        self.assertFalse(net.has_species('0110'))

        with self.assertRaises(ValueError):
            net.remove_species('0110')

        self.assertTrue(net.has_reaction(r1))
        net.remove_species('10')
        self.assertFalse(net.has_reaction(r1))

        self.assertEqual(set(net.species), set(['1001', '01']))
