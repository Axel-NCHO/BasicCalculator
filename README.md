# BasicCalculator

This program evaluate simple math expression that only contain numbers, parentheses and binary operators +, -, *, and /.  

## Examples
```shell
python3 basic_calculator.py 
BasicCalculator.
This program evaluate simple math expression that only contain numbers, parentheses and binary operators +, -, *, and /.
You can either enter an expression or 'q' or 'Q' to exit the program.

Enter an expression $ ((8 + 2) * 3) - (5 / (6 - 4))
27.5

Enter an expression $ 
```

There is a `debug` mode to see the intermediate binary tree representation of the expression in postfix read order. Ue the `-d` argument.
```shell
python3 basic_calculator.py -d
BasicCalculator.
This program evaluate simple math expression that only contain numbers, parentheses and binary operators +, -, *, and /.
You can either enter an expression or 'q' or 'Q' to exit the program.

Enter an expression $ ((8 + 2) * 3) - (5 / (6 - 4))
Evaluating expression ((8 + 2) * 3) - (5 / (6 - 4))
Evaluation tree: (- (* (+ 8 2) 3) (/ 5 (- 6 4)))
Evaluation: 27.5

Enter an expression $ 
```
Enter `'q'` or `'Q'` to exit the program.
```shell
python3 basic_calculator.py 
BasicCalculator.
This program evaluate simple math expression that only contain numbers, parentheses and binary operators +, -, *, and /.
You can either enter an expression or 'q' or 'Q' to exit the program.

Enter an expression $ ((8 + 2) * 3) - (5 / (6 - 4))
27.5

Enter an expression $ q

Goodbye!

Process finished with exit code 0
```
