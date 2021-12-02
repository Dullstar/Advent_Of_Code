import time
import os
import enum


class Operator(enum.Enum):
    ADD = enum.auto()
    MUL = enum.auto()


# Note that this problem involves changing the order of operations.
# A lot of these are static methods packaged with this class for organization purposes - having them keep the object's
# state intact allows us to more safely reuse bits and pieces in Part 2.

# An older version of this script had cleaner parsing, but it assumed all numbers in the input file were between
# 0 and 9, which was probably fine, but the problem description never explicitly states this.
# It's probably possible to clean this up again, but it would require rewriting the parsing.
class Expression:
    def __init__(self, string: str):
        self.terms = []
        check = True
        resume_check = -1
        string = self.remove_spaces(string)
        last_was_num = False
        current_num_str = ""
        for i, char in enumerate(string):
            if check:
                if char.isdigit():
                    current_num_str += char
                    last_was_num = True
                    continue
                elif last_was_num:
                    self.terms.append(current_num_str)
                    # print("Appended the number: ", current_num_str)
                    current_num_str = ""
                    last_was_num = False
                if char == "(":
                    check = False
                    expr, resume_check = self.find_subexpression(string, i)
                    self.terms.append(expr)
                elif char == "+" or char == "*":
                    self.terms.append(char)
                else:
                    raise IOError(f"Invalid character in input: {char}")
            elif i >= resume_check:
                check = True
        if last_was_num:
            self.terms.append(current_num_str)
        self._result = None
        self._result_2 = None

    @property
    def result(self):
        """Gets the result of the expression."""
        if self._result is not None:
            return self._result
        else:
            self._result = self.evaluate(self.terms, 1)
            return self._result

    @property
    def result_2(self):
        """Gets the result of the expression for Part 2, where addition is to be done first"""
        if self._result_2 is not None:
            return self._result_2
        else:
            self._result_2 = self.evaluate_2(self.terms)
            return self._result_2

    @staticmethod
    def find_subexpression(string: str, offset: int):
        """Creates a subexpression from parentheses given the location of the starting parenthesis.
        Returns the expression and the index of the final parenthesis"""
        to_ignore = 0  # to_ignore is used to handle nested parentheses
        offset += 1  # We don't need to check the original character that triggered this call
        for i, char in enumerate(string[offset:], offset):
            if char == "(":
                to_ignore += 1
            if char == ")":
                if to_ignore > 0:
                    to_ignore -= 1
                    continue
                else:
                    return Expression(string[offset:i]), i  # those nested parentheses we ignored get handled here
        print(string[offset:])
        raise IOError(
            "Triggered find_subexpression, but didn't find an end. Either the code is wrong or a parenthesis "
            "in the original expression is mismatched."
        )

    @staticmethod
    def remove_spaces(string: str) -> str:
        """Removes spaces from the given expression and returns the result."""
        output = ""
        for char in string:
            if char != " ":
                output += char
        return output

    @staticmethod
    def evaluate(terms: list, rule_set: int):
        """Evaluates the expression given by an already-parsed list of terms. Can be explicitly called, but it's better
        to call this through the result property, which will make the call if it needs to."""
        running_total = 0
        current_operand = Operator.ADD  # defaulting to add will make it convenient to get started
        for term in terms:
            if term == "+":
                current_operand = Operator.ADD
                continue
            if term == "*":
                current_operand = Operator.MUL
                continue

            if type(term) == Expression:
                if rule_set == 1:
                    term = term.result
                elif rule_set == 2:
                    term = term.result_2
                else:
                    raise ValueError(f"Unrecognized rule set ID: {rule_set}")

            term = int(term)

            if current_operand is Operator.ADD:
                running_total += term
            elif current_operand is Operator.MUL:
                running_total *= term
            else:
                raise ValueError("No operator currently loaded. This should never happen.")
        return running_total

    @staticmethod
    def evaluate_2(terms: list):
        """Evaluates the expression by the second rule_set. Like the evaluate function, it can be explicitly called,
        but it's still better to call this through the result_2 property, which will make the call if it needs to."""

        add_terms = []
        mul_terms = []
        for term in terms:
            if term == "*":
                mul_terms.append(Expression.evaluate(add_terms, 2))
                add_terms = []
            else:
                add_terms.append(term)
        mul_terms.append(Expression.evaluate(add_terms, 2))
        product = 1
        for term in mul_terms:
            # Notice that mul_term's contents are only created by appending the result of evaulate(), which returns
            # an int: thus, we don't need to worry about the possibility of finding an expression in here.
            product *= term

        return product


def parse_input(filename):
    with open(filename, "r") as file:
        expressions = [Expression(expression) for expression in [line.strip() for line in file]]
    return expressions


def main(input_filename: str):
    start_time = time.time()
    expressions = parse_input(input_filename)
    part1_start = time.time()
    results1 = [expression.result for expression in expressions]
    print(f"All the expressions left to right sum to {sum(results1)}")
    part2_start = time.time()
    results2 = [expression.result_2 for expression in expressions]
    print(f"All the expressions addition before multiplication sum to {sum(results2)}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2020/day18.txt")
