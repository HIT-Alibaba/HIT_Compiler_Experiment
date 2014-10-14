import sys
from lexer import get_tokens

current_index = -1;
current_token = None
token_list = []

def match(token):
    if token in current_token:
        next_token()
        return True
    else:
        syntax_error(token + 'not matched')
        next_token()
        return False

def is_eof(token):
    return token[0] == '$'
    
def next_token():
    global current_index
    global current_token
    current_index = current_index + 1
    current_token = token_list[current_index]
    
def is_type_specifier(token):
    return token[0].upper() in ['FLOAT', 'VOID', 'DOUBLE', 'INT']
    
def is_identifier(token):
    return token[0] == 'ID'
        
def syntax_error(msg):
    print(msg)

def program():
    declaration_list()
    
def ID():
    print('ID -> idn')
    if is_identifier(current_token):
        next_token()

def type_specifier():
    if is_type_specifier(current_token):
        next_token()
        
def func_declaration():
    type_specifier()
    ID()
    match('(')
    match(')')
    compound_stmt()

def var_declaration():
    print('Var-declaration -> type ID')
    type_specifier()
    ID()
    match(';')

def declaration_list():
    print("Declist -> Declaration*")
    while True:
        if is_type_specifier(current_token):
            var_declaration()
        if is_eof(current_token):
            break
        
def compound_stmt():
    match('{')
    statement_list()
    match('}')
    
def statement_list():
    r = True
    while r:
        r = statement()
    
def statement():
    pass
    
def normal_expression():
    var()
    op()
    var()

def assignment():
    var()
    match('=')
    expression()
    
def expression():
    pass
    
def main():
    file_name = sys.argv[1]
    global token_list
    token_list = get_tokens(file_name)
    next_token()
    program()
    
if __name__ == '__main__':
    main()
    
