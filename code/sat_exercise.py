"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import csv
import sys

import myplot
import Pmf
import thinkstats


def ReadRanks(filename='sat_ranks.csv'):
    """Reads a CSV file of SAT scores.

    Args:
      filename: string filename

    Returns:
      list of (score, number) pairs
    """
    fp = open(filename)
    reader = csv.reader(fp)
    res = []

    for t in reader:
        try:
            score = int(t[0])
            number = int(t[1])
            res.append((score, number))
        except ValueError:
            pass

    return res


def ReadScale(filename='sat_scale.csv', col=2):
    """Reads a CSV file of SAT scales (maps from raw score to standard score).

    Args:
      filename: string filename
      col: which column to start with (0=Reading, 2=Math, 4=Writing)

    Returns:
      list of (raw score, standardize score) pairs
    """
    def ParseRange(s):
        t = [int(x) for x in s.split('-')]
        return 1.0 * sum(t) / len(t)

    fp = open(filename)
    reader = csv.reader(fp)
    raws = []
    scores = []

    for t in reader:
        try:
            raw = int(t[col])
            raws.append(raw)
            score = ParseRange(t[col+1])
            scores.append(score)
        except:
            pass

    raws.sort()
    scores.sort()
    return thinkstats.Interpolator(raws, scores)


def ReverseScale(pmf, scale):
    """Applies the reverse scale to the values of a PMF.

    Args:
        pmf: Pmf of scaled scores
        scale: Interpolator object

    Returns:
        Pmf of raw scores
    """
    new = Pmf.Pmf()
    for val, prob in pmf.Items():
        raw = scale.Reverse(val)
        new.Incr(raw, prob)
    return new


def DivideValues(pmf, denom):
    """Divides the values in a PMF by denom.  Returns a new PMF."""
    new = Pmf.Pmf()
    for val, prob in pmf.Items():
        if val >= 0:
            x = 1.0 * val / denom
            new.Incr(x, prob)
    return new


class Exam:
    """Encapsulates information about an exam.

    Contains the distribution of scaled scores and an
    Interpolator that maps between scaled and raw scores.
    """
    def __init__(self):
        # scores is a list of (scaled score, number pairs)
        scores = ReadRanks()

        # hist is the histogram of scaled scores
        hist = Pmf.MakeHistFromDict(dict(scores))

        # scaled is the PMF of scaled scores
        self.scaled = Pmf.MakePmfFromHist(hist)

        # scale is an Interpolator from raw scores to scaled scores
        self.scale = ReadScale()

        # raw is the PMF of raw scores
        self.raw = ReverseScale(self.scaled, self.scale)

        # max_score is the highest raw score
        self.max_score = max(self.raw.Values())

    def GetRawScore(self, scaled_score):
        """Looks up a scaled score and returns a raw score."""
        return self.scale.Reverse(scaled_score)

    def GetPrior(self):
        """Returns a new PMF of p, which is (raw_score / max_score)."""
        prior = DivideValues(self.raw, denom=self.max_score)
        return prior

    def GetMaxScore(self):
        """Returns the highest raw score, presumed to the the max possible."""
        return self.max_score


def main(script):

    # make an exam object with data from the 2010 SAT
    exam = Exam()

    # look up Alice's raw score
    alice = 780
    alice_correct = exam.GetRawScore(alice)
    print 'Alice raw score', alice_correct

    # display the distribution of raw scores for the population
    prior = exam.GetPrior()
    myplot.Pmf(prior, show=True)


if __name__ == '__main__':
    main(*sys.argv)
