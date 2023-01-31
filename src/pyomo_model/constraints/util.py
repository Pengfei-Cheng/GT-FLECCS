import string
import re

def translate_jump_constraint(s):

    # remove wrapper
    _s = s.split("@constraint(")[1]
    _s = ")".join(_s.split(")")[:-1])

    # parse the components
    components = _s.split(',')
    model_name = components[0]
    name_idx = components[1]
    expr = ",".join(components[2:])
    # re-parse when there are indices
    if '[' in name_idx:
        _str_1 = _s.split(']')[0]
        model_name = _str_1.split(',')[0]
        name_idx = ','.join(_str_1.split(',')[1:]) + ']'
        expr = ']'.join(_s.split(']')[1:])[1:]

    # remove whitespaces
    model_name = remove_whitespaces(model_name)
    name_idx = remove_whitespaces(name_idx)
    # for expression, retain basic ones
    expr = expr.strip().translate({ord(c): ' ' for c in string.whitespace})
    # remove redundant whitespaces
    expr = re.sub(' +', ' ', expr)

    name, indices_sets = parse_name_idx(name_idx)
    indices, sets = parse_idx_set(indices_sets)

    func_res = 'def ' + name + '(m'

    if indices:
        for i in indices:
            func_res += ', ' + i
    func_res += '):\n'

    func_res += '\treturn ' + expr + '\n'

    declare_res = model_name + '.' + name + ' = Constraint('
    if sets:
        declare_res += ', '.join(sets)
        declare_res += ', '
    declare_res += 'rule=' + name + ')\n'

    res = func_res + declare_res

    return res

def parse_name_idx(name_idx):
    if len(name_idx.split("[")) == 1:
        name = name_idx.split("[")[0]
        indices_sets = None
    else:
        name = name_idx.split("[")[0]
        indices_sets = name_idx.split("[")[1][:-1]
    return name, indices_sets

def parse_idx_set(indices_sets):
    indices = []
    sets = []
    if indices_sets:
        i_s_list = indices_sets.split(",")
        for i_s in i_s_list:
            i, s = i_s.split("=")
            indices.append(i)
            sets.append(s)
    return indices, sets

def remove_whitespaces(s):
    return s.translate({ord(c): None for c in string.whitespace})
