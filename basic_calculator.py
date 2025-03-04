#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################

import argparse
import os

###############################################################################
DEBUG = False


###############################################################################
class BinaryTree:
    """Binary tree implementation"""
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self):
        return f"({self.val} {self.left} {self.right})" if self.left and self.right else str(self.val)


###############################################################################
class ExpressionParser:
    """"""
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

    def __init__(self, expr: str):
        self.tokens = list(expr.replace(' ', ''))
        self.index = 0

    def __current_token(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def __advance(self):
        self.index += 1

    def __operand(self):
        token: str = self.__current_token()
        if token is None:
            raise ValueError("Unexpected end of expression")

        if token.isnumeric():  # Direct number
            self.__advance()
            next_token = self.__current_token()
            while next_token and (next_token.isnumeric() or next_token == '.'):
                token += next_token
                self.__advance()
                next_token = self.__current_token()
            return BinaryTree(token)

        elif token == "(":  # Handle parentheses
            self.__advance()  # Consume '('
            subexpr_tree = self.operands_list()
            if self.__current_token() != ")":
                raise ValueError("Mismatched parentheses")
            self.__advance()  # Consume ')'
            return subexpr_tree

        raise ValueError(f"Unexpected token: {token}")

    def __is_operator(self):
        return self.__current_token() in ExpressionParser.PRECEDENCE

    def __operator(self):
        op = self.__current_token()
        if not self.__is_operator():
            raise ValueError(f"Expected operator but got: {op}")
        self.__advance()
        return op

    def operands_list(self):
        operand_stack = []
        operator_stack = []

        def apply_operator():
            """Pop an operator and apply it to the top two operands in the operand stack."""
            _operator = operator_stack.pop()
            right = operand_stack.pop()
            left = operand_stack.pop()
            node = BinaryTree(_operator)
            node.set_left(left)
            node.set_right(right)
            operand_stack.append(node)

        operand_stack.append(self.__operand())  # First operand

        while self.__is_operator():
            operator = self.__operator()
            while (operator_stack and
                   ExpressionParser.PRECEDENCE[operator_stack[-1]] >= ExpressionParser.PRECEDENCE[operator]):
                apply_operator()

            operator_stack.append(operator)
            operand_stack.append(self.__operand())

        while operator_stack:
            apply_operator()

        return operand_stack[0]  # Root of the expression tree


###############################################################################
def evaluate_tree(eval_tree: BinaryTree):
    if eval_tree.is_leaf():
        val: str = eval_tree.val
        return float(val) if '.' in val else int(val)
    eval_left: int|float = evaluate_tree(eval_tree.left)
    eval_right: int|float = evaluate_tree(eval_tree.right)
    match eval_tree.val:
        case "+":
            return eval_left + eval_right
        case "-":
            return eval_left - eval_right
        case "*":
            return eval_left * eval_right
        case "/":
            return eval_left / eval_right
        case _:
            raise ValueError(f"Unexpected operator: {eval_tree.val}")


###############################################################################
def get_args():

    """
    Command line parsing and help.
    """
    script_name = os.path.basename(__file__)
    my_parser = argparse.ArgumentParser(description="Evaluate a basic math expression with number, parentheses and binary operators +, -, *, and /.")
    my_parser.add_argument("-d", "--debug", default=False, action="store_true",
                           help="The expression to evaluate. Should only contain numbers, parentheses and binary operators +, -, *, and /.")
    return my_parser.parse_args()


###############################################################################
if __name__ == "__main__":
    args = get_args()
    DEBUG = args.debug
    print("BasicCalculator.\nThis program evaluate simple math expression that only contain numbers, parentheses and binary operators +, -, *, and /.")
    print("You can either enter an expression or 'q' or 'Q' to exit the program.\n")
    if DEBUG:
        print("Running with debug mode.")
    expression = str(input("Enter an expression $ "))
    while expression.lower() != "q":
        try:
            if DEBUG:
                print(f"Evaluating expression {expression}")
            parser = ExpressionParser(expression)
            tree = parser.operands_list()
            if DEBUG:
                print(f"Evaluation tree: {tree}")
            if DEBUG:
                print(f"Evaluation:", end=" ")
            print(evaluate_tree(tree))
        except ValueError as e:
            print(e)
        finally:
            print()
            expression = str(input("Enter an expression $ "))

    print("\nGoodbye!")
