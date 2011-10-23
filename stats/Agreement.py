import math
import unittest
from collections import defaultdict

class Agreement:
    """
    Class for computing inter-rater reliability

    """

    def __init__(self, rater_responses):
        """
        Arguments:
        rater_responses -- a list of maps of item labels.  ex. [{'item1':1, 'item2':5}, {'item1':2}]
        """
        if len(rater_responses) < 2:
            return

        self.ratings = rater_responses
        pass

    def krippendorffAlpha(self, metric=None):
        if metric is None:
            metric = Agreement.differenceNominal
        items = set([k for r in self.ratings for k in r.keys()])
        valueCounts, coincidence = self.computeCoincidenceMatrix(items, self.ratings)
        n = sum(valueCounts.values())


        numeratorItems = [coincidence[c][k] * metric(c,k) \
            for (c, nc) in valueCounts.iteritems() for (k, nk) in valueCounts.iteritems()]
                
        denominatorItems = [nc * nk * metric(c,k)  for (c, nc) in valueCounts.iteritems() for (k, nk) in valueCounts.iteritems()]
        Do = (n-1) * sum(numeratorItems)
        De = sum(denominatorItems)
        alpha = 1 - Do / De

        return alpha



    def computeCoincidenceMatrix(self, items, ratings):
        """
        From Wikipedia: A coincidence matrix cross tabulates the n pairable values
        from the canonical form of the reliability data into a v-by-v square
        matrix, where v is the number of values available in a variable. Unlike
        contingency matrices, familiar in association and correlation statistics,
        which tabulate pairs of values (Cross tabulation), a coincidence matrix
        tabulates all pairable values. A coincidence matrix omits references to
        coders and is symmetrical around its diagonal, which contains all perfect
        matches, c = k. The matrix of observed coincidences contains frequencies:
        o_ck = sum(# of c-k pairs in u (ratings) / m_u -1)
    
        ratings - list[dict[item] => label]
    
        returns - dict[label] => int = valueCounts
                  dict[(label,label)] => double coincidence value,
        """
    
        coincidence = defaultdict(lambda: defaultdict(int))
        valueCounts = defaultdict(int)

        for item in items:
            itemRatings = [r[item] for r in ratings if item in r]
            numRaters = len(itemRatings)
            if numRaters < 2: continue

            fractionalCount = 1.0 / (numRaters-1)       # m_u = numRaters - 1
            for i, ri in enumerate(itemRatings):
                valueCounts[ri] += 1
                for j, rj in enumerate(itemRatings):
                    if i == j: continue
                    coincidence[ri][rj] += fractionalCount

        return valueCounts, coincidence

         

    @classmethod
    def differenceNominal(cls, c, k):
        return int (c != k)

    @classmethod
    def differenceOrdinal(cls, nc, nk):
        return 0

    @classmethod
    def differenceInterval(cls, c, k):
        return math.pow(c-k, 2)

    @classmethod
    def differenceRatio(cls, c, k):
        return math.pow(float(c-k)/(c+k), 2)


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

