import re


#TOKENS:
IF = 0
THEN = 1
ELSE = 2
END = 3
PRINT = 4
GREATER = 5
LESSER = 6
EQUAL = 7
GREATER_EQ = 8
LESSER_EQ = 9
PLUS = 10
MINUS = 11
TIMES = 12
DIVIDE = 13
SEMI = 14
EOF = 15
CONST = 16
ID = 17
UNDEFINED = 18
ENTER = 19
INPUT = 20

COMPARE_EXPRESSIONS = [GREATER, LESSER, EQUAL, GREATER_EQ, LESSER_EQ]
ARITH_EXPRESSIONS = [PLUS, MINUS, TIMES, DIVIDE]

EXPRESSION_END = [SEMI, EOF, GREATER, LESSER, EQUAL, GREATER_EQ, LESSER_EQ]

regex = {
    IF:r"if",
    THEN:r"then",
    ELSE:r"else",
    END:r"end",
    PRINT:r"print",
    INPUT:r"input",
    GREATER:r">",
    LESSER:r"<",
    EQUAL:r"==",
    GREATER_EQ:r">=",
    LESSER_EQ:r"<=",
    ENTER:r"=",
    PLUS:r"\+",
    MINUS:r"\-",
    TIMES:r"\*",
    DIVIDE:r'/',
    SEMI:r";",
    CONST:r"X{,3}((IX)?|VI{,3}|IV|I{,3})",
    ID:r"[a-zA-Z]+[a-zA-Z_]*"
}

class Token:
    def __init__(self, token, value):
        self.token = token
        self.value = value
    tokens_map = {
        IF:"IF",
        THEN:"THEN",
        ELSE:"ELSE",
        END:"END",
        PRINT:"PRINT",
        GREATER:"GREATER",
        LESSER:"LESSER",
        EQUAL:"EQUAL",
        GREATER_EQ:"GREATER_EQ",
        LESSER_EQ:"LESSER_EQ",
        PLUS:"PLUS",
        MINUS:"MINUS",
        TIMES:"TIMES",
        DIVIDE:"DIVIDE",
        SEMI:"SEMI",
        EOF:"EOF",
        CONST:"CONST",
        ID:"ID",
        UNDEFINED:"UNDEFINED",
        ENTER:"ENTER",
        INPUT:"INPUT"
    }

    def __str__(self):
        return self.tokens_map[self.token] + ":" + str(self.value)



def readFile(path = r'sample program.txt'):
    with open(path, "r") as file:
        text = file.read()
        return text

def do_text_preprocess(text):
    text = re.sub(r'\b;', ' ;', text)
    text = re.sub(r'end\s*;', 'end', text)
    text = re.sub(r'[a-zA-Z_0-9\+\-\*\\/()];', ' ;', text)
    text = re.sub(r'\s', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def get_number(line):
    c_IX = len(re.findall(r'IX', line))
    line = re.sub(r'IX', '', line)
    c_IV = len(re.findall(r'IV', line))
    line = re.sub(r'IV', '', line)
    c_X = len(re.findall(r'X', line))
    c_V = len(re.findall(r'V', line))
    c_I = len(re.findall(r'I', line))
    num = 10 * c_X + 9 * c_IX + 5 * c_V + 4 * c_IV + 1 * c_I
    return num

def tokenize(text):
    splited = re.split(r'\s', text)
    tokens = []
    for word in splited:
        t = Token(UNDEFINED, word)
        for key in regex:
            if re.fullmatch(regex[key], word):
                if key == CONST:
                    num = get_number(word)
                    t = Token(CONST, num)
                else:
                    t = Token(key, word)

                break
        tokens.append(t)
        if t.token == UNDEFINED:
            print("Could not parse token:", word)
    tokens.append(Token(EOF, "__EOF__"))
    return tokens

def getTokensFromFile(path = r'sample program.txt'):
    text = readFile(path)
    return tokenize(do_text_preprocess(text))