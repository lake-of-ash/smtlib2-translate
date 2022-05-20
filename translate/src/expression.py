from typing import *

class Variable:
    def __init__(self, t: str, s: str):
        self.type = t
        self.symbol = s
        self.count = 0
        self.loop_count = 0

    def get_type(self):
        return self.type

    def get_symbol(self, loop: bool = False):
        if loop:
            return "l_" + self.symbol
        return self.symbol

    def get_count(self, loop: bool = False):
        if loop:
            return self.loop_count
        return self.count

    def increment(self, loop: bool = False):
        if loop:
            self.loop_count += 1
        else:
            self.count += 1

class Expression:
    def __init__(self, t: str):
        self.type = t

    def get_type(self):
        return self.type

    def to_smt(self):
        return ""

    def get_vars(self):
        return []

    def get_varexes(self):
        return []

class VariableExpression(Expression):
    def __init__(self, v: Variable, loop: bool = False, plain: bool = False):
        t = v.get_type()
        super().__init__(t)
        self.variable = v
        self.loop = loop
        self.plain = plain
        if self.plain:
            self.count = -1
        else:
            self.count = self.variable.get_count(self.loop)
            self.variable.increment(self.loop)

    def to_smt(self):
        if self.plain:
            return self.variable.get_symbol(self.loop)
        return f"{self.variable.get_symbol(self.loop)}{self.count}"

    def get_variable(self):
        return self.variable

    def get_vars(self):
        return [self.variable]

    def get_varexes(self):
        return [self]

class LiteralExpression(Expression):
    def __init__(self, lit: Union[int, bool]):
        t = "Int" if isinstance(lit, int) else "Bool"
        super().__init__(t)
        self.literal = lit

    def to_smt(self):
        if self.get_type() == "Int":
            return str(self.literal)
        elif self.literal:
            return "true"
        else:
            return "false"

class OperatorExpression(Expression):
    def __init__(self, op: str, args: Sequence[Expression]):
        self.operator = op
        self.arguments = args
        if (self.match("not", ["Bool"])
                or self.match("=>", ["Bool", "Bool"])
                or self.match("and", ["Bool", "Bool"])
                or self.match("or", ["Bool", "Bool"])
                or self.match("xor", ["Bool", "Bool"])
                or self.match("=", ["Bool", "Bool"])
                or self.match("=", ["Int", "Int"])
                or self.match("distinct", ["Bool", "Bool"])
                or self.match("distinct", ["Int", "Int"])
                or self.match("<", ["Int", "Int"])
                or self.match("<=", ["Int", "Int"])
                or self.match(">", ["Int", "Int"])
                or self.match(">=", ["Int", "Int"])
                or self.match("ite", ["Bool", "Bool", "Bool"])):
            t = "Bool"
        elif (self.match("-", ["Int"])
                or self.match("abs", ["Int"])
                or self.match("+", ["Int", "Int"])
                or self.match("-", ["Int", "Int"])
                or self.match("*", ["Int", "Int"])
                or self.match("div", ["Int", "Int"])
                or self.match("mod", ["Int", "Int"])
                or self.match("ite", ["Bool", "Int", "Int"])):
            t = "Int"
        else:
            raise TypeError(f"Could not find an operation {op} matching types of {[arg.get_type() for arg in self.arguments]}")
        super().__init__(t)

    def match(self, op: str, arg_types: Sequence[str]):
        if self.operator == op:
            if len(self.arguments) == len(arg_types):
                matches = [self.arguments[i].get_type() == arg_types[i] for i in range(len(arg_types))]
                return all(matches)
        return False

    def to_smt(self):
        rep = f"({self.operator}"
        for e in self.arguments:
            rep += " " + e.to_smt()
        rep += ")"
        return rep

    def get_vars(self):
        vs = []
        for e in self.arguments:
            for v in e.get_vars():
                if v not in vs:
                    vs.append(v)
        return vs

    def get_varexes(self):
        ves = []
        for e in self.arguments:
            for ve in e.get_varexes():
                if ve not in ves:
                    ves.append(ve)
        return ves
