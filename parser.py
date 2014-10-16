from util import Production, Symbol


TERMINAL_SET = set()

NON_TERMINAL_SET = set()

SYMBOL_DICT = {}

PRODUCTION_LIST = []

ANALYSIS_TABLE = {}


def symbol_for_str(str):
    return SYMBOL_DICT[str]


def is_terminal(str):
    return str in TERMINAL_SET


def prepare_symbols_and_productions():
    f = open('grammer.txt', 'r')
    lines = f.readlines()
    terminal = False
    production = False
    for l in lines:
        if l.strip() == '*terminals':
            terminal = True
            production = False
            continue
        if l.strip() == '*productions':
            terminal = False
            production = True
            continue
        if l.strip() == '*end':
            break
        if terminal:
            TERMINAL_SET.update([l.strip()])
        if production:
            left = l.split('::=')[0].strip()
            NON_TERMINAL_SET.update([left])

            try:
                right = l.split('::=')[1].strip()
                if right == '':
                    raise IndexError
                p = Production(left, right.split(' '))
            except IndexError:
                p = Production(left, ['null'])

            PRODUCTION_LIST.append(p)

    for s in TERMINAL_SET:
        sym = Symbol(s, sym_type='T')
        SYMBOL_DICT[s] = sym

    for s in NON_TERMINAL_SET:
        sym = Symbol(s, sym_type='N')
        SYMBOL_DICT[s] = sym


def get_nullable():
    # init is_nullable
    changes = True
    while changes:
        changes = False
        for p in PRODUCTION_LIST:
            if not symbol_for_str(p.left).is_nullable:
                if p.right[0] == 'null':
                    symbol_for_str(p.left).is_nullable = True
                    changes = True
                    continue
                else:
                    right_is_nullable = symbol_for_str(p.right[0]).is_nullable
                    for r in p.right[1:]:
                        right_is_nullable = right_is_nullable & symbol_for_str(r).is_nullable

                    if right_is_nullable:
                        changes = True
                        symbol_for_str(p.left).is_nullable = True


def get_first():
    for s in TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        sym.first_set = set([s])

    for s in NON_TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        if sym.is_nullable:
            sym.first_set = set(['null'])
        else:
            sym.first_set = set()

    while True:
        first_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if p.right[0] == 'null':
                sym_left.first_set.update(set(['null']))
                continue
            previous_first_set = set(sym_left.first_set)

            for s in p.right:
                sym_right = symbol_for_str(s)
                sym_left.first_set.update(sym_right.first_set)
                if sym_right.is_nullable:
                    continue
                else:
                    break

            if previous_first_set != sym_left.first_set:
                first_set_is_stable = False

        if first_set_is_stable:
            break


def get_follow():
    for s in NON_TERMINAL_SET:
        sym = symbol_for_str(s)
        sym.follow_set = set()

    symbol_for_str('<s>').follow_set.update(set(['#']))

    while True:
        follow_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if sym_left.is_terminal():
                continue
            for s in p.right:
                if s == 'null':
                    continue
                if symbol_for_str(s).is_terminal():
                    continue
                current_symbol = symbol_for_str(s)
                previous_follow_set = set(current_symbol.follow_set)
                next_is_nullable = True
                for s2 in p.right[p.right.index(s) + 1:]:
                    next_symbol = symbol_for_str(s2)
                    current_symbol.follow_set.update(next_symbol.first_set)
                    if next_symbol.is_nullable:
                        continue
                    else:
                        next_is_nullable = False
                        break
                if next_is_nullable:
                    current_symbol.follow_set.update(sym_left.follow_set)

                if current_symbol.follow_set != previous_follow_set:
                    follow_set_is_stable = False

        if follow_set_is_stable:
            break


def get_select():
    while True:
        select_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            previous_select = set(p.select)
            if p.right[0] == 'null':
                p.select.update(sym_left.follow_set)
                continue
            sym_right = symbol_for_str(p.right[0])
            p.select.update(sym_right.first_set)
            if sym_right.is_nullable:
                p.select.update(sym_right.first_set.union(sym_left.follow_set))
            if previous_select != p.select:
                select_set_is_stable = False
        if select_set_is_stable:
            break


def get_analysis_table():
    global ANALYSIS_TABLE
    for non_terminal in NON_TERMINAL_SET:
        for p in PRODUCTION_LIST:
            if non_terminal == p.left:
                for s in p.select:
                    d = {s : p}
                    ANALYSIS_TABLE[non_terminal] = d


def syntax_error(msg):
    print(msg)


def main():
    # file_name = sys.argv[1]
    prepare_symbols_and_productions()
    get_nullable()
    get_first()
    get_follow()
    for s in NON_TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        print sym

    get_select()
    for p in PRODUCTION_LIST:
        print p

    get_analysis_table()


if __name__ == '__main__':
    main()