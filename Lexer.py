from pygments.lexers import get_lexer_by_name
from pygments.token import Token

def process(token):
    if token[0] == Token.Text:
        return ('Text', token[1])
    elif token[0] in [Token.Comment.Single, Token.Comment.Multiline]:
        return ('Comment', token[1])
    elif token[0] in Token.Comment.Preproc:
        return ('Preproc', token[1])
    elif token[0] == Token.Comment.PreprocFile:
        return ('PreprocFile', token[1])
    elif token[0] == Token.Punctuation:
        if token[1] in ['(', ')', '[', ']', '{', '}', ',', ';', '.', ':']:
            return ('Punctuation', token[1])
    elif token[0] == Token.Operator:
        if token[1] in ['*', '=', '+', '-', '>', '<', '!', '&', '|', ':', '~', '?', '/', '%', '^']:
            return ('Operator', token[1])
    elif token[0] == Token.Name:
        return ('Identifier', token[1])
    elif token[0] in Token.Keyword:
        return ('Keyword', token[1])
    elif token[0] in Token.Literal.String:
        return ('String', token[1])
    elif token[0] == Token.Name.Function:
        return ('Funcname', token[1])
    elif token[0] in Token.Literal.Number:
        return ('Number', token[1])
    elif token[0] == Token.Name.Builtin:
        return ('Builtinname', token[1])
    elif token[0] == Token.Name.Label:
        return ('Label', token[1])
    print('Unrecognized token: ', token)
    return token


def remove_invalid_token(inp:list):
    removed_map = []
    for i in range(len(inp)):
        cont = inp[i][1] if inp[i][1] else inp[i][0]
        if(((len(cont.strip()) == 0) and (inp[i][0] != 'Preproc')) or (inp[i][0] == 'Comment')):
            pass
        else:
            removed_map.append(i)
    return removed_map


class Lexer:
    def __init__(self):
        self.kernel = get_lexer_by_name('c')

    def lex(self, texts):
        output = []
        tokens = self.kernel.get_tokens(texts)
        for token in tokens:
            output.append(process(token))
        output_map = remove_invalid_token(output)
        return output, output_map

    
    def lex_kernel(self, texts):
        return self.kernel.get_tokens(texts)
