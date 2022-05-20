from typing import *
from .expression import *
from .statement import *

RV = TypeVar('RV', bound=tuple[Variable, VariableExpression])

class Invariant:
    def __init__(self, name: str, e: Expression):
        self.expression = e
        self.name = name

    def to_smt_vars(self, replace: Sequence[RV] = [], types: bool = False):
        rep_vars = ""
        for ve in self.expression.get_varexes():
            for (u, ue) in replace:
                if ve.get_variable() is u:
                    ve = ue
            if len(rep_vars) != 0:
                rep_vars += " "
            if types:
                rep_vars += f"({ve.to_smt()} {ve.get_type()})"
            else:
                rep_vars += ve.to_smt()
        return rep_vars

    def to_smt_function(self):
        return f"(define-fun {self.name} ({self.to_smt_vars(types = True)}) {self.expression.get_type()} {self.expression.to_smt()})"

    def to_smt_call(self, replace: Sequence[RV] = []):
        return f"({self.name} {self.to_smt_vars(replace)})"

    def to_smt(self, replace: Sequence[RV] = []):
        return self.to_smt_call(replace)

class RankingFunction(Invariant):
    def to_smt(self, replace: Sequence[RV] = [], replace_2: Sequence[RV]|None = None):
        if replace_2 is not None:
            return f"(> {self.to_smt_call(replace)} {self.to_smt_call(replace_2)})"
        return f"(> {self.to_smt_call(replace)} 0)"

class SupportingInvariant(Invariant):
    pass
