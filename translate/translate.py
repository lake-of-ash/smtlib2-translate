from .src import *

class Parser:
    pass

def parse(filename):
    #TODO
    pass

def to_smt(stem: StatementSequence, loop: StatementSequence, ranking_function: RankingFunction, supporting_invariant: SupportingInvariant):
    smt_lines = []
    smt_lines.append(f"(set-option :produce-proofs true)")
    smt_lines.append(f"(set-logic QF_NIA)")

    smt_lines.append(ranking_function.to_smt_function())
    smt_lines.append(supporting_invariant.to_smt_function())

    for stmt in stem.get_statements():
        smt_lines.append(stmt.to_smt())

    stem_replace = stem.get_replacements()
    smt_lines.append(f"(assert {ranking_function.to_smt(stem_replace)})")
    smt_lines.append(f"(assert {supporting_invariant.to_smt(stem_replace)})")

    loop_replace_final = loop.get_replacements()
    for stmt in loop.get_statements():
        smt_lines.append(stmt.to_smt())

    loop_replace_initial = loop.get_replacements(initial = True)
    smt_lines.append(f"(assert {ranking_function.to_smt(loop_replace_initial)})")
    smt_lines.append(f"(assert {supporting_invariant.to_smt(loop_replace_initial)})")

    loop_replace_final = loop.get_replacements()
    smt_lines.append(f"(define-const not_ranking_invariant_1 Bool (not {ranking_function.to_smt(loop_replace_final)}))")
    smt_lines.append(f"(define-const not_ranking_invariant_2 Bool (not {ranking_function.to_smt(loop_replace_initial, loop_replace_final)}))")
    smt_lines.append(f"(define-const not_supporting_invariant Bool (not {supporting_invariant.to_smt(loop_replace_final)}))")
    smt_lines.append(f"(assert (or not_ranking_invariant_1 not_ranking_invariant_2 not_supporting_invariant))")

    smt_lines.append(f"(check-sat)")
    smt_lines.append(f"(get-model)")
    smt_lines.append(f"(exit)")
    return smt_lines

def output(filename, smt_lines):
    with open(filename, "w") as f:
        for line in smt_lines:
            f.write(line + "\n")
