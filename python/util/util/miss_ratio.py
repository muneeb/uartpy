
import math

from scipy.optimize import newton

def miss_ratio_rnd(rdist_hist, cache_size_lines):
    ref_count = sum(rdist_hist.values())

    def f(replacements):
        return 1.0 - math.pow(1.0 - 1.0 / cache_size_lines, replacements)

    def hist_misses(miss_ratio, rdist_hist):
        return sum(map(lambda (rdist, count) : count * f(miss_ratio * rdist), rdist_hist.items()))

    def obj(miss_ratio):
        lhs = miss_ratio * ref_count
        rhs = hist_misses(miss_ratio, rdist_hist)
        return lhs - rhs

    mr = newton(obj, 0.1);
    return mr