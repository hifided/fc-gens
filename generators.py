import numpy as np


# linear shift register
# tap_list - numbers of input sequence bits that are terms in a linear function F
def lfsr(input_sequence, tap_list):
    current_sequence = input_sequence[1:]
    current_sequence.append(np.sum(np.asarray(input_sequence) * np.asarray(tap_list)) % 2)
    return current_sequence, input_sequence[0]


# representation of the linear callback function in a convenient form
# Example: if input_sequence_length = 7: 1+x1+x2+x3+x2+x5 -> [1, 1, 0, 1, 0, 1, 0]
def parse_taps(tap_string, input_sequence_length):
    gh = []
    try:
        parsed_taps_string = tap_string.split('+')  # split terms by "+"
    except ValueError:
        raise ValueError(F"Syntax error. Can't split linear callback function {tap_string} by +")
    for term in parsed_taps_string:
        if not term:
            raise IndexError(F"Given wrong function {tap_string}\n Empty term introduced.")
        if term[0] == 'x' or term[0] == 'X':  # upper and lower register support
            if not term[1:].isdigit():
                raise IndexError(F"Wrong index in term x{term[1:]}")
            if int(term[1:]) > input_sequence_length:
                raise IndexError(F"Index x{term[1:]} is out of range")
            else:
                gh.append(int(term[1:]))  # form array of tap_string terms positions
        elif term.isdigit():
            if int(term) % 2:
                gh.append(0)
        else:
            raise ValueError(F"Syntax error. Given wrong term {term} in linear callback function {tap_string}")
    out = []
    # array of terms positions to binary sequence
    for value in range(input_sequence_length):
        if gh.count(value) % 2:
            out.append(1)
        else:
            out.append(0)
    return out


# representation of the nonlinear filter function in a convenient form
# Example: x1*x2*x5+x1+9+3*x6+2*x7+1 -> [[0, 1, 4], [0], 1, [5], 1]
def parse_nonlinear_func(nonlinear_func_string):
    out = []
    try:
        parsed_nonlinear_func_string = nonlinear_func_string.split('+')  # split terms by "+"
    except ValueError:
        raise ValueError(F"Syntax error. Can't split nonlinear filter function {nonlinear_func_string} by +")
    for term in parsed_nonlinear_func_string:
        gh = []
        if term.isdigit():
            if int(term) % 2:
                out.append(1)
            continue
        try:
            buffer = term.split('*')  # split multipliers in terms by "*"
        except ValueError:
            raise ValueError(F"Syntax error. Can't split nonlinear filter function {nonlinear_func_string} by *")
        for variable in buffer:
            if not variable:
                raise IndexError(F"Given wrong function {nonlinear_func_string}\n Empty multiplier introduced.")
            if variable[0] == 'x' or variable[0] == 'X':  # upper and lower register support
                try:
                    gh.append(int(variable[1:])-1)  # form array of nonlinear_func_string terms positions
                except:
                    raise ValueError(F"Syntax error. Given wrong variable {variable} in function {nonlinear_func_string}")
            elif variable.isdigit():
                if int(variable) % 2 == 0:  # find zero term cause of even multiplier
                    gh = []
                    break
            else:
                raise ValueError(F"Given wrong variable {variable} in function {nonlinear_func_string}")
        # skip zero terms
        if gh:
            out.append(gh)
    return out


# nonlinear filter function evaluation on a given bin sequence
def calculator(sequence, parsed_nonlinear_func_list):
    sum_result = 0
    for term in parsed_nonlinear_func_list:  # for per terms
        if term == 1:
            sum_result += term
            continue
        buffer = 1
        for multiplier in term:  # for per multipliers in term
            try:
                buffer *= int(sequence[multiplier])
            except IndexError:
                raise IndexError(F"Index x{str(multiplier+1)} is out of range")
        sum_result += buffer
    return sum_result % 2  # output value 0 or 1


# filter generator
def filter_generator(input_sequence, tap_string, nonlinear_func_string, output_sequence_length):
    # input sequence validation
    if input_sequence.count("1") + input_sequence.count("0") != len(input_sequence):
        raise ValueError(F"The input sequence {input_sequence} contains characters other than 0 and 1")
    if len(input_sequence) < 1:
        raise ValueError("Empty input sequence")
    list_input_sequence = [int(x) for x in input_sequence]
    tap_list = parse_taps(tap_string, len(list_input_sequence))
    parsed_nonlinear_func_list = parse_nonlinear_func(nonlinear_func_string)
    output_sequence = []
    for _ in range(output_sequence_length):  # output_sequence_length is a number of filter generator calls
        sequence, _ = lfsr(list_input_sequence, tap_list)  # F called
        list_input_sequence = sequence
        sum_result = calculator(sequence, parsed_nonlinear_func_list)  # N called
        if sum_result != None:
            output_sequence.append(sum_result)
        else:
            raise ValueError("The output value is non-numeric")
    # convert output bin array to string        
    new_output_sequence = [str(value) for value in output_sequence]
    output_string = ''.join(new_output_sequence)
    return output_string


# combining generator - set of multiple linear shift register with an output value calculated by the nonlinear function
def combining_generator(input_sequence, tap_string, nonlinear_func_string, output_sequence_length):
    # input sequences validation
    for single_sequence in input_sequence:
        if single_sequence.count("1") + single_sequence.count("0") != len(single_sequence):
            raise ValueError(F"The input sequence {single_sequence} contains characters other than 0 and 1")
        if len(single_sequence) < 1:
            raise ValueError("Empty input sequence")
    number_of_lfsr = len(input_sequence)
    tap_list = []
    parsed_nonlinear_func_list = parse_nonlinear_func(nonlinear_func_string)
    for num in range(number_of_lfsr):
        tap_list.append(parse_taps(tap_string[num], len(input_sequence[num])))  # list of parsed F functions
    output_sequence = []
    for _ in range(output_sequence_length):
        # output_sequence_length is a number of filter generator calls
        current_sequence = []
        list_input_sequence = [int(x) for x in input_sequence[num]]
        for num in range(number_of_lfsr):  # for per linear shift registers 
            sequence, output_value = lfsr(list_input_sequence, tap_list[num])  # current lfsr called
            input_sequence[num] = sequence
            current_sequence.append(output_value)
        sum_result = calculator(current_sequence, parsed_nonlinear_func_list)  # N called
        if sum_result != None:
            output_sequence.append(sum_result)
        else:
            raise ValueError("The output value is non-numeric")
    # convert output bin array to string     
    new_output_sequence = [str(value) for value in output_sequence]
    output_string = ''.join(new_output_sequence)
    return output_string
