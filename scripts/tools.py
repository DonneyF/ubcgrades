from nameparser import HumanName
from nameparser.util import u
import math

class HumanNameHashable(HumanName):
    def __hash__(self):
        return hash((u(self)).lower())

    def is_equal_except_middle(self, name):
        return self.first == name.first and self.last == name.last and self.title == name.title and \
               self.suffix == name.suffix and self.nickname == name.nickname and self.middle != name.middle


def combine_educator(educators: str):
    """Combines educators if they differ only by middle name. Keep the one with the middle name."""

    educators_set = {HumanNameHashable(educator) for educator in educators.split(';')}
    skip = set()
    for educator in set(educators_set):
        if educator in skip:
            continue
        # Check similarity of this educator against every other educator. This is O(n^2) maybe can be improved.
        educators_to_rm = set()
        for other_educator in educators_set:
            if educator.is_equal_except_middle(other_educator) and educator not in educators_to_rm:
                # Find which one has the longer middle name
                if len(educator.middle) > len(other_educator.middle):
                    # Keep the current educator
                    educators_to_rm.add(other_educator)
                else:
                    educators_to_rm.add(educator)

        for del_educator in educators_to_rm:
            educators_set.remove(del_educator)
            skip.add(del_educator)

    return ';'.join({str(educator) for educator in educators_set})


def composite_SD(means, SDs, ncounts):
    '''Calculate combined standard deviation via ANOVA (ANalysis Of VAriance)
       See:  http://www.burtonsys.com/climate/composite_standard_deviations.html
       Inputs are:
         means, the array of group means
         SDs, the array of group standard deviations
         ncounts, number of samples in each group (can be scalar
                  if all groups have same number of samples)
       Result is the overall standard deviation.
    '''
    G = len(means)  # number of groups
    if G != len(SDs):
        raise Exception('inconsistent list lengths')
    if not hasattr(ncounts, '__contains__'):
        ncounts = [ncounts] * G  # convert scalar ncounts to array
    elif G != len(ncounts):
        raise Exception('wrong ncounts list length')

    # calculate total number of samples, N, and grand mean, GM
    N = sum(ncounts)  # total number of samples
    if N <= 1:
        raise Exception("Warning: only " + str(N) + " samples, SD is incalculable")
    GM = 0.0
    for i in range(G):
        GM += means[i] * ncounts[i]
    GM /= N  # grand mean

    # calculate Error Sum of Squares
    ESS = 0.0
    for i in range(G):
        ESS += ((SDs[i]) ** 2) * (ncounts[i] - 1)

    # calculate Total Group Sum of Squares
    TGSS = 0.0
    for i in range(G):
        TGSS += ((means[i] - GM) ** 2) * ncounts[i]

    # calculate standard deviation as square root of grand variance
    result = math.sqrt((ESS + TGSS) / (N - 1))
    return result