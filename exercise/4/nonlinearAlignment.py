import numpy as np


# a
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
    # reached last point
    if len(test) == 0 or len(ref) == 0:
        return 0
    # only (t-1)/insertion is possible
    if len(ref) == 1:
        sum = 0
        for elem in range(0, len(test)-1):
            sum += (2 + abs(test[elem] - ref[0]))
        return sum
    elif memo[len(ref)-1][len(test)-1] == -1:
        local_costs = abs(test[-1] - ref[-1])
        memo[len(ref)-1][len(test)-1] = local_costs
        if len(test) <= 2:
            print 'asdf'
            return 0
        else:
            print test

            return local_costs + min(2 + nonlinear_alignment_recursive_with_memoization(test[:-1], ref, memo)) # (t-1)

    elif memo[len(ref)-2][len(test)-1] == -1:
        local_costs = abs(test[-1] - ref[-2])
        memo[len(ref)-1][len(test)-1] = local_costs
        return local_costs + min(nonlinear_alignment_recursive_with_memoization(test[:-1], ref[:-1], memo))  # (t-1)(s-1)

    elif memo[len(ref)-3][len(test)-1] == -1:
        local_costs = abs(test[-1] - ref[-3])
        memo[len(ref)-1][len(test)-1] = local_costs
        return local_costs + min(2 + nonlinear_alignment_recursive_with_memoization(test[:-1], ref[:-2], memo)) # (t-1)(s-2)


# c
def nonlinear_alignment_iterative(test, ref, cost_matrix, backpointer_matrix, dist_calculations):

    start_range = 0
    for t in range(0, len(test)):
        # limit search space by setting the range of S
        if start_range < len(ref)-1:
            if start_range % 2 == 1:
                start_range += 1
        if start_range < len(ref):
            start_range += 1

        s = 0
        for i in range(0, start_range):
            # set all possible costs to infinity
            ins_costs = float("inf")
            sub_costs = float("inf")
            skp_costs = float("inf")

            if t == 0:
                dist_calculations += 1
                cost_matrix[0][0] = abs(test[0] - ref[0])
            else:
                # compute local costs
                local_costs = abs(test[t] - ref[s])

                dist_calculations +=1
                # compute all possible previous costs
                # (t-1)
                if t-1 != -1:
                    ins_costs = 2 + cost_matrix[s][t-1]
                    dist_calculations +=1

                    # (t-1)(s-1)
                    if s-1 != -1:
                        #sub_costs = abs(test[t-1] - ref[s-1])
                        sub_costs = cost_matrix[s-1][t-1]
                        dist_calculations +=1
                        # (t-1)(s-2)
                        if s-2 != -1:
                            #skp_costs = 2 + abs(test[t-1] - ref[s-2])
                            skp_costs = 2 + cost_matrix[s-2][t-1]
                            dist_calculations +=1
                costs = local_costs + int(min(ins_costs, sub_costs, skp_costs))

                cost_matrix[s][t] = costs
            s += 1

    return cost_matrix, dist_calculations

            

test_dat = np.fromfile('test.dat', sep='\n')
ref_dat = np.fromfile('ref.dat', sep='\n')

# --------------------- recursive alignment -------------------------------------
print '--------------------- recursive alignment ------------------------------------\n' \
      'function call is uncommented because it does not terminate with the given data'
#dist_calculations = []
#result_a = nonlinear_alignment_recursive(test_dat, ref_dat)
#print result_a


# --------------------- recursive alignment  with memo --------------------------
#print '--------------------- recursive alignment with memo---------------------------\n'
memo_matrix = np.empty((len(ref_dat), len(test_dat),))
memo_matrix[:] = -1

#print memo_matrix[len(ref_dat)-1][len(test_dat)-1]
#print nonlinear_alignment_recursive_with_memoization(test_dat, ref_dat, memo_matrix)


# --------------------- dynamic search ------------------------------------------

print '--------------------- dynamic alignment ---------------------------------------\n'
cost_matrix = np.empty((len(ref_dat),len(test_dat),))
cost_matrix[:] = float("inf")
result_c = nonlinear_alignment_iterative(test_dat, ref_dat, cost_matrix, 0, 0)
print 'Took ' + str(result_c[1]) + ' distance calculations and the minimum distance is: ' + str(result_c[0][len(ref_dat)-1][len(test_dat)-1])
# uncomment to print cost matrix

print 'Cost matrix:'
for row in range(0, len(result_c[0])):
    full_row = ''
    for column in  range(0, len(result_c[0][row])):
        full_row += str(result_c[0][row][column]) +' '
    print full_row