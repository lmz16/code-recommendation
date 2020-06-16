from Ast import AstNode

class Parser:
    def __init__(self):
        self.text = None
        self.text_map = []
        self.pointer = -1
        self.AstNodes = []
        self.temp_cont = ''
    

    def get_input(self, inp:list, inp_map:list):
        self.text = inp
        self.text_map = inp_map

    
    def token_append(self, value):
        self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
        self.pointer += 1
        self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
        #print(self.temp_cont)

    
    def get_temp_cont(self):
        if(self.pointer < len(self.text_map)):
            self.temp_cont = self.text[self.text_map[self.pointer]][1]
        else:
            print("There is no tokens!")

    
    def get_next_cont(self, num=1):
        if(self.pointer + num - 1 < len(self.text_map)):
            temp_cont = []
            for i in range(num):
                token = self.text[self.text_map[self.pointer + i]]
                if(token[1] == None):
                    temp_cont.append(token[0])
                else:
                    temp_cont.append(token[1])
            return temp_cont
        else:
            print("There is no enough tokens!")


    def parse(self):
        self.pointer = 0
        self.temp_cont = ''
        self.AstNodes = []
        if self.text == None:
            print("Text doesn't exist\n")
            return -1
        else:
            self.process_0(way=0)

    
    #entrance of parse process
    def process_0(self, way:int, value=None):
        if(self.pointer > len(self.text_map) - 1):
            return 0
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=0, content=None, subNode=[]))
            return self.process_0(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_1(way=0))
                return self.process_0(way=1, value=value)
            else:
                self.AstNodes[value].subNode.append(self.process_3(way=0))
                return self.process_0(way=1, value=value)
                

    #rule of preprocgroup
    def process_1(self, way:int, value=None):
        if(self.pointer > len(self.text_map) - 1):
            return value
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=10, content=None, subNode=[]))
            return self.process_1(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_2(way=0))
                return self.process_1(way=1, value=value)
            else:
                return value


    #rule of preproc
    def process_2(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=3, content=None, subNode=[]))
            return self.process_2(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if('\n' in self.temp_cont):
                self.token_append(value)
                return value
            else:
                self.token_append(value)
                return self.process_2(way=1, value=value)


    #rule of function implementation or variable declaration or anything else
    def process_3(self, way:int, value=None):
        if(self.pointer > len(self.text_map) - 1):
            return value
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=6, content=None, subNode=[]))
            return self.process_3(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.text[self.text_map[self.pointer]][0] == 'Keyword'):
                return self.process_3(way=2, value=value)
            else:
                return self.process_3(way=4, value=value)
        #start with keywords
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == 'struct'):
                self.token_append(value)
                return self.process_3(way=6, value=value)
            elif((self.text[self.text_map[self.pointer]][0] == 'Keyword') or (self.temp_cont == '*')):
                self.token_append(value)
                return self.process_3(way=2, value=value)
            elif(self.text[self.text_map[self.pointer]][0] ==  'Funcname'):
                self.token_append(value)
                return self.process_3(way=3, value=value)
            else:
                return self.process_3(way=5, value=value)
        #function implementation or declaration
        elif(way == 3):
            self.get_temp_cont()
            if(self.temp_cont == ';'):
                self.token_append(value)
                self.AstNodes[value].ntype = 26
                return value
            elif(self.temp_cont == '{'):
                self.AstNodes[value].ntype = 7
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return value
            else:
                self.token_append(value)
                return self.process_3(way=3, value=value)
        #plain statement
        elif(way == 4):
            self.AstNodes[value].ntype = 5
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return value
            elif(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_2(way=0))
                return value
            elif(self.text[self.text_map[self.pointer]][0] == 'Label'):
                self.AstNodes[value].subNode.append(self.process_15(way=0))
                return value
            else:
                return self.process_3(way=5, value=value)
        #other
        elif(way == 5):
            self.AstNodes[value].ntype = 2
            self.get_temp_cont()
            if(self.temp_cont == ';'):
                self.token_append(value)
                return value
            elif(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_21(way=0))
                return self.process_3(way=5, value=value)
            else:
                self.token_append(value)
                return self.process_3(way=5, value=value)
        elif(way == 6):
            self.token_append(value)
            return self.process_3(way=2, value=value)


    #rule of compst
    def process_4(self, way:int, value=None):
        if(self.pointer > len(self.text_map) - 1):
            return value
        if((way == 0) and (self.temp_cont == '{')):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=4, content=None, subNode=[sub1]))
            return self.process_4(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == '}'):
                self.token_append(value)
                return value
            elif(self.temp_cont == 'if'):
                self.AstNodes[value].subNode.append(self.process_6(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == 'for'):
                self.AstNodes[value].subNode.append(self.process_11(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == 'while'):
                self.AstNodes[value].subNode.append(self.process_13(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == 'switch'):
                self.AstNodes[value].subNode.append(self.process_16(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == 'do'):
                self.AstNodes[value].subNode.append(self.process_23(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_2(way=0))
                return self.process_4(way=1, value=value)
            elif(self.text[self.text_map[self.pointer]][0] == 'Label'):
                self.AstNodes[value].subNode.append(self.process_15(way=0))
                return self.process_4(way=1, value=value)
            else:
                self.AstNodes[value].subNode.append(self.process_5(way=0))
                return self.process_4(way=1, value=value)
        else:
            return self.process_error(value)

    
    #rule of statement
    def process_5(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=2, content=None, subNode=[]))
            return self.process_5(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == ';'):
                self.token_append(value)
                return value
            # elif(self.temp_cont == '{'):
            #     self.AstNodes[value].subNode.append(self.process_4(way=0))
            #     return value
            else:
                self.token_append(value)
                return self.process_5(way=1, value=value)
    

    #rule of ifstmts
    def process_6(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=11, content=None, subNode=[]))
            return self.process_6(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            temp_conts = self.get_next_cont(2)
            if(temp_conts[0] == 'if'):
                self.AstNodes[value].subNode.append(self.process_7(way=0))
                return self.process_6(way=2, value=value)
            elif(temp_conts == ['else', 'if']):
                self.AstNodes[value].subNode.append(self.process_8(way=0))
                return self.process_6(way=2, value=value)
            elif(temp_conts[0] == 'else'):
                self.AstNodes[value].subNode.append(self.process_9(way=0))
                return self.process_6(way=2, value=value)
            else:
                return value
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return self.process_6(way=1, value=value)
            else:
                self.AstNodes[value].subNode.append(self.process_5(way=0))
                return self.process_6(way=1, value=value)


    #rule of ifexp
    def process_7(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=12, content=None, subNode=[sub1]))
            return self.process_7(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.AstNodes[value].subNode.append(self.process_10(way=0))
            return value
        
    
    #rule of ifelseexp
    def process_8(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=13, content=None, subNode=[sub1, sub1 - 1]))
            return self.process_8(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.AstNodes[value].subNode.append(self.process_10(way=0))
            return value

    
    #rule of elseexp
    def process_9(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=14, content=None, subNode=[sub1]))
            return self.process_9(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.AstNodes[value].subNode.append(self.process_10(way=0))
            return value

        
    #rule of exp
    def process_10(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=15, content=None, subNode=[]))
            return self.process_10(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            parentheses_count = 0
            while(True):
                self.get_temp_cont()
                if(self.temp_cont in [';', '{', '}']):
                    break
                elif(self.temp_cont == ')'):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count -= 1
                    if(parentheses_count == 0):
                        break
                elif(self.temp_cont == '('):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count += 1
                else:
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
            return value

    
    #rule of forstmts
    def process_11(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=16, content=None, subNode=[]))
            return self.process_11(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == 'for'):
                self.AstNodes[value].subNode.append(self.process_12(way=0))
                return self.process_11(way=2, value=value)
            else:
                return self.process_error(value)
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return value
            else:
                self.AstNodes[value].subNode.append(self.process_5(way=0))
                return value

    
    #rule of forexp
    def process_12(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=17, content=None, subNode=[sub1]))
            return self.process_12(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            parentheses_count = 0
            while(True):
                self.get_temp_cont()
                if(self.temp_cont in ['{', '}']):
                    break
                elif(self.temp_cont == ')'):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count -= 1
                    if(parentheses_count == 0):
                        break
                elif(self.temp_cont == '('):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count += 1
                else:
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
            return value
        

    #rule of whilestmts
    def process_13(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=18, content=None, subNode=[]))
            return self.process_13(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == 'while'):
                self.AstNodes[value].subNode.append(self.process_14(way=0))
                return self.process_13(way=2, value=value)
            else:
                return self.process_error(value)
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return value
            else:
                self.AstNodes[value].subNode.append(self.process_5(way=0))
                return value


    #rule of whileexp
    def process_14(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=19, content=None, subNode=[sub1]))
            return self.process_14(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            parentheses_count = 0
            while(True):
                self.get_temp_cont()
                if(self.temp_cont in [';', '{', '}']):
                    break
                elif(self.temp_cont == ')'):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count -= 1
                    if(parentheses_count == 0):
                        break
                elif(self.temp_cont == '('):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count += 1
                else:
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
            return value


    #rule of jumplabel
    def process_15(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=20, content=None, subNode=[]))
            return self.process_15(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            while(True):
                self.get_temp_cont()
                self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                self.pointer += 1
                self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                if(self.temp_cont == ':'):
                    break
            return value
            

    #rule of switchstmts
    def process_16(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=21, content=None, subNode=[]))
            return self.process_16(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == 'switch'):
                self.AstNodes[value].subNode.append(self.process_17(way=0))
                return self.process_16(way=2, value=value)
            else:
                return self.process_error(value)
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_18(way=0))
                return value


    #rule of switchexp
    def process_17(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=22, content=None, subNode=[sub1]))
            return self.process_17(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            parentheses_count = 0
            while(True):
                self.get_temp_cont()
                if(self.temp_cont in [';', '{', '}']):
                    break
                elif(self.temp_cont == ')'):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count -= 1
                    if(parentheses_count == 0):
                        break
                elif(self.temp_cont == '('):
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                    parentheses_count += 1
                else:
                    self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                    self.pointer += 1
                    self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
            return value

    
    #rule of switchcompst
    def process_18(self, way:int, value=None):
        if((way == 0) and (self.temp_cont == '{')):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=23, content=None, subNode=[sub1]))
            return self.process_18(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '}'):
                self.token_append(value)
                return value
            elif(self.temp_cont in ['default', 'case']):
                self.AstNodes[value].subNode.append(self.process_19(way=0))
                return self.process_18(way=1, value=value)
            elif(self.text[self.text_map[self.pointer]][0] == 'Label'):
                self.AstNodes[value].subNode.append(self.process_15(way=0))
                return self.process_18(way=1, value=value)
            elif(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_2(way=0))
                return self.process_18(way=1, value=value)
            else:
                return self.process_error(value)


    #rule of switchcase
    def process_19(self, way:int, value=None):
        if((way == 0) and (self.temp_cont in ['default', 'case'])):
            self.AstNodes.append(AstNode(ntype=24, content=None, subNode=[self.process_20(way=0)]))
            return self.process_19(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
                return self.process_4(way=1, value=value)
            elif(self.temp_cont in ['}', 'default', 'case']):
                return value
            elif(self.temp_cont == 'if'):
                self.AstNodes[value].subNode.append(self.process_6(way=0))
                return self.process_19(way=1, value=value)
            elif(self.temp_cont == 'for'):
                self.AstNodes[value].subNode.append(self.process_11(way=0))
                return self.process_19(way=1, value=value)
            elif(self.temp_cont == 'while'):
                self.AstNodes[value].subNode.append(self.process_13(way=0))
                return self.process_19(way=1, value=value)
            elif(self.temp_cont == 'switch'):
                self.AstNodes[value].subNode.append(self.process_16(way=0))
                return self.process_19(way=1, value=value)
            elif(self.temp_cont == 'do'):
                self.AstNodes[value].subNode.append(self.process_23(way=0))
                return self.process_19(way=1, value=value)
            elif(self.temp_cont == '#'):
                self.AstNodes[value].subNode.append(self.process_2(way=0))
                return self.process_19(way=1, value=value)
            elif(self.text[self.text_map[self.pointer]][0] == 'Label'):
                self.AstNodes[value].subNode.append(self.process_15(way=0))
                return self.process_19(way=1, value=value)
            else:
                self.AstNodes[value].subNode.append(self.process_5(way=0))
                return self.process_19(way=1, value=value)


    #rule of switchcaseexp
    def process_20(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=25, content=None, subNode=[]))
            return self.process_20(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            parentheses_count = 0
            while(True):
                self.get_temp_cont()
                self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                self.pointer += 1
                self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                if(self.temp_cont == ':'):
                    break
                elif(self.temp_cont == ')'):
                    parentheses_count -= 1
                    if(parentheses_count == 0):
                        break
                elif(self.temp_cont == '('):
                    parentheses_count += 1
            return value

    
    #rule of itemcompst
    def process_21(self, way:int, value=None):
        if((way == 0) and (self.temp_cont == '{')):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=27, content=None, subNode=[sub1]))
            return self.process_21(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '}'):
                self.token_append(value)
                return value
            else:
                self.AstNodes[value].subNode.append(self.process_22(way=0))
                return self.process_21(way=1, value=value)


    #rule of item
    def process_22(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=28, content=None, subNode=[]))
            return self.process_22(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            while(True):
                self.get_temp_cont()
                self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                self.pointer += 1
                self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                if(self.temp_cont in [';', ',']):
                    break
            return value

    
    #rule of dowhilestmts
    def process_23(self, way:int, value=None):
        if((way == 0) and (self.temp_cont == 'do')):
            self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
            self.pointer += 1
            sub1 = len(self.AstNodes) - 1
            self.AstNodes.append(AstNode(ntype=29, content=None, subNode=[sub1]))
            return self.process_23(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            self.get_temp_cont()
            if(self.temp_cont == '{'):
                self.AstNodes[value].subNode.append(self.process_4(way=0))
            return self.process_23(way=2, value=value)
        elif(way == 2):
            self.get_temp_cont()
            if(self.temp_cont == 'while'):
                self.AstNodes[value].subNode.append(self.process_24(way=0))
                return value
            else:
                self.AstNodes[value].ntype = 4
                return value
    

    #rule of dowhileexp
    def process_24(self, way:int, value=None):
        if(way == 0):
            self.AstNodes.append(AstNode(ntype=30, content=None, subNode=[]))
            return self.process_24(way=1, value=(len(self.AstNodes) - 1))
        elif(way == 1):
            while(True):
                self.get_temp_cont()
                self.AstNodes.append(AstNode(ntype=1, content=self.pointer, subNode=[]))
                self.pointer += 1
                self.AstNodes[value].subNode.append(len(self.AstNodes) - 1)
                if(self.temp_cont == ';'):
                    break
            return value


    #rule of error
    def process_error(self, value=None):
        if(value):
            print("error happens in Astnode: " + str(value))
        else:
            print("error happens")
        return -1