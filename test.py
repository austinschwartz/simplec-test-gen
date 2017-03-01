#!/usr/bin/env python3

# http://dl.acm.org/citation.cfm?id=357091
import random, sys, string

ARGUMENT_MAX_LENGTH = 20
ARGUMENT_MAX_COUNT = 20
VARIABLE_MAX_LENGTH = 10
LONG_MAX_POS = (1e6)
LONG_MAX_NEG = -(1e6)
DOUBLE_MAX_POS = (1e6)
DOUBLE_MAX_NEG = -(1e6)

def unary_op():
    return ["+", "-", "&", "*"]

def binary_op():
    return ["+", "-", "*", "/", ">", "<", ">=", "<=", "||", "&&"]

class Generator:
    def __init__(self):
        self.r = 0
        self.k = 0

    def print_for(self):
        print("for(" + self.random_assignment() + ";" + 
                       self.primary_expr() + ";" + 
                       self.random_assignment() +  ")", end = '')

    def print_while(self):
        print("while(" + self.primary_expr() + ")", end = '')


    def print_pre_compound(self):
        rand = random.uniform(0, 1)
        if rand < 0.4:
            self.print_for()
        elif rand < .75:
            self.print_while()

    def unary_expr(self):
        rand = random.uniform(0, 1)
        if rand < 0.5:
            unop = random.choice(unary_op())
            return unop + self.unary_expr()
        else:
            return self.primary_expr()

    def expression(self):
        rand = random.uniform(0, 1)
        if rand < 0.5:
            return self.unary_expr()
        else:
            binop = random.choice(binary_op())
            return self.primary_expr() + binop + self.primary_expr()

    def primary_expr(self):
        rand = random.uniform(0, 1)
        # STRING_CONST
        if rand < 0.1:
            return "\"" + self.random_name() + "\""
        # CHAR_CONST
        elif rand < 0.2:
            return "'" + random.choice(string.ascii_lowercase) + "'"
        # call
        elif rand < 0.3:
            return self.call_expr()
        # ID
        elif rand < 0.4:
            return self.random_name()
        # ID LBRACE expression RBRACE
        elif rand < 0.5:
            return self.random_name() + "[" + self.primary_expr() + "]"
        # INTEGER_CONST
        elif rand < 0.6:
            return str(random.randint(LONG_MAX_NEG, LONG_MAX_POS))
        # DOUBLE_CONST
        elif rand < 0.7:
            return str(random.uniform(DOUBLE_MAX_NEG, DOUBLE_MAX_POS))
        # LPARENT expression RPARENT
        return "(" + self.expression() + ")"


    def random_name(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(1, VARIABLE_MAX_LENGTH)))

    def random_assignment(self):
        return self.random_name() + "=" + self.primary_expr()

    def open(self):
        self.print_pre_compound()
        print("{", end = '')
        self.r = self.r + 1
        self.k = self.k - 1

    def close(self):
        print("}", end = '')
        self.r = self.r - 1
        self.k = self.k - 1

    def random_args(self):
        lst = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(0, ARGUMENT_MAX_LENGTH)))
        ret = []
        prevIsComma = False
        for i, char in enumerate(lst):
            ret.append(char)
            if i == len(lst) - 1:
                break
            if not prevIsComma:
                if random.uniform(0, 1) < 0.3:
                    prevIsComma = True
                    ret.append(',')
                else:
                    prevIsComma = False
            else:
                prevIsComma = False
        return ''.join(ret)


    def call_expr(self):
        return self.random_name() + "(" + self.random_args() + ")"

    def print_call_stmt(self):
        rand = random.uniform(0, 1)
        if rand < 0.3:
            print(self.call_expr() + ";", end = '')

    def prob_close(self):
        return ((self.r * (self.r + self.k + 2))/(2 * self.k * (self.r + 1)))

    def gen(self, n):
        self.k = 2 * n
        self.r = 0
        print("long main(){", end = '')
        while self.r != self.k:
            if self.r == 0:
                self.open()
            elif random.uniform(0, 1) < 0.7:
                self.print_call_stmt()
            elif random.uniform(0, 1) < self.prob_close():
                self.close()
            else:
                self.open()
        while self.k != 0:
            self.close()
        print("}")

x = Generator()
if len(sys.argv) < 2:
    print("first arg is # of parens")
    sys.exit()

x.gen(int(sys.argv[1]))
            
