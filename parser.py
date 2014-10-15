import sys
from lexer import current_row, current_line
from util import Production, Symbol

TERMINAL_LIST = ["<ID>","<(>","<)>","<VOID>","<INT>","<CHAR>","<FLOAT>","<LONG>","<DOUBLE>","<SHORT>","<,>",
				 "<;>","<{>","<}>","<=>","<CONTINUE>","<BREAK>","<RETURN>","<WHILE>","<IF>","<ELSE>",
				 "<:>","<>>","<<>","<>=>","<<=>","<!=>","<==>","<=>","<+=>","<-=>","<*=>","</=>","<%=>",
                 "<+>","<->","<*>","</>","<%>","<++>","<-->","<int>","<float>", "<short>" ,"<long>", "<string>","<!>","#"]
                 
NON_TERMINAL_LIST = ['<s>','<type>', '<func_declaration>','<compound_stmt>','<define_stmt>','<define_stmts>', '<stmts>', '<stmt>', '<iter_stmt>', '<else_stmt>',
                    '<selection_stmt>', '<expression>', '<assignment>', '<compare_op>', '<arith_op>', '<operation>','<term>', '<terms>', '<value>',
                    '<factor>','<factors>', '<const>', '<declarations>', '<declaration>']

SYMBOL_DICT = {}

PRODUCTION_LIST = []

def symbol_for_str(str):
    return SYMBOL_DICT[str]

def is_terminal(str):
    return str in TERMINAL_LIST

def prepare_symbols():
    for s in TERMINAL_LIST:
        sym = Symbol(s, sym_type='T')
        SYMBOL_DICT[s] = sym
         
    for s in NON_TERMINAL_LIST:
        sym = Symbol(s, sym_type='N')
        SYMBOL_DICT[s] = sym
        
def prepare_productions():
    p1 = Production('<type>', ['<INT>'])
    p2 = Production('<type>', ['<FLOAT>']) 
    p3 = Production('<type>', ['<DOUBLE>'])  
    p4 = Production('<type>', ['<SHORT>'])
    p5 = Production('<type>', ['<LONG>'])
    p6 = Production('<const>', ['<int>'])
    p7 = Production('<const>', ['<float>'])
    p8 = Production('<const>', ['<short>'])
    p9 = Production('<const>', ['<long>'])
    p10 = Production('<const>', ['<string>'])
    p11 = Production('<compare_op>', ['<>>'])
    p12 = Production('<compare_op>', ['<<>'])
    p13 = Production('<compare_op>', ['<>=>'])
    p14 = Production('<compare_op>', ['<<=>'])
    p15 = Production('<compare_op>', ['<==>'])
    p16 = Production('<compare_op>', ['<!=>'])
    p17 = Production('<arith_op>', ['<+>'])
    p18 = Production('<arith_op>', ['<->'])
    p19 = Production('<arith_op>', ['<*>'])
    p20 = Production('<arith_op>', ['</>'])
    p21 = Production('<arith_op>', ['<%>'])
    p22 = Production('<arith_op>', ['<+=>'])
    p23 = Production('<arith_op>', ['<-=>'])
    p24 = Production('<arith_op>', ['<*=>'])
    p25 = Production('<arith_op>', ['</=>'])
    p26 = Production('<arith_op>', ['<%=>'])
    p27 = Production('<factor>', ['<arith_op>', '<factor>'])
    p28 = Production('<factor>', ['<const>'])
    p29 = Production('<factor>', [])
    p30 = Production('<factor>', ['<(>', '<expression>', '<)>'])
    p31 = Production('<factors>', ['<arith_op>', '<factor>', '<factors>'])
    p32 = Production('<factors>', [])
    p33 = Production('<term>', ['<factor>', '<factors>'])
    p34 = Production('<terms>', ['<arith_op>', '<term>', '<terms>'])
    p35 = Production('<terms>', [])
    p36 = Production('<value>', ['<term>', '<terms>'])
    p37 = Production('<operation>', ['<arith_op>', '<value>'])
    p38 = Production('<operation>', ['<compare_op>', '<value>'])
    p39 = Production('<operation>', [])
    p40 = Production('<expression>', ['<value>', '<operation>'])

    p41 = Production('<assignment>', ['<=>', '<expression>'])
    p42 = Production('<assignment>', [])
    p43 = Production('<define_stmt>', ['<type>', '<ID>', '<assignment>'])
    p44 = Production('<define_stmts>', ['<define_stmt>', '<define_stmts>'])
    p45 = Production('<define_stmts>', [])
    p46 = Production('<compound_stmt>', ['<define_stmts>', '<stmts>'])
    p47 = Production('<iter_stmt>', ['<WHILE>', '<(>', '<expression>', '<stmt>'])
    p48 = Production('<selection_stmt>', ['<IF>', '<(>', '<expression>', '<(>', '<stmt>', '<else_stmt>'])
    p49 = Production('<else_stmt>', ['<ELSE>', '<stmt>', '<else_stmt>'])
    p50 = Production('<else_stmt>', [])
    p51 = Production('<stmt>', ['<compound_stmt>'])
    p52 = Production('<stmt>', ['<iter_stmt>'])
    p53 = Production('<stmt>', ['<selection_stmt>'])
    p54 = Production('<stmt>', ['<expression>', '<,>'])
    p55 = Production('<stmts>', ['<stmt>', '<stmts>'])
    p56 = Production('<stmts>', [])
    p57 = Production('<func_declaration>', ['<type>', '<ID>', '<(>', '<)>', '<compound_stmt>'])
    p56 = Production('<s>', ['<declarations'])
    p56 = Production('<declarations>', ['<func_declaration>', '<declarations'])
    p56 = Production('<declarations>', [])

    PRODUCTION_LIST.append(p1)
    PRODUCTION_LIST.append(p2)
    PRODUCTION_LIST.append(p3)
    PRODUCTION_LIST.append(p4)
    PRODUCTION_LIST.append(p5)
    PRODUCTION_LIST.append(p6)
    PRODUCTION_LIST.append(p7)
    PRODUCTION_LIST.append(p8)
    PRODUCTION_LIST.append(p9)
    PRODUCTION_LIST.append(p10)
    PRODUCTION_LIST.append(p11)
    PRODUCTION_LIST.append(p12)
    PRODUCTION_LIST.append(p13)
    PRODUCTION_LIST.append(p14)
    PRODUCTION_LIST.append(p15)
    PRODUCTION_LIST.append(p16)
    PRODUCTION_LIST.append(p17)
    PRODUCTION_LIST.append(p18)
    PRODUCTION_LIST.append(p19)
    PRODUCTION_LIST.append(p20)
    PRODUCTION_LIST.append(p21)
    PRODUCTION_LIST.append(p22)
    PRODUCTION_LIST.append(p23)
    PRODUCTION_LIST.append(p24)
    PRODUCTION_LIST.append(p25)
    PRODUCTION_LIST.append(p26)
    PRODUCTION_LIST.append(p27)
    PRODUCTION_LIST.append(p28)
    PRODUCTION_LIST.append(p29)
    PRODUCTION_LIST.append(p30)
    PRODUCTION_LIST.append(p31)
    PRODUCTION_LIST.append(p32)
    PRODUCTION_LIST.append(p33)
    PRODUCTION_LIST.append(p34)
    PRODUCTION_LIST.append(p35)
    PRODUCTION_LIST.append(p36)
    PRODUCTION_LIST.append(p37)
    PRODUCTION_LIST.append(p38)
    PRODUCTION_LIST.append(p39)
    PRODUCTION_LIST.append(p40)
    PRODUCTION_LIST.append(p41)
    PRODUCTION_LIST.append(p42)
    PRODUCTION_LIST.append(p43)
    PRODUCTION_LIST.append(p44)
    PRODUCTION_LIST.append(p45)
    PRODUCTION_LIST.append(p46)
    PRODUCTION_LIST.append(p47)
    PRODUCTION_LIST.append(p48)
    PRODUCTION_LIST.append(p49)
    PRODUCTION_LIST.append(p50)
    PRODUCTION_LIST.append(p51)
    PRODUCTION_LIST.append(p52)
    PRODUCTION_LIST.append(p53)
    PRODUCTION_LIST.append(p54)
    PRODUCTION_LIST.append(p55)
    PRODUCTION_LIST.append(p56)
    PRODUCTION_LIST.append(p57)

    
def get_derived_empty():
    # init derived_empty
    changes = True
    while changes:
        changes = False
        for p in PRODUCTION_LIST:
            if not symbol_for_str(p.left).derived_empty:
                if len(p.right) == 0:
                    symbol_for_str(p.left).derived_empty = True
                    changes = True
                    continue
                else:
                    right_derived_empty = symbol_for_str(p.right[0]).derived_empty
                    for r in p.right[1:]:
                        right_derived_empty = right_derived_empty & symbol_for_str(r).derived_empty
                        
                    if right_derived_empty:
                        changes = True
                        symbol_for_str(p.left).derived_empty = True
                
        
def get_first():
    for s in TERMINAL_LIST:
        sym = SYMBOL_DICT[s]
        sym.first_set = set([s])
        
    for s in NON_TERMINAL_LIST:
        sym = SYMBOL_DICT[s]
        if sym.derived_empty:
            sym.first_set=set(['null'])
        else:
            sym.first_set = set()
        
    first_set_is_stable = True
    while True:
        first_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            for s in p.right:
                sym_right = symbol_for_str(s)
                temp_set = sym_left.first_set.union(sym_right.first_set)
                if temp_set != sym_left.first_set:
                    sym_left.first_set = temp_set
                    first_set_is_stable = False
                if sym_right.derived_empty:
                    continue
        if first_set_is_stable:
            break;

def get_follow():
    for s in NON_TERMINAL_LIST:
        sym = symbol_for_str(s)
        sym.follow_set = set()

    follow_set_is_stable = True
    while True:
        follow_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if sym_left.is_terminal():
                continue
            for s in p.right:
                if symbol_for_str(s).is_terminal():
                    continue
                previous_follow_set = symbol_for_str(s).follow_set
                next_r = None
                try:
                    next_r = p.right[p.right.index(s) + 1]
                except IndexError:
                    break
                symbol_for_str(next_r).first_set.difference_update(set(['null']))
                r = symbol_for_str(next_r).first_set
                symbol_for_str(s).follow_set.update(r)

                if 'null' in symbol_for_str(next_r).first_set:
                    symbol_for_str(s).follow_set = symbol_for_str(s).follow_set.union(symbol_for_str(sym_left).follow_set)

                if previous_follow_set != symbol_for_str(s).follow_set:
                    follow_set_is_stable = False

        if follow_set_is_stable:
            break;

def syntax_error(msg):
    print(msg)
    
def main():
    #file_name = sys.argv[1]
    prepare_symbols()
    prepare_productions()
    get_derived_empty()
    get_first()
    get_follow()
    for s in NON_TERMINAL_LIST:
        sym = SYMBOL_DICT[s]
        print sym
       

if __name__ == '__main__':
    main()
    
