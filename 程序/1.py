import pandas as pd
L = ''.join([chr(i) for i in range(97, 123)])
L += L.upper()  #字母
D = '0123456789'   #数字
DF0 = '=<+-*/();,[]'   #单分界符
ed = DF0 + '. \r\n\t:'
DF1 = []
for i in DF0:
    DF1.append(i)
DF = pd.Series(['EQ', 'LT', 'PLUS', 'MINUS', 'TIMES', 'OVER', 'LPAREN', 'RPAREN',
                'SEMI', 'COMMA', 'LMIDPAREN', 'RMIDPAREN'], index=DF1)
DF1 = pd.Series(['ASSIGN', 'UNDERANGE', 'DOT'], index=[':=', '..', '.'])
Type = ['ENDFILE', 'ERROR',  #
        'PROGRAM', 'PROCEDURE', 'TYPE', 'VAR', 'IF', 'THEN', 'ELSE', 'FI', 'WHILE',
        'DO', 'ENDWH', 'BEGIN', 'END', 'READ', 'WRITE', 'ARRAY', 'OF', 'RECORD',
        'RETURN',                           #保留字
        'INTEGER', 'CHAR',                 #类型
        'ID', 'INTC', 'CHARC',                #单词类型
        'ASSIGN', 'EQ', 'LT', 'PLUS', 'MINUS', 'TIMES','OVER', 'LPAREN', 'RPAREN',  
        'DOT', 'COLON', 'SEMI', 'COMMA', 'LMIDPAREN', 'RMIDPAREN', 'UNDERANGE']
Reserved = Type[2:23] #保留字
reserved = []
for i in Reserved:
    reserved.append(i.lower())
def GetWord(line, i, state):  #返回(word，word_type,i)
    while i < len(line):
        if state =='s0':
            if line[i] in L:        state = 's1' #第一个是字母/标识符
            elif line[i] in D:      state = 's2' #第一个是数字/常熟
            elif line[i] in DF0:     return line[i], DF[line[i]], i+1#单分界符
            elif line[i] == ':':    state = 's4' #(:=)双分界符
            elif line[i] == '{':    state = 's6' #注释
            elif line[i] == '.':    state = 's8' #结束或数组下标
            elif line[i] == '\'':    state = 's10'
            elif line[i] in ' \t\n': pass 
            else:   
                b = i
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
            i += 1
        if state == 's1' :                      #标识符或保留字
            b = i - 1
            while (i < len(line))and((line[i] in L) or (line[i] in D)):
                i += 1
            word_type = 'ID'          #'ID'表示标识符
            word = line[b:i]
            if word in reserved:     # 说明是保留字，由各自大写字母表示
                return word,word.upper(),i
            return word,word_type,i
        elif state == 's2' :                      #数字
            b = i - 1
            while (i < len(line))and(line[i] in D):
                i += 1  
            if line[i] not in ed:
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
            else:
                word_type = 'INTC'       # INTC表示常数
                return int(line[b:i]),word_type,i
        elif state == 's4':          #':='双分界符
            if (i < len(line)) and line[i] == '=':
                return ':=','ASSIGN',i+1
            else: 
                b = i
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
        elif state == 's6' :                    #注释
            while (i<len(line)) and (line[i] != '}') :
                i+=1
            if i >= len(line) :
                return 0,'COMMENT',-1          #-1表示注释还没完，延续到下一行
            else: 
                i += 1
                state = 's0'
        elif state == 's8':                  
            if (i < len(line)) and line[i] == '.':          #数组下标
                return '..','UNDERANGE',i+1
            else :return '.','DOT',i   #程序结束标志
        elif state == 's10':   #字符
            b = i-1
            while (i<len(line)) and line[i] != '\'':  
                i+=1
            if i >= len(line):
                return line[b:i],'CHARC',-1    #-1同注释
            else :
                return line[b:i+1],'CCHARC',i+1    #返回该字符串
    return 0,0,0
#filename = raw_input("Please input the file's name:")
filename = 'c1.txt'
fp = open(filename,'r')
state0 = []
ch = ''
for i in range(13):
    state0.append('s' + str(i))
Translated = []
state ='s0'
k=0
for line in fp.readlines():
    k += 1
    i = 0
    #if line[len(line)-1] == '\n':
        #line = line[:len(line)-1]
    while(i<len(line)):
        word,word_type,i = GetWord(line,i,state)
        if(i==-1):   #注释或字符串还没完
            if(word_type == 'CHARC'):
                state = 's10'
                ch += word
            else :
                state = 's8'
            i = len(line)
        elif(i == 0 ):
            state = 's0'
            i = len(line)
        else :
            if (word_type == 'CHARC'):
                ch += word
                Translated.append([k,word_type,ch])
                ch = ''
            else :
                Translated.append([k,word_type,word])
            state = 's0'
fp.close()
for i in Translated:
    print i