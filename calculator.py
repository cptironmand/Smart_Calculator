import collections
from math import pow

""" A program that reads integer numbers, variable assignments, or take mathematical equations as input. It then
prints the output of the requested math in the standard output.  Numbers can be positive, negative, or zero. 
Math identifiers can be plus '+', minus '-', division '/', multiplication '*', power '^'. or combinations """

operators = {'-': 1, '+': 1, '/': 3, '*': 4, '^': 5, '(': 0, ')': 0}
end_program = False     # True means the program should be ended
escape = False          # True means there is an escape sequence and to bypass the math

my_dict = {}            # Empty dictionary to store future variables as reference


def take_inputs(inputs=None):
    """ Takes an input string from the user and returns it """

    if inputs is None:
        inputs = input()
    return inputs


def check_escapes(str_in, list_in, dict_in):
    """ Takes the input string, checks if there is an escape sequence, processes appropriate
    escapes, and returns (1) whether the program should end and, (2) if there is an escape sequence """

    if "/exit" in str_in:
        return True, True

    elif "/help" in str_in:
        print('The program calculates the sum of numbers')
        return False, True

    elif "/dict" in str_in:
        print("Here are the stored variables so far:")
        print(dict_in)
        return False, True

    elif "/" in str_in:
        num = (list_in.index('/'))
        if num == 0:
            print('Unknown command')
            return False, True
        else:
            return False, False

    else:
        return False, False


def convert_to_list(inp_str):
    """ Function takes in the original input string, breaks it into a list one char at a time and returns it """

    output_list = []
    for i in inp_str:
        if i != " ":
            output_list.append(i)

    return output_list


def check_multi_digits(input_list):
    """ Function takes in the input list, recombines multi-digit words and numbers, and returns a deque """

    input_deque = collections.deque()
    updated_deque = collections.deque()
    for i in input_list:
        input_deque.append(i)

    while len(input_deque) > 0:
        if len(updated_deque) < 1:
            updated_deque.append(input_deque.popleft())
        else:
            a = updated_deque.pop()
            b = input_deque.popleft()

            if (a.isnumeric() and b.isnumeric()) or (a.isalpha() and b.isalpha()):
                var = a + b
                updated_deque.append(var)
                continue
            else:
                updated_deque.append(a)
                updated_deque.append(b)

    return updated_deque


def check_multi_operators(input_deque):
    """ Function takes in the updated deque, eliminates repetitive operators and returns the updated deque """

    ops = ["*", "/", "^"]
    updated_deque = collections.deque()

    while len(input_deque) > 0:
        if len(updated_deque) < 1:
            updated_deque.append(input_deque.popleft())
        else:
            a = updated_deque.pop()
            b = input_deque.popleft()

            if (a == "+" and b == "+") or (a == "-" and b == "-"):
                updated_deque.append("+")
                continue
            elif ("-" in a or "-" in b) and ("+" in a or "+" in b):
                updated_deque.append("-")
            elif a in ops and b in ops:
                updated_deque.append("Invalid expression")
            else:
                updated_deque.append(a)
                updated_deque.append(b)

    return updated_deque


def store_in_dict(input_deque, dict_in):
    """ Takes the current deque and existing dictionary, creates a dictionary addition,
    and returns the updated dictionary"""

    if len(input_deque) == 3:
        a = input_deque.popleft()
        b = input_deque.pop()
        valid_key = check_valid(a)
        valid_value = check_valid(b)

        if valid_key and valid_value:
            key = {str(a)}
            value = b

            # Check for an existing key in the dict now being used as a value
            if value in dict_in:
                value = dict_in[value]

            elif not value.isnumeric():
                print("Invalid assignment")
                return dict_in

            new_dict = dict.fromkeys(key, value)
            dict_in.update(new_dict)

        elif not valid_key:
            print("Invalid identifier")

        elif valid_key and not valid_value:
            print("Invalid assignment")

    # This sequence checks for variable declarations that are too long
    elif len(input_deque) > 3:
        print("Invalid assignment")

    # Necessary to ensure the dictionary is never in a 'None' state due to violations above
    return dict_in


def check_valid(str_check):
    """ Takes the left or right side of the variable definition, checks it and returns whether or not it's valid """

    letter = False
    number = False
    neither = False
    for i in str_check:
        if i.isalpha():
            letter = True
        elif i.isnumeric():
            number = True
        else:
            neither = True

    if neither:
        return False

    elif letter and number:
        return False

    elif letter or number:
        return True

    elif not letter and not number and not neither:
        return False


def check_parens(str_check):
    """ Checks the input strings for opening and closing parenthesis to ensure a math equation is entered correctly.
    It returns if the input is valid """

    counter = 0
    for i in str_check:
        if i == "(":
            counter += 1
        elif i == ")":
            counter -= 1
        if counter < 0:
            print("Invalid expression")
            return False

    if counter == 0:
        return True
    else:
        print("Invalid expression")
        return False


def check_input_length(deque_in, dict_in):
    """ Takes the user entered string as a list, checks a series of input failure scenarios, and returns
    if it's a valid input to be processed for math """
    global operators

    if len(deque_in) == 0:  # Emtpy line should not return anything
        return False

    if len(deque_in) == 1:  # Single value entry scenarios
        var = deque_in.pop()

        if var == "":
            return False

        # Check if the input is a number, and if so then print
        try:
            if type(int(var)) == int:
                print(var)
                return False
        except ValueError:
            # Check if the input is a defined variable, and if so then print
            if var in dict_in:
                print(dict_in[var])

            else:
                print("Unknown variable")
            return False

    elif len(deque_in) > 1:  # Multiple values passed into the program for evaluation
        for i in deque_in:
            if i in dict_in:
                continue
            if i in operators:
                continue
            if i == "=":
                continue
            return True
        print("Unknown variable")
        return False


def create_postfix(infix_deque, dict_in):
    """ Takes the inputted mathematical equation in 'infix' notation along with the current dictionary of variables,
    and creates a postfix notation.  From here, it returns the result of the 'do_math' function """

    global operators

    postfix = collections.deque()   # deque to store the postfix formula
    stack = collections.deque()     # deque to hold the stack where the math is done

    while len(infix_deque) > 0:
        var = infix_deque.popleft()
        # Check to see if 'i' is a stored variable, make i = the stored variable
        if var in dict_in:
            i = dict_in[var]
        else:
            i = var

        if i.isnumeric():
            postfix.append(i)
        elif i == "(":
            stack.append(i)
            continue
        elif i == ")":
            value = ""
            while value != "(":
                value = stack.pop()
                if value != '(':
                    postfix.append(value)
            continue
        elif i in operators:
            if len(stack) == 0:
                stack.append(i)
                continue

            op = stack.pop()
            if operators[i] > operators[op]:
                stack.append(op)
                stack.append(i)
            else:
                stack.append(i)
                postfix.append(op)
                for j in range(len(stack)):
                    if len(stack) > 1:
                        op_in = stack.pop()
                        op_exist = stack.pop()
                        if operators[op_in] <= operators[op_exist]:
                            postfix.append(op_exist)
                            stack.append(op_in)
                        else:
                            stack.append(op_exist)
                            stack.append(op_in)
                            break

    if len(stack) > 0:
        for i in range(len(stack)):
            op = stack.pop()
            postfix.append(op)

    return do_math(postfix, stack)


def do_math(postfix, stack):
    """Takes in the postfix notation along with a created stack, performs the math, and returns the final value"""

    while len(postfix) > 0:
        var = postfix.popleft()
        if var not in operators:
            stack.append(int(var))

        else:
            a = stack.pop()
            b = stack.pop()
            if var == "+":
                var = b + a
            elif var == "-":
                var = b - a
            elif var == "*":
                var = b * a
            elif var == "/":
                var = b / a
            elif var == "^":
                var = pow(b, a)
            stack.append(var)

    return int(stack.pop())


""" MAIN BODY OF PROGRAM """
while not end_program:
    valid_input = True  # True means that the input string can be processed for math

    input_string = take_inputs()
    working_list = convert_to_list(input_string)
    end_program, escape = check_escapes(input_string, working_list, my_dict)

    if escape:
        continue
    elif end_program:
        break

    try:
        if type(int(input_string)) == int:
            print(input_string)
            continue
    except ValueError:
        keep_moving = True

    working_deque = check_multi_digits(working_list)
    final_deque = check_multi_operators(working_deque)

    if "=" in working_list:
        my_dict = store_in_dict(final_deque, my_dict)
        continue

    if "(" in working_list or ")" in working_list:
        valid_input = check_parens(input_string)

    if not valid_input:
        continue

    if "Invalid expression" in final_deque:
        print("Invalid expression")
        continue

    valid_input = check_input_length(final_deque, my_dict)

    if valid_input:
        print(create_postfix(final_deque, my_dict))

print("Bye!")
