type_name = [
    'program',#0
    'token',
    'statement',
    'preproc',
    'compst',
    'stmts',#5
    'function implementation or variable declaration or anything else',
    'funcimple',
    'vardec',
    'splitspace',
    'preprocgroup',#10
    'ifstmts',
    'ifexp',
    'elseifexp',
    'elseexp',
    'exp',#15
    'forstmts',
    'forexp',
    'whilestmts',
    'whileexp',
    'jumplabel',#20
    'switchstmts',
    'switchexp',
    'switchcompst',
    'switchcase',
    'switchcaseexp',#25
    'funcdec',
    'itemcompst',
    'item',
    'dowhilestmts',
    'dowhileexp'#30
]

class AstNode:
    def __init__(self, ntype, content=None, subNode:list=[]):
        self.ntype = ntype
        self.content = content
        self.subNode = subNode