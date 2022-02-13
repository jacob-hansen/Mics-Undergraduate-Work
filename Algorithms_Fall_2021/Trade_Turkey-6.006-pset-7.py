import math
import sys
sys.setrecursionlimit(10000)

def trade_turkey(prices, k):
    """"
    Dynamic Programming algorithm to solve optimal buy/sell conditions given contraints. The

    Find the optimal way to buy and sell turkeys to maximize
    the total profit.

    Args:
        prices: a list of turkey prices, where prices[i] is the price
        of a turkey on day i.
        k: the maximum number of turkeys you can buy

    Returns:
        a list of up to k non-overlapping trades that gives you the
        max total profit, where each trade is of format (buy_index, sell_index)

    Run-time: O(n^2*k) where k is the maximum turkeys one can buy in one season
    """

    distance = len(prices)
    if distance < 2:
        return []
    maximums = [False]+[(prices[i] > prices[i-1] and prices[i] >= prices[i+1]) for i in range(1, distance-1)]+[(prices[-1] > prices[-2])]
    minimums = [(prices[0] <= prices[1])]+[(prices[i] <= prices[i-1] and prices[i] < prices[i+1]) for i in range(1, distance-1)]+[False]


    index_zip = [i for i in zip(prices, [i for i in range(len(prices))])]
    index_zip.sort(key = lambda x: x[0])
    min_ind = [i[1] for i in index_zip]
    max_ind = min_ind[::-1]
    starts = []
    ends = []
    for i in range(distance):
        if maximums[max_ind[i]]:
            ends.append(max_ind[i])
        if minimums[min_ind[i]]:
            starts.append(min_ind[i])


    cache = {}

    def find_best_k(mins, maxs, k, pos = 0):
        if k == 0:
            return (0, [])
        elif len(maxs)==pos:
            return (0, [])
        elif (k,)+tuple(maxs[pos:]) in cache:
            return cache[(k,)+tuple(maxs[pos:])]
        else:
            best_option = find_best_k(mins, maxs, k, pos+1)
            for i in range(pos, len(maxs)):
                try:
                    if i < len(maxs):
                        next_set = find_best_k(mins, maxs, k-1, i+1)
                        next_option = (next_set[0]+prices[maxs[i]]-prices[mins[pos]], [(mins[pos], maxs[i])]+next_set[1])
                    else:
                        next_option = (prices[maxs[i]]-prices[mins[pos]], [(mins[pos], maxs[i])])
                    if next_option[0] > best_option[0]:
                        best_option = next_option
                except:
                    continue
            cache[(k,)+tuple(maxs[pos:])] = best_option
            return best_option
    starts.sort()
    ends.sort()
    return find_best_k(starts, ends, k)[1]
