class Production(object):
    def __init__(self, left, right, select=None):
        self.left = left
        self.right = right
        self.select = set()
        
    def __str__(self):
        return self.left + ' -> ' + str(self.right) + ' Select: ' + str(self.select)


class Symbol(object):
    def __init__(self, symbol, first_set=None, follow_set=None, sym_type='N'):
        self.symbol = symbol
        self.first_set = first_set
        self.follow_set = follow_set
        self.sym_type = sym_type
        self.is_nullable = False
        self.attr = {}
        self.father = None
        self.children = []
        self.lexical_value = None
        
    def __str__(self):
        return self.symbol + ' Derive_empty:' + str(self.is_nullable) + ' First:' + str(self.first_set) + ' Follow:' + str(self.follow_set)
        
    def is_terminal(self):
        return self.sym_type == 'T'

class Entry(object):
    def __init__(self, type, length, name):
        self.type = type
        self.length = length
        self.name = name

    def __str__(self):
        return self.name + ' ' + self.type + ' ' + str(self.length)