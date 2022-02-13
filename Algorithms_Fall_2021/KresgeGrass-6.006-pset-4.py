class KresgeGrass(object):
    '''
    Represents an array data structure which allows incrementing over
    athetheRange of indices. For example, if we started with an array:

    A = [5, 1, 7, 2, 11]

    Here are some example queries:
        get(0) --> 5
        get(1) --> 1
        get(2) --> 7
        get(3) --> 2
        get(4) --> 11

    However, if we then called:
        increment(2, 4, 6) --> A = [5, 1, 13, 8, 17]
        increment(0, 3, 2) --> A = [7, 3, 15, 10, 17]

    So the previous queries would now yield:
        get(0) --> 7
        get(1) --> 3
        get(2) --> 15
        get(3) --> 10
        get(4) --> 17

    Runtime:
        init(H) in O(n) for n grass heights
        get(i) returns the height i'th grass spot in O(logn)
        increment(a, b, h): increases height of every spot between a and b in O(logn)
    '''
    def __init__(self, A, myParent = False, theRange = False):
        '''Initializing the Data Structure from array/list A'''
        if theRange == False:
            theRange = (0, len(A))
        self.parent = myParent
        self.index =theRange[0]+(theRange[1]-theRange[0])//2
        self.height = A[self.index]
        self.inc = 0
        self.lMax = A[theRange[0]]
        self.rMax = A[theRange[1]-1]

        if self.parent != False:
            if self.index > self.parent.index:
                self.flow = 1 # it is a right child
            else:
                self.flow = 0 # ie it is a left child
        else: self.flow = -1 # ie it is the root


        if (self.index > theRange[0]):
            self.left = KresgeGrass(A, self, (theRange[0], self.index))
        else:
            self.left = False
        if (self.index < theRange[1]-1):
            self.right = KresgeGrass(A, self, (self.index+1,theRange[1]))
        else:
            self.right = False



    def get(self, i):
        '''Return the i-th element in your data structure'''
        if self.index == i:
            return self.height+self.inc
        elif self.index < i:
            return self.right.get(i)+self.inc
        return self.left.get(i)+self.inc

    def change(self, i, k):
        '''Increases i-th element in your data structure by k'''
        if self.index == i:
            self.height += k
            return None
        elif self.index < i:
            self.right.change(i, k)
            return None
        self.left.change(i, k)
        return None

    def travelLeft(self, a, k):
        if self.index == a:
            if self.left != False:
                self.left.inc -= k
            return None
        if self.index < a:
            self.inc -= k
            self.right.inc += k
            self.right.travelLeft(a, k)
            return None
        if self.left != False:
            self.left.travelLeft(a, k)
        return None

    def travelRight(self, b, k):
        if self.index == b:
            if self.right != False:
                self.right.inc -= k
            return None
        if self.index > b:
            self.inc -=k
            self.left.inc += k
            self.left.travelRight(b, k)
            return None
        if self.right != False:
            self.right.travelRight(b, k)
        return None

    def increment(self, a, b, k) -> None:
        '''Increment elements from indices a to b by k'''
        if (a <= self.index and b >= self.index):
            self.inc += k
            self.travelRight(b, k)
            self.travelLeft(a, k)
            return None

        elif(self.index > b):
            self.left.increment(a, b, k)
            return None
        else:
            self.right.increment(a, b, k)
            return None

# A = [i + 2 for i in range(26)]
# test = KresgeGrass(A)
# for j in range(13):
#     test.increment(j, 25 - j, 1)
#     print([test.get(i) for i in range(len(A))])
