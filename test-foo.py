from translate import *

var_x = Variable("Int", "x")
var_y = Variable("Int", "y")
varex_x = VariableExpression(var_x, plain = True)
varex_y = VariableExpression(var_y, plain = True)
opex0 = OperatorExpression("+", [varex_x, varex_y])
ranking_function = RankingFunction("rf", opex0)

litex0 = LiteralExpression(0)
opex1 = OperatorExpression(">", [varex_x, litex0])
opex2 = OperatorExpression(">", [varex_y, varex_x])
opex3 = OperatorExpression("and", [opex1, opex2])
supporting_invariant = SupportingInvariant("si", opex3)

varex_x0 = VariableExpression(var_x)
litex1 = LiteralExpression(3)
assign0 = AssignmentStatement(varex_x0, litex1)
varex_y0 = VariableExpression(var_y)
litex2 = LiteralExpression(1)
assign1 = AssignmentStatement(varex_y0, litex2)
litex3 = LiteralExpression(0)
opex4 = OperatorExpression(">", [varex_y0, litex3])
assert0 = AssertionStatement(opex4)
stem = StatementSequence([assign0, assign1, assert0])

varex_x1 = VariableExpression(var_x, loop = True)
declare0 = DeclarationStatement(varex_x1)
varex_y1 = VariableExpression(var_y, loop = True)
declare1 = DeclarationStatement(varex_y1)
litex4 = LiteralExpression(0)
opex5 = OperatorExpression(">", [varex_x1, litex4])
assert1 = AssertionStatement(opex5)
varex_x2 = VariableExpression(var_x, loop = True)
litex5 = LiteralExpression(1)
opex6 = OperatorExpression("-", [varex_x1, litex5])
assign2 = AssignmentStatement(varex_x2, opex6)
loop = StatementSequence([declare0, declare1, assert1, assign2])

smt_lines = to_smt(stem, loop, ranking_function, supporting_invariant)

if __name__ == "__main__":
    output("foo.smt2", smt_lines)
