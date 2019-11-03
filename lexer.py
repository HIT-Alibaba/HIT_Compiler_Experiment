#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

KEYWORD_LIST = [
    "if",
    "else",
    "while",
    "break",
    "continue",
    "for",
    "double",
    "int",
    "float",
    "long",
    "short",
    "switch",
    "case",
    "return",
    "void",
]

SEPARATOR_LIST = ["{", "}", "[", "]", "(", ")", "~", ",", ";", ".", "?", ":"]

OPERATOR_LIST = [
    "+",
    "++",
    "-",
    "--",
    "+=",
    "-=",
    "*",
    "*=",
    "%",
    "%=",
    "->",
    "|",
    "||",
    "|=",
    "/",
    "/=",
    ">",
    "<",
    ">=",
    "<=",
    "=",
    "==",
    "!=",
    "!",
]

CATEGORY_DICT = {
    "double": 265,
    "int": 266,
    "break": 268,
    "else": 269,
    "switch": 271,
    "case": 272,
    "char": 276,
    "return": 278,
    "float": 281,
    "continue": 284,
    "for": 285,
    "void": 287,
    "do": 292,
    "if": 293,
    "while": 294,
    "static": 295,
    "{": 299,
    "}": 300,
    "[": 301,
    "]": 302,
    "(": 303,
    ")": 304,
    "~": 305,
    ",": 306,
    ";": 307,
    "?": 310,
    ":": 311,
    "<": 314,
    "<=": 315,
    ">": 316,
    ">=": 317,
    "=": 318,
    "==": 319,
    "|": 320,
    "||": 321,
    "|=": 322,
    "^": 323,
    "^=": 324,
    "&": 325,
    "&&": 326,
    "&=": 327,
    "%": 328,
    "%=": 329,
    "+": 330,
    "++": 331,
    "+=": 332,
    "-": 333,
    "--": 334,
    "-=": 335,
    "->": 336,
    "/": 337,
    "/=": 338,
    "*": 339,
    "*=": 340,
    "!": 341,
    "!=": 342,
    "ID": 256,
    "INT10": 346,
    "FLOAT": 347,
    "STRING": 351,
}

current_row = -1
current_line = 0
input_str = []


def is_keyword(s):
    return s in KEYWORD_LIST


def is_separator(s):
    return s in SEPARATOR_LIST


def is_operator(s):
    return s in OPERATOR_LIST


def get_cate_id(s):
    return CATEGORY_DICT[s]


def getchar():
    global current_row
    global current_line
    current_row += 1

    if current_row == len(input_str[current_line]):
        current_line += 1
        current_row = 0

    if current_line == len(input_str):
        return "SCANEOF"

    return input_str[current_line][current_row]


def ungetc():
    global current_row
    global current_line
    current_row = current_row - 1
    if current_row < 0:
        current_line = current_line - 1
        current_row = len(input_str[current_row]) - 1
    return input_str[current_line][current_row]


def read_source_file(file):
    global input_str
    f = open(file, "r")
    input_str = f.readlines()
    f.close()


def lexical_error(msg, line=None, row=None):
    if line is None:
        line = current_line + 1
    if row is None:
        row = current_row + 1
    print(str(line) + ":" + str(row) + " Lexical error: " + msg)


def scanner():
    current_char = getchar()
    if current_char == "SCANEOF":
        return ("SCANEOF", "", "")
    if current_char.strip() == "":
        return
    if current_char.isdigit():
        int_value = 0
        while current_char.isdigit():
            int_value = int_value * 10 + int(current_char)
            current_char = getchar()

        if current_char != ".":
            ungetc()
            return ("INT", int_value, get_cate_id("INT10"))

        float_value = str(int_value) + "."
        current_char = getchar()
        while current_char.isdigit():
            float_value += current_char
            current_char = getchar()
        ungetc()
        return ("FLOAT", float_value, get_cate_id("FLOAT"))
    if current_char.isalpha() or current_char == "_":
        string = ""
        while current_char.isalpha() or current_char.isdigit() or current_char == "_":
            string += current_char
            current_char = getchar()
            if current_char == "SCANEOF":
                break

        ungetc()
        if is_keyword(string):
            return (string, "", get_cate_id(string))
        else:
            return ("ID", string, get_cate_id("ID"))

    if current_char == '"':
        str_literal = ""
        global current_line
        global current_row
        line = current_line + 1
        row = current_row + 1

        current_char = getchar()
        while current_char != '"':
            str_literal += current_char
            current_char = getchar()
            if current_char == "SCANEOF":
                lexical_error('missing terminating "', line, row)

                current_line = line
                current_row = row
                return ("SCANEOF", "", "")
        return ("STRING_LITERAL", str_literal, get_cate_id("STRING"))

    if current_char == "/":
        next_char = getchar()
        line = int(current_line) + 1
        row = int(current_row) + 1
        if next_char == "*":
            comment = ""
            next_char = getchar()
            while True:
                if next_char == "SCANEOF":
                    lexical_error("unteminated /* comment", line, row)
                    return ("SCANEOF", "", "")
                if next_char == "*":
                    end_char = getchar()
                    if end_char == "/":
                        # Comment, return None to ignore it.
                        return None
                    if end_char == "SCANEOF":
                        lexical_error("unteminated /* comment", line, row)
                        return ("SCANEOF", "", "")
                comment += next_char
                next_char = getchar()
        else:
            ungetc()
            op = current_char
            current_char = getchar()
            if is_operator(current_char):
                op += current_char
            else:
                ungetc()
            return ("OP", op, get_cate_id(op))

    if is_separator(current_char):
        return ("SEP", current_char, get_cate_id(current_char))

    if is_operator(current_char):
        op = current_char
        current_char = getchar()
        if is_operator(current_char):
            op += current_char
        else:
            ungetc()
        return ("OP", op, get_cate_id(op))
    else:
        lexical_error("unknown character: " + current_char)


def main():
    file_name = sys.argv[1]
    read_source_file(file_name)
    while True:
        r = scanner()
        if r is not None:
            if r[0] == "SCANEOF":
                break
            print(r)


if __name__ == "__main__":
    main()
