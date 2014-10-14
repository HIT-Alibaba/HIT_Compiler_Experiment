import sys
from lexer import get_tokens

current_index = -1;
current_token = None
token_list = []

def match(token):
    if token in current_token:
        print(current_token)
        next_token()
        return True
    else:
        syntax_error(token + 'not matched')
        return False
    
def next_token():
    global current_index
    global current_token
    current_index = current_index + 1
    current_token = token_list[current_index]
    
def syntax_error(msg):
    print(msg)

def program():
    pass
    
def function():
    pass
    
def statements():
    pass
    
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
    
