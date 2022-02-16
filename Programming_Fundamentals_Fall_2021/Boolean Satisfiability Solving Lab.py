#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    False
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    False
    >>> satisfying_assignment([[('e', False), ('b', False)], [('f', False)], [('a', False), ('e', True)], [('i', True)], [('a', True), ('h', False)], [('c', False)], [('a', True), ('h', False)], [('a', True)], [('g', True), ('h', True)], [('c', True), ('e', False)], [('e', False)], [('j', False)], [('j', True)], [('b', False), ('a', True)], [('i', False), ('b', False)], [('h', True)], [('c', True), ('c', False)], [('b', True), ('h', True)], [('d', False), ('g', True)], [('d', True)], [('f', False)], [('e', True), ('d', True)], [('d', True)], [('h', True)], [('f', False)], [('i', True)], [('f', False), ('d', False)], [('c', True), ('g', False)], [('g', False)], [('j', False), ('g', True)], [('j', False), ('j', True)], [('j', False), ('i', False)], [('c', True), ('i', False)], [('h', False), ('e', False)], [('a', True), ('j', True)], [('h', False)], [('e', False)], [('d', True), ('d', False)], [('h', True)], [('j', False), ('e', False)], [('b', False)], [('j', True)], [('i', True)], [('d', False), ('e', False)], [('f', False), ('j', False)], [('h', True)], [('b', True)], [('d', True), ('e', True)], [('j', False)], [('e', True), ('b', False)], [('d', True)], [('j', False)], [('a', True), ('e', True)], [('a', False)], [('d', False), ('i', False)], [('c', False)], [('a', True)], [('d', False), ('d', True)], [('h', True)], [('c', False)], [('f', False)], [('f', False), ('j', True)], [('a', False)], [('g', True), ('g', False)], [('d', True), ('i', False)], [('d', True), ('f', True)], [('i', False)], [('f', False), ('c', False)], [('h', True)], [('h', True)], [('h', False), ('i', True)], [('c', False), ('d', False)], [('a', True), ('d', True)], [('e', False), ('a', True)], [('c', False)], [('j', False)], [('e', True), ('e', True)], [('g', True), ('c', True)], [('g', True)], [('h', True)], [('h', False)], [('g', True)], [('d', True)], [('e', True)], [('e', True)], [('c', False)], [('f', False)], [('a', True)], [('j', True)], [('j', False)], [('c', True)], [('e', False)], [('j', True), ('f', False)], [('e', True)], [('c', True), ('f', True)], [('f', False)], [('f', True)], [('f', True), ('f', True)], [('a', True)], [('i', False)]])
    False
    >>> satisfying_assignment([[('b', True), ('a', True)], [('b', True)], [('b', False), ('a', False)], [('c', True), ('d', True)]])
    False
    """
    if len(formula) == 0:
        return {}
    newFormula = [set(i) for i in formula] # creating sets to iterate over faster
    newFormula = sorted(newFormula, key = lambda clause: len(clause))

    newFormula, knowns = simplify(newFormula)
    if newFormula == False:
        return None

    def tryFind(simpleForm, attempt = {}):
        if len(simpleForm) == 0:
            test, furtherConstraints = isSatisfyable(formula, attempt)
            returnList = attempt.copy()
            returnList.update(furtherConstraints)
            test, furtherConstraints = isSatisfyable(formula, returnList) # checks if the proposed solution
            if test != False and test != None:
                return returnList
            return False

        newSimpleForm, newConstraints = simplify(simpleForm, (next(iter(simpleForm[0])))) # propagates the solution and removes all uniclauses and returns new variables as newConstraints
        if newSimpleForm == False:
            return False
        nextAttempt = attempt.copy() # make a copy to avoid aliasing
        nextAttempt.update(newConstraints)
        testNext = tryFind(newSimpleForm, nextAttempt)

        if testNext == False and len(simpleForm) != 0: # test assigning the variable to the opposite assignment
            value = next(iter(simpleForm[0]))
            newSimpleForm, newConstraints = simplify(newSimpleForm, (value[0], not value[1]))
            if newSimpleForm == False:
                return False
            nextAttempt = attempt.copy()
            nextAttempt.update(newConstraints)
            testNext = tryFind(newSimpleForm, nextAttempt)
        return testNext


    returnValue = tryFind(newFormula, knowns) # call tryFind function which does the bulk of the work.
    if returnValue == False:
        return None
    return returnValue



def simplify(formula, var = False):
    """
    formula is a CNF list, var is a tuple (name, bool) to be removed.
    If there is a contridiction, this returns False, {False, False}
    Otherwise, it returns the newFormula, newConstraints
    """

    newConstraints = set() # a set of tuples with new assignments (as in the input tuple)
    if var != False:
        newConstraints.add(var)

    def takeOutOnes(aFormula):
        """
        function takes out all uniclauses and adds them to newConstraints, returns nothing
        """
        length = len(aFormula)
        for i in reversed(range(length)):
            if (len(aFormula[i]) == 1):
                value = list(aFormula[i])[0]
                if ((value[0], not value[1]) in newConstraints):
                    return False, {(False, False)}
                newConstraints.add(value)
                aFormula[i] = aFormula[-1]
                aFormula.pop(-1)
    takeOutOnes(formula)
    check = newConstraints

    while len(check) > 0:
        newCheck = set()
        length = len(formula)
        for i in reversed(range(length)): # removes items in check from the formula clauses
            next = False
            for item in check:
                if item in formula[i]: # when it is removing them, it swaps the item with the last item and then removes it in O(1) time
                    if i == length-1:
                        formula.pop()
                    else:
                        formula[i] = formula.pop()
                    length -= 1
                    next = True
                    break
                else:
                    formula[i].discard((item[0], not item[1]))
            if next: # this is to continue the iteration in case the clause was removed
                continue
            if len(formula[i]) == 0:
                if i == length-1:
                    formula.pop(-1)
                else:
                    formula[i] = formula.pop()
                length -= 1
            elif len(formula[i]) == 1:
                for y in formula[i]:
                    pass
                if (y[0], not y[1]) in newConstraints or (y[0], not y[1]) in newCheck:
                    return False, {(False, False)}
                if i == length-1:
                    formula.pop()
                    newCheck.add(y)
                else:
                    newCheck.add(y)
                    formula[i] = formula.pop()
                length -= 1
        newConstraints = newConstraints | newCheck
        check = newCheck
    returnConstraints = {i[0]: i[1] for i in newConstraints}
    return formula, returnConstraints # returnConstraints includes the original contraint imposed on the formula and any uniclauses removed.



def isSatisfyable(formula, constraints):
    """
    Returns True or None depending if the expression is still satisfyable
    returns a dictionary of items mapped to an assignment for the assignments that don't matter and
    are note included in the contraints.
    """
    constraints = constraints.copy() # to avoid aliasing because we mutate the contraints
    repeat = False
    testList = []
    anyValue = {}
    for andSt in formula: # check every and statement to be true
        appendSet = []
        for i in andSt:
            if(i[0] not in constraints):
                constraints[i[0]] = False
                anyValue[i[0]] = False
                repeat = True
            appendSet.append(constraints[i[0]] == i[1])
        testList.append(not any(appendSet))
    if repeat == True:
        return isSatisfyable(formula, constraints)
    if (any(testList) == True):
        return None, anyValue
    return True, anyValue



def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.

    >>> boolify_scheduling_problem({'student0': {'session6', 'session8', 'session3', 'session4', 'session0', 'session2'}, 'student1': {'session3', 'session1', 'session6', 'session7'}, 'student7': {'session3', 'session5', 'session4', 'session9', 'session2', 'session1'}, 'student4': {'session6', 'session5', 'session9', 'session7', 'session2', 'session1'}, 'student3': {'session5'}, 'student2': {'session3', 'session5', 'session4', 'session7', 'session2'}, 'student9': {'session6', 'session5', 'session9', 'session0', 'session1'}, 'student6': {'session6', 'session8', 'session5', 'session2', 'session1'}, 'student8': {'session8', 'session3', 'session9', 'session7', 'session0', 'session2'}, 'student5': {'session0', 'session7', 'session8'}}, {'session6': 1, 'session8': 4, 'session1': 3, 'session2': 0, 'session9': 3, 'session7': 6, 'session0': 3, 'session5': 0, 'session3': 7, 'session4': 2})
    False
    >>> boolify_scheduling_problem({'Alice': {'basement', 'penthouse'},'Bob': {'kitchen'},'Charles': {'basement', 'kitchen'},'Dana': {'kitchen', 'penthouse', 'basement'}}, {'basement': 1, 'kitchen': 2, 'penthouse': 4})
    False
    >>> boolify_scheduling_problem({'student13': {'session3', 'session2'}, 'student14': {'session3', 'session0', 'session4'}, 'student4': {'session3', 'session0', 'session1'}, 'student11': {'session4'}, 'student16': {'session3', 'session4', 'session0', 'session2', 'session1'}, 'student8': {'session3', 'session0', 'session2', 'session1'}, 'student0': {'session3', 'session4'}, 'student12': {'session0', 'session2'}, 'student10': {'session2'}, 'student7': {'session2'}, 'student6': {'session3', 'session0', 'session1'}, 'student1': {'session3', 'session0', 'session2', 'session1'}, 'student15': {'session3', 'session0'}, 'student2': {'session4'}, 'student5': {'session3', 'session4', 'session2', 'session1'}, 'student3': {'session3', 'session2', 'session1'}, 'student9': {'session4', 'session2'}}, {'session0': 15, 'session1': 2, 'session4': 6, 'session3': 0, 'session2': 1})
    False
    """
    roomFillings = {}
    studentReq = []
    for room in room_capacities:
        roomFillings[room] = set()
    for i in student_preferences: # makes contraints for stuedents being in their preffered rooms.
        studentReq.append([(i+'_'+j, True) for j in student_preferences[i]])
        for j in student_preferences[i]:
            roomFillings[j].add(i)

    def comboSet(listOfNums, n):
        """
        mutates a storage set to add all the possible combinations of a list
        if storage is left as default, no set will be mutated and a list of possiblities with duplicates will be returned
        """
        if n == 0:
            return [[]]
        returnList = []
        for i in range(len(listOfNums)):
            thisValue = listOfNums[i]
            remList = listOfNums[i+1:]
            for j in comboSet(remList, n-1):
                returnList.append([thisValue]+j)
        return returnList

    notTwice = []
    for student in student_preferences: # makes contraints so that a student is only assigned to one room
        rooms = list(student_preferences[student])
        roomNumCombos = comboSet(rooms, 2)
        for i in roomNumCombos:
            notTwice.append([(student+'_'+i[0], False), (student+'_'+i[1], False)])
    allRooms = []
    for room in roomFillings: # makes contraints to avoid over capacity
        students = list(roomFillings[room])
        if (room_capacities[room] < len(students)):
            studentCombos = comboSet(students, room_capacities[room]+1)
            for i in studentCombos:
                appendList = []
                for student in i:
                    appendList.append((student+'_'+room, False))
                allRooms.append(appendList)

    return studentReq+notTwice+allRooms




if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #doctest.testmod(optionflags=_doctest_flags)

    x = boolify_scheduling_problem({'student0': {'session8', 'session6', 'session4', 'session0', 'session3', 'session2'}, 'student1': {'session3', 'session6', 'session7', 'session1'}, 'student7': {'session4', 'session9', 'session3', 'session1', 'session2', 'session5'}, 'student4': {'session6', 'session7', 'session9', 'session1', 'session2', 'session5'}, 'student3': {'session5'}, 'student2': {'session7', 'session4', 'session3', 'session2', 'session5'}, 'student9': {'session6', 'session1', 'session0', 'session9', 'session5'}, 'student6': {'session8', 'session6', 'session1', 'session2', 'session5'}, 'student8': {'session8', 'session7', 'session9', 'session3', 'session0', 'session2'}, 'student5': {'session0', 'session7', 'session8'}}, {'session6': 1, 'session8': 4, 'session1': 3, 'session2': 0, 'session9': 3, 'session7': 6, 'session0': 3, 'session5': 0, 'session3': 7, 'session4': 2})
    print(satisfying_assignment(x))
