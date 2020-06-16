from Lexer import Lexer
from Parser import Parser
from Ast import type_name
from Eval import travel, print_tokens
import json
import pickle

filename = 'inline.c'
file = open(filename, 'r')
code = file.read()
file.close()

lexer = Lexer()
tokens, tokens_map = lexer.lex(code)
# count = 0
# for token in tokens:
#     count += 1
# print(count)
# print(len(tokens_map))
#print(lexer.lex(code))
parser = Parser()
parser.get_input(tokens, tokens_map)
parser.parse()
parse_result = {'tokens':[token[1] for token in tokens], 'tokens_map':tokens_map, 'astnodes':[[node.ntype, node.content, node.subNode] for node in parser.AstNodes]}
with open('inline.pkl', 'wb') as f:
    pickle.dump(parse_result, f)

    

#print_tokens(parser.AstNodes, 838, tokens_map, tokens)
# start, end = eval(parser.AstNodes, 425, -1, -1)
# print(start, end, tokens_map[start], tokens_map[end])
# for i in range(tokens_map[start], tokens_map[end]):
#     print(tokens[i][1], end='')

# for i in range(len(parser.AstNodes)):
#     if(parser.AstNodes[i].subNode != []):
#         print("id: ", i, end='')
#         print("\ttype: " + type_name[parser.AstNodes[i].ntype], end='')
#     # print("id: ", i, end='')
#     # if(parser.AstNodes[i].content != None):
#     #     print("\tcontent: ", parser.AstNodes[i].content, end='')
#     # if(parser.AstNodes[i].subNode != []):
#         print("\tsubnode: ", end='')
#         for subn in parser.AstNodes[i].subNode:
#             print(subn, end=', ')
#         print("\n"+"*"*32+"\n")
#     # print("\n"+"*"*32+"\n")
#     # if(astnode.ntype == 2):
#     #     print("\n"+"*"*32+"\n")
#     #     for subn in astnode.subNode:
#     #         print(parser.AstNodes[subn].content, end='')

