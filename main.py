class BinaryOperator:

    def __init__(self, val: str):
        self.val = val

    def apply(self, operand1: int | float, operand2: int | float):
        match self.val:
            case '+':
                return operand1 + operand2
            case '-':
                return operand1 - operand2
            case '*':
                return operand1 * operand2
            case '/':
                return operand1 / operand2
            case _:
                raise Exception(f"Invalid operation: {self.val}")

    def __gt__(self, other):
        if not isinstance(other, BinaryOperator):
            return False
        return self.val in "/*" and other.val in "+-"

    def __lt__(self, other):
        if not isinstance(other, BinaryOperator):
            return False
        return self.val in "+-" and other.val in "*/"


class BinaryTree:

    def __init__(self, val: int|float|BinaryOperator):
        self.val = val
        self.left = None
        self.right = None

    def set_left(self, val: int|float|BinaryOperator):
        self.left = BinaryTree(val)

    def set_left_tree(self, tree):
        self.left = tree

    def set_right(self, val: int|float|BinaryOperator):
        self.right = BinaryTree(val)

    def set_right_tree(self, tree):
        self.right = tree

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def has_two_children(self) -> bool:
        return self.left and self.right

    def eval(self) -> int|float:
        can_eval = self.has_two_children() or self.is_leaf()
        if not can_eval:
            raise Exception("Invalid expression. Malformed expression.")

        if self.is_leaf():
            if isinstance(self.val, BinaryOperator):
                raise Exception("Invalid expression. Operand can't be str.")
            return self.val

        val1: int|float = self.left.eval()
        val2: int|float = self.right.eval()

        if isinstance(self.val, BinaryOperator):
            operation: BinaryOperator = self.val
            return operation.apply(val1, val2)
        else:
            raise Exception("Invalid expression. Malformed expression.")



class BasicCalculator:

    def __init__(self, expression: str):
        self.expression = expression
        self.parse_idx = 0
        self.strategy: BinaryTree

    def eval(self) -> int|float:
        self.__expression()
        return self.strategy.eval()

    def __expression(self):
        if self.expression[self.parse_idx] == '(':
            self.__accept('(')
            self.strategy = self.__operands_list()
            self.__accept(')')
        else:
            self.strategy = self.operands_list()

    def __operands_list(self):
        operand: int|float = self.__operand()
        while self.__is_operator():
            operator: BinaryOperator = self.__operator()
            operand2 = self.__operand()
            if self.strategy is None:
                self.strategy = BinaryTree(operator)
                self.strategy.set_left(operand)
                self.strategy.set_right(operand2)
            else:
                last_operation: BinaryOperator = self.strategy.val
                if last_operation < operator:
                    last_operand = self.strategy.right.val
                    self.strategy.set_right(operator)
                    self.strategy.right.set_left(last_operand)
                    self.strategy.right.set_right(operand2)
                else:
                    new_strategy: BinaryTree = BinaryTree(operator)
                    new_strategy.set_left_tree(self.strategy)
                    new_strategy.set_right(operand2)
                    self.strategy = new_strategy


    def __operand(self):
        if self.__is("("):
            self.__accept('(')
            self.__expression()


    def __accept(self, symbol: str):
        if self.expression[self.parse_idx] == symbol:
            self.parse_idx += 1
        else:
            raise Exception("Invalid expression. Malformed expression.")


    def __is(self, symbol: str):
        return len(self.expression) > self.parse_idx and self.expression[self.parse_idx] == symbol



tree = BinaryTree(BinaryOperator('+'))
tree.set_left(1)
tree.set_right(2)

print(tree.eval())