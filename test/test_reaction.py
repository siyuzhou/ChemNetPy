import unittest
import chemnet


class TestReaction(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestReaction, self).__init__(*args, **kwargs)

        r1 = chemnet.Species('10', 1, 0.2, 0.1, 0.1)
        r2 = chemnet.Species('01', 2, 0.3, 0.2, 0)
        p1 = chemnet.Species('1001', 1, 0.5, 0.15, 0)

        self.reaction = chemnet.Reaction([r1, r2], [p1], 1, 1, 'reaction1')

    def test_reaction_name(self):
        self.assertEqual(self.reaction.name, 'reaction1')

    def test_reaction(self):
        change = self.reaction.react(0.1)
        self.assertAlmostEqual(change['10'], -0.1)
        self.assertAlmostEqual(change['01'], -0.14)
        self.assertAlmostEqual(change['1001'], 0.085)

    def test_update(self):
        self.reaction.react(0.1, update=True)
        self.assertAlmostEqual(
            self.reaction.reactants['10'].concentration, 0.9)
        self.assertAlmostEqual(
            self.reaction.reactants['01'].concentration, 1.86)
        self.assertAlmostEqual(
            self.reaction.products['1001'].concentration, 1.085)
