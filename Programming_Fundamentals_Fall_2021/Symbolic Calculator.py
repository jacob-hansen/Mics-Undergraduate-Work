import doctest


def test_num(other):
    """
    Assignments for unclassified numbers and variables
    """
    if(isinstance(other, (int, float, complex)) and not isinstance(other, bool)):
        other = Num(other)
    if isinstance(other, str):
        other = Var(other)
    return other

class Symbol:
    def __add__(self, other):
        """
        returns a BinOp of the addition
        >>> Var('x') + 2
        Add(Var('x'), Num(2))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Add(self, other)
    def __radd__(self, other):
        """
        returns a BinOp of the reverse addition
        >>> 2 + Var('x')
        Add(Num(2), Var('x'))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Add(other, self)
    def __mul__(self, other):
        """
        returns a BinOp of the mulplication
        >>> Var('a') * Var('b')
        Mul(Var('a'), Var('b'))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Mul(self, other)
    def __rmul__(self, other):
        """
        returns a BinOp of the reverse multiplication
        >>> Var('a') * 2
        Mul(Var('a'), Num(2))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Mul(other, self)
    def __sub__(self, other):
        """
        returns a BinOp of the reverse subtraction
        >>> Num(4) - 3
        Sub(Num(4), Num(3))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Sub(self, other)
    def __rsub__(self, other):
        """
        returns a BinOp of the reverse subtraction
        >>> 2 - Num(4)
        Sub(Num(2), Num(4))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Sub(other, self)
    def __truediv__(self, other):
        """
        returns a BinOp of the division
        >>> Num(3) / 2
        Div(Num(3), Num(2))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Div(self, other)
    def __rtruediv__(self, other):
        """
        returns a BinOp of the reverse division
        >>> 2 / Num(4)
        Div(Num(2), Num(4))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Div(other, self)
    def __pow__(self, other):
        """
        returns a BinOp of the power
        >>> Num(3) ** 2
        Pow(Num(3), Num(2))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Pow(self, other)
    def __rpow__(self, other):
        """
        returns a BinOp of the reverse power
        >>> 3 ** Var('x')
        Pow(Num(3), Var('x'))
        """
        other = test_num(other) # assignments for unclassified numbers and variables
        return Pow(other, self)






class BinOp(Symbol):
    def __init__(self, *elements):
        """
        Inializer.
        >>> z = Add(Var('x'), Sub(Var('y'), Num(2)))
        >>> repr(z)  # notice that this result, if fed back into Python, produces an equivalent object.
        "Add(Var('x'), Sub(Var('y'), Num(2)))"
        >>> str(z)  # this result cannot necessarily be fed back into Python, but it looks nicer.
        'x + y - 2'
        """
        self.left = elements[0]
        self.right = elements[1]

    def __str__(self):
        """
        prints out a string representation of the equation like how you would write it
        """
        print_out = [str(self.left), str(self.right)]
        if hasattr(self.right, 'level') and self.right.level[0] < self.level[0]: # right side for when operations need parenthesis, such as x + 2 * y != ( x + 2 ) * y
                print_out[1] = '('+print_out[1]+')'
        elif hasattr(self.right, 'level') and not self.level[1] and self.right.level[0] <= self.level[0] and not isinstance(self.right, Pow):
                print_out[1] = '('+print_out[1]+')'

        elif hasattr(self.left, 'level') and self.name=='Pow': # special case for power function, it's unique
                 print_out[0] = '('+print_out[0]+')'

        if hasattr(self.left, 'level') and self.left.level[0] < self.level[0]: # left side for when operations need parenthesis
                print_out[0] = '('+print_out[0]+')'
        print_out = self.oper.join(print_out)
        return print_out

    def __repr__(self):
        """
        Prints out the encoded class representation of the formula
        """
        print_out = [repr(self.left), repr(self.right)]
        print_out = self.name+'('+', '.join(print_out)+')'
        return print_out






class Add(BinOp):
    oper = ' + '
    name = 'Add'
    level = (1, True) # False is for if elements can be switched around without changing signs
    def deriv(self, variable):
        """
        Derivative of Addition
        x = sym('(x ** 2)')
        >>> x = Pow(Var('x'), Num(2))
        >>> x.deriv('x')
        Mul(Mul(Num(2), Pow(Var('x'), Sub(Num(2), Num(1)))), Num(1))
        """
        return Add(self.left.deriv(variable), self.right.deriv(variable))

    def simplify(self):
        """
        Simplifies expressions by the following rules:
        -Any binary operation on two numbers should simplify to a single number containing the result.
        -Adding 0 to (or subtracting 0 from) any expression EE should simplify to EE.
        -A single number or variable always simplifies to itself.

        >>> z = 2*x - x*y + 3*y
        >>> print(sym((2 * x - x * y + 3 * y)).simplify())
        2 * x - x * y + 3 * y
        >>> print(sym((2 * x - x * y + 3 * y)).deriv('x').simplify())
        2 - y
        >>> Add(Add(Num(2), Num(-2)), Add(Var('x'), Num(0))).simplify()
        Var('x')
        """
        right_sim = self.right.simplify() # the right subgroup simplified
        left_sim = self.left.simplify() # the left subgroup simplified
        if hasattr(right_sim, 'n') and right_sim.n == 0: # don't need to add 0
            return left_sim
        elif hasattr(left_sim, 'n') and left_sim.n == 0: # don't need to add 0
            return right_sim
        elif hasattr(left_sim, 'n') and hasattr(right_sim, 'n'): # return a single number
            return Num(left_sim.n+right_sim.n)
        return Add(left_sim, right_sim) # otherwise it is already simplified

    def eval(self, variables):
        """
        Plugs in values for the variables and evaluates the expression.
        """
        return self.left.eval(variables)+self.right.eval(variables)

class Mul(BinOp):
    oper = ' * '
    name = 'Mul'
    level = (2, True) # False is for if elements can be switched around without changing signs
    def deriv(self, variable):
        """
        Derivative of Multiplication
        """
        return Add(Mul(self.left, self.right.deriv(variable)), Mul(self.right, self.left.deriv(variable)))
    def simplify(self):
        """
        Simplifies expressions by the following rules:
        -Any binary operation on two numbers should simplify to a single number containing the result.
        -Multiplying or dividing any expression EE by 11 should simplify to EE.
        -Multiplying any expression EE by 00 should simplify to 00.
        -A single number or variable always simplifies to itself.
        """
        right_sim = self.right.simplify()
        left_sim = self.left.simplify()
        if (hasattr(right_sim, 'n') and right_sim.n == 0) or (hasattr(left_sim, 'n') and left_sim.n == 0): # multiply by 0
            return Num(0)
        elif (hasattr(left_sim, 'n') and left_sim.n == 1): # multiply by 1
            return right_sim
        elif (hasattr(right_sim, 'n') and right_sim.n == 1): # multiply by 1
            return left_sim
        elif hasattr(left_sim, 'n') and hasattr(right_sim, 'n'): # multiply two numbers
            return Num(left_sim.n*right_sim.n)
        return Mul(left_sim, right_sim) # otherwise already simple
    def eval(self, variables):
        """
        Plugs in values for the variables and evaluates the expression.
        """
        return self.left.eval(variables)*self.right.eval(variables)

class Sub(BinOp):
    oper = ' - '
    name = 'Sub'
    level = (1, False) # False is for if elements can be switched around without changing signs
    def deriv(self, variable):
        """
        Derivative of Subtraction
        """
        return Sub(self.left.deriv(variable), self.right.deriv(variable))
    def simplify(self):
        """
        Simplifies expressions by the following rules:
        -Any binary operation on two numbers should simplify to a single number containing the result.
        -Adding 0 to (or subtracting 0 from) any expression EE should simplify to EE.
        -A single number or variable always simplifies to itself.
        """
        right_sim = self.right.simplify()
        left_sim = self.left.simplify()
        if (hasattr(right_sim, 'n') and right_sim.n == 0): # subtracting 0
            return left_sim
        elif hasattr(left_sim, 'n') and hasattr(right_sim, 'n'): # combining two numbers
            return Num(left_sim.n-right_sim.n)
        return Sub(left_sim, right_sim) # otherwise already simple

    def eval(self, variables):
        """
        Plugs in values for the variables and evaluates the expression.
        """
        return self.left.eval(variables)-self.right.eval(variables)

class Div(BinOp):
    oper = ' / '
    name = 'Div'
    level = (2, False)  # False is for if elements can be switched around without changing signs
    def deriv(self, variable):
        """
        Derivative of Division
        -Any binary operation on two numbers should simplify to a single number containing the result.
        -Dividing 00 by any expression EE should simplify to 00.
        -A single number or variable always simplifies to itself.
        """
        return Div(Sub(Mul(self.right, self.left.deriv(variable)), Mul(self.left, self.right.deriv(variable))), Mul(self.right, self.right))
    def simplify(self):
        right_sim = self.right.simplify()
        left_sim = self.left.simplify()
        if (hasattr(left_sim, 'n') and left_sim.n == 0): # 0/something = 0
            return Num(0)
        elif (hasattr(right_sim, 'n') and right_sim.n == 1): # divide by 1 is the same
            return left_sim
        elif hasattr(left_sim, 'n') and hasattr(right_sim, 'n'): # divide two numbers
            return Num(left_sim.n/right_sim.n)
        return Div(left_sim, right_sim) # otherwise it is already simple
    def eval(self, variables):
        """
        Plugs in values for the variables and evaluates the expression.
        """
        return self.left.eval(variables)/self.right.eval(variables)

class Pow(BinOp):
    oper = ' ** '
    name = 'Pow'
    level = (3, True)  # False is for if elements can be switched around without changing signs
    def deriv(self, variable):
        """
        Derivative of a Power Function
        print(Pow(Add(Var('x'), Var('y')), Num(1)).simplify())
        x + y

        >>> 2 ** Var('x')
        Pow(Num(2), Var('x'))
        """
        if (isinstance(self.right, Var)):
            raise TypeError
        return Mul(Mul(self.right, Pow(self.left, self.right-Num(1))), self.left.deriv(variable))

    def simplify(self):
        right_sim = self.right.simplify()
        left_sim = self.left.simplify()
        if (hasattr(right_sim, 'n') and right_sim.n == 0):
            return Num(1)
        elif (hasattr(left_sim, 'n') and left_sim.n == 0):
            return Num(0)
        elif (hasattr(right_sim, 'n') and right_sim.n == 1):
            return left_sim
        elif hasattr(left_sim, 'n') and hasattr(right_sim, 'n'):
            return Num(left_sim.n**right_sim.n)
        return Pow(left_sim, right_sim)
    def eval(self, variables):
        """
        Plugs in values for the variables and evaluates the expression.
        """
        return self.left.eval(variables)**self.right.eval(variables)

class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Var(" + repr(self.name) + ")"

    def deriv(self, variable):
        if variable == self.name:
            return Num(1)
        return Num(0)
    def simplify(self):
        return self
    def eval(self, variables):
        if self.name not in variables:
            raise ValueError
        return variables[self.name]

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return "Num(" + repr(self.n) + ")"

    def deriv(self, variable):
        return Num(0)
    def simplify(self):
        return self
    def eval(self, variables):
        return self.n



def sym(text):
    tokens = tokenize(text)
    parsed = parse(tokens)[0]
    #answer = parsed.simplify()
    return parsed

def parse(tokens):
    """
    1+2+3/4+5
    2*x+5+6*y**(2*x)
    """
    if len(tokens) == 1:
        try:
            return [Num(int(tokens[0]))]
        except:
            return [Var(tokens[0])]


    tokens = tokens[:]
    oper_order = [(Pow, '**'), (Div, '/'), (Mul, '*'), (Sub, '-'), (Add, '+')]
    #def parse_expression(index):
    looking = 0
    i = 0
    start_index = -1
    while isinstance(tokens, list) and i < len(tokens):
        if tokens[i] == '(':
            if start_index == -1:
                start_index = i
            looking += 1
        elif tokens[i] == ')':
            looking -= 1
            if looking == 0:
                print(tokens)
                new_block = parse(tokens[start_index+1:i])[0]
                if i < len(tokens):
                    tokens = tokens[0: start_index]+[new_block]+tokens[i+1:]
                else:
                    tokens = tokens[0: start_index]+[new_block]
                i -= i-start_index
                start_index = -1
        i += 1

    def collapse(opera, symbol, tokens):
        i = 0
        while isinstance(tokens, list) and i < len(tokens):
            if tokens[i] == symbol:
                left = convert(tokens[i-1])
                right = convert(tokens[i+1])
                new_block = opera(left, right)
                if i < len(tokens)-2:
                    tokens = tokens[:max(i-1, 0)]+[new_block]+tokens[i+2:]
                else:
                    tokens = tokens[:max(i-1, 0)]+[new_block]
                i -= 1
            i += 1
        return tokens
    for opera in oper_order:
        tokens = collapse(opera[0], opera[1], tokens)
    return tokens

def convert(expression):
    """
    Convert expression to Number or Variable
    """
    if expression == 'pi':
        return Num(3.14159265358979323846)
    if expression == 'euler':
        return Num(2.7182818284590)
    if(isinstance(expression, (Mul, Add, Sub, Pow, Div, Num, Var))):
        return expression
    try:
        return Num(int(expression))
    except:
        return Var(expression)


def tokenize(text):
    """
    creates a generator that will return characters in the text
    """
    split_text = text.split()
    i = 0
    while i < len(split_text): # iterate over every character, note i changes in the case that we mutate split_text
        value = split_text[i]
        if ('(' in value and value != '(') or (')' in value and value != ')'): # detecting the opening and closing parens
            to_add = [] # to add to the new text
            num = 0
            while num < len(value): # this while statement contains the if statements to be able to find and tokenize parenthesis that are next to each other
                if value[num] == '(' or value[num] == ')':
                    to_add.append(value[num])
                else:
                    append_val = value[num:].split(')')[0]
                    to_add.append(append_val)
                    num += len(append_val)-1
                num += 1
            if i < len(split_text)-1:
                split_text = split_text[:i]+to_add+split_text[i+1:]
            else:
                split_text = split_text[:i]+to_add
        i += 1
    return split_text


if __name__ == "__main__":
    #print(tokenize('((((x * -234))))'))
    #print(repr(sym('((x + A) ** (y + z))'))) ( 3 + 7 )
    #print(repr(sym('((a * ((((((((v - x) - (-8 - 2)) + ((G / 6) - (P - -2))) - w) * b) / -8) + -3) / s)) / ((s / (7 * (e * (((6 - 10) - (((K * 8) + (-6 + V)) - (S + (I - w)))) / ((((4 - q) + B) / (-7 + (c / X))) - (7 * (m / b))))))) + 9))')))
    #print(repr(sym('x')))
    print('4 * pi + 3 * euler = ')
    print(sym('4 * pi + 3 * euler').simplify())
    #doctest.testmod()
