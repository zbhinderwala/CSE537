#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L
class Golumb_Ruler:
    M = 0  # Marker Order
    L = 0  # Length

    def __init__(self, M, L):
        self.M = M
        self.L = L

class BackTracking:
    n = 0
    d = 0
    c = 0  # number of constraints
    counter = 0
    consistent_dict = dict()

    def __init__(self, ruler):
        self.n = ruler.M
        self.d = ruler.L + 1
        self.domain = [[1 for x in range(self.d)] for x in range(self.n)]
        self.assignment = dict()
        for i in range(self.n):
            self.assignment[i] = None

    def complete(self,assignment):
        b = True
        for i in range(self.n):
            if assignment[i] is None:
                b = False
        return b

    def select_unassigned_variable(self):
        for i in range(self.n):
            if self.assignment[i] is None:
                return i


    def order_domain_values(self,var,asignment):
        available_values = []
        for i in range(len(self.domain[var])):
            if self.domain[var][i] != 0:
                available_values.append(i)
        return available_values

    def consistency(self,var,value,source_assignment):

        # Creating a partial consistency with value
        assignment = {}
        for i in range(len(source_assignment)):
            if i == var:
                assignment[i] = value
            else:
                assignment[i]=source_assignment[i]

        # If this assignment is already part of consistenct_dict return its value
        if tuple(assignment.items()) in self.consistent_dict:
            return self.consistent_dict[tuple(assignment.items())]

        # Checking constraint  1 og i ncreasing order values
        for i in range (1,len(assignment)):
            if assignment[i]== None or assignment[i-1]==None:
                continue
            if assignment[i]<=assignment[i-1]:
                self.consistent_dict[tuple(assignment.items())] = False
                return False

        # Calculate all distance between assignment values
        distance_list=[]
        for i in range(self.n):
            for j in range(self.n-1-i):
                b=assignment[self.n-1-i]
                a=assignment[(self.n-1-i)-(j+1)]

                if b is None or a is None:
                    continue
                distance_list.append(b-a)

        distance_list.sort()
        if len(distance_list) > len(set(distance_list)):
            self.consistent_dict[tuple(assignment.items())]=False
            return False

        if assignment[self.n-1] is not None and assignment[self.n-1]-assignment[0]<self.d-1:
            return False

        self.consistent_dict[tuple(assignment.items())]=True
        return True

    def inference(self, var, value):
        """
        find out the inference for the new assignment
        :param var:
        :param value:
        :returns: a list of (var, value) tuples
        """
        temp = set()
        return temp

    def deepcopy_domain(self, domain, other):
        for i in range(len(other)):
            for j in range(len(other[i])):
                domain[i][j] = other[i][j]


def recursive_BT(assignment,backtrack,count):
    #count = count +1
    #failure = -1,{}
    if backtrack.complete(assignment):
        return assignment,count

    var = backtrack.select_unassigned_variable()
    domain_values = backtrack.order_domain_values(var,assignment)
    for i in domain_values:
        if backtrack.consistency(var,i,assignment):
            assignment[var] = i
            domain = [[1 for x in range(backtrack.d)] for x in range(backtrack.n)]
            backtrack.deepcopy_domain(domain, backtrack.domain)
            count = count + 1
            result,count = recursive_BT(assignment,backtrack,count)
            if result is not False:
                return assignment,count
            assignment[var]=None
            backtrack.deepcopy_domain(backtrack.domain, domain)


    return False,count




#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    count =0
    result = -1,[]
    optimalresult = -1,[]
    while (L >= M):
        print (L)
        ruler=Golumb_Ruler(M,L)
        backtrack=BackTracking(ruler)
        result,count = recursive_BT(backtrack.assignment,backtrack,count)
        if result is not False:
            optimalresult=result
            L=L-1
            continue
        else:
            return optimalresult,count
    return optimalresult,count


#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]


print (BT(34,8))