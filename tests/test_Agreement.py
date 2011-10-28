import unittest
import stats
from stats.Agreement import *

class TestAgreement(unittest.TestCase):
    """
    Unit tests for Agreement class
    """

    def setUp(self):
        # Build ratings data
        # Ratings are list of dicts that map items to labels/values

        self.ratingsNoMissing = [
            {1:'a', 2:'a', 3:'b', 4:'b', 5:'d', 6:'c', 7:'c', 8:'c', 9:'e', 10:'d', 11:'d', 12:'a'},
            {1:'b', 2:'a', 3:'b', 4:'b', 5:'b', 6:'c', 7:'c', 8:'c', 9:'e', 10:'d', 11:'d', 12:'d'},
        ]

        self.ratingsMissing = [
            {1:1, 2:2, 3:3, 4:3, 5:2, 6:1, 7:4, 8:1, 9:2}, 
            {1:1, 2:2, 3:3, 4:3, 5:2, 6:2, 7:4, 8:1, 9:2, 10:5}, 
            {     2:3, 3:3, 4:3, 5:2, 6:3, 7:4, 8:2, 9:2, 10:5, 11:1, 12:3}, 
            {1:1, 2:2, 3:3, 4:3, 5:2, 6:4, 7:4, 8:1, 9:2, 10:5, 11:1}]

    def testNoMissing(self):
        self.agreement = Agreement(self.ratingsNoMissing) 
        alpha = self.agreement.krippendorffAlpha()
        self.assertEqual(round(alpha, 3), 0.692)

    def testMetricNominal(self):
        self.agreement = Agreement(self.ratingsMissing) 
        alpha = self.agreement.krippendorffAlpha(Agreement.differenceNominal)
        self.assertEqual(round(alpha, 3), 0.743)

    def testMetricOrdinal(self):
        self.agreement = Agreement(self.ratingsMissing) 
        alpha = self.agreement.krippendorffAlpha(Agreement.differenceOrdinal)
        self.assertEqual(round(alpha, 3), 0.815)

    def testMetricInterval(self):
        self.agreement = Agreement(self.ratingsMissing) 
        alpha = self.agreement.krippendorffAlpha(Agreement.differenceInterval)
        self.assertEqual(round(alpha, 3), 0.849)

    def testMetricRatio(self):
        self.agreement = Agreement(self.ratingsMissing) 
        alpha = self.agreement.krippendorffAlpha(Agreement.differenceRatio)
        self.assertEqual(round(alpha, 3), 0.797)

if __name__ == '__main__':
    unittest.main()

