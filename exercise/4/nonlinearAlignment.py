import numpy as np

#a 
def nonlinear_alignment_recursive(test, ref):
    # reached the last point
    if len(test) == 0 or len(ref) == 0:
        return 0
    # only (t-1)/insertion is possible
    elif len(ref) == 1:
        sum = 0
        for elem in range(0, len(test)-1):
            sum += (2 + abs(test[elem] - ref[0]))
        return sum
    # compute minimal costs in all possible directions
    else:
        return abs(test[-1] - ref[-1]) + min(2 + nonlinear_alignment_recursive(test[:-1], ref),       # (t-1)
                                             0 + nonlinear_alignment_recursive(test[:-1], ref[:-1]),  # (t-1)(s-1)
                                             2 + nonlinear_alignment_recursive(test[:-1], ref[:-2]))  # (t-1)(s-2)
# b TODO
def nonlinear_alignment_recursive_with_memoization(test, ref, memo):
    # store current point
    if len(test) == 0 or len(ref) == 0:
        return 0
    elif memo[len(ref)-1][len(test)-1] == -1:
        memo[len(ref)-1][len(test)-1] = 1
        return abs(test[-1] - ref[-1]) + min(2 + nonlinear_alignment_recursive_with_memoization(test[:-1], ref, memo),       # (t-1)
                                             0 + nonlinear_alignment_recursive_with_memoization(test[:-1], ref[:-1], memo),  # (t-1)(s-1)
                                             2 + nonlinear_alignment_recursive_with_memoization(test[:-1], ref[:-2], memo))  # (t-1)(s-2)
    else:
        return 0 

# c TODO
def nonlinear_alignment_iterative(test, ref, cost_matrix):
    s = len(ref)-1
    t = len(test)-1
    #print cost_matrix[s][t]
    for elem_s in range(s, -1, -1):
        for elem_t in range(t, -1, -1):

            #local_costs = 
            print elem_s, elem_t
            print cost_matrix[elem_s][elem_t]
            

test_dat = np.fromfile('test.dat', sep='\n')
ref_dat = np.fromfile('ref.dat', sep='\n')



print nonlinear_alignment_recursive(test_dat, ref_dat)

memo_matrix = np.empty((len(ref_dat), len(test_dat),))
memo_matrix[:] = -1
#print memo_matrix

#print memo_matrix[len(ref_dat)-1][len(test_dat)-1]
#print nonlinear_alignment_recursive_with_memoization(test_dat, ref_dat, memo_matrix)

#print recursive_search(test_dat[:-1], ref_dat[:-1])
#print test_dat[:-1]
search_matrix = 0
costs = [0] 
#print alignment_recursive(costs, test_dat, ref_dat)

cost_matrix = np.empty((len(ref_dat),len(test_dat),))
cost_matrix[:] = np.NAN
#nonlinear_alignment_iterative(test_dat, ref_dat, cost_matrix)
