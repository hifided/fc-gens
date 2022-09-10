from generators import filter_generator
from generators import combining_generator

if __name__ == "__main__":
    ## TEST FILTER GENERATOR ##
    
    # input binary sequence
    input_sequence = "1101111011010011"
    # tap_list - numbers of input sequence bits that are terms in a linear function F
    tap_string = 'x2+x4+x7+x12'
    # nonlinear function N
    nonlinear_func_string = 'x1*x4+x5*x7+x11'
    # output sequence length - number of filter generator calls
    output_sequence_length = 128
    print(filter_generator(input_sequence, tap_string, nonlinear_func_string, output_sequence_length))

    ## TEST COMBINING GENERATOR ##
    # combinig generator with 3 linear shift registers
    input_sequences_list = ["0010010110110101", "1101001001000111", "1001010110001011"]
    tap_strings_list = ['x1+x2+x3', 'x1+x3+x5+x7+x8', 'x1+x4']
    nonlinear_func_string = 'x1*x3'
    output_sequence_length = 128
    print(combining_generator(input_sequences_list, tap_strings_list, nonlinear_func_string, output_sequence_length))