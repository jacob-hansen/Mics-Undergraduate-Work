class BackFront():
    """
    List class that allows:
    O(1) init empty
    O(1) set/get at index
    O(1) amortized prepend/delete front
    O(1) amortized append/delete back
    O(n) return as list
    """
    def __init__(self):
        self.L = []
        self.S = 0
        self.E = 0
    def __setitem__(self, key, value):
        self.L[self.S+key] = value

    def __getitem__(self, key):
        return self.L[self.S+key]

    def prepend(self, value):
        if(len(self.L) == 0):
            self.L.append(value)
        else:
            if(self.S == 0):
                self.S = len(self.L)
                self.E += len(self.L)
                self.L = [False] * len(self.L) + self.L
            self.L[self.S-1] = value
            self.S -= 1

    def append(self, value):
        if(len(self.L) == 0):
            self.L.append(value)
        else:
            if(self.E+1 < len(self.L)):
                self.L[self.E+1] = value
            else:
                self.L.append(value)
            self.E += 1

    def as_list(self):
        return [self.L[i] for i in range(self.S, self.E+1)]

    def delete_last(self):
        self.L[self.E] = False
        self.E -= 1

    def delete_first(self):
        self.L[self.S] = False
        self.S += 1
