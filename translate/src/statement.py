from typing import *
from .expression import *

class Statement:
    def __init__(self, e: Expression):
        self.expression = e

    def to_smt(self):
        return ""

    def get_vars(self):
        return self.expression.get_vars()

    def get_varexes(self):
        return self.expression.get_varexes()

class AssertionStatement(Statement):
    def to_smt(self):
        return f"(assert {self.expression.to_smt()})"

class AssignmentStatement(Statement):
    def __init__(self, ve: VariableExpression, e: Expression):
        super().__init__(e)
        self.varex = ve

    def to_smt(self):
        return f"(define-const {self.varex.to_smt()} {self.expression.get_type()} {self.expression.to_smt()})"

    def get_varex(self):
        return self.varex

    def get_vars(self):
        vs = super().get_vars()
        v = self.varex.get_variable()
        if v not in vs:
            vs.append(v)
        return vs

    def get_varexes(self):
        ves = super().get_varexes()
        if self.varex not in ves:
            ves.append(self.varex)
        return ves

class DeclarationStatement(Statement):
    def __init__(self, ve: VariableExpression):
        super().__init__(Expression(ve.get_type()))
        self.varex = ve

    def to_smt(self):
        return f"(declare-const {self.varex.to_smt()} {self.varex.get_type()})"

    def get_varex(self):
        return self.varex

    def get_vars(self):
        vs = super().get_vars()
        v = self.varex.get_variable()
        if v not in vs:
            vs.append(v)
        return vs

    def get_varexes(self):
        ves = super().get_varexes()
        if self.varex not in ves:
            ves.append(self.varex)
        return ves

class StatementSequence:
    def __init__(self, stmts: Sequence[Statement]):
        self.statements = stmts

    def get_statements(self):
        return self.statements

    def get_vars(self):
        vs = []
        for stmt in self.statements:
            stmt_vs = stmt.get_vars()
            for v in stmt_vs:
                if v not in vs:
                    vs.append(v)
        return vs

    def get_varexes(self):
        ves = []
        for stmt in self.statements:
            stmt_ves = stmt.get_varexes()
            for ve in stmt_ves:
                if ve not in ves:
                    ves.append(ve)
        return ves

    def get_replacements(self, initial = False):
        rvs = []
        for v in self.get_vars():
            match_ve = None
            for ve in self.get_varexes():
                if ve.get_variable() is v:
                    match_ve = ve
                    if initial:
                        break
            if match_ve is not None:
                rvs.append((v, match_ve))
        return rvs
