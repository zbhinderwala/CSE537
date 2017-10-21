#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

## Defined a class for Golomb_Ruler
class Golomb_Ruler:
    """
    The Golomb ruler consists of M Markers whose total length is L
    """
    M = 0  # Markers
    L = 0  # Length of ruler

    def __init__(self, L, M):
        self.M = M
        self.L = L

## Backtracking class with initialising the ruler ,domain and assignments
class BackTracking:
    n = 0
    d = 0
    consistent_assignments = dict() # Keeping a track of all different assignments encountered

    def __init__(self, ruler):
        self.n = ruler.M
        self.d = ruler.L + 1 # Domain size
        # Domain values take all integers on the number line starting from 0 to L
        self.domain = [x for x in range(self.d)]
        self.assignment = dict() # Assignment dictionary
        # Initially assign all Markers as None and the first one with 0
        for i in range(self.n):
            self.assignment[i] = None
        self.assignment[0]=0

    def complete(self,assignment):
        """
        Check if an assignment is complete and returns true or false
        """
        b = True
        for i in range(self.n):
            if assignment[i] is None:
                b = False
        return b


    def select_unassigned_variable(self):
        """
        # Returns the first unassigned marker variable
        :return: marker
        """
        for i in range(self.n):
            if self.assignment[i] is None:
                return i


    def order_domain_values(self,marker,asignment):
        """
        # Return all the available domain values for a variable
        :param var: Marker for which domain is sought
        :param asignment:
        :return:domain
        """
        return self.domain


    def consistency(self,marker,value,assignment):
        """
        This method performs the folloing consistency checks
        1. X1<X2<X3<...Xn where Xi is the ith Marker value
        2. Distance between every pair of marker is unique
        :param marker:
        :param value:
        :param assignment:
        :return: True if assignment of value to marker is consistent else False
        """
        temp_assignment = {} # Dictionary to hold intermediate assignment
        for i in range(len(assignment)):
            if i == marker:
                temp_assignment[i] = value # Assign marker the value
            else:
                temp_assignment[i]=assignment[i]

        # If this assignment is already part of consistenct assignment return its status
        if tuple(temp_assignment.items()) in self.consistent_assignments:
            return self.consistent_assignments[tuple(temp_assignment.items())]

        # Checking constraint  1 of values in increasing order
        for i in range (1,len(temp_assignment)):
            if temp_assignment[i]== None or temp_assignment[i-1]==None:
                continue
            if temp_assignment[i]<=temp_assignment[i-1]:
                # Previous marker value is greater that current marker assignment then this is an inconsistent assignment return False
                self.consistent_assignments[tuple(temp_assignment.items())] = False
                return False

        # Calculate all distance between assignment values
        distance_list=[]
        for i in range(self.n):
            for j in range(self.n-1-i):
                b=temp_assignment[self.n-1-i]
                a=temp_assignment[(self.n-1-i)-(j+1)]

                if b is None or a is None:
                    continue
                distance_list.append(b-a) # Append all distances of every marker values

        distance_list.sort()
        # If list has duplicate values means that distances are not unique and assignment is inconsistent
        if len(distance_list) > len(set(distance_list)):
            self.consistent_assignments[tuple(temp_assignment.items())]=False
            return False
        # Check if the distance of last marker value and first marker value is less than length of ruler then return False
        if temp_assignment[self.n-1] is not None and temp_assignment[self.n-1]-temp_assignment[0]<self.d-1:
            return False
        # If none of the conistency checks are failed then return True
        self.consistent_assignments[tuple(temp_assignment.items())]=True
        return True

# ForwardChecking class with its domain , variables and assignment
class ForwardChecking:
    n = 0
    d = 0
    consistent_assignments = dict()  # Keeping a track of all different assignments encountered

    def __init__(self, ruler):
        self.n = ruler.M
        self.d = ruler.L + 1
        # For FC we will keep the domain as a dictionary of all values initially set to 0
        self.domain = [[0 for x in range(self.d)] for x in range(self.n)]
        self.assignment = dict()
        # Setting the initial domain list for every variable
        for i in range(self.n):
            if i == 0:
                temp_list = [1 for x in range(self.d)]
                temp_list[0] = 0
                self.domain[i] = temp_list
            elif i == self.n - 1:
                temp_list = [1 for x in range(self.d)]
                temp_list[self.d - 1] = 0
                self.domain[i] = temp_list
            else:
                temp_list = [0 for x in range(self.d)]
                for j in range(i + 1, self.n):
                    temp_list[self.d - self.n + j] = 1
                self.domain[i] = temp_list

        # Initially assign all Markers as None and the first one with 0
        for i in range(self.n):
            self.assignment[i] = None
        self.assignment[0]=0

    def copy_domain(self, domain1, domain2):
        """
        Copy the domain temporarily before modifying it
        :param domain1:
        :param domain2:
        :return:
        """
        for i in range(len(domain2)):
            for j in range(len(domain2[i])):
                domain1[i][j] = domain2[i][j]

    def complete(self, assignment):
        """
        Check if an assignment is complete and returns true or false
        """
        b = True
        for i in range(self.n):
            if assignment[i] is None:
                b = False
        return b

    def select_unassigned_variable(self):
        """
        Returns the first unassigned marker variable
        :return: marker
        """
        for i in range(self.n):
            if self.assignment[i] is None:
                return i


    def order_domain_values(self, var, assignment):
        """
        Return domain values for a variable
        :param var:
        :param assignment:
        :return:domain
        """
        # We first Forward check and disable the domain variables that has already been assigned
        for i in range(self.n):
            if self.assignment[i] is None:
                continue
            value = assignment[i]
            for j in range (self.n):
                if j != i and self.domain[j][value]!=1:
                    self.domain[j][value]=1

        domain_values = []
        for i in range(len(self.domain[var])):
            if self.domain[var][i] != 1:
                domain_values.append(i)
        return domain_values


    def consistency(self, marker, value, assignment):
        """
        This method performs the folloing consistency checks
        1. X1<X2<X3<...Xn where Xi is the ith Marker value
        2. Distance between every pair of marker is unique
        :param marker:
        :param value:
        :param assignment:
        :return: True if assignment of value to marker is consistent else False
        """
        temp_assignment = {}  # Dictionary to hold intermediate assignment
        for i in range(len(assignment)):
            if i == marker:
                temp_assignment[i] = value  # Assign marker the value
            else:
                temp_assignment[i] = assignment[i]

        # If this assignment is already part of consistenct assignment return its status
        if tuple(temp_assignment.items()) in self.consistent_assignments:
            return self.consistent_assignments[tuple(temp_assignment.items())]

        # Checking constraint  1 of values in increasing order
        for i in range(1, len(temp_assignment)):
            if temp_assignment[i] == None or temp_assignment[i - 1] == None:
                continue
            if temp_assignment[i] <= temp_assignment[i - 1]:
                # Previous marker value is greater that current marker assignment then this is an inconsistent assignment return False
                self.consistent_assignments[tuple(temp_assignment.items())] = False
                return False

        # Calculate all distance between assignment values
        distance_list = []
        for i in range(self.n):
            for j in range(self.n - 1 - i):
                b = temp_assignment[self.n - 1 - i]
                a = temp_assignment[(self.n - 1 - i) - (j + 1)]

                if b is None or a is None:
                    continue
                distance_list.append(b - a)  # Append all distances of every marker values

        distance_list.sort()
        # If list has duplicate values means that distances are not unique and assignment is inconsistent
        if len(distance_list) > len(set(distance_list)):
            self.consistent_assignments[tuple(temp_assignment.items())] = False
            return False
        # Check if the distance of last marker value and first marker value is less than length of ruler then return False
        if temp_assignment[self.n - 1] is not None and temp_assignment[self.n - 1] - temp_assignment[0] < self.d - 1:
            return False
        # If none of the conistency checks are failed then return True
        self.consistent_assignments[tuple(temp_assignment.items())] = True
        return True


def recursive_BT(assignment,backtrack):
    """
    Recursive Backtrack function which picks up an unassigned variable and for every domain value checks the consistency and assigns it
    and then does a recursive call to itself for the next variable assignment
    :param assignment:
    :param backtrack:
    :return: optimal result
    """
    # If assignment is complete return it
    if backtrack.complete(assignment):
        return assignment
    # Get the next unassigned variable
    var = backtrack.select_unassigned_variable()
    # Get all its possible domain values
    domain_values = backtrack.order_domain_values(var,assignment)
    for i in domain_values: # Loop through the domain values
        if backtrack.consistency(var,i,assignment):
            assignment[var] = i
            # Call the function again to backtrack again for current assignment
            result= recursive_BT(assignment,backtrack)
            if result is not False:
                return assignment
            assignment[var]=None

    return False


def recursive_FC(assignment,fc):
    """
    Recursive Forward Check function which picks up an unassigned variable and for every domain value checks the consistency and assigns it
    and then does a recursive call to itself for the next variable assignment
    :param assignment:
    :param backtrack:
    :return:optimal result
    """
    # If assignment is complete return it
    if fc.complete(assignment):
        return assignment
    # Get the next unassigned variable
    var = fc.select_unassigned_variable()
    # Get all its possible domain values
    domain_values = fc.order_domain_values(var,assignment)
    for i in domain_values:# Loop through the domain values
        if fc.consistency(var,i,assignment):
            assignment[var] = i
            # Maintain a copy of the domain before calling the function again to backtrack again for current assignment
            domain = [[1 for x in range(fc.d)] for x in range(fc.n)]
            fc.copy_domain(domain, fc.domain)
            result = recursive_FC(assignment,fc)
            if result is not False:
                return assignment
            assignment[var]=None
            fc.copy_domain(fc.domain, domain) # Reassign domain back in case of False

    return False

#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    """
    Backtrack function finds the optimal length ruler for a given L and M
    """
    optimal_length = -1
    optimalresult = []
    # Loop till L is greater or equal to M
    while (L >= M):
        ruler=Golomb_Ruler(L,M)
        backtrack=BackTracking(ruler)
        result = recursive_BT(backtrack.assignment,backtrack)
        if result is not False: # If optimal result found store it and check for L =L-1
            optimalresult=result
            L=L-1
            continue
        else: # if result is False return the previous optimal result
            if optimalresult:
                optimal_length = optimalresult[M - 1] - optimalresult[0]
                optimalresult = optimalresult.values()
                return optimal_length, optimalresult
            else:
                return optimal_length,optimalresult
    return optimal_length,optimalresult


#Your backtracking+Forward checking function implementation
#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    """
    Forward Checking with Backtrack finds an optimal length ruler for given L and M
    """
    optimal_length=-1
    optimalresult = []
    # Loop till L is greater or equal to M
    while (L >= M):
        ruler = Golomb_Ruler(L, M)
        fc = ForwardChecking(ruler)
        result = recursive_FC(fc.assignment,fc)
        if result is not False:# If optimal result found store it and check for L =L-1
            optimalresult = result
            L = L - 1
            continue
        else: # if result is False return the previous optimal result
            if optimalresult:
                optimal_length = optimalresult[M - 1] - optimalresult[0]
                optimalresult = optimalresult.values()
                return optimal_length, optimalresult
            else:
                return optimal_length,optimalresult
    return optimal_length, optimalresult


#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

print BT(6,4)
print FC(6,4)