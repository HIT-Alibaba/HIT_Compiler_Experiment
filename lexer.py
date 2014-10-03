#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

KEYWORD_LIST = ['if', 'else', 'while', 'break', 'continue', 'for', 'double', 'int', 'float', 'long', 'short',
                'switch', 'case', 'return']
        
SEPARATOR_LIST = ['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '#', '?', ':']

OPERATOR_LIST = ['+', '++', '-', '--', '*', '/', '>', '<', '>=', '<=', '=', '==', '!=']

current_pos = -1
current_line = 0
input_str = []

def is_keyword(s):
    return s in KEYWORD_LIST
    
def is_separator(s):
    return s in SEPARATOR_LIST
    
def is_operator(s):
    return s in OPERATOR_LIST
    
def getchar():
    global current_pos
    global current_line
    current_pos = current_pos + 1
    if current_pos == len(input_str[current_line]):
        current_line = current_line + 1
        current_pos = 0;

    if current_line == len(input_str):
        return 'SCANEOF'
    return input_str[current_line][current_pos]
    
def ungetc():
    global current_pos
    global current_line
    current_pos = current_pos - 1
    if current_pos < 0:
        current_line = current_line - 1;
        current_pos = 0;
    return input_str[current_line][current_pos]
    
def read_file(file):
    global input_str
    f = open(file, 'r');
    input_str = f.readlines();
    f.close()
    
def lexical_error(info):
    print(str(current_line+1) + ':' + str(current_pos+1) + ' Lexical error: ' + info)

def scanner():
    current_char = getchar()
    if current_char == 'SCANEOF':
        return 'SCANEOF'
    if current_char.strip() == '':
        return
    if current_char.isdigit():
        int_value = 0
        while current_char.isdigit():
            int_value = int_value * 10 + int(current_char)
            current_char = getchar()
        
        if current_char != '.':
            ungetc()
            return ('INT', int_value)
        
        float_value = int_value
        d = 10.0
        current_char = getchar()
        while current_char.isdigit():
            float_value = float_value + int(current_char) / d
            d = d * 10
            current_char = getchar()
        ungetc()
        return ('FLOAT', float_value)
    if current_char.isalpha():
        string = ''
        while current_char.isalpha():
            string += current_char
            current_char = getchar()
        ungetc()
        if is_keyword(string):
            return ('KEYWORD', string)
        else:
            return ('ID', string)
    if is_separator(current_char):
        return ('SEP', current_char)
    if is_operator(current_char):
        op = ''
        while is_operator(current_char):
            op += current_char
            current_char = getchar()
        ungetc()
        return ('OP', op)
    else:
        lexical_error('unknown character')
            
def main():
    global input_str
    global current_pos
    global current_line
    file_name = sys.argv[1]
    read_file(file_name)
    while True:
        r = scanner()
        if r == 'SCANEOF':
            break;
        if r is not None:
            print(r)
        
if __name__ == '__main__':
    main()
    
    